# AI-DEV-TEAM Setup

This guide is for anyone configuring the project for the first time.

## What we will do

The agents are versioned under `agents/` in this repository. Codex looks for
global agents in a user-specific folder. The automation creates a **junction**,
which works like a folder bridge:

```text
%USERPROFILE%\.codex\agents
        → this repository's agents/ folder
```

Codex uses the bridge, but the files remain in one place: the repository. We
do not need to keep two copies synchronized.

## Before you start

You need:

- Windows;
- Codex installed and working;
- this repository saved locally;
- Python 3.11 or newer for the validator.

Do not put passwords, tokens, or `.env` files in this repository.

## Three-step setup

### Step 1 — open a terminal at the root

Open PowerShell in the folder containing this README. If preferred:

```powershell
cd <repository-root>
```

### Step 2 — run the automation

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-windows.ps1
```

The script checks the agent folder, creates the bridge if it does not exist,
and confirms that it points to this repository. It never replaces a real folder
or a junction pointing somewhere else.

If everything is correct, you will see a message similar to:

```text
Junction already configured: ...\.codex\agents -> ...\agents
validation=passed
```

Running the command again is safe; it does not recreate a valid junction.

### Step 3 — validate the files

```powershell
python .\scripts\validate-agents.py
```

Look for:

```text
agent_count=13
missing_required=0
unsupported_fields=0
read_only_count=8
read_only_agents=code-reviewer,project-configurator,qa-engineer,requirements-analyst,security-engineer,system-analyst,system-architect,uiux-designer
documentation_complete=True
validation=passed
```

If `validation=failed` appears, read the `ERROR` lines and fix the indicated
file before opening Codex.

## Visual confirmation

In File Explorer, open `%USERPROFILE%\.codex\agents`. The folder should appear
as a junction/system link and contain the same `.toml` files as `agents/` in
this repository.

For a technical confirmation that changes nothing:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-windows.ps1 -CheckOnly
```

## Undo the setup

To stop exposing the catalog globally, remove only the junction:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\remove-junction-windows.ps1
```

The repository files are not deleted. The script refuses to remove a real
folder or a junction pointing somewhere else.

## Common problems

### “Python was not found”

Install Python 3.11+ or run the junction check with `-SkipValidation`. TOML
validation remains pending until Python is available.

### “The destination already exists and is not a junction”

The script stopped to avoid deleting a real folder. Inspect its contents and
make a backup before deciding manually what to do. Do not delete anything just
to force the script.

### “The junction points somewhere else”

An earlier configuration exists. Do not use `Remove-Item` directly. Confirm the
target and use the removal script only if that junction really belongs to
AI-DEV-TEAM.

### Codex does not show the agents

1. run the validator;
2. run `setup-windows.ps1 -CheckOnly`;
3. confirm that the correct repository is open in Codex;
4. restart the Codex session if it was already open before setup;
5. confirm that files exist under `agents/` and end in `.toml`.

After setup, return to the root README and follow **First use**.
