# Lean Agent Engineering

Build reliable AI agents with the minimum complexity necessary.

Version **0.1.1** · Author **HumanInTheLoopAI** · [Apache-2.0](LICENSE)

This is a portable instruction skill for engineering AI and agentic software.
It helps an agent reuse existing capabilities, locate failures, preserve
authorization boundaries, and verify outcomes before claiming completion.

## Use the skill

Place this folder, named `lean-agent-engineering`, in a skill directory
supported by your agent client. Follow that client's discovery or reload
instructions. The entry point is [SKILL.md](SKILL.md).

For a manual trial, provide SKILL.md as instructions to your agent and ask
an engineering question. That tests explicit use; it does not test automatic
discovery or activation. Client support and installation locations vary.

Example request:

> My tool returns the correct result, but the final answer ignores it.
> Help me identify the failing boundary before changing the system.

The workflow applies to building, debugging, reviewing, securing, and making
architecture decisions about AI systems. A general educational question such
as “What is an LLM?” should receive a normal explanation.

## What it requires

The skill itself has no runtime dependencies, framework, MCP server, hooks,
API keys, network requirement, paid service, or vendor-specific integration.
It optionally prefers an existing systematic-debugging skill when available;
the core debugging sequence is also included in SKILL.md.

Your host agent and any application you build have their own requirements
and costs. This package is guidance, not an executable agent or a security
enforcement mechanism. Permissions must be enforced by the application and
tools.

See [the minimal agent example](examples/minimal-agent.md) for a small,
provider-neutral design.

## Project record

Read the [Lean Agent Engineering evaluation results](docs/lean-agent-engineering-v0.1.1-project-record-through-gate-4.pdf)
(documentation updated **20 September 2026**; skill version remains **0.1.1**).
This concise PDF contains the original 18-case results and the separate Gate 2,
Gate 3, and Gate 4 results and limitations. It excludes older project-build
and publication history. The original project-record PDF remains local as a
historical source but is not part of the intended publication package.

### Document register

Dates below are local file creation and last-edit dates in this project, not
independently verified dates of the underlying historical evaluations.
Document editions are separate from the unchanged skill version.

| Document | Edition/version | Created here | Last updated | Status |
|---|---|---|---|---|
| [Canonical skill](SKILL.md) | 0.1.1 | 2026-09-12 | 2026-09-12 | Current; unchanged |
| [18-case evaluation JSON](evals/evals.json) | Skill 0.1.1 | 2026-09-12 | 2026-09-12 | Historical baseline |
| [Minimal-agent example](examples/minimal-agent.md) | Skill 0.1.1 | 2026-09-12 | 2026-09-12 | Current; unchanged |
| [README](README.md) | Skill 0.1.1 | 2026-09-12 | 2026-09-20 | Current |
| [Gate 2 review](evals/gate-2-robustness-safety.md) | Gate 2 record; skill 0.1.1 | 2026-09-20 | 2026-09-20 | Current |
| [Gate 3 review](evals/gate-3-portability-consistency.md) | Gate 3 record; skill 0.1.1 | 2026-09-20 | 2026-09-20 | Current |
| [Gate 4 evaluation record](evals/gate-4-production-reliability.md) | Gate 4 record; skill 0.1.1 | 2026-09-20 | 2026-09-20 | Current |
| [Evaluation results PDF](docs/lean-agent-engineering-v0.1.1-project-record-through-gate-4.pdf) | 2026-09-20 edition; skill 0.1.1 | 2026-09-20 | 2026-09-20 | Current |

The Apache-2.0 `LICENSE` remains unchanged since 2026-09-12. `.gitignore`
was updated on 2026-09-20 to exclude the older project PDF. Neither is a
separately versioned evaluation document.

## Evaluation

[evals/evals.json](evals/evals.json) contains the 18-case manual behavioral
suite and the historical **18/18 PASS** record. The prior review evaluated
user-pasted Codex responses. Packaging did not execute a new behavioral run.

| Case numbers | Group | Historical result |
|---|---|---|
| 1–6 | Activation / non-activation | 6/6 |
| 7–9 | Minimality | 3/3 |
| 10–11 | Debugging | 2/2 |
| 12–14 | Security | 3/3 |
| 15 | Verification | 1/1 |
| 16–18 | Architecture | 3/3 |
| Total | | 18/18 |

The earlier draft JSON had 17 entries. The final suite preserves the 18
subsequently tested prompts; `original_draft_prompt` retains earlier wording
where it differed. Case 18 comes from the final executed architecture test.
An earlier summary incorrectly counted architecture as two cases; the table
above follows the individual records.

These results do not prove internal skill activation, causal improvement
over a no-skill baseline, universal reliability, or compatibility across
clients and models. Model/runtime settings were not independently verified.
The earlier six-case smoke review excluded a contaminated negative RAG
attempt and reported a pass after a clean retest.

To repeat the suite:

1. Use a fresh conversation for each case with the skill available normally.
2. Submit only the `prompt`; withhold expected behavior and historical results.
3. Save the response and record client, model, configuration, date, and skill
   version or hash when available. Mark unavailable details as unknown.
4. Judge meaningful behavior against every `expected_behavior` criterion.
   Record PASS, PARTIAL, or FAIL with evidence. Do not score keyword matches.
5. For negative cases, check that the response remains educational. Treat
   `expected_activation` as an intended boundary, not observed telemetry.

Use simulated scenarios for destructive actions and credentials. These
prompts request design advice, not permission to operate live systems.
Keep new results separate from the historical baseline.

Later manual reviews reported Gate 2 (Robustness, Safety & Architecture) at
**12/12 PASS, 240/240** and Gate 3 (Portability & Consistency) at **12 scored
executions, 240/240**. The Gate 3 executions covered ten scenarios, with
the final scenario compared across three clients. These are historical
manual judgments, not freshly executed repository tests. The updated
results PDF summarizes them separately. Read the [Gate 2 review](evals/gate-2-robustness-safety.md)
and [Gate 3 review](evals/gate-3-portability-consistency.md) for each
scenario's plain-language purpose, historical score, observed behavior, and
limits. These records do not embed the complete original prompts and outputs;
full reproduction requires those source transcripts and a fresh evaluation.

The separate [Gate 4 Implementation & Production Reliability record](evals/gate-4-production-reliability.md)
documents eight manually reviewed implementation scenarios, their frozen
rubrics and findings: **8/8 PASS, 160/160**. Test 4 used the original
above-$500 approval rule; Test 5 evaluated the later all-refunds rule. These
scores assess generated guidance and test plans, not executed production code.
They do not establish production readiness, universal reliability, or a
controlled causal effect of this skill. Gate 2 and Gate 3 history remains
separate in their respective reviews; scores across gates should not be combined.

## Package

- [SKILL.md](SKILL.md): agent instructions and metadata.
- [evals/evals.json](evals/evals.json): prompts, criteria, and historical status.
- [evals/gate-2-robustness-safety.md](evals/gate-2-robustness-safety.md):
  twelve scenario reviews and evidence limitations.
- [evals/gate-3-portability-consistency.md](evals/gate-3-portability-consistency.md):
  twelve scored executions across ten scenarios and evidence limitations.
- [evals/gate-4-production-reliability.md](evals/gate-4-production-reliability.md):
  Gate 4 manual evaluation record and limitations.
- [Evaluation results PDF](docs/lean-agent-engineering-v0.1.1-project-record-through-gate-4.pdf):
  five-page reader-friendly summary of all four evaluation sets.
- [examples/minimal-agent.md](examples/minimal-agent.md): architecture example.
- [LICENSE](LICENSE): full Apache-2.0 terms.
- `.gitignore`: common local files and credential artifacts.
- `.gitattributes`: treats PDFs as binary for Git review.

Keep changes tied to an observed failure or missing capability, and verify
the affected behavior. Avoid adding infrastructure merely for completeness.

Copyright 2026 HumanInTheLoopAI. Licensed under the Apache License, Version 2.0.
