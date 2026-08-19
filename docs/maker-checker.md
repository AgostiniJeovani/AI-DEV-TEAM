# Maker and Checker

This document defines the first verification gate for the AI-DEV-TEAM loop.

## Plain-language idea

The maker does the work. The checker inspects the work. The checker does not
silently repair the work or change the maker's files.

```text
maker
  |
  | artifact + acceptance evidence
  v
checker
  |
  +--> pass       the work is acceptable for this gate
  +--> revise     a correctable problem must be fixed and checked again
  +--> block      the work cannot safely continue without approval, input, or
                  a boundary decision
```

## What the maker must deliver

The maker submission must identify:

- the task and responsible maker;
- produced artifacts and their paths;
- each acceptance criterion;
- evidence for each criterion;
- scope and security boundary observations;
- required approvals and whether they were granted;
- known findings or limitations.

An agent saying “done” is not evidence. Evidence must point to an artifact,
validation result, test, review, approval, or other observable fact.

## Checker decision rules

The first checker applies these rules in order:

1. `block` if a required approval is missing.
2. `block` if the submission reports a boundary violation, unsafe side effect,
   or unknown destructive action.
3. `revise` if a required acceptance criterion is missing evidence or is not
   verified.
4. `revise` if there is a correctable finding.
5. `pass` only when all required criteria have evidence and no blocking or
   revision finding remains.

`pass` does not mean the whole project is finished. It means this checker gate
passed for the declared task and quality profile. A later QA, security, or
release gate may still be required.

## Finding severity

- `critical` or `high`: normally `block`, especially for security, privacy,
  destructive actions, credentials, production, or external publication;
- `medium` or `low` with `correctable=true`: `revise`;
- informational findings may be recorded without changing the outcome.

The checker must report the problem, why it matters, where it was observed,
and the next action. It should not edit code, rewrite the maker's explanation,
or lower the severity just to obtain `pass`.

## Independence

The strongest version uses a different model or agent for checking. The first
local checker is deterministic and provider-neutral, so it can run even when a
second model is unavailable. The result must state whether the checker was a
script, a separate agent, a separate model, or the same operator.

## Independent review report

When a second agent or model is available, pass its report to the checker:

```powershell
python .\scripts\check-workflow.py `
  --submission .\docs\evaluation\checker-fixtures\pass.json `
  --review-report .\docs\evaluation\checker-fixtures\review-pass.json
```

The report must identify the reviewer, say whether it was independent, return
`pass`, `revise`, or `block`, and list its findings. The combined decision uses
the strongest outcome: `block` beats `revise`, and `revise` beats `pass`.
The deterministic gate still has final authority over hard boundaries and
missing approvals. It also upgrades an inconsistent review report: a `high` or
`critical` finding cannot coexist with an effective `pass`, even if the report
claims `pass`.

## Current limitation

This gate validates submissions and returns a decision. It does not yet
orchestrate agents, enforce filesystem permissions at runtime, create
checkpoints, or retry a revision. Those responsibilities belong to the later
loop and recovery stages.
