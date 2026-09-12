# A minimal personal agent

Suppose a personal Python application needs to answer questions and call
two existing, read-only functions. Start with one application process, one
model interface, and those functions. This is an illustrative design, not
an executable implementation or a provider API contract.

```text
User request
    |
    v
Application builds context and tool descriptions
    |
    v
LLM returns an answer or proposes a tool call
    |
    v
Application validates arguments and enforces authorization
    |
    v
Existing function returns data or an error
    |
    v
Application supplies the result to the LLM
    |
    v
LLM drafts an answer; application checks the outcome
    |
    v
User receives the answer or an honest failure report
```

The model proposes actions. The application controls execution. A tool
result appearing in a log is insufficient: it must reach the context used
to generate the final answer.

## Application responsibilities

Keep an explicit allowlist of the two functions. Validate each proposed
function name and its arguments before execution. Enforce the user's
permissions at the application or tool boundary; a model proposal never
grants authority. Treat returned text as data rather than new instructions.

Bound the number of tool rounds and use appropriate timeouts. Return an
honest failure when a call fails or the limit is reached. If a tool later
gains external side effects, add safeguards appropriate to those effects
and the application's authorization policy. Do not blindly retry mutations.

Use the host model interface's documented message format to associate
results with their originating calls. Keep provider-specific formatting
inside that interface, so the ordinary Python functions remain reusable.

## Small verification plan

Try one question that needs no tool, one for each function, an invalid
argument, a function failure, an unauthorized call, and a tool-round limit.
Check that each valid result reaches the final answer and each failure
remains visible. Use synthetic data and avoid logging credentials.

For example, if a synthetic weather fixture returns 21 degrees Celsius,
the answer should use that value and unit. If the answer ignores it,
inspect the exact follow-up model request before changing the function.

Direct function calls and basic logs are sufficient for this starting
design. Add a framework or separate service only after a measured need
cannot be met by a smaller local change.
