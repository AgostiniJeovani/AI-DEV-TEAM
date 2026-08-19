# Research Decisions

Decision status:

- `accepted`: applies to the current milestone;
- `open`: requires a later design choice or experiment;
- `rejected`: explicitly outside the current approach.

## Accepted decisions

### R-001 — Keep the first loop repository-local

**Status:** accepted

The first task contract, state file, checkpoints, traces, and evaluation
results will live in versioned or ignored repository-local files. This keeps
the proof portable, inspectable, and easy to test on Windows. A database,
queue, or hosted tracing system is not justified before the local proof fails
to meet a concrete requirement.

### R-002 — Use explicit terminal states

**Status:** accepted

Every loop task must finish as `completed`, `blocked`, `needs_review`,
`failed`, `cancelled`, or `timed_out`. The orchestrator must not interpret an
empty response or a model claim as completion.

### R-003 — Separate making from checking

**Status:** accepted

The first verification flow will use a maker artifact plus independent checker
criteria. The checker may request revision or block the task. Automated tests,
validators, and policy checks should be preferred over subjective approval.

### R-004 — Require human approval at side-effect boundaries

**Status:** accepted

Sensitive changes pause before execution or publication. Approval must resume
the same task state and record the decision. The system fails closed when a
required reviewer or approval state is unavailable.

### R-005 — Preserve the current agent boundaries

**Status:** accepted

Agents marked read-only remain design, analysis, or review roles rather than
implementers. The future `agent-engineer` may propose improvements to this
repository, but it must not silently modify its own active definition or
bypass the approval and evaluation path.

### R-006 — Start with one narrow workflow

**Status:** accepted

The first end-to-end demonstration will focus on a repository-maintenance
task, such as proposing and validating a change to an agent or documentation
artifact. We will expand only after the state, evidence, and stop behavior are
observable.

### R-007 — Do not pin models by default

**Status:** accepted

Agent TOML files will avoid a fixed model unless an experiment explicitly
needs a stable comparison target. The harness must record the effective model
when that information is available.

### R-008 — Make budgets part of the task contract

**Status:** accepted

Every loop task must carry visible limits for model calls, context, output,
retries, subagents, wall time, and estimated money/credits. A budget is a
runtime control, not merely a suggestion in an agent prompt. Raising a budget
requires an explicit approval or policy decision.

### R-009 — Keep the core provider-neutral

**Status:** accepted

The core stores responsibilities, contracts, handoffs, states, evidence,
rubrics, and budgets. Codex, Claude, and Hermes-specific registration,
tooling, permissions, and memory behavior belong in adapters. Feature parity
must be tested rather than assumed.

### R-010 — Optimize for useful work per unit cost

**Status:** accepted

The project will measure success, evidence quality, tokens, calls, retries,
latency, and estimated cost together. Fewer tokens or calls count as an
improvement only when the artifact still meets its acceptance criteria.

### R-011 - Use quality profiles to control verification depth

**Status:** accepted

Tasks will declare a default quality profile: `prototype`, `alpha`, `beta`, or
`ga`. The profile controls the suggested verification tail and expected cost,
while risk, security, approval, and architecture requirements can still force
stronger checks. A profile is not permission to bypass a required control.

### R-012 - Persist state and evidence in repository artifacts

**Status:** accepted

The loop must keep contracts, checkpoints, acceptance traceability, review
findings, and synchronization reports in durable files. Chat history is useful
for interaction, but it is not the source of truth for resuming a task.

### R-013 - Give each durable artifact one owner

**Status:** accepted

Agents may read another agent's artifact and report that it is stale, but they
must not silently rewrite another agent's source of truth. This keeps handoffs
legible and limits accidental prompt or policy drift.

## Open decisions

### R-101 — State format

Should the first task state use one human-readable Markdown/JSON pair, a
single JSON document, or append-only JSONL events plus a materialized summary?

### R-102 — Checker independence

Should the first checker be a separate Codex subagent, a deterministic script,
or both? The likely answer is both, but the minimum useful combination needs
an experiment.

### R-103 — Trace schema

Which fields are required for later cost, latency, handoff, and reliability
analysis without recording unnecessary private context?

### R-104 — Agent-engineer scope

Which repository changes may `agent-engineer` propose automatically, and which
always require a human-authored task or explicit approval?

### R-105 — Public benchmark

Which small, reproducible tasks best demonstrate the project publicly without
pretending that they represent general software-engineering reliability?

### R-106 — Numeric budget defaults

What initial per-task and per-session limits are appropriate for the first
prototype, given the selected runtime and the user's plan or API billing model?
