# Setup

This is step 2 of the guided path. It activates the versioned agent catalog
for Codex on Windows.

## What activation does

The repository keeps its agent files in `agents/`. Codex discovers personal
agents in `%USERPROFILE%\.codex\agents`. The setup script creates a Windows
junction between those locations:

```text
%USERPROFILE%\.codex\agents  →  <repository>\agents
```

The junction is a folder bridge, not a second copy. Edit the repository files;
never edit the global side of the bridge.

## Activate

From the repository root, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-windows.ps1
```

The script creates the junction only when safe. It refuses to replace a real
folder or a junction that points to another location.

## Verify or undo

Verify without changing anything:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-windows.ps1 -CheckOnly
```

To stop exposing this catalog globally, remove only its junction:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\remove-junction-windows.ps1
```

Neither command deletes the agent files in this repository.

## If activation stops

- If Python is unavailable, install Python 3.11+ and run validation later.
- If the destination is a real folder, inspect and back it up manually; the
  setup script will not delete it.
- If the junction points elsewhere, confirm its owner before using the removal
  script.

## Next step

Read [`scripts/README.md`](../scripts/README.md) completely to validate and
test the activated catalog.
