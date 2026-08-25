# Agents

This is step 4 of the guided path. Each TOML file is an executable Codex agent
definition. Its `developer_instructions` are the source of truth; this guide
helps you choose the correct one.

Read-only agents inspect, plan, or review. They do not modify application
files by default. Writing agents may change files only when the user has
authorized a clear scope.

| Agent | Mode | Use it for |
|---|---|---|
| `project-configurator` | read-only | Map a repository, its stack, commands, and rules. |
| `requirements-analyst` | read-only | Clarify requirements, acceptance criteria, and exclusions. |
| `system-analyst` | read-only | Model domain concepts, flows, states, and contracts. |
| `system-architect` | read-only | Analyze architecture, trade-offs, risks, and implementation plans. |
| `uiux-designer` | read-only | Design user journeys, interfaces, and accessibility. |
| `frontend-engineer` | workspace-write | Implement authorized user-interface work. |
| `backend-engineer` | workspace-write | Implement authorized APIs, domain logic, persistence, and integrations. |
| `data-ai-engineer` | workspace-write | Implement authorized data, RAG, LLM, and evaluation work. |
| `qa-engineer` | read-only | Define and execute quality checks. |
| `code-reviewer` | read-only | Report defects, risks, and maintenance concerns without fixing them. |
| `security-engineer` | read-only | Assess threats, privacy, controls, and abuse risks. |
| `devops-engineer` | workspace-write | Prepare authorized delivery, operations, observability, and rollback work. |
| `technical-writer` | workspace-write | Update authorized documentation and handoffs. |
| `agent-engineer` | read-only | Propose evidence-backed improvements to this catalog and its loop. |

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

Global behavior, authorization, safety, and handoff rules remain in
[`AGENTS.md`](../AGENTS.md).

## Next step

Read [`docs/README.md`](../docs/README.md) completely to learn the controlled
workflow available after the catalog is active.
