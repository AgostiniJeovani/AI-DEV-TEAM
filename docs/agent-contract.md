# Agent Contract

## Codex TOML schema

Every standalone agent must have these three required fields:

```toml
name = "agent-name"
description = "When and why to use this agent."
sandbox_mode = "read-only"

developer_instructions = """
Complete agent instructions.
"""
```

`sandbox_mode` is optional in the Codex schema, but this repository defines it
to make autonomy explicit. We use `read-only` for analysis, architecture,
security, QA, and review; and `workspace-write` for authorized implementation,
operations, or documentation.

We do not use `model` or `model_reasoning_effort` in this first version. The
environment can resolve an available model without breaking the catalog when
availability changes.

## Where team concepts live

The Codex schema has no native fields for `role`, `responsibilities`,
`handoff_targets`, or `non_responsibilities`. These concepts live inside
`developer_instructions` in language the agent can follow.

`description` should remain short and guide selection. Instructions should
explain purpose, responsibilities, boundaries, autonomy, expected outputs, and
handoffs.

## Review checklist

When creating or reviewing an agent, ask:

1. Which decision or work does it improve?
2. Which boundary prevents overlap?
3. What must it read before acting?
4. Can it write? If yes, does the request authorize the change?
5. How does the user verify the result?
6. Which agent receives the output?
7. Does `scripts/validate-agents.py` pass?
