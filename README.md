# AI-DEV-TEAM

AI-DEV-TEAM is a versioned catalog of Codex agents for planning, building,
reviewing, securing, operating, and documenting software. It is an
experimental, local-first project: it does not deploy, publish, install
dependencies, or access credentials by itself.

This guide is deliberately linear. Read each step to the end before moving to
the single next document. That gives you a complete first use without hunting
through the repository.

## Before you start

You need Windows, Codex, Python 3.11 or newer, and a local copy of this
repository. Do not place secrets, tokens, `.env` files, or production data in
this repository.

The source of truth is the `agents/` folder. `AGENTS.md` contains the global
rules that all agents follow.

## Step 1 — Install the repository

Clone or download the repository to a folder you control, then open that
folder in a terminal and in Codex. No dependency installation is required.

Do not edit the global Codex agent folder directly. The next step connects it
to the versioned files in this repository safely.

## Next step

Read [`setup/README.md`](setup/README.md) completely to activate the catalog.
