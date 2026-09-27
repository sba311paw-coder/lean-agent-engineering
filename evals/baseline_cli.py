#!/usr/bin/env python3
"""With-skill vs. no-skill baseline for lean-agent-engineering, via the Claude Code CLI.

Stages:
  generate  answer every prompt with and without SKILL.md (resumable)
  judge     blind-grade every answer against expected_behavior (resumable)
  report    write summary.md and summary.json

Standard library only. Run from anywhere; paths resolve from this file.
"""
import argparse
import datetime
import json
import random
import re
import subprocess
import sys
import tempfile
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals" / "evals.json"
NEUTRAL = ROOT / "evals" / "neutral-prompts.json"
SKILL = ROOT / "SKILL.md"
BASE_PROMPT = "You are a helpful assistant answering a question in a chat. You cannot see the user's files, code or environment, so answer from the question alone."
SCORE = {"PASS": 1.0, "PARTIAL": 0.5, "FAIL": 0.0}
CONDITIONS = ["baseline", "skill"]
REDACT = re.compile(r"lean[- ]agent[- ]engineering", re.I)

JUDGE_SYSTEM = """You grade one AI response against a numbered list of criteria.
Judge what the response actually does, not whether it contains keywords.
For each criterion give a verdict:
- PASS: clearly met
- PARTIAL: partly met, or met only weakly or late
- FAIL: not met, or contradicted
Give short evidence from the response for each verdict.
Output only JSON, with one entry per criterion in the same order:
{"criteria": [{"n": 1, "verdict": "PASS", "evidence": "..."}]}"""


def load_items(variants):
    data = json.loads(EVALS.read_text(encoding="utf-8"))
    neutral = json.loads(NEUTRAL.read_text(encoding="utf-8"))["prompts"]
    items = []
    for c in data["cases"]:
        if "original" in variants:
            items.append({"case": c, "variant": "original", "prompt": c["prompt"]})
        if "neutral" in variants and c["id"] in neutral:
            items.append({"case": c, "variant": "neutral", "prompt": neutral[c["id"]]})
    return items


def skill_body():
    text = SKILL.read_text(encoding="utf-8")
    m = re.match(r"^---\n.*?\n---\n", text, re.S)
    return text[m.end():] if m else text


def run_claude(system_file, prompt, model, workdir, retries=3):
    cmd = [
        "claude", "-p",
        "--model", model,
        "--system-prompt-file", str(system_file),
        "--tools", "",
        "--disable-slash-commands",
        "--safe-mode",
        "--no-session-persistence",
        "--output-format", "json",
    ]
    for attempt in range(1, retries + 1):
        try:
            p = subprocess.run(cmd, input=prompt, cwd=workdir, capture_output=True,
                               text=True, timeout=600, encoding="utf-8")
            if p.returncode == 0:
                out = json.loads(p.stdout)
                if not out.get("is_error") and out.get("result"):
                    return out
            err = (p.stderr or p.stdout).strip()[-400:]
        except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
            err = str(e)
        wait = 30 * attempt
        print(f"    attempt {attempt}/{retries} failed, waiting {wait}s: {err}", file=sys.stderr)
        time.sleep(wait)
    raise RuntimeError("claude call kept failing (usage limit?). Rerun the same command later to resume.")


def key_of(item, condition, rnd):
    return f"{item['case']['id']}__{item['variant']}__{condition}__r{rnd}"


def generate(args, items, out, workdir):
    resp_dir = out / "responses"
    resp_dir.mkdir(parents=True, exist_ok=True)
    base_file = workdir / "baseline.txt"
    skill_file = workdir / "with-skill.txt"
    base_file.write_text(BASE_PROMPT + "\n", encoding="utf-8")
    skill_file.write_text(BASE_PROMPT + "\n\n" + skill_body(), encoding="utf-8")

    jobs = [(i, c, r) for i in items for c in CONDITIONS for r in range(1, args.rounds + 1)]
    random.Random(args.seed).shuffle(jobs)
    todo = [j for j in jobs if not (resp_dir / f"{key_of(*j)}.json").exists()]
    print(f"generate: {len(jobs)} total, {len(todo)} to run")
    for n, (item, cond, rnd) in enumerate(todo, 1):
        key = key_of(item, cond, rnd)
        print(f"  [{n}/{len(todo)}] {key}")
        sys_file = skill_file if cond == "skill" else base_file
        res = run_claude(sys_file, item["prompt"], args.model, workdir)
        record = {
            "key": key, "case_id": item["case"]["id"], "case_number": item["case"]["case_number"],
            "category": item["case"]["category"], "expected_activation": item["case"]["expected_activation"],
            "variant": item["variant"], "condition": cond, "round": rnd,
            "prompt": item["prompt"], "response": res["result"],
            "model_usage": res.get("modelUsage"), "usage": res.get("usage"),
            "cost_usd": res.get("total_cost_usd"), "duration_ms": res.get("duration_ms"),
        }
        (resp_dir / f"{key}.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
        time.sleep(args.sleep)


def parse_judge(text, n_criteria):
    start, end = text.find("{"), text.rfind("}")
    data = json.loads(text[start:end + 1])
    crit = data["criteria"]
    if len(crit) != n_criteria or any(c.get("verdict") not in SCORE for c in crit):
        raise ValueError("judge output does not match criteria")
    return crit


def judge(args, items, out, workdir):
    resp_dir, judged_dir = out / "responses", out / "judged"
    judged_dir.mkdir(parents=True, exist_ok=True)
    judge_file = workdir / "judge.txt"
    judge_file.write_text(JUDGE_SYSTEM + "\n", encoding="utf-8")
    criteria = {i["case"]["id"]: i["case"]["expected_behavior"] for i in items}

    files = sorted(resp_dir.glob("*.json"))
    random.Random(args.seed + 1).shuffle(files)
    todo = [f for f in files if not (judged_dir / f.name).exists()]
    print(f"judge: {len(files)} responses, {len(todo)} to grade")
    for n, f in enumerate(todo, 1):
        rec = json.loads(f.read_text(encoding="utf-8"))
        crit = criteria.get(rec["case_id"])
        if crit is None:
            continue
        print(f"  [{n}/{len(todo)}] {f.stem}")
        body = REDACT.sub("[redacted]", rec["response"])
        numbered = "\n".join(f"{k}. {c}" for k, c in enumerate(crit, 1))
        msg = (f"USER REQUEST:\n{rec['prompt']}\n\nCRITERIA:\n{numbered}\n\n"
               f"RESPONSE TO GRADE:\n<<<\n{body}\n>>>")
        verdicts = None
        for _ in range(2):
            res = run_claude(judge_file, msg, args.judge_model, workdir)
            try:
                verdicts = parse_judge(res["result"], len(crit))
                break
            except (ValueError, KeyError, json.JSONDecodeError):
                print("    judge output unreadable, retrying", file=sys.stderr)
        if verdicts is None:
            print("    skipped: judge output unreadable twice", file=sys.stderr)
            continue
        scores = [SCORE[v["verdict"]] for v in verdicts]
        rec_out = {k: rec[k] for k in ("key", "case_id", "case_number", "category",
                                       "expected_activation", "variant", "condition", "round")}
        rec_out.update({
            "criteria": [dict(v, criterion=c) for v, c in zip(verdicts, crit)],
            "score": sum(scores) / len(scores),
            "case_pass": all(s == 1.0 for s in scores),
            "judge_cost_usd": res.get("total_cost_usd"),
        })
        (judged_dir / f.name).write_text(json.dumps(rec_out, indent=2), encoding="utf-8")
        time.sleep(args.sleep)


def pct(x):
    return f"{100 * x:.0f}%"


def report(args, out):
    recs = [json.loads(f.read_text(encoding="utf-8")) for f in sorted((out / "judged").glob("*.json"))]
    if not recs:
        sys.exit("report: nothing judged yet")

    def agg(rows):
        return (sum(r["case_pass"] for r in rows) / len(rows), sum(r["score"] for r in rows) / len(rows), len(rows))

    by_vc, by_cat, by_case = defaultdict(list), defaultdict(list), defaultdict(list)
    for r in recs:
        by_vc[(r["variant"], r["condition"])].append(r)
        by_cat[(r["variant"], r["category"], r["condition"])].append(r)
        by_case[(r["case_number"], r["case_id"], r["variant"], r["condition"])].append(r)

    try:
        version = subprocess.run(["claude", "-v"], capture_output=True, text=True).stdout.strip()
    except OSError:
        version = "unknown"
    models = set()
    for f in (out / "responses").glob("*.json"):
        mu = json.loads(f.read_text(encoding="utf-8")).get("model_usage") or {}
        models.update(mu.keys())

    lines = [
        "# Baseline results: with skill vs. without skill", "",
        f"- Date: {datetime.date.today().isoformat()}",
        f"- Claude Code: {version}",
        f"- Answer model: {args.model} (resolved: {', '.join(sorted(models)) or 'unknown'})",
        f"- Judge model: {args.judge_model}, blind to condition, skill name redacted",
        f"- Rounds per prompt: {args.rounds}; judged responses: {len(recs)}",
        "- Case pass = every criterion PASS. Score = mean over criteria (PASS 1, PARTIAL 0.5, FAIL 0).",
        "", "## Overall", "",
        "| Prompt set | Condition | Case pass rate | Mean score | n |",
        "|---|---|---|---|---|",
    ]
    summary = {"overall": {}, "by_category": {}, "by_case": {}}
    for (v, c), rows in sorted(by_vc.items()):
        p, s, n = agg(rows)
        lines.append(f"| {v} | {c} | {pct(p)} | {s:.2f} | {n} |")
        summary["overall"][f"{v}/{c}"] = {"pass_rate": p, "mean_score": s, "n": n}

    lines += ["", "## By category (mean score)", "",
              "| Prompt set | Category | Baseline | Skill | Difference |", "|---|---|---|---|---|"]
    for v, cat in sorted({(v, cat) for v, cat, _ in by_cat}):
        b, k = by_cat.get((v, cat, "baseline")), by_cat.get((v, cat, "skill"))
        if b and k:
            bs, ks = agg(b)[1], agg(k)[1]
            lines.append(f"| {v} | {cat} | {bs:.2f} | {ks:.2f} | {ks - bs:+.2f} |")
            summary["by_category"][f"{v}/{cat}"] = {"baseline": bs, "skill": ks}

    lines += ["", "## By case (mean score across rounds)", "",
              "| # | Case | Prompt set | Baseline | Skill |", "|---|---|---|---|---|"]
    for num, cid, v in sorted({(n, i, v) for n, i, v, _ in by_case}):
        b, k = by_case.get((num, cid, v, "baseline")), by_case.get((num, cid, v, "skill"))
        bs = f"{agg(b)[1]:.2f}" if b else "-"
        ks = f"{agg(k)[1]:.2f}" if k else "-"
        lines.append(f"| {num} | {cid} | {v} | {bs} | {ks} |")
        summary["by_case"][f"{cid}/{v}"] = {"baseline": bs, "skill": ks}

    lines += ["", "## Limits", "",
              "- One model family answers and judges; the judge may share its biases.",
              "- Small sample: treat differences under about 0.10 as noise.",
              "- The skill is given as a system prompt, so this tests the instructions, not automatic skill discovery.",
              "- The redaction hides the skill's name, but its style may still reveal the condition to the judge."]
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"report: wrote {out / 'summary.md'}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stage", choices=["all", "generate", "judge", "report"], default="all")
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--judge-model", default="sonnet")
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--variants", default="original,neutral")
    ap.add_argument("--only", help="comma-separated case ids")
    ap.add_argument("--smoke", action="store_true", help="1 case, 1 round, to check setup")
    ap.add_argument("--sleep", type=float, default=2.0, help="seconds between calls")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--out", default=str(ROOT / "evals" / "baseline-results"))
    args = ap.parse_args()

    items = load_items(set(args.variants.split(",")))
    if args.only:
        wanted = set(args.only.split(","))
        items = [i for i in items if i["case"]["id"] in wanted]
    out = Path(args.out)
    if args.smoke:
        items = [i for i in items if i["case"]["id"] == "debugging-01"]
        args.rounds = 1
        out = out.parent / (out.name + "-smoke")
    out.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        if args.stage in ("all", "generate"):
            generate(args, items, out, workdir)
        if args.stage in ("all", "judge"):
            judge(args, items, out, workdir)
    if args.stage in ("all", "report"):
        report(args, out)


if __name__ == "__main__":
    main()
