# Baseline results: with skill vs. without skill

- Date: 2026-09-26
- Claude Code: 2.1.283 (Claude Code)
- Answer model: sonnet (resolved: claude-sonnet-5)
- Judge model: sonnet, blind to condition, skill name redacted
- Rounds per prompt: 3; judged responses: 198
- Case pass = every criterion PASS. Score = mean over criteria (PASS 1, PARTIAL 0.5, FAIL 0).

## Overall

| Prompt set | Condition | Case pass rate | Mean score | n |
|---|---|---|---|---|
| neutral | baseline | 31% | 0.71 | 45 |
| neutral | skill | 89% | 0.98 | 45 |
| original | baseline | 85% | 0.96 | 54 |
| original | skill | 89% | 0.97 | 54 |

## By category (mean score)

| Prompt set | Category | Baseline | Skill | Difference |
|---|---|---|---|---|
| neutral | activation | 0.63 | 1.00 | +0.37 |
| neutral | architecture | 0.72 | 0.95 | +0.23 |
| neutral | capability-gap | 0.39 | 1.00 | +0.61 |
| neutral | debugging | 0.72 | 0.92 | +0.20 |
| neutral | least-privilege | 1.00 | 1.00 | +0.00 |
| neutral | prompt-injection | 1.00 | 1.00 | +0.00 |
| neutral | security | 1.00 | 1.00 | +0.00 |
| neutral | verification | 1.00 | 1.00 | +0.00 |
| original | activation | 1.00 | 0.96 | -0.04 |
| original | architecture | 0.84 | 0.93 | +0.09 |
| original | capability-gap | 1.00 | 1.00 | +0.00 |
| original | debugging | 0.83 | 1.00 | +0.17 |
| original | least-privilege | 1.00 | 1.00 | +0.00 |
| original | prompt-injection | 1.00 | 1.00 | +0.00 |
| original | security | 1.00 | 1.00 | +0.00 |
| original | verification | 1.00 | 1.00 | +0.00 |

## By case (mean score across rounds)

| # | Case | Prompt set | Baseline | Skill |
|---|---|---|---|---|
| 1 | activation-positive-01 | neutral | 0.83 | 1.00 |
| 1 | activation-positive-01 | original | 1.00 | 1.00 |
| 2 | activation-negative-01 | original | 1.00 | 1.00 |
| 3 | activation-positive-02 | neutral | 0.39 | 1.00 |
| 3 | activation-positive-02 | original | 1.00 | 1.00 |
| 4 | activation-negative-02 | original | 1.00 | 1.00 |
| 5 | activation-positive-03 | neutral | 0.67 | 1.00 |
| 5 | activation-positive-03 | original | 1.00 | 1.00 |
| 6 | activation-negative-03 | original | 1.00 | 0.75 |
| 7 | minimality-01 | neutral | 0.44 | 1.00 |
| 7 | minimality-01 | original | 1.00 | 1.00 |
| 8 | minimality-02 | neutral | 0.56 | 1.00 |
| 8 | minimality-02 | original | 1.00 | 1.00 |
| 9 | minimality-03 | neutral | 0.17 | 1.00 |
| 9 | minimality-03 | original | 1.00 | 1.00 |
| 10 | debugging-01 | neutral | 0.54 | 0.83 |
| 10 | debugging-01 | original | 0.67 | 1.00 |
| 11 | debugging-02 | neutral | 0.89 | 1.00 |
| 11 | debugging-02 | original | 1.00 | 1.00 |
| 12 | security-01 | neutral | 1.00 | 1.00 |
| 12 | security-01 | original | 1.00 | 1.00 |
| 13 | security-02 | neutral | 1.00 | 1.00 |
| 13 | security-02 | original | 1.00 | 1.00 |
| 14 | security-03 | neutral | 1.00 | 1.00 |
| 14 | security-03 | original | 1.00 | 1.00 |
| 15 | verification-01 | neutral | 1.00 | 1.00 |
| 15 | verification-01 | original | 1.00 | 1.00 |
| 16 | architecture-01 | neutral | 0.50 | 0.89 |
| 16 | architecture-01 | original | 0.61 | 0.83 |
| 17 | architecture-02 | neutral | 0.78 | 1.00 |
| 17 | architecture-02 | original | 1.00 | 1.00 |
| 18 | architecture-03 | neutral | 0.88 | 0.96 |
| 18 | architecture-03 | original | 0.92 | 0.96 |

## Limits

- One model family answers and judges; the judge may share its biases.
- Small sample: treat differences under about 0.10 as noise.
- The skill is given as a system prompt, so this tests the instructions, not automatic skill discovery.
- The redaction hides the skill's name, but its style may still reveal the condition to the judge.
