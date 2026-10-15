# Engineering resources and future capabilities

Updated 10-15-2026. This is a documentation addendum, not a skill release or an executable runtime.

See [architecture diagrams and options](ARCHITECTURE-OPTIONS.md) for the application/model/tool boundary, optional paths, and evidence loop.

A concrete anticipated future use can justify building a bounded optional capability before a current failure occurs. Describe the use, alternatives, prerequisites, maintenance, activation policy, and verification. Simplicity remains a design preference, not a ban on useful future functionality. Credentials, paid usage, external data, and production authority are separate decisions.

## Ordered engineering backlog

1. Maintain source-linked documentation and learning references.
2. Define provider-independent evaluation case, trace, decision, and result contracts.
3. Add metadata-first trace correlation and explicit usage accounting.
4. Consolidate safety, recovery, and context datasets; calibrate advisory semantic graders.
5. Build optional capability registries, decision providers, compaction, and framework adapters with disabled/unavailable paths and clear activation criteria.

This repository supplies guidance. Deterministic enforcement belongs to the host application and tools. No package integration or new runtime is claimed here. Existing baseline scores evaluate explicit skill instructions and must not be relabeled as automatic discovery, universal portability, or a production security proof. SKILL.md version 0.1.2 and its evaluation history are unchanged by this addendum.

## Official learning references

| Topic | References | Evidence expected |
|---|---|---|
| Context and durable state | [Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) | Selective context and readable task state preserve sources and corrections |
| Evaluation | [Anthropic agent evaluations](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), [OpenAI agent evaluations](https://developers.openai.com/api/docs/guides/agent-evals), [LangSmith evaluation](https://docs.langchain.com/langsmith/evaluation) | Frozen cases, repeated trials, actual outcomes, and human calibration |
| Tracing | [Claude OpenTelemetry](https://platform.claude.com/docs/en/manage-claude/opentelemetry), [NVIDIA toolkit v1.9.0](https://github.com/NVIDIA/NeMo-Agent-Toolkit/releases/tag/v1.9.0) | Correlation, redaction, retention, and nonduplicated usage |
| Decision providers | [OpenAI Decisions](https://developers.openai.com/api/docs/guides/decisions), [Jev confidence](https://docs.typesafe.ai/confidence), [Jev limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13) | Raw provider semantics, abstention, option permutation, policy independent of confidence |
| Skills | [Deep Agents skills](https://docs.langchain.com/oss/python/deepagents/skills), [TypeSafe skill](https://docs.typesafe.ai/agent-skill), [NVIDIA catalog](https://github.com/NVIDIA/skills/tree/main/skills) | Discovery and negative activation checked separately from instruction quality |
| Tools and coding workflows | [xAI function calling](https://docs.x.ai/developers/tools/function-calling), [Open SWE](https://github.com/langchain-ai/open-swe), [Deep Agents Code](https://docs.langchain.com/oss/deepagents/code/overview) | Tool/result association, isolation, approval, bounded retries |
| Documentation evidence | [OpenWiki](https://github.com/langchain-ai/openwiki) | Versioned source claims and reviewed drift handling |

References reviewed 10-15-2026. Verify current APIs, models, release maturity, license, hardware, privacy, and cost before implementation. A source's availability does not establish an installed integration. Do not compare different providers' confidence values as interchangeable measurements. Do not use opaque model context as authorization state.
