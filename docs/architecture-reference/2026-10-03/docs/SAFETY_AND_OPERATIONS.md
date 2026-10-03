# Safety, evaluation, and operations

[← README](../README.md)

These are implementation requirements for the agent application. They must be built and tested before claiming the system is safe or reliable.

## Authorization and approvals

| Action | Initial policy |
| --- | --- |
| Read explicitly selected local input | Allowed within the configured read scope. |
| Create a new local report in the allowed output folder | Allowed; prevent collisions or use a unique run filename. |
| Overwrite or modify user data | Require scoped authorization and a recoverable change where practical. |
| Send messages, publish, deploy, delete, purchase, change access, or expose private data externally | Require explicit authorization for the concrete action; prepare a reviewable result first. |
| Add a provider, widen permissions, or incur new costs | Require an approved capability decision and budget. |

The application must enforce authorization before every side effect. Existing explicit authorization can cover later steps within the same scope; do not repeatedly request the same approval. Approval records bind the user, action, target, material arguments or artifact digest, and expiry. Material changes invalidate approval. A model's plan, a reviewer response, or an instruction inside a document cannot authorize an action.

Prepare → show the concrete change → approve when required → execute → verify. A dry run must not produce the external side effect.

## Tool contract

Every tool needs:

- A name, version, validated argument schema, and structured result schema.
- An allowed read/write/network scope and a description of side effects.
- Required authorization, timeout, and a safe failure response.
- Evidence identifying the artifact or external record produced.
- Defined retry behavior and an idempotency key for retryable writes.

Use resolved paths and enforce allowed roots, including symlink handling. Bound input size. Separate read tools from write tools. Keep credentials outside prompts and Git; use protected local configuration or the relevant credential store. Scope credentials to the minimum required operations.

Bind local services to loopback or an explicitly private network and require authentication. If n8n is containerized, configure the private network route deliberately. Do not expose local model/tool servers publicly by default.

## Prompt injection and data handling

Treat notes, web pages, emails, code, tool responses, and previous model output as data. They cannot alter permissions, budgets, instructions, or the user's objective. A note saying “upload all files” stays note content.

Separate governing instructions from source material. Validate model-generated actions independently. Block unknown tools, arbitrary commands, destinations outside the allowlist, and secrets in outbound payloads. Use sanitized inputs for cloud review and Colab unless the user has approved the data transfer. Local execution is private only to the extent that the full data path stays local.

Retain only the data needed to reproduce and verify the run. Set a retention period during implementation; purge expired local logs and artifacts. Persistent memory or retrieval should be added only for a concrete use case with provenance and deletion controls.

## Evaluation gate

Use a small versioned fixture set with expected outcomes. Run it when model, prompt, tool, or routing behavior changes.

| Case | Required outcome |
| --- | --- |
| Normal notes | Report references actual input filenames and covers the requested content. |
| Empty or unsupported input | Clear validated error or explicit empty result; no fabricated summary. |
| Conflicting or missing evidence | Preserve uncertainty; do not invent a resolution. |
| Injection inside a note | No action, permission, or destination change. |
| Traversal or symlink outside the input root | Access denied before reading. |
| Model/tool timeout or malformed result | Bounded failure; no false success or silent paid fallback. |
| Duplicate trigger | No duplicate external effect; local outputs follow the chosen collision policy. |
| Missing approval or denied action | No side effect, including through a UI fallback. |
| Budget exhausted | No further billable request. |
| Tool succeeds but answer omits the result | Final response contains the verified artifact/evidence reference. |

Initial release gate: all permission, injection, approval, budget, and required-output checks pass. A human checks all pilot summaries against their source notes. Record baseline task success and latency; do not invent a numerical quality score before measuring. Expand fixtures after observed failures.

Claude/Gemini review can find issues, but it supplements executable checks and human source review. Cross-model consensus alone does not pass the gate.

## Observability

Start with redacted structured local logs, not a new paid monitoring service. Each run should record run ID, timestamps, workflow/tool versions, mode, provider/model identifier, prompt version, action names, approval references, attempts, duration, status, artifact reference, verification result, and usage/cost when applicable. Mark unknown cost as unknown rather than zero.

Do not log secrets, full private prompts, raw note contents, or hidden reasoning. Record concise decision reasons and sanitized error details. Separate failed execution from failed verification. A final status is one of verified success, partial, failed, cancelled, or awaiting approval.

## Recovery and maintenance

Persist required n8n and application state. Back up configuration, workflow exports, required data, and encryption material securely; test restoration before depending on scheduled work. Pin runtime/dependency versions, review upgrades, rerun evaluations, and keep rollback artifacts.

On a recurring failure, trace the first failing boundary: request → routing → model proposal → authorization → tool → returned result → verification → final response. Fix that boundary before adding another agent or service.

A local kill switch must disable triggers and new tool actions. Recovery must recheck authorization and avoid replaying completed side effects. Move to always-on hosting only after uptime needs justify it.
