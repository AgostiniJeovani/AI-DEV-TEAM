# Setup

This is step 2 of the guided path. It activates the versioned agent catalog and
its reusable skills for Codex on Windows.

## What activation does

The repository keeps agent files in `agents/` and skill folders in `skills/`.
The setup script creates a Windows junction for the agent catalog and one safe
child junction per AI-DEV-TEAM skill:

```text
%USERPROFILE%\.codex\agents  →  <repository>\agents
%USERPROFILE%\.codex\skills\<skill-name>  →  <repository>\skills\<skill-name>
```

These are folder bridges, not second copies. Edit files in the repository;
never edit the global side of a bridge. The script refuses to replace a real
folder or a junction that points elsewhere, including your unrelated skills.

## Activate

From the repository root, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-windows.ps1
```

The script creates every junction only when safe. It validates all destinations
before changing anything, so a conflicting folder does not leave activation
partially configured.

## Verify or undo

Verify without changing anything:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-windows.ps1 -CheckOnly
```

To stop exposing this catalog globally, remove only its verified agent and
skill junctions:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\remove-junction-windows.ps1
```

Neither command deletes repository files or unrelated personal skills.

## If activation stops

- If Python is unavailable, install Python 3.11+ and run validation later.
- If the destination is a real folder, inspect and back it up manually; the
  setup script will not delete it.
- If the junction points elsewhere, confirm its owner before using the removal
  script.

## Next step

Read [`scripts/README.md`](../scripts/README.md) completely to validate and
test the activated catalog.
