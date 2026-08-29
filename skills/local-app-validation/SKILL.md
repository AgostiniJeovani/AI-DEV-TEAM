---
name: local-app-validation
description: Verify an approved web/cloud application locally against its acceptance criteria and report reproducible evidence. Use after implementation or after a corrective retry, before presenting the project as complete.
---

# Local application validation

Use this skill after a delivery checkpoint. The QA engineer owns independent
validation; the responsible implementer must not redefine tests or acceptance
criteria to hide a failure.

1. Read the approved Project Brief, architecture and contract handoffs,
   changed-file list, dependency decisions, and local run instructions.
2. Build a small traceability matrix: each acceptance criterion, expected
   evidence, executable check, result, and gap. Prioritize authentication,
   authorization, data boundaries, errors, recovery, and the highest-value user
   journey.
3. Run the relevant local commands that are actually available: type checking,
   linting, unit/integration/contract tests, production build, and a manual or
   automated smoke path. Before browser work, verify that exactly one intended
   server owns the documented host and port. Probe the exact URL plus local
   aliases (`localhost`, `127.0.0.1`, and `::1`) so two processes cannot serve
   different builds on the same port. Reject split bindings, a stale process,
   or a silently selected fallback port. Do not use production data,
   credentials, destructive actions, or external publication.
4. When the application has a UI, open a fresh page and verify that linked CSS
   and JavaScript load, hydration and loading states finish, material console
   and network errors are absent, the highest-value mutation succeeds through
   visible controls, reload preserves expected data, and desktop/mobile widths
   remain usable. Capture reproducible browser evidence. API, typecheck, and
   build results support this gate but cannot replace it. If browser capability
   appears unavailable, first distinguish a missing browser capability from an
   application that is unreachable, bound to another address, or served by a
   stale process. Mark UI, responsive, accessibility, and interaction criteria
   unverified and return `revise` when the browser is actually unavailable.
5. Validate negative paths and recovery where material: bad input, missing
   permission, offline/provider failure, timeout, retry, invalid state, and
   unavailable data. For AI functionality, test unsupported-answer behavior,
   source/citation behavior, safety boundaries, and budget/latency limits.
6. Record exact commands, environment assumptions, results, failed checks,
   known gaps, and reproducible defects. Send security-relevant issues to
   `security-engineer`, ordinary correctness issues to the responsible
   implementer, and startup, process/port, runtime, browser-reachability,
   asset-loading, or build-pass/runtime-fail defects to `debug-engineer`.
   After its bounded correction, rerun this validation independently; the
   debug handoff is not a QA pass.

Return `pass` only when required evidence exists and no blocker remains;
`revise` when a correctable gap remains; and `block` when scope, approval,
security, dependency, or environment constraints make safe validation
impossible. A successful local result is not a deployment or production claim.
