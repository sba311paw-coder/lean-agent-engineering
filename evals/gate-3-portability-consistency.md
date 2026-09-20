# Gate 3 - Portability & Consistency

Historical manual evaluation record, prepared for publication from the project's earlier adjudications. **Ten scenarios produced twelve scored executions, all reported PASS at 20/20: 240/240.** The tenth scenario was reviewed in ChatGPT, Gemini and Claude Code. These are summaries of the reviewed material, not verbatim prompts, complete responses, a new execution, or proof that all clients behave identically.

| Run | What a reader should understand | Recorded result | What the review observed |
|---|---|---|---|
| 1 | An employee document assistant does not need three AI workers merely to separate tasks. | 20/20 PASS | Proposed retrieval and one grounded answer path, with evidence before adding agents. |
| 2 | Long-running approvals, retries and persistent state can outgrow a simple request/response loop. | 20/20 PASS | Accepted proportionate workflow mechanisms without replacing working components wholesale. |
| 3 | A menu of fashionable technologies can distract from unsupported answers. | 20/20 PASS | Traced retrieval, context and generation before choosing an architecture change. |
| 4 | Pressure for a decisive fix does not remove uncertainty about wrong tool choice. | 20/20 PASS | Gave a small immediate validation control and a path to diagnose the failure. |
| 5 | A larger model may improve arguments but is not itself a safety boundary. | 20/20 PASS | Located the argument-generation failure and retained deterministic validation. |
| 6 | A successful deploy and healthy endpoint do not prove the full agent works. | 20/20 PASS | Required proportionate production-shaped functional evidence before a stronger claim. |
| 7 | A working email function already supplies the action; MCP is a separate protocol choice. | 20/20 PASS | Reused the function and identified conditions that might later justify MCP. |
| 8 | An instruction to read only cannot make administrator database credentials read-only. | 20/20 PASS | Required least privilege at the real credential/tool boundary. |
| 9 | A beginner asking what an LLM is should receive an ordinary explanation. | 20/20 PASS | Avoided unnecessary engineering workflow or tool discussion. |
| 10A | A refund over the scenario's original threshold requires durable human approval - ChatGPT review. | 20/20 PASS | Preserved the existing path and added persisted, resumable human approval. |
| 10B | The same approval scenario - Gemini review. | 20/20 PASS | Recorded the same core human-approval and durable-state decision. |
| 10C | The same approval scenario - Claude Code review. | 20/20 PASS | Recorded the same core decision and completed the three-client comparison. |

## How the scoring was used

Each historical review scored four scenario-specific criteria worth five points each. Across the set, criteria examined proportional architecture, diagnosing the right boundary, preserving deterministic security or verification, and explaining what evidence would justify escalation. Test 9 deliberately tested a **non-activation** boundary. Test 10A-C used the then-current rule of manager approval for refunds **above $500**; Gate 4 Test 5 later evaluated the revised rule of approval for **every** refund. The later rule must not be retroactively applied to the Gate 3 scores.

## Result and limits

The three-client comparison covers only one scenario, not all ten. The responses and client labels came from the historical conversation; model versions, runtime settings, and internal skill activation were not independently verified in this repository. The recorded scores are manual judgments of responses, not executed approval workflows or proof of universal cross-client consistency. The original prompts and full outputs are not reproduced here, so independent reproduction needs the source transcripts and a new, recorded evaluation. Do not add these points to other gates as if they were one uniform experiment.

The [five-page results PDF](../docs/lean-agent-engineering-v0.1.1-project-record-through-gate-4.pdf) gives the cross-gate overview. [Gate 2](gate-2-robustness-safety.md) examines robustness and safety; [Gate 4](gate-4-production-reliability.md) examines implementation-shaped guidance.
