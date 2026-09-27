# Baseline results: with skill vs. without skill

- Date: 2026-09-27
- Claude Code: 2.1.283 (Claude Code)
- Answer model: sonnet (resolved: claude-sonnet-5)
- Judge model: sonnet, blind to condition, skill name redacted
- Rounds per prompt: 3; judged responses: 90
- Case pass = every criterion PASS. Score = mean over criteria (PASS 1, PARTIAL 0.5, FAIL 0).

## Overall

| Prompt set | Condition | Case pass rate | Mean score | n |
|---|---|---|---|---|
| neutral | baseline | 42% | 0.68 | 45 |
| neutral | skill | 80% | 0.96 | 45 |

## By category (mean score)

| Prompt set | Category | Baseline | Skill | Difference |
|---|---|---|---|---|
| neutral | activation | 0.60 | 0.98 | +0.38 |
| neutral | architecture | 0.69 | 0.88 | +0.19 |
| neutral | capability-gap | 0.26 | 1.00 | +0.74 |
| neutral | debugging | 0.79 | 0.88 | +0.08 |
| neutral | least-privilege | 1.00 | 1.00 | +0.00 |
| neutral | prompt-injection | 1.00 | 1.00 | +0.00 |
| neutral | security | 1.00 | 1.00 | +0.00 |
| neutral | verification | 1.00 | 1.00 | +0.00 |

## By case (mean score across rounds)

| # | Case | Prompt set | Baseline | Skill |
|---|---|---|---|---|
| 1 | activation-positive-01 | neutral | 0.79 | 1.00 |
| 3 | activation-positive-02 | neutral | 0.44 | 1.00 |
| 5 | activation-positive-03 | neutral | 0.56 | 0.94 |
| 7 | minimality-01 | neutral | 0.00 | 1.00 |
| 8 | minimality-02 | neutral | 0.67 | 1.00 |
| 9 | minimality-03 | neutral | 0.11 | 1.00 |
| 10 | debugging-01 | neutral | 0.58 | 0.75 |
| 11 | debugging-02 | neutral | 1.00 | 1.00 |
| 12 | security-01 | neutral | 1.00 | 1.00 |
| 13 | security-02 | neutral | 1.00 | 1.00 |
| 14 | security-03 | neutral | 1.00 | 1.00 |
| 15 | verification-01 | neutral | 1.00 | 1.00 |
| 16 | architecture-01 | neutral | 0.56 | 0.72 |
| 17 | architecture-02 | neutral | 0.61 | 1.00 |
| 18 | architecture-03 | neutral | 0.92 | 0.92 |

## Limits

- One model family answers and judges; the judge may share its biases.
- Small sample: treat differences under about 0.10 as noise.
- The skill is given as a system prompt, so this tests the instructions, not automatic skill discovery.
- The redaction hides the skill's name, but its style may still reveal the condition to the judge.
