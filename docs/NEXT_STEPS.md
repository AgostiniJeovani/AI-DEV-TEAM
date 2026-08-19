# AI-DEV-TEAM — Next Steps

## Mission for this milestone

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
├── DECISIONS.md
└── PORTABILITY_AND_COST.md
```

### W2 — Agent and task contracts — completed for the first iteration

Status: first iteration completed. The contract and state model are now the
closed baseline for this milestone. Numeric defaults will be calibrated by the
evaluation harness instead of guessed in isolation.

The contract is documented in [`docs/task-contract.md`](task-contract.md),
with an example in
[`docs/examples/task-contract.json`](examples/task-contract.json). Numeric
budget defaults and the first state-storage implementation remain open for the
next iteration.

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

The following patterns were added to the baseline after reviewing the
JavaScript Mastery workflow skills:

- durable state must live in repository files, not only in chat history;
- every acceptance criterion receives an identifier and an evidence trail;
- each durable artifact has one owner and other agents must not silently
  rewrite another agent's source of truth;
- `prototype`, `alpha`, `beta`, and `ga` quality profiles control default
  verification depth and token cost;
- runtime verification and independent code review are separate actions;
- an architectural assumption must be recorded instead of being hidden;
- a future synchronization step must flag stale documentation and decisions;
- a task can resume from its contract and latest checkpoint without replaying
  the whole conversation.

These are design decisions for our loop, not a requirement to copy the
external repository's commands, agents, or provider-specific behavior.

### W3 — Evaluation harness — completed for the first baseline

This is the next active stage. Create a small benchmark of representative
tasks. Each task should have a
known expected outcome and a scoring rubric covering:

- correctness;
- scope adherence;
- evidence quality;
- security boundary compliance;
- test quality;
- handoff quality;
- cost and latency when measurable.

The harness should compare the current version with a proposed version before
any improvement is accepted. It must exercise more than successful runs:

- a task that completes with valid evidence;
- a task that needs revision after checker findings;
- a task that becomes blocked by missing input or approval;
- a task that reaches a retry or budget limit;
- a task that tests read-only and allowed-path boundaries.

The first harness should remain file-backed and provider-neutral. It should
measure enough to compare versions without introducing a database or a
distributed orchestration service.

First baseline completed: [`docs/evaluation/manual-baseline-001.json`](evaluation/manual-baseline-001.json).
The result is `83.67/100` with `4/5` expected states matching. The timeout
scenario remains `in_progress` because no loop controller currently enforces
runtime limits or writes checkpoints. This is a measured capability gap and
the first input for W5, not a hidden failure.

Initial implementation: [`docs/evaluation/README.md`](evaluation/README.md),
[`docs/evaluation/benchmark.json`](evaluation/benchmark.json), and
[`scripts/evaluate-workflow.py`](../scripts/evaluate-workflow.py). The
benchmark definition validates successfully and contains five scenarios. The
the five scenarios were run against the current manual workflow and the
measured baseline is recorded above.

### W4 — Verification and maker/checker flow — completed for the first iteration

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

Initial implementation: [`docs/maker-checker.md`](maker-checker.md) and
[`scripts/check-workflow.py`](../scripts/check-workflow.py). The deterministic
gate has fixtures for `pass`, `revise`, and `block`. Independent model review
and retry orchestration remain open for this workstream. Independent review is
now supported through a provider-neutral review report; retry orchestration is
deferred to W5.

### W5 — State, retries, and recovery — next active stage

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

### Monday, August 17 — Baseline and research intake

- Run the current agent validator and junction check.
- Freeze the current baseline output.
- Create the research structure.
- Collect and classify the first high-quality sources.
- Record terminology and competing approaches.

Exit criteria: the baseline passes and the research questions are explicit.

### Tuesday, August 18 — Research corpus and synthesis

- Expand the source set across prompt, context, harness, loops, evaluation,
  state, orchestration, and safety.
- Write short evidence-based notes and mark claims that need validation.
- Record accepted, rejected, and still-open approaches.

Exit criteria: the research corpus is useful enough to guide the next design
decisions without copying articles into the repository.

### Wednesday, August 19 — Contracts and state model — completed early

- Define the task contract.
- Define terminal states and approval levels.
- Define the minimum checkpoint format.
- Decide what belongs in prompts, context, tools, and loop state.

Exit criteria: a sample task can be represented without hidden state. The
first version is complete; remaining numeric defaults will be calibrated by
W3.

### Thursday, August 20 — Evaluation harness — completed early

- Create the first benchmark tasks.
- Define scoring rubrics and pass thresholds.
- Add a repeatable evaluation command.
- Capture baseline results from the current workflow.
- Include the four quality profiles and failure paths in the benchmark.
- Record criterion-to-evidence traceability in each result.

Exit criteria: a proposed change can be compared with the baseline.

### Friday, August 21 — Maker/checker verification — completed early

- Define checker responsibilities.
- Add review gates for correctness, scope, security, and evidence.
- Test pass, revise, and block outcomes.
- Use the checker-revision result from the manual baseline as the first case.

Exit criteria: weak work is rejected with actionable findings.

### Monday, August 24 — Recovery and bounded retries — current next step

- Implement or document checkpoints.
- Add retry limits and stop conditions.
- Define escalation behavior.
- Test interruption and resume scenarios.

Exit criteria: the loop cannot run forever and a partial failure is explainable.

### Tuesday, August 25 — First orchestrated loop and agent-engineer design

- Implement the smallest useful loop prototype.
- Connect task state, maker/checker validation, and handoffs.
- Draft `agent-engineer.toml` from the contracts and evaluation findings.
- Keep the new agent read-only until its proposal workflow is tested.

Exit criteria: one narrow workflow runs end to end with evidence and safe stops.

### Wednesday, August 26 — First narrow loop prototype

- Implement the smallest useful loop around a repository-maintenance task.
- Connect task state, maker/checker validation, and handoffs.
- Capture evidence for every transition and terminal state.

Exit criteria: one narrow workflow runs end to end in a controlled environment.

### Thursday, August 27 — Safety and regression review

- Test blocked, failed, cancelled, timed-out, and needs-review paths.
- Review permissions, approval gates, retry limits, and external side effects.
- Compare the prototype with the baseline benchmark.

Exit criteria: the loop is bounded, reviewable, and does not weaken the
original agent catalog.

### Friday, August 28 — Documentation freeze and public-facing cleanup

- Run the full baseline and regression suite.
- Review permissions and external side effects.
- Update README and docs from the actual workflow.
- Document known limitations and next backlog.
- Prepare a public-facing summary of the experiment.

Exit criteria: the first loop is reproducible, bounded, documented, and ready
for human review — not yet autonomous in unrestricted production.

### Saturday and Sunday, August 29–30 — Light review and milestone close

- Review the final diff and research decisions.
- Re-run the validator and smoke checks.
- Record known limitations and the next backlog.
- Close the milestone only if the definition of done is satisfied.

The final weekend is intentionally reserved for light review and handoff, not
for introducing large architectural changes.

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
