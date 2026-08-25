# Controlled Workflow

This is step 5 of the guided path. The catalog can be used on its own after the
previous steps. This document explains the optional local workflow used when a
task needs explicit state, verification, recovery, and a handoff.

## The normal team flow

```text
project configuration → requirements → system analysis → architecture
→ authorized implementation → QA → code review → operations → documentation
```

Use only the roles a task needs. Bring in security early for authentication,
personal data, payments, external integrations, AI, migrations, or public
exposure. A handoff ends one owner’s responsibility and names the next owner,
objective, evidence, risks, open items, and next action.

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

