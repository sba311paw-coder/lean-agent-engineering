# Cost policy

[← README](../README.md)

## Spending order

| Order | Preferred path | Rule |
| --- | --- | --- |
| 1 | Local / free / self-hosted | Python, local models, n8n Community, suitable freely available resources, and optional Colab free experiments. |
| 2 | Existing subscriptions | Use supported ChatGPT/Codex, Claude, and Gemini product access already paid for. |
| 3 | Usage-based APIs | Add only for a proven quality, capability, or unattended-execution gap. |
| 4 | New paid subscriptions | Last resort after simpler and already-paid options fail to meet the requirement. |

“Local” and “free” do not mean zero total cost: hardware, electricity, storage, maintenance, and time still matter. Minimize incremental spending while meeting a measured reliability requirement. A cheapest option that repeatedly fails is not the right option.

Existing subscriptions are user-reported in the source conversation. This package has not audited account entitlements, remaining quotas, or invoices. API access and subscription access must be evaluated separately; see [official provider references](TECHNOLOGY_DECISIONS.md#model-and-provider-strategy).

## Gate for any escalation

Write down all of the following before adding a paid service or greater complexity:

1. The exact missing capability and the acceptance test it must pass.
2. What was tried using current tools, and reproducible failure evidence.
3. Simpler local/free alternatives considered, including reducing scope.
4. A bounded comparison showing the proposed option fixes the gap.
5. Expected volume, estimated cost with assumptions, privacy impact, and maintenance burden.
6. The spending cap, approval owner, expiry/review date, and removal plan.

Approval applies to the named service and limits. It does not authorize future vendors, unlimited usage, or automatic renewal. No Devin or other new agent subscription without this evidence and explicit user approval.

## Runtime budget controls

Initial incremental paid-API budget: **zero until approved**. This is the proposed implementation default; it does not cancel existing subscriptions.

Before enabling billable calls, configure a currency-denominated per-run and monthly cap, provider/model allowlist, token limit, tool-step limit, retry limit, and timeout. Unset caps disable billable routing. Reserve estimated cost before a call; reconcile recorded usage afterward. Treat unknown usage conservatively and stop when remaining budget cannot cover the next call.

Do not rely solely on provider dashboards as hard enforcement. Keep an application ledger, account for other users of shared credentials, and use provider-side controls where available. Include embedding calls, reviewer calls, retries, background jobs, hosted inference, storage, and compute in estimates.

On local failure or quota exhaustion, stop or hand off with the recorded reason. Never silently switch to a paid API or new subscription.

## Review costs only when there is something to review

After the first workflow passes, record success rate, elapsed time, local resource use, and incremental paid spend. Compare on representative tasks before changing providers. Revisit a paid addition when its approved review date arrives or its workload changes; remove it if the original gap no longer exists.

Prices and product limits are deliberately not hard-coded here. Check official terms at the point of purchase and record the date and assumptions in the decision.
