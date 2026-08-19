# AI-DEV-TEAM

A team of specialized agents supporting software projects across discovery,
requirements, architecture, design, implementation, data/AI, quality,
security, operations, and documentation.

> [!WARNING]
> **Experimental study repository.** AI-DEV-TEAM is unfinished and is being
> developed as a public study of prompt engineering, context engineering, and
> loop engineering. It is not a production-ready agent framework. Review the
> scripts, permissions, agent definitions, and Windows junction behavior before
> using it. Run it only on systems and projects you control, do not provide
> secrets, and clone or extend it at your own responsibility. The long-term
> goal is a provider-neutral framework with bounded autonomy, evidence,
> evaluation, maker/checker verification, recovery, and runtime adapters.

This README is the entry point. It does not teach every detail at once: it
shows the right path and sends you to the relevant document when a topic gets
specific.

## Start here

### If you are new to the project

Read only these sections first:

1. [What this is](#what-this-is);
2. [Repository structure](#repository-structure);
3. [How the agents work](#how-the-agents-work);
4. [First use](#first-use).

Then choose the path in **Recommended reading order** below. Open
`docs/NEXT_STEPS.md` only if you are studying or contributing to the loop
engineering work. You do not need to read the README from top to bottom.

### If you want to configure the team

Go directly to [`setup/README.md`](setup/README.md). It explains the Windows
junction in plain language, runs the automation, and shows how to undo it.

### If you want to understand the agents

Read [`agents/README.md`](agents/README.md), then read the `.toml` files in
workflow order. The TOML files are the source of truth for agent instructions.

### If you want to test

Start with [`docs/testing.md`](docs/testing.md) for automated validation and
behavioral smoke tests.

### If you want to follow system evolution

Read [`docs/NEXT_STEPS.md`](docs/NEXT_STEPS.md). It contains the milestone
backlog, research path, and criteria for evolving from the current catalog to a
controlled agent loop. The research artifacts are in
[`docs/research/README.md`](docs/research/README.md).

### Recommended reading order

You do not need to read every Markdown file before trying the catalog. Use this
short path:

1. This README, through **First use**.
2. [`setup/README.md`](setup/README.md), if you want to activate the agents.
3. [`agents/README.md`](agents/README.md), then the agent TOML files you need.
4. [`docs/testing.md`](docs/testing.md), to validate the setup.
5. [`docs/task-contract.md`](docs/task-contract.md), when studying controlled
   task execution.

The files under `docs/evaluation/`, `docs/research/`, and
[`docs/NEXT_STEPS.md`](docs/NEXT_STEPS.md) describe the laboratory work used to
evolve the project. They are important for contributors, but they are not
required reading for a first agent activation.

## What this is

AI-DEV-TEAM is a versioned catalog of specialist agents for Codex. Each agent
has a primary responsibility, explicit boundaries, an autonomy mode, and
handoff instructions.

The goal is to divide work without unnecessary overlap:

- discovery and analysis agents understand the problem;
- architecture agents define decisions and plans;
- engineering agents implement when authorized;
- QA, review, and security agents verify the result;
- DevOps and documentation prepare operations and continuity.

Principles that must not be lost:

- read context before acting;
- keep responsibilities clear;
- use explicit handoffs;
- avoid over-engineering;
- apply security by design;
- prefer evidence over preference;
- give autonomy proportional to the role;
- keep changes reversible and authorized;
- do not fix a model or provider without need.

## Repository structure

```text
AI-DEV-TEAM/
├── README.md                         ← entry point
├── AGENTS.md                         ← global team rules
├── .gitignore
├── agents/                           ← versioned Codex agents
├── docs/                             ← workflow, contracts, tests, research
├── setup/                            ← beginner-friendly configuration guide
├── scripts/                          ← Windows validation and automation
├── skills/                           ← planned reusable skills
├── tools/                            ← shared contracts and utilities
└── adapters/                         ← future runtime integrations
```

The functional parts of this version are `agents/`, `docs/`, `setup/`, and
`scripts/`. `skills/`, `tools/`, and `adapters/` are prepared and documented,
but do not yet contain concrete implementations.

## How the agents work

Recommended flow for a new project:

```text
project-configurator
        ↓
requirements-analyst
        ↓
system-analyst
        ↓
system-architect ───────→ security-engineer when needed
        ↓
uiux-designer / frontend-engineer / backend-engineer / data-ai-engineer
        ↓
qa-engineer → code-reviewer → devops-engineer → technical-writer
```

The flow is adaptable. Small tasks may skip stages; changes involving
authentication, personal data, payments, AI, migrations, critical
infrastructure, or public exposure should involve the appropriate reviews.

### Quick catalog

| Agent | Main role | Mode |
|---|---|---|
| `project-configurator` | Maps project, stack, commands, and local rules | read-only |
| `requirements-analyst` | Defines requirements and acceptance criteria | read-only |
| `system-analyst` | Models domain, flows, states, and contracts | read-only |
| `system-architect` | Defines architecture, decisions, and incremental plan | read-only |
| `uiux-designer` | Defines journeys, interface, and accessibility | read-only |
| `frontend-engineer` | Implements React/Next/TypeScript/Tailwind interfaces | authorized writing |
| `backend-engineer` | Implements APIs, domain, persistence, and integrations | authorized writing |
| `data-ai-engineer` | Implements data, RAG, LLMs, and AI evaluation | authorized writing |
| `qa-engineer` | Defines and executes quality strategy | read-only |
| `code-reviewer` | Reviews bugs, risks, and maintenance | read-only |
| `security-engineer` | Assesses threats, controls, privacy, and abuse | read-only |
| `devops-engineer` | Handles delivery, operations, observability, and rollback | authorized writing |
| `technical-writer` | Maintains setup, decisions, and useful documentation | authorized writing |

The details and boundaries are in the `.toml` files under `agents/`.
`system-architect` does not implement: it delivers decisions, specifications,
and handoffs.

## First use

### 1. Configure

From the repository root, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-windows.ps1
```

The script connects `%USERPROFILE%\.codex\agents` to the repository's
`agents/` folder through a Windows junction. The files remain versioned here.
See [`setup/README.md`](setup/README.md) for the explanation, expected output,
removal, and troubleshooting.

### 2. Validate

```powershell
python .\scripts\validate-agents.py
```

Expected output includes:

```text
agent_count=13
missing_required=0
unsupported_fields=0
read_only_count=8
read_only_agents=code-reviewer,project-configurator,qa-engineer,requirements-analyst,security-engineer,system-analyst,system-architect,uiux-designer
documentation_complete=True
validation=passed
```

If validation fails, fix it before testing agent behavior. The script does not
publish changes, install dependencies, or access secrets.

### 3. Run the first smoke test

Open the AI-DEV-TEAM folder in Codex and ask:

```text
Use the project-configurator agent to map this repository.
Do not change any files. Return structure, stack, validation commands, risks,
and a handoff to requirements-analyst.
```

Expected result: an evidence-based analysis with no file changes and a clear
handoff.

Then test the architect:

```text
Use system-architect to analyze a small hypothetical feature.
Produce assumptions, alternatives, architecture, risks, security,
an incremental plan, and a handoff. Do not create or change files.
```

Expected result: planning, not implementation. For the complete route,
including implementers, QA, review, and security boundaries, follow
[`docs/testing.md`](docs/testing.md).

## Handoffs

A handoff is the formal passage of a result to the next owner. It is not an
additional responsibility for the agent.

Minimum format:

```text
HANDOFF
From: <agent>
To: <agent or user>
Objective: <expected result>
Context: <what was analyzed>
Decisions: <decisions and reasons>
Artifacts: <files, links, or evidence>
Open items: <unresolved questions>
Risks: <risks and mitigations>
Next step: <concrete action and owner>
```

Detailed flow and conditional cases are in [`docs/workflow.md`](docs/workflow.md)
and [`docs/handoff-protocol.md`](docs/handoff-protocol.md).

## Skills, tools, and adapters

Skills are reusable capabilities separate from agent identity. This first
version has no concrete `SKILL.md` files; the planned catalog is in
[`skills/README.md`](skills/README.md).

`tools/` is reserved for shared contracts and utilities. Every tool must
document permissions, inputs, outputs, and risks.

`adapters/` is reserved for future integrations with Claude Code, Hermes, or
other runtimes. An adapter may change execution format, but not agent
responsibilities or boundaries.

## Maintenance

When changing an agent:

1. edit the TOML under `agents/`;
2. preserve `name` and the primary role;
3. run `scripts/validate-agents.py`;
4. update affected documentation if the flow changed;
5. repeat relevant smoke tests;
6. review the diff before versioning.

Do not edit the copy accessed through the junction. Always edit the source in
`agents/`.

For the TOML format, see [`docs/agent-contract.md`](docs/agent-contract.md).
For skills, follow [`skills/README.md`](skills/README.md) and add a complete
`SKILL.md`.

## Reference documents

Read these only when the topic appears:

- [`AGENTS.md`](AGENTS.md) — global rules the team must follow;
- [`setup/README.md`](setup/README.md) — beginner-friendly configuration;
- [`agents/README.md`](agents/README.md) — catalog and activation;
- [`docs/agent-contract.md`](docs/agent-contract.md) — TOML schema and review;
- [`docs/task-contract.md`](docs/task-contract.md) — task inputs, states,
  budgets, approvals, retries, checkpoints, quality profiles, evidence, and
  artifact ownership;
- [`docs/evaluation/README.md`](docs/evaluation/README.md) — first benchmark,
  scoring, and baseline comparison;
- [`docs/maker-checker.md`](docs/maker-checker.md) — maker delivery, checker
  rules, and `pass` / `revise` / `block` outcomes;
- [`docs/workflow.md`](docs/workflow.md) — work cycle and responsibilities;
- [`docs/handoff-protocol.md`](docs/handoff-protocol.md) — handoff format;
- [`docs/testing.md`](docs/testing.md) — validation and behavioral tests;
- [`docs/NEXT_STEPS.md`](docs/NEXT_STEPS.md) — milestone backlog and criteria;
- [`docs/research/README.md`](docs/research/README.md) — research sources and decisions;
- [`docs/glossary.md`](docs/glossary.md) — English terms explained in Portuguese;
- [`scripts/README.md`](scripts/README.md) — available automation.

For current standalone-agent behavior and supported locations, see the
[official Codex Subagents documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents).
