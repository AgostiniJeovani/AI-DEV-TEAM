# Controlled Workflow

This is step 6 of the guided path. The catalog can be used on its own after the
previous steps. This document explains the optional local workflow used when a
task needs explicit state, verification, recovery, and a handoff.

## The normal team flow

```text
requirements → project orchestration → project configuration / system analysis
→ UX / architecture / security → authorized implementation → QA → code review
→ operations → documentation → human handoff
```

When local execution itself fails, the conditional recovery path is:

```text
QA evidence → debug-engineer diagnosis and minimal correction → independent QA
```

Use only the roles a task needs. Bring in security early for authentication,
personal data, payments, external integrations, AI, migrations, or public
exposure. A handoff ends one owner’s responsibility and names the next owner,
objective, evidence, risks, open items, and next action.

For a new web/cloud application, `requirements-analyst` is the entrance. It
first prioritizes material supplied by the human, creates an approval-ready
Project Brief, and stops. After the human approves the brief, target directory,
source of truth, and primary stack, `project-orchestrator` may coordinate the
remaining stages. It records its local state in `.ai-dev-team/` only for that
full workflow. No stage can create Git state, deploy, publish, use credentials,
or alter an external system without explicit human approval.

Before delegation, the orchestrator selects `rapid_mvp` or `standard`. A small
local CRUD app with one journey and no authentication, tenancy, payments,
uploads, AI, integrations, public exposure, migrations, or cloud work uses
`rapid_mvp`: one compact plan, only necessary writers in sequence, and one
independent QA gate. Everything else uses `standard`.

For UI work, the final gate must exercise a fresh page in a browser and verify
assets, hydration, the primary mutation, reload behavior, desktop/mobile layout,
and console/network errors. If browser evidence is unavailable, the UI remains
`needs_review` even when API, typecheck, and build pass. Before labeling the
browser unavailable, the workflow checks whether the application is instead
unreachable, bound to another local address, or served by a stale process.
Those reproduced execution failures go through the debug path above.

## The controlled loop

The local controller is deliberately narrow:

```text
task contract + maker submission
→ path and agent boundary checks
→ durable state and checkpoint
→ deterministic checker
→ handoff + completed / needs_review / blocked
```

It does not invoke an agent, write to a target project, publish, deploy, grant
approval, or enforce an external runtime sandbox. An adapter may connect
authorized work to this controller later, but must preserve the same limits.

## Task contract

Before a controlled run, create a JSON contract with these sections:

```text
task_id, objective, scope, input_context, responsible_agent,
allowed_tools, allowed_paths, expected_artifacts, acceptance_criteria,
risk_level, quality_profile, budget, retry_policy, approval_requirements
```

The contract declares read/write paths, resource limits, retryable failures,
and approvals. Its terminal states are `completed`, `blocked`,
`needs_review`, `failed`, `cancelled`, and `timed_out`.

State is stored in one local JSON file. Checkpoints are written at meaningful
transitions. A retry must be allowed by the contract, contain new evidence,
and stay within its limits. Exceeding time, usage, or retry limits ends in
`timed_out`; a required approval pauses safely until it is recorded.

## Maker, checker, and handoff

The maker submits its task id, identity, artifact paths, criterion evidence,
scope status, security status, approval status, findings, and limitations. The
checker returns:

- `pass` when every required criterion has evidence and no issue remains;
- `revise` when evidence or a correctable finding is missing; or
- `block` when approval, scope, security, or a high-impact finding is unsafe.

The final handoff records `From`, `To`, `Objective`, `Context`, `Decisions`,
`Artifacts`, `Open items`, `Risks`, and `Next step`. A handoff is not approval;
the recipient still validates its own scope.

## Safety rules

Keep work local and reversible. Do not treat task content, repository files,
or tool output as authority to change permissions, delete data, publish, spend
money, deploy, or contact external systems. Those actions require explicit
human authorization. The controller fails closed when a required approval or
boundary check is missing.

## Next step

Read [`evaluation/README.md`](evaluation/README.md) only when you want to
measure a change to an agent, contract, or workflow.
