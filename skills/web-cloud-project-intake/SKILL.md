---
name: web-cloud-project-intake
description: Start or refine a web/cloud application request through the AI-DEV-TEAM requirements flow. Use when a user wants to turn an idea, existing repository, brief, or supplied research into an approval-ready project plan before implementation.
---

# Web/cloud project intake

Use this skill before implementation of a new or materially changed web/cloud
application with an API or backend. It is the entry point for a full project
loop, not a replacement for a focused agent used independently.

1. Confirm the one target project directory. Do not create files outside it.
2. Ask `requirements-analyst` to lead discovery. Give it the user's goal,
   constraints, existing repository context, and every file or URL supplied by
   the human.
3. Enforce source priority: human-provided materials first, target-project
   evidence second, authoritative research third, clearly labeled assumptions
   last.
4. Let the analyst ask read-only specialists only for focused uncertainty:
   `project-configurator` for an existing codebase, `system-analyst` for
   domain behavior, `uiux-designer` for experience, `system-architect` for
   technical options, and `security-engineer` for material risk.
5. Require one concise Project Brief: problem, users, scope and exclusions,
   prioritized requirements, acceptance criteria, source register,
   assumptions, risks, dependency needs, and decisions requested from the
   human.
6. Stop for the human to approve scope, source of truth, and primary stack.
   Ask only questions whose answers materially change the result. Do not write
   application code, install packages, or create `.ai-dev-team/` during intake.

The output is ready for `web-cloud-project-delivery` only after explicit human
approval. If the request is for mobile, desktop, embedded, deployment, or a
different platform, explain that it is outside this v1 skill rather than
pretending the workflow covers it.
