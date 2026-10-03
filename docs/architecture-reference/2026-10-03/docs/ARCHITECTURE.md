# Lean agent architecture

[← README](../README.md)

## Canonical philosophy

Start with the outcome and the evidence needed to verify it. Reuse existing capabilities. Prefer direct tools and predictable workflows. Add the smallest capability that closes a demonstrated gap.

The agent application is the assistant application, not a particular model, chat subscription, or orchestration vendor. Provider changes must not change tool permissions or the definition of success.

## Runtime and development are separate

| Layer | Responsibility | Boundary |
| --- | --- | --- |
| User / trigger | Supplies goal, scope, and authorized actions. | Scheduled work inherits only its saved authorization. |
| n8n Community | Coordinates steps, schedules, branches, bounded retries, and approval waits. | Does not give models unrestricted credentials or action authority. |
| Python agent application | Validates input, selects workflow/model, enforces budgets, calls tools, and verifies results. | Owns tool allowlists, approval checks, and stopping rules. |
| Model adapter | Translates task and tool-result data into a provider request and normalizes its response. | Model output is an untrusted proposal until validated. |
| Python tools | Perform narrow file, API, database, and calculation operations. | Each tool has explicit inputs, side effects, permissions, and evidence. |
| State / artifacts | Stores run status, approvals, source references, reports, and checkpoints locally. | Minimum required retention; no implicit permanent memory. |
| Verifier | Checks output against task requirements and source evidence. | Completion requires evidence, not a successful exit alone. |
| Development / lab | Codex implementation, optional Claude/Gemini review, Hugging Face research, optional Colab experiments. | Review and experiments do not authorize runtime actions. |

Start with local files and structured run records. Add a database, retrieval store, queue, or remote host only when actual persistence, search, concurrency, or availability needs justify it. Do not add a vector database or agent framework by default.

## One request, end to end

1. Accept a user request or an authorized n8n trigger; assign a run ID.
2. Validate the input, allowed data, destination, action scope, and budget.
3. Choose a fixed workflow when the steps are known. Use a bounded single-agent loop only for uncertain decisions.
4. If judgment is needed, call an appropriate local model first. Route to another provider only under the cost and data policies.
5. Validate any proposed tool call against its schema and allowlist. Check authorization at the tool boundary. Obtain approval when the policy requires it.
6. Execute the narrow Python tool. Capture a structured result, failures, and evidence.
7. Return the result to the application and, if useful, the model. Keep retrieved content separate from governing instructions.
8. Verify the intended outcome. Retry only within saved limits; otherwise return a clear partial or failed result.
9. Save the artifact and a redacted run record. Tell the user what was verified and what remains unresolved.

For the first workflow, n8n should call a private authenticated Python entry point that accepts a named operation and validated arguments. Do not expose a generic shell executor. A containerized n8n instance needs an explicitly configured route to the local service; its localhost is not the Mac's localhost.

## Workflow → agent → multi-agent

| Mode | Use when | Escalation gate |
| --- | --- | --- |
| Direct tool or script | A calculation, conversion, lookup, or other known operation suffices. | No model needed. |
| n8n workflow | Steps, conditions, and failure paths can be written down. | A model node may handle one bounded classification or summary without turning the whole workflow into an agent. |
| Single agent | The next useful step depends on observations and cannot be expressed reliably as fixed branches. | Define allowed tools, success evidence, step/time/cost limits, and stopping rules first. |
| Multi-agent | Work has separable tasks or a valuable independent review, and a single worker has a demonstrated limitation. | Measure benefit against coordination cost; require defined roles, shared contracts, one coordinator, and one verifier. |

Use Codex as the development worker because it is already subscribed. Use Claude or Gemini for targeted independent review when the stakes or ambiguity justify it. Sequential review is enough in many cases; cross-provider review does not require building a multi-agent runtime.

No recursive delegation, automatic purchase, or unbounded “keep trying” loop. On exhaustion, report the evidence and ask for a changed scope or authorized escalation.

## Browser and computer-use hierarchy

Use the highest reliable option available for the task:

1. Existing tool, connector, or documented application API with suitable permissions.
2. Purpose-built CLI or SDK using the same narrow authorization.
3. Browser automation using page structure, stable selectors, and observable state.
4. Visual browser interaction when page structure is unavailable or unreliable.
5. Native computer use for desktop-only tasks or remaining UI gaps.
6. Human handoff when state, access, or the result cannot be safely verified.

Before moving down the hierarchy, record the missing capability or failure. Do not change channels to evade a permission denial. Browser and desktop automation inherit the same action policy as APIs: inspect and prepare first; approve high-impact execution at the final boundary. Verify the resulting saved record or artifact, not just a click or screenshot of a success message. Do not bypass authentication challenges or access controls.

## MCP placement

Keep Python functions and their direct interface as the source of truth. If another client later needs these stable tools, expose a small MCP adapter that delegates to the same implementation and authorization checks. MCP standardizes an interface; it does not replace the application, verifier, or permission policy. See [Technology decisions](TECHNOLOGY_DECISIONS.md#mcp).

## Deployment boundary

The first deployment target is the local Mac. A sleeping or offline Mac cannot provide reliable scheduled execution. Move selected services to an always-on host only after an availability requirement is established, backup/restore is tested, and the cost is approved. Colab stays outside the production path.
