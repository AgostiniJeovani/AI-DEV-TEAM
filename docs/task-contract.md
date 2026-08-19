# Task Contract

This document defines the minimum contract for a controlled AI-DEV-TEAM loop.
It is provider-neutral: Codex, Claude, Hermes, or another runtime may execute
it through an adapter.

The contract prevents hidden state. A task must say what it is trying to do,
what context and tools are allowed, what evidence is required, how much it may
consume, and how it ends.

## Required fields

| Field | Meaning |
|---|---|
| `task_id` | Stable identifier for the task and its checkpoints. |
| `objective` | Concrete outcome the task is expected to achieve. |
| `scope` | What is included and explicitly excluded. |
| `input_context` | Files, references, requirements, and assumptions available to the task. |
| `responsible_agent` | Agent accountable for the current stage. |
| `allowed_tools` | Tools the stage may use. An omitted tool is not implicitly allowed. |
| `allowed_paths` | Files or directories the stage may read or write. |
| `expected_artifacts` | Files, reports, decisions, tests, or handoffs the task should produce. |
| `acceptance_criteria` | Observable conditions for success. |
| `risk_level` | `low`, `medium`, `high`, or `critical`. |
| `quality_profile` | Suggested verification depth: `prototype`, `alpha`, `beta`, or `ga`. |
| `budget` | Calls, tokens, retries, subagents, time, and estimated cost limits. |
| `retry_policy` | Which failures may be retried and how many times. |
| `approval_requirements` | Actions that require human approval before execution. |
| `state` | Current lifecycle state. |
| `evidence` | Links to checks, outputs, traces, and decisions. |

The `quality_profile` controls the default verification depth. It is a cost
and risk control, not an unconditional gate:

| Profile | Default stages after implementation | Typical use |
|---|---|---|
| `prototype` | Maker self-check | Experiments and throwaway work. |
| `alpha` | Runtime verification | Low-risk internal or early product work. |
| `beta` | Runtime verification and tests | Normal feature work. |
| `ga` | Runtime verification, tests, independent review, and documentation | High-risk, public, security-sensitive, or release work. |

A high-risk task may require a stronger profile than the project default. A
low profile must never bypass an architectural, security, approval, or policy
decision that the task genuinely requires.

## Lifecycle states

```text
created
   ↓
in_progress ───────→ needs_review ───────→ completed
   │                      │
   │                      └──────────────→ blocked
   ├────────────────────────────────────→ failed
   ├────────────────────────────────────→ cancelled
   └────────────────────────────────────→ timed_out
```

### Non-terminal state

- `created`: contract exists but execution has not started;
- `in_progress`: an authorized stage is actively working;
- `needs_review`: execution paused for human or checker review.

### Terminal states

- `completed`: acceptance criteria passed and required evidence exists;
- `blocked`: progress requires an external decision, permission, or missing input;
- `failed`: execution ended after a non-retryable or exhausted failure;
- `cancelled`: a user or policy intentionally stopped the task;
- `timed_out`: the time or budget limit was reached before completion.

Do not use `completed` because an agent says it is done. Completion requires
acceptance evidence. A budget exhaustion should normally become `timed_out`
with a reason such as `token_budget_exceeded` or `retry_budget_exceeded`.

## Evidence and traceability

Each acceptance criterion should have a stable identifier, such as `AC-01`.
Artifacts, verification steps, tests, review findings, and handoffs should
reference those identifiers. A task may only reach `completed` when every
required criterion is either proven by evidence or explicitly waived by an
authorized human with a recorded reason.

The minimum trace is:

```text
acceptance criterion -> artifact or code -> verification -> test or review -> evidence
```

This prevents an agent from reporting success based only on a plausible answer
or a file that was created without being validated.

## Artifact ownership

Every durable artifact has one owner. Other agents may read it, propose a
change, or report that it is stale, but they must not silently rewrite another
agent's source of truth.

Recommended ownership for the first loop:

| Artifact | Owner |
|---|---|
| Task contract and checkpoints | Loop controller or future `agent-engineer` |
| Requirements and acceptance criteria | `requirements-analyst` |
| Architecture decisions and specifications | `system-architect` |
| Implementation | The relevant engineering agent |
| Verification plan and test evidence | `qa-engineer` |
| Independent review findings | `code-reviewer` or `security-engineer` |
| Documentation and release notes | `technical-writer` |
| Synchronization and stale-state report | Future `agent-engineer` |

Agents marked read-only remain analysis or review roles. They may produce
analysis artifacts when authorized by the runtime, but they must not implement
application code or modify protected production files. The specific mode for
each agent is defined in its TOML file and validated by the catalog validator.

## Budget contract

Every task must have visible limits. Numeric defaults are still an open
decision, but the shape is fixed:

```json
{
  "max_model_calls": 12,
  "max_input_tokens": 50000,
  "max_output_tokens": 12000,
  "max_subagents": 1,
  "max_retries_per_transition": 2,
  "max_wall_time_seconds": 900,
  "max_estimated_cost": null
}
```

`null` means that the runtime does not expose a comparable currency estimate;
it does not mean unlimited execution. The other limits still apply.

## Retry policy

A retry is allowed only when:

1. the failure is classified as transient or correctable;
2. the next attempt has new evidence, a changed input, or a revised plan;
3. the retry remains within the budget;
4. repeating the action is safe and idempotent.

Do not retry authentication failures, policy violations, destructive actions,
unknown side effects, or the same unchanged error indefinitely. Escalate to a
checker or human when the retry limit is reached.

## Approval requirements

The contract must list actions that pause before execution. At minimum, this
includes:

- modifying agent definitions or permissions;
- deleting or overwriting user data;
- external publication, deployment, or communication;
- production or billing changes;
- access to sensitive data or external systems;
- raising the task budget.

An approval records who decided, what was approved or rejected, when, and the
task state that will resume. Approval resumes the same task; it does not create
a new hidden task.

## Checkpoint contract

Write a checkpoint after every meaningful transition and before a pause for
approval. A checkpoint should contain:

```json
{
  "task_id": "task-2026-08-17-001",
  "checkpoint_id": "cp-0003",
  "created_at": "2026-08-17T20:00:00Z",
  "state": "needs_review",
  "current_stage": "checker",
  "responsible_agent": "code-reviewer",
  "attempts": {"checker": 1},
  "artifacts": ["proposal.md", "validation.txt"],
  "evidence": ["validation=passed"],
  "pending_approval": "apply_agent_definition",
  "next_action": "wait_for_human_decision"
}
```

Checkpoints must be sufficient to resume without relying on private model
memory. Store references to large files rather than duplicating their complete
contents in every checkpoint.

The repository is the durable memory of the loop. A new session must be able
to resume from the contract, the latest checkpoint, and the referenced
artifacts without replaying the entire chat history.

## Example

See [`examples/task-contract.json`](examples/task-contract.json) for a complete
repository-maintenance task using this contract.
