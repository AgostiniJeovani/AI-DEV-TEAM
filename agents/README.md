# Agents

This is step 4 of the guided path. Each TOML file is an executable Codex agent
definition. Its `developer_instructions` are the source of truth; this guide
helps you choose the correct specialist and understand the handoff sequence.

Read-only agents inspect, plan, or review. They do not modify application
files by default. Writing agents may change files only when the user has
authorized a clear scope.

| Agent | Mode | Specialist responsibility |
|---|---|---|
| `requirements-analyst` | read-only | Leads the conversation from idea to an approval-ready Project Brief; it coordinates focused discovery and asks only material questions. |
| `project-orchestrator` | workspace-write | After human approval, selects `rapid_mvp` or `standard`, coordinates only necessary handoffs, retries, and local proof of completion. |
| `project-configurator` | read-only | Maps an existing codebase, local rules, runtime, dependencies, and verified commands before anyone changes it. |
| `system-analyst` | read-only | Makes actors, rules, states, data flows, error behavior, and contracts precise and testable. |
| `system-architect` | read-only | Produces evidence-based architecture, trade-offs, security-by-design, and phased implementation plans. |
| `uiux-designer` | read-only | Specifies accessible, responsive journeys, components, and interaction states for the frontend. |
| `frontend-engineer` | workspace-write | Implements approved browser-facing behavior with accessibility, contract discipline, and local validation. |
| `backend-engineer` | workspace-write | Implements approved APIs, domain rules, persistence, integrations, and observable recovery behavior. |
| `data-ai-engineer` | workspace-write | Uses data/AI only when justified and adds provenance, evaluation, safety, cost, and fallback controls. |
| `debug-engineer` | workspace-write | Enters only on a reproducible local execution failure, isolates its root cause, applies the smallest reversible correction, and returns the result to QA. |
| `qa-engineer` | read-only | Independently validates acceptance criteria and risk paths, requiring browser evidence for UI claims; it never masks a failure. |
| `code-reviewer` | read-only | Independently reviews the diff for defects, contract drift, safety, and maintainability, then returns pass/revise/block. |
| `security-engineer` | read-only | Threat-models the application and proposed dependencies, privacy, supply-chain, abuse, and cloud risks. |
| `devops-engineer` | workspace-write | Builds approved local operational foundations, observability, recovery, and delivery configuration without publishing externally. |
| `technical-writer` | workspace-write | Keeps concise, verified setup, test, operation, limitation, and handoff documentation. |
| `agent-engineer` | read-only | Proposes measured improvements to this catalog, its skills, loop, and evaluation without applying its own proposal. |

`system-architect` is intentionally detailed: it may inspect code, tests,
configuration, dependencies, and Git metadata, but it cannot implement,
install, deploy, mutate infrastructure, or change Git state. It produces a
handoff to the appropriate specialist.

`agent-engineer` follows this fixed proposal cycle:

```text
inspect → propose → evaluate in isolation → report → human approval → apply
```

It never applies its own proposal, edits its active TOML, raises budgets, or
weakens a safety boundary.

## Maintaining the catalog

1. Edit only the TOML source in this folder.
2. Keep `name`, `description`, and `developer_instructions` valid.
3. Use `sandbox_mode = "read-only"` for every analysis, architecture, QA,
   review, security, and agent-engineer role.
4. Run `python .\scripts\validate-agents.py`.
5. Review the diff before versioning it.

For a new web/cloud application, begin with `requirements-analyst`. It may
consult other read-only roles, returns one brief for your approval, and only
then hands it to `project-orchestrator`. The coordinator never creates commits,
branches, deployments, cloud resources, or external publications; those remain
human-only actions.

For a small local CRUD application without authentication, payments, uploads,
AI, integrations, or cloud work, the coordinator should choose `rapid_mvp`.
That lane keeps one delegated agent active at a time, avoids duplicate review
threads, and finishes with one independent browser-aware QA gate. It invokes
`debug-engineer` only when a startup, process/port, runtime, asset, or browser
reachability failure has reproducible evidence; healthy runs do not pay that
extra handoff cost.

Global behavior, authorization, safety, dependency, and handoff rules remain
in [`AGENTS.md`](../AGENTS.md).

## Next step

Read [`skills/README.md`](../skills/README.md) completely to learn the reusable
workflows that make the catalog practical in a new Codex task.
