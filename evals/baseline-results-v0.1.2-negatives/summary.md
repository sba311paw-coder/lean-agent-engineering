# Baseline results: with skill vs. without skill

- Date: 2026-09-27
- Claude Code: 2.1.283 (Claude Code)
- Answer model: sonnet (resolved: claude-sonnet-5)
- Judge model: sonnet, blind to condition, skill name redacted
- Rounds per prompt: 3; judged responses: 18
- Case pass = every criterion PASS. Score = mean over criteria (PASS 1, PARTIAL 0.5, FAIL 0).

## Overall

| Prompt set | Condition | Case pass rate | Mean score | n |
|---|---|---|---|---|
| original | baseline | 100% | 1.00 | 9 |
| original | skill | 100% | 1.00 | 9 |

## By category (mean score)

| Prompt set | Category | Baseline | Skill | Difference |
|---|---|---|---|---|
| original | activation | 1.00 | 1.00 | +0.00 |

## By case (mean score across rounds)

| # | Case | Prompt set | Baseline | Skill |
|---|---|---|---|---|
| 2 | activation-negative-01 | original | 1.00 | 1.00 |
| 4 | activation-negative-02 | original | 1.00 | 1.00 |
| 6 | activation-negative-03 | original | 1.00 | 1.00 |

## Limits

- One model family answers and judges; the judge may share its biases.
- Small sample: treat differences under about 0.10 as noise.
- The skill is given as a system prompt, so this tests the instructions, not automatic skill discovery.
- The redaction hides the skill's name, but its style may still reveal the condition to the judge.
