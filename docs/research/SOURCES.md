# Research Sources

Initial collection date: August 17, 2026.

Status values:

- `accepted`: directly informs the current design;
- `contextual`: useful background, but not sufficient on its own;
- `needs follow-up`: promising source that still needs deeper reading;
- `rejected`: reviewed and intentionally not used for the current milestone.

## First-party engineering and documentation

| ID | Source | Topic | Why it matters here | Status |
|---|---|---|---|---|
| OAI-01 | [Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/) | Agent loop | Describes the model–tool–environment interaction that a harness coordinates. | accepted |
| OAI-02 | [Harness engineering](https://openai.com/index/harness-engineering/) | Harness engineering | Shows the importance of repository legibility, executable constraints, feedback loops, and continuous cleanup. | accepted |
| OAI-03 | [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Custom agents | Defines the current standalone TOML shape, narrow agent responsibilities, permissions, and parallel-work tradeoffs. | accepted |
| OAI-04 | [Orchestration and handoffs](https://developers.openai.com/api/docs/guides/agents/orchestration) | Routing | Distinguishes ownership-transfer handoffs from manager-style specialist calls and warns against splitting too early. | accepted |
| OAI-05 | [Guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals) | Safety | Establishes automatic guardrails and approval interruptions as separate controls, with resumable state. | accepted |
| OAI-06 | [Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals) | Evaluation | Recommends traces for debugging, then datasets and repeatable eval runs for regression measurement. | accepted |
| OAI-07 | [Trace grading](https://developers.openai.com/api/docs/guides/trace-grading) | Observability | Treats the end-to-end trace, including tools and handoffs, as a first-class evaluation object. | accepted |
| OAI-08 | [Working with evals](https://developers.openai.com/api/docs/guides/evals) | Evaluation lifecycle | Describes task definition, test inputs, graders, and iteration; also documents the Evals platform transition. | contextual |
| OAI-09 | [Running Codex safely](https://openai.com/index/running-codex-safely/) | Permissions | Provides a first-party view of technical boundaries, explicit higher-risk actions, and telemetry. | accepted |
| OAI-10 | [Model guidance](https://developers.openai.com/api/docs/guides/latest-model) | Token efficiency | Recommends lean prompts, relevant tools, prompt caching, and measuring quality, tokens, latency, and cost together. | accepted |

## Agent design and context

| ID | Source | Topic | Why it matters here | Status |
|---|---|---|---|---|
| ANT-01 | [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents) | Workflow patterns | Covers sequential, parallel, orchestrator-workers, and evaluator-optimizer patterns and when not to use them. | accepted |
| ANT-02 | [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Context | Frames context as a finite, continuously curated state rather than only a system prompt. | accepted |
| ANT-03 | [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Agent evaluation | Explains why multi-turn tool traces require more than final-answer grading. | accepted |
| ANT-04 | [Long-running Claude for scientific computing](https://www.anthropic.com/research/long-running-Claude) | Long-running work | Highlights progress files, test oracles, persistent memory, and orchestration for resumable work. | contextual |
| ANT-05 | [Trustworthy agents in practice](https://www.anthropic.com/research/trustworthy-agents) | Governance | Frames human control, transparency, security, and privacy as design principles for agentic systems. | contextual |
| ANT-06 | [Manage tool context](https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context) | Context and cost | Describes tool search, programmatic tool calling, prompt caching, and context editing as distinct context controls. | accepted |
| ANT-07 | [Claude API pricing](https://platform.claude.com/docs/en/about-claude/pricing) | Cost | Documents prompt-cache economics and why repeated stable context should be treated as a cost concern. | contextual |

## Research papers and benchmarks

| ID | Source | Topic | Why it matters here | Status |
|---|---|---|---|---|
| PAP-01 | [ReAct](https://arxiv.org/abs/2210.03629) | Reason–act loop | Foundational evidence for interleaving reasoning and environment actions instead of planning once. | contextual |
| PAP-02 | [Reflexion](https://arxiv.org/abs/2303.11366) | Feedback memory | Shows a feedback-and-memory pattern without updating model weights; useful, but self-reflection is not independent verification. | contextual |
| PAP-03 | [SWE-agent](https://arxiv.org/abs/2405.15793) | Agent-computer interface | Demonstrates that tool/interface design materially affects software-agent performance. | accepted |
| PAP-04 | [SWE-bench](https://arxiv.org/abs/2310.06770) | Benchmarking | Establishes realistic issue-resolution tasks and executable tests as an evaluation pattern. | accepted |
| PAP-05 | [Loop engineering taxonomy](https://arxiv.org/abs/2607.00038) | Loop design | Proposes explicit triggers, goals, verification levels, architectures, and terminal states for coding-agent loops. | needs follow-up |

## Safety and governance

| ID | Source | Topic | Why it matters here | Status |
|---|---|---|---|---|
| SEC-01 | [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) | Threats | Covers prompt injection, insecure output handling, sensitive disclosure, excessive agency, and tool/supply-chain risks. | accepted |
| SEC-02 | [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) | Governance | Provides a reusable risk-management vocabulary and lifecycle for govern, map, measure, and manage. | contextual |

## Runtime portability

| ID | Source | Topic | Why it matters here | Status |
|---|---|---|---|---|
| HERMES-01 | [Hermes tools and toolsets](https://github.com/hermes-agent-org/hermes/blob/main/website/docs/user-guide/features/tools.md) | Runtime capabilities | Shows explicit toolsets, delegation, memory, and terminal/file surfaces that an adapter may need to map. | accepted |
| HERMES-02 | [Hermes Agent repository](https://github.com/NousResearch/hermes-agent) | Runtime architecture | Confirms the intended portability target is a multi-model, multi-surface agent runtime rather than a Codex-only file format. | contextual |

## Workflow skills

| ID | Source | Topic | Why it matters here | Status |
|---|---|---|---|---|
| JSM-01 | [JavaScript Mastery Engineering Workflow Skills](https://github.com/jsmastery-pro/skills) | File-backed workflow | Provides useful patterns for durable repository state, scoped skills, quality profiles, separate runtime verification and independent review, explicit artifact ownership, and synchronization. We adapt the patterns without importing its commands or provider-specific behavior. | accepted |

## Source-selection note

The corpus intentionally mixes first-party implementation guidance, academic
work, benchmarks, and safety standards. Product documentation tells us what a
current platform exposes; papers and standards help us reason about general
patterns and limitations. None of these sources replaces local evaluation.
