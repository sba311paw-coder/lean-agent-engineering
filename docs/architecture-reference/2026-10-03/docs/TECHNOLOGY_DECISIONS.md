# Reference technology profile

[← README](../README.md)

Decisions below consolidate the user's canonical stack. Roles express project policy, not universal vendor rankings. Official references were checked on **2026-10-03**; versions, entitlements, limits, and terms must be rechecked when implementing or purchasing.

## Model and provider strategy

| Technology | Chosen role | Access and constraints |
| --- | --- | --- |
| Ollama | Preferred programmatic local inference path. | Use an explicitly local model and endpoint; evaluate on the target Mac before adopting it. |
| LM Studio | Explore and compare local models; alternate local serving when needed. | Reuse the same tool contracts; do not run duplicate servers without a reason. |
| OpenAI / ChatGPT / Codex | Codex is the default coding and implementation agent; ChatGPT supports human-led planning. | Existing subscription for supported product access; OpenAI API calls need separate API access and billing controls. |
| Claude | Secondary architecture, reasoning, and code review. | Start with existing subscribed product access; API automation is a separate decision. |
| Gemini | Secondary validation; evaluate for multimodal, larger-context, and Google-related tasks when relevant. | Start with existing product access; verify Gemini API tier, billing, and data handling separately. |
| Hugging Face | Discover model weights, datasets, model cards, and evaluation resources. | Check each resource's license, provenance, runtime format, memory needs, and permitted use. Hosted inference is a separate service choice. |

Ollama documents a local HTTP API. LM Studio documents local serving interfaces. Those capabilities support the chosen roles; they do not establish that a particular model fits this Mac or passes our evaluations. [Ollama API](https://docs.ollama.com/api/introduction), [LM Studio developer documentation](https://lmstudio.ai/docs/developer).

Codex access through supported ChatGPT plans has plan-specific limits. ChatGPT subscription access and API billing are separate. Claude likewise distinguishes subscriptions from API access; Gemini API documents its own free and paid tiers. Do not promise unlimited automation or assume a chat subscription is an API credit balance. [Codex plan access](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan), [ChatGPT Plus and API billing](https://help.openai.com/en/articles/6950777-what-is-chatgpt-plus), [Claude API separation](https://support.claude.com/en/articles/9876003-i-have-a-paid-claude-subscription-pro-max-team-or-enterprise-plans-why-do-i-have-to-pay-separately-to-use-the-claude-api-and-console), [Gemini API billing](https://ai.google.dev/gemini-api/docs/billing).

### Selection rules

- Use no model when a deterministic tool suffices.
- Benchmark a small suitable local model first. Choose by task success, grounding, latency, memory use, and license, rather than popularity.
- Pin the chosen model identifier, artifact revision or digest where available, runtime version, and prompt version. Record changes and rerun evaluations.
- Use existing subscribed tools for supported human-led development and review. Do not automate subscription web interfaces to substitute for an API.
- Add an API adapter only for a demonstrated unattended-runtime or quality gap. Apply explicit data permission and budget caps.
- Reviewers must inspect source evidence and tests. Agreement among models is not proof of correctness.

Hugging Face model cards and repository licenses inform resource selection; presence on the Hub does not mean unrestricted use or local compatibility. [Models](https://huggingface.co/docs/hub/models), [Model cards](https://huggingface.co/docs/hub/model-cards), [Licenses](https://huggingface.co/docs/hub/repositories-licenses).

No fixed “best model” or model size is selected here because hardware capacity and workload results have not been established.

## n8n Community

Use self-hosted n8n Community for scheduling, predictable workflow control, routing, retries, and approval checkpoints. Keep reusable business logic and tool safety in Python so workflows remain thin and inspectable.

Community is a free self-hosted edition, with feature differences from paid editions. It is distributed under n8n's Sustainable Use License; do not describe it as unrestricted open-source software. Before changing to a customer-facing or resale use case, review the applicable license. [Edition comparison](https://github.com/n8n-io/n8n-docs/blob/main/docs/deploy/host-n8n/community-edition-features.md), [Official license](https://github.com/n8n-io/n8n/blob/master/LICENSE.md).

Start with one local instance and one manual workflow. Persist instance data and protect the credential-encryption key; test restoration. Export sanitized workflow JSON to Git manually. Do not depend on paid built-in source-control, external-secrets, or log-streaming features. Implement the project's approval checks and redacted logging at the Python boundary.

## Google Colab

Use the free tier when an interactive experiment needs temporary compute beyond the Mac: PyTorch learning, embedding comparisons, model benchmarks, or small fine-tuning/LoRA trials. Whether an experiment fits depends on the allocated hardware, model, and data.

Google says free resources, including accelerators, are available but not guaranteed; limits fluctuate and virtual machines have finite lifetimes. Therefore Colab is not the the agent application runtime, n8n host, persistent API, or unattended worker. [Official Colab FAQ](https://research.google.com/colaboratory/faq.html).

Save notebooks, dependency versions, results, and checkpoints outside the temporary runtime. Strip secrets and sensitive outputs before committing. Use approved or sanitized data; a cloud lab is outside the local privacy boundary. If free capacity is unavailable, wait, reduce the experiment, or document the gap before considering payment.

**Mac first. Colab when temporary compute is needed. Production cloud only when the project requires it.**

## Python

Use Python for narrow tool functions, schema validation, provider adapters, policy enforcement, tests, and result verification. Start with the standard library and add focused dependencies only when needed. Separate model calls from file/API operations. Do not let generated text become executable code or arbitrary shell commands.

## MCP

MCP is an interoperability protocol with host, client, and server roles. In this architecture it is an optional adapter, not a mandatory orchestration layer. [Official architecture](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture).

Add it only after the underlying tools have stable inputs/outputs, permission checks, failure behavior, meaningful tests, and a real second-client need. Expose only the required tools. Keep direct Python access and MCP access behaviorally equivalent. Connecting a server must not imply blanket permission for all its tools.

## Deferred purchases and additions

Devin and other new paid coding-agent subscriptions are reference options only. No paid hosted agent platform, paid n8n tier, new orchestration framework, always-on GPU, or multi-agent platform is planned by default. The [cost policy](COST_POLICY.md) governs exceptions.
