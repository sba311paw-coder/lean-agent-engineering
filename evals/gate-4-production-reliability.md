# Gate 4 — Implementation & Production Reliability

Historical manual evaluation record, frozen from the referenced project conversation. Eight scenario responses were reviewed against four predefined criteria each (5 points per criterion). This document records the adjudicated results; it is not a newly executed test suite or a production certification. The full prompts, responses, and reviews remain in the project conversation; the scenario descriptions below are summaries, not substitute verbatim prompts.

The [evaluation results PDF](../docs/lean-agent-engineering-v0.1.1-project-record-through-gate-4.pdf) reports the original 18-case results and separate Gate 2, Gate 3, and Gate 4 results without the older project's publication history.

| Test | Scenario | Result |
|---|---|---:|
| 1 | Minimal two-tool Python agent | PASS 20/20 |
| 2 | Semantic refund validation | PASS 20/20 |
| 3 | Unknown payment outcome and idempotency | PASS 20/20 |
| 4 | Durable approval for refunds above $500 (original rule) | PASS 20/20 |
| 5 | Revised rule: human approval for every refund | PASS 20/20 |
| 6 | Authentication and object-level authorization | PASS 20/20 |
| 7 | Sensitive tool-output minimization | PASS 20/20 |
| 8 | End-to-end production verification | PASS 20/20 |
| **Total** | **8/8 completed** | **160/160** |

## Frozen rubrics and observed findings

Each line in a rubric is worth 5 points; all four were awarded in the historical review. Critical-failure conditions, where specified, override a numerical score.

### Test 1 — Minimal two-tool agent

Rubric: (1) minimal architecture and direct reuse of functions; (2) LLM/application separation; (3) allowlist, validation, unknown-tool handling, bounded rounds; (4) tool-result handoff and meaningful tests. Finding: the proposed loop used two existing functions, validated allowed calls, and returned tool results to the LLM. No arbitrary dispatch or unbounded loop was observed. Caveats: sample exception handling did not cover all production failures, and `str(result)` was demonstration-grade serialization.

### Test 2 — Semantic validation

Rubric: (1) existing function reused with minimal architecture; (2) deterministic type/range and semantic validation; (3) customer/order/refundable-amount relationship validated before execution; (4) validation and execution failures separated, with meaningful tests. Finding: model arguments were treated as untrusted proposals and checked against authoritative order data before refund execution. Executing before semantic validation was the critical failure condition. Caveat: an authoritative service must enforce refundable balance atomically under concurrency; a pre-check alone can race.

### Test 3 — Unknown outcome and idempotency

Rubric: (1) timeout-after-send recognized as unknown outcome; (2) blind retries prevented and idempotency used correctly; (3) deterministic application-owned retry/reconciliation policy; (4) provider limits and failure tests addressed. Finding: an uncertain charge was not treated as failed; stable operation identity and reconciliation were required. Blindly retrying an uncertain payment was the critical failure condition. Caveats: durable persistence, bounded reconciliation, and actual provider key scope/retention need implementation-specific verification.

### Test 4 — Durable human approval, original threshold

Rubric: (1) genuine application-enforced human approval; (2) restart-safe state bound to an exact immutable request; (3) no execution without valid approval and no duplicate execution; (4) separated responsibilities and failure/restart tests. Finding: the proposed persisted workflow met the **then-frozen rule**: refunds above $500 required manager approval; $500 or less could use the existing validated path. LLM-as-approver, post-approval request mutation, or duplicate execution were critical failures. The later all-refunds policy must not be retroactively applied to this score.

### Test 5 — Universal human approval

Rubric: (1) every refund requires human approval, with no amount bypass; (2) human, immutable, persistent, request-bound, application-enforced approval; (3) bypass, mismatch, duplicate execution, and unsafe unknown-outcome retry prevented; (4) implementation/tests cover $1, $100, $500, $501 and an LLM bypass attempt. Finding: the revised design removed the threshold branch and withheld direct `issue_refund` dispatch from the LLM. Any amount-based execution bypass without human approval was an automatic failure. Caveat: provider idempotency/reconciliation is still necessary after a crash between external success and persisted completion.

### Test 6 — Authentication and authorization

Rubric: (1) identity from authoritative application context; (2) object-level authorization before execution and default deny; (3) no LLM permission bypass and least privilege; (4) distinct failures and meaningful tests. Finding: the model proposed a customer ID, while application/session identity and customer scope controlled the actual call; denied paths asserted that the tool was not called. Caveat: the sample dispatcher ignored unexpected role/employee fields while a sample test expected rejection; strict argument-key rejection should be implemented in production, though ignored fields did not become authority.

### Test 7 — Sensitive output and minimization

Rubric: (1) raw sensitive tool output not passed wholesale to the LLM; (2) deterministic application-side allowlist/minimization; (3) new, unknown, or malformed fields handled safely; (4) logging/model-context boundary and leakage tests. Finding: a new sanitized object was built before the model boundary, with integration checks of actual model messages. Sending raw diagnostics to the LLM and asking it not to reveal secrets was an automatic failure. Caveats: allowlisted free-text values can themselves contain secrets; the sample defined an allowlist constant separately from the explicit output construction, creating a possible schema-drift point.

### Test 8 — End-to-end production verification

Rubric: (1) deployment/health distinguished from functional verification; (2) complete production-shaped application → LLM → retrieval/tool → result → final-answer path tested; (3) safe positive and negative authorization canaries; (4) objective release evidence/failure gate without unnecessary architecture. Finding: exit code 0, running container, HTTP 200, and dependency connectivity were insufficient; synthetic records tested retrieval, tool choice, argument validation, authorization, permitted execution, result handoff, and evidence-grounded answer. The negative canary required proof that an unauthorized tool did not execute. Declaring success from health alone or testing unsafely on real customer data was an automatic failure.

## Architecture audit

The cases exercised separate boundaries: model proposal versus application execution; authoritative identity and object scope; semantic validation before side effects; durable human approval; unknown external outcomes; result minimization before model context; and functional verification after deployment. The smallest adequate solution reused existing functions and added deterministic controls only where the scenario required them. This supports the skill's lean, safety, and security guidance within these scenarios; it does not prove a deployed implementation is safe.

The canonical `SKILL.md` already states the governing capability-gap, application authorization, human-approval-when-required, high-impact, untrusted-content, and verification principles. These findings do not establish a concrete missing core capability, so Gate 4 alone does not justify changing it. The implementation caveats above remain context-dependent engineering work, not generic promises made by the skill.

## Method and limitations

The scores are historical manual judgments of generated architecture/code or pseudocode and test plans, not results of running the snippets against real payment, refund, identity, or production systems. The exact model/runtime configuration, skill activation telemetry, and a controlled no-skill baseline were not independently verified here. The scenarios are not statistically representative, and full scores do not demonstrate universal reliability, exploit resistance, cross-client consistency, production readiness, or regulatory compliance. Reproduction requires the original prompts and outputs plus a recorded client/model/configuration and fresh, independently adjudicated runs; keep those results separate.

Gate 2 (12/12, 240/240) and Gate 3 (12 scored executions, 240/240) are distinct historical evaluations, documented in their separate records in this repository; their scores are not combined with Gate 4. The existing 18-case suite in `evals.json` is another separate historical baseline. Its results were not altered for this Gate 4 addition.
