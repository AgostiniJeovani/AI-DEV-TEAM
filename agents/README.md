# Agents

The files in this folder are custom agents compatible with Codex standalone
agent files. Each file contains only supported fields: `name`, `description`,
`developer_instructions`, and, when needed, `sandbox_mode`.

For Codex to use this catalog globally, the recommended configuration for this
repository is a Windows junction:

```text
%USERPROFILE%\.codex\agents
    └── junction → <repository-root>\agents
```

The repository remains the single source of truth while Codex sees the agents
through its global path. `scripts/setup-windows.ps1` creates or verifies this
junction.

For an isolated project, you can instead copy the files to:

- `.codex/agents/` for project-specific agents; or
- `~/.codex/agents/` for personal global agents.

The filename should match the `name` field. Do not pin `model` or
`model_reasoning_effort` in this first version; Codex can resolve these values
from the environment and current availability.
