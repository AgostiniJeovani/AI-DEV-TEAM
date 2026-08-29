---
name: web-cloud-project-delivery
description: Deliver an approved web/cloud application through AI-DEV-TEAM specialist handoffs, checkpointed local work, and human approval gates. Use only after a requirements brief and target stack have explicit human approval.
---

# Web/cloud project delivery

Use this skill only when the human has approved a Project Brief, primary stack,
source-of-truth material, and one target project root. Invoke
`project-orchestrator` as the coordinator.

1. Establish a durable goal with the approved outcome, target directory, stop
   conditions, time budget, and validation commands. Classify the work as
   `rapid_mvp` or `standard` using the rules in `project-orchestrator`. The goal
   must end at a locally working application, not a deployment.
2. Let the coordinator create `.ai-dev-team/README.md` and
   `.ai-dev-team/state.json` only if this full workflow is creating or
   improving the target project. Record phase, owner, evidence, risks, and
   next action at each checkpoint.
3. Obtain ordered read-only design inputs as needed: project configuration,
   system analysis, UX, architecture, and security. For `rapid_mvp`, use one
   concise UX handoff for a new interface and consult other roles only for a
   concrete risk or unresolved decision. Keep one delegated agent active at a
   time. If any input changes the approved scope or stack, stop and ask the
   human rather than continuing.
4. Write a single implementation plan with file boundaries, dependency
   candidates, acceptance criteria, owners, and local validation commands.
5. Send one writer at a time for overlapping areas: frontend, backend, data/AI,
   DevOps, or technical writing. Each writer stays inside the target root and
   returns changed files plus executed evidence.
6. Apply `dependency-safety-gate` before every dependency install or
   manifest/lockfile change.
7. Send the resulting work through `local-app-validation`. In `rapid_mvp`, one
   independent QA pass is the final gate; add security or code review only for
   a concrete trigger. In `standard`, use the approved QA, security, and code
   review gates. Route ordinary findings to the responsible implementer. Route
   a reproduced startup, process/port, runtime, browser-reachability, asset, or
   build-pass/runtime-fail defect to `debug-engineer`, then send the correction
   back through independent validation. Checkpoint a bounded retry; do not loop
   indefinitely or repeat an unchanged attempt.
8. For browser-facing work, require interactive evidence from a fresh page on
   one documented server: loaded CSS/JavaScript, completed hydration, the main
   mutation journey, reload persistence where expected, desktop/mobile layout,
   and console/network status. Without browser access, return `needs_review`
   for UI claims. Finish only with a local run path, configuration instructions
   without secrets, acceptance evidence, known limitations, and a human handoff.

Never create a commit or branch, push, deploy, publish, access credentials,
create cloud resources, spend money, or contact an external party. Those are
human-only actions even if a local build is complete.
