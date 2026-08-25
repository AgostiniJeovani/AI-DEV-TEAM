# AI-DEV-TEAM Copilot Review Instructions

AI-DEV-TEAM is an experimental, local-first catalog of specialized Codex
agents and a small controlled workflow. Treat it as a study project, not a
production-ready autonomous framework.

## Review scope

When reviewing a change or pull request:

1. Read the relevant repository guidance before judging the diff. Start with
   `README.md` and `AGENTS.md`; then use the README in the affected folder:
   `agents/README.md`, `setup/README.md`, `scripts/README.md`,
   `docs/README.md`, or `docs/evaluation/README.md`.
2. Review only the stated scope. Flag unrelated changes rather than expanding
   the review into a redesign.
3. Check that agent modes, approval requirements, file boundaries, and
   read-only responsibilities remain consistent with the agent TOML files and
   `AGENTS.md`.
4. Require observable evidence for claims about validation, completion,
   safety, cost, or autonomy. Do not accept an agent's assertion as evidence.
5. For controlled-workflow changes, check explicit task states, stop
   conditions, retries, checkpoints, handoffs, and failure paths. Prefer
   repository-local, inspectable behavior over hidden state.
6. Check that the affected README and applicable validation commands are
   updated when agent behavior, scripts, setup, or workflow boundaries change.

## Review outcome

Use one explicit outcome:

- `pass`: no blocking or revision finding remains;
- `revise`: a correctable defect, missing evidence, incomplete validation, or
  documentation gap must be addressed;
- `block`: a security, permission, approval, destructive-action, or scope
  boundary prevents safe progress.

List findings by severity. Every finding must name the affected file or
artifact, explain why it matters, and propose a concrete next action. Separate
real defects from optional suggestions. Do not invent test results, project
requirements, credentials, or deployment state.

## Safety and collaboration

Do not recommend bypassing human approval for external publication,
deployment, billing, secrets, destructive changes, or sensitive data. Keep
reviews concise and evidence-based. The reviewer reports findings; the maker
or responsible owner decides and implements the fix.
