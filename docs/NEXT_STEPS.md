# AI-DEV-TEAM — Next Steps

## Mission for this week

Turn the current AI-DEV-TEAM catalog into a controlled agent-loop foundation
by Sunday, August 30, 2026.

The goal is not unrestricted autonomy. The goal is a measurable, inspectable,
and recoverable workflow in which agents can plan, act, verify, hand off work,
recover from bounded failures, and stop safely.

## Current baseline

The repository already provides:

- 13 specialized Codex agents;
- explicit responsibilities and read-only/write boundaries;
- `AGENTS.md` global guidance;
- handoff conventions;
- a Windows junction connecting Codex to the versioned agent catalog;
- TOML validation;
- setup and removal automation;
- initial smoke-test documentation.

This baseline must remain green throughout the work. Changes to agent prompts,
permissions, or orchestration must not silently weaken the current boundaries.

## Principles for the next phase

1. Research before redesign.
2. Measure before claiming improvement.
3. Prefer explicit state and stop conditions over vague autonomy.
4. Keep human approval for external, destructive, financial, deployment, and
   security-sensitive actions.
5. Never allow the improvement agent to modify its own production definition
   without review and evaluation.
6. Every automated action must leave evidence that another person can inspect.
7. Preserve the simplest architecture that proves the behavior.

## Workstreams

### W1 — Research corpus

Before changing the loop, collect and compare strong sources on:

- prompt engineering;
- context engineering;
- agent loops and harness engineering;
- multi-agent orchestration;
- maker/checker and independent verification;
- agent evaluations and regression suites;
- state, checkpoints, retries, recovery, and stop conditions;
- human-in-the-loop approvals and permission boundaries;
- observability, cost, latency, and reliability;
- safety, prompt injection, tool misuse, and indirect prompt injection.

Store links, short summaries, evidence, applicability, and rejected ideas in a
versioned research area. Do not copy complete articles. Prefer primary sources,
official documentation, papers, and technically detailed engineering reports.

Planned artifacts:

```text
docs/research/
├── README.md
├── SOURCES.md
├── NOTES.md
└── DECISIONS.md
```

### W2 — Agent and task contracts

Define a common contract for every loop task:

- objective;
- input context;
- allowed tools and files;
- responsible agent;
- expected artifacts;
- acceptance criteria;
- risk level;
- budget and time limit;
- retry policy;
- approval requirements;
- terminal states.

The contract must distinguish `completed`, `blocked`, `needs_review`,
`failed`, `cancelled`, and `timed_out`.

### W3 — Evaluation harness

Create a small benchmark of representative tasks. Each task should have a
known expected outcome and a scoring rubric covering:

- correctness;
- scope adherence;
- evidence quality;
- security boundary compliance;
- test quality;
- handoff quality;
- cost and latency when measurable.

The harness should compare the current version with a proposed version before
any improvement is accepted.

### W4 — Verification and maker/checker flow

Separate production from verification:

```text
maker agent
    ↓
artifact and evidence
    ↓
checker agent
    ↓
pass / revise / block
```

The checker must be able to reject work with concrete findings. A checker is
not a rubber stamp and should not share the maker's assumptions blindly.

### W5 — State, retries, and recovery

Design explicit state storage and checkpoints for a task. Define:

- what is persisted;
- when a checkpoint is written;
- how a task resumes;
- which failures are retryable;
- maximum attempts;
- backoff behavior;
- when to escalate to a human;
- how partial changes are isolated or rolled back.

Do not add a database or distributed infrastructure until a file-backed or
repository-local proof is insufficient.

### W6 — Loop orchestration

Turn the current manual workflow into a small, inspectable state machine or
workflow specification. The first loop should be narrow, for example:

```text
discover → analyze → plan → implement → test → review → handoff → complete
```

Each transition must have an owner, input, output, validation, and failure
path. The first version should not attempt to automate every agent or every
project type.

### W7 — Agent Engineer

Design a new `agent-engineer` agent as the maintainer of the AI-DEV-TEAM system.
It should improve agents, skills, contracts, loops, evaluations, and docs — not
directly modify application code by default.

The agent-engineer must operate through a proposal loop:

```text
inspect → propose → evaluate in isolation → report → human approval → apply
```

It must not self-edit its own active definition, bypass read-only boundaries,
or publish changes without approval.

## Delivery plan

### Monday, August 17 — Baseline and research

- Run the current agent validator and junction check.
- Freeze the current baseline output.
- Create the research structure.
- Collect and classify the first high-quality sources.
- Record terminology and competing approaches.

Exit criteria: the baseline passes and the research questions are explicit.

### Tuesday, August 18 — Contracts and state model

- Define the task contract.
- Define terminal states and approval levels.
- Define the minimum checkpoint format.
- Decide what belongs in prompts, context, tools, and loop state.

Exit criteria: a sample task can be represented without hidden state.

### Wednesday, August 19 — Evaluation harness

- Create the first benchmark tasks.
- Define scoring rubrics and pass thresholds.
- Add a repeatable evaluation command.
- Capture baseline results from the current workflow.

Exit criteria: a proposed change can be compared with the baseline.

### Thursday, August 20 — Maker/checker verification

- Define checker responsibilities.
- Add review gates for correctness, scope, security, and evidence.
- Test pass, revise, and block outcomes.

Exit criteria: weak work is rejected with actionable findings.

### Friday, August 21 — Recovery and bounded retries

- Implement or document checkpoints.
- Add retry limits and stop conditions.
- Define escalation behavior.
- Test interruption and resume scenarios.

Exit criteria: the loop cannot run forever and a partial failure is explainable.

### Saturday, August 22 — First orchestrated loop and agent-engineer design

- Implement the smallest useful loop prototype.
- Connect task state, maker/checker validation, and handoffs.
- Draft `agent-engineer.toml` from the contracts and evaluation findings.
- Keep the new agent read-only until its proposal workflow is tested.

Exit criteria: one narrow workflow runs end to end with evidence and safe stops.

### Sunday, August 23 — Integration, documentation, and review

- Run the full baseline and regression suite.
- Review permissions and external side effects.
- Update README and docs from the actual workflow.
- Document known limitations and next backlog.
- Prepare a public-facing summary of the experiment.

Exit criteria: the first loop is reproducible, bounded, documented, and ready
for human review — not yet autonomous in unrestricted production.

## Definition of done for this milestone

The milestone is complete when:

1. research sources and decisions are versioned;
2. task contracts and terminal states are documented;
3. benchmark tasks and evaluation criteria exist;
4. maker/checker verification is demonstrated;
5. retries, checkpoints, and stop conditions are bounded;
6. one narrow workflow runs end to end;
7. `agent-engineer` has a reviewed first specification;
8. human approval remains required for sensitive actions;
9. the original 13-agent baseline still validates;
10. README and setup instructions match the actual implementation.

## Explicit non-goals for this week

- unrestricted self-modification;
- autonomous production deployment;
- automatic financial or external communication actions;
- a generalized distributed orchestration platform;
- adding infrastructure before the smallest loop is proven;
- claiming reliability from a single successful run;
- replacing human judgment for architecture, security, or release decisions.

## Resume checklist

When returning to this project:

1. Read this file.
2. Run `python .\scripts\validate-agents.py`.
3. Run `powershell -ExecutionPolicy Bypass -File .\scripts\setup-windows.ps1 -CheckOnly`.
4. Review the latest files under `docs/research/`.
5. Work on the next unfinished workstream only.
6. Update this file when scope, dates, decisions, or exit criteria change.

