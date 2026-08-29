# Scripts

This is step 3 of the guided path. Run commands from the repository root.
Every script is local, deterministic, and avoids credentials, publishing, and
unapproved side effects.

## First validation

```powershell
python .\scripts\validate-agents.py
```

Success ends with `validation=passed`. The current catalog must report 16
agents and 9 read-only agents, plus four valid local skills. Run this after any
change to an agent TOML, skill, or catalog structure.

## Activation commands

`setup-windows.ps1` creates or verifies the Codex agent junction and each
AI-DEV-TEAM skill junction. Add `-CheckOnly` to inspect them without changing
anything. `remove-junction-windows.ps1` removes only the verified
AI-DEV-TEAM junctions, never source files or unrelated personal skills.

## Controlled-loop commands

These commands do not call a model or perform work in a target project. They
record and check data supplied by an authorized operator or runtime.

| Script | Purpose | Main inputs | Output |
|---|---|---|---|
| `task-state.py` | Creates and updates durable task state | contract and state JSON | state JSON and checkpoints |
| `check-workflow.py` | Applies the deterministic maker/checker gate | maker submission; optional review | `pass`, `revise`, or `block` JSON |
| `run-workflow.py` | Connects state, boundary checks, checker, and handoff | contract, submission, state, report, handoff paths | report, handoff, terminal state |
| `evaluate-workflow.py` | Validates or compares benchmark results | benchmark; optional baseline and candidate results | validation or score comparison |

`task-state.py` has the subcommands `init`, `show`, `transition`, `retry`,
`resume`, `usage`, and `cancel`. Use `python .\scripts\task-state.py <command>
--help` to see the required fields for one operation.

Run the narrow loop with disposable JSON inputs and local outputs:

```powershell
python .\scripts\run-workflow.py `
  --contract <contract.json> `
  --submission <submission.json> `
  --state .\.evaluation\results\state.json `
  --report .\.evaluation\results\report.json `
  --handoff .\.evaluation\results\handoff.md
```

The `.evaluation/results/` location is ignored by Git; it is safe for your own
tests and never belongs in the catalog.

## Behavioral test in Codex

Ask the `project-configurator` agent to map this repository without changing
files. Its answer should cite observed files, name risks and validation
commands, and hand off to `requirements-analyst`.

Then ask `system-architect` to analyze a small hypothetical feature without
editing files. It should return architecture, trade-offs, risks, an incremental
plan, and handoffs—not implementation.

For the end-to-end web/cloud flow, invoke `web-cloud-project-intake` in a new
target project. It begins with `requirements-analyst`, stops for your approval
of the Project Brief and stack, then `web-cloud-project-delivery` coordinates
the local build and validation. A small local CRUD app should select
`rapid_mvp`, avoid duplicate reviewer threads, and remain `needs_review` until
its primary UI flow is exercised in a browser at desktop and mobile widths.
To test recovery, occupy the documented port with a known disposable process
or serve different test pages on IPv4 and IPv6. The flow should diagnose the
ownership and split binding through `debug-engineer`, never stop an unrelated
process, and return the corrected run to independent QA.
Details are in the next two guides.

## Next step

Read [`agents/README.md`](../agents/README.md) completely to understand the
agents you just activated.
