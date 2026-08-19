# Portability and Cost Policy

This document adds two non-negotiable constraints to the research baseline:
the system must remain adaptable to more than one agent runtime, and a loop
must be unable to spend without an explicit budget.

The Hermes references here mean the [Hermes Agent by Nous
Research](https://github.com/NousResearch/hermes-agent). If the project later
targets another Hermes runtime, it should receive a separate adapter profile.

## What stays provider-neutral

These artifacts belong to the AI-DEV-TEAM core and must not depend on a vendor:

- agent identity, responsibility, and non-responsibilities;
- task input and output contracts;
- handoff schema and acceptance criteria;
- permissions, risk levels, and approval requirements;
- task state, checkpoints, retries, and terminal states;
- evidence and trace fields;
- benchmark tasks, rubrics, and pass thresholds;
- token, call, time, and retry budgets.

The core should describe capabilities, not vendor-specific model names. A task
may request `read_only_repository_analysis` or `typescript_implementation`,
while an adapter maps that capability to the runtime and model configuration
that are available.

## What belongs in an adapter

Each runtime adapter may define:

- how an agent is registered and discovered;
- where instructions are loaded from;
- how tools and permissions are declared;
- how a handoff or delegation is invoked;
- how approvals and resumable state are represented;
- how usage and cost metadata are collected;
- which provider-specific features are optional.

The Codex adapter currently uses standalone TOML files with `name`,
`description`, and `developer_instructions`, plus optional session settings.
Claude and Hermes should not be forced to pretend their configuration models
are identical. The shared contract is the stable interface; adapters translate
it into runtime-native files and calls.

## Portability rules

1. Never put a provider-only feature in the core task contract.
2. Keep provider-specific instructions in `adapters/<runtime>/` or the
   runtime's native configuration layer.
3. Record the effective runtime, model, toolset, and adapter version in each
   run when available.
4. Maintain a capability matrix instead of assuming feature parity.
5. Evaluate the same task contract across runtimes only when the evidence and
   tool surface are comparable.
6. Treat memory, skills, MCP, sandboxing, and delegation as capabilities that
   may be absent, different, or differently priced.
7. Do not make portability a reason to erase useful runtime-specific safety
   controls.

## Token and cost budgets

Every loop task should have a budget envelope before it starts:

| Budget | Example control | Stop behavior |
|---|---|---|
| Model calls | Maximum model/tool turns | Finish or escalate when exhausted |
| Output tokens | Maximum generated output per call and run | Request concise output or stop |
| Input/context tokens | Maximum context assembled per turn | Summarize, retrieve selectively, or stop |
| Subagents | Maximum concurrent and total delegated agents | Continue sequentially or stop |
| Retries | Maximum attempts per transition | Mark `failed` or `needs_review` |
| Wall time | Maximum task duration | Mark `timed_out` |
| Money/credits | Maximum estimated cost per task and session | Require approval before increase |

The exact numeric defaults should be chosen during the evaluation-harness
workstream, not guessed in agent prompts. The important decision is that the
limits exist, are visible, and are enforced by the harness.

## Cost-control tactics

### Use the least expensive sufficient path

Start with read-only inspection, deterministic validation, and a concise
planning step. Escalate to a stronger model, more context, more retries, or
parallel specialists only when a measured failure or risk justifies it.

### Keep prompts and tools lean

State each instruction once. Load only the tools relevant to the task. Use
structured outputs and short evidence references instead of asking an agent to
repeat full files, logs, or prior responses.

### Control context growth

Pass scoped files and summaries, not the entire repository by default. Preserve
stable prefixes when the runtime supports prompt caching. Remove stale tool
results from long-running conversations when they no longer affect the next
decision.

### Avoid wasteful multi-agent fan-out

Parallel agents are useful for genuinely independent read-heavy work, but each
agent consumes its own model and tool budget. A single manager plus a bounded
checker is the default; fan-out requires a reason and a cap.

### Stop repeated failure

The harness should detect repeated identical errors, no-progress iterations,
duplicate tool calls, and oscillating plans. It should stop or escalate rather
than blindly retrying.

### Measure before optimizing

Record at least task success, total input tokens, output tokens, reasoning
tokens when available, cached tokens when available, model calls, tool calls,
wall time, retries, and estimated cost. A cheaper run that produces an
unusable artifact is not an optimization.

## Proposed default policy for the first prototype

Until the benchmark provides better numbers:

- one primary agent and at most one checker;
- no parallel fan-out by default;
- no automatic model escalation;
- no retry of the same transition more than twice;
- no retry without new evidence or a changed plan;
- no unbounded context replay;
- no side-effecting action without the required approval;
- stop and report when a budget is exhausted;
- require human approval to raise a budget.

These are safety defaults, not permanent performance limits. They can be
relaxed only after the evaluation harness shows that additional spend produces
a meaningful improvement.
