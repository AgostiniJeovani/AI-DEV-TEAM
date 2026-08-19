# AI-DEV-TEAM Research

This folder is the versioned research record for the agent-loop milestone.
It supports design decisions; it is not intended to reproduce source
articles.

## How to use this folder

1. Start with [`SOURCES.md`](./SOURCES.md) to see the source inventory.
2. Read [`NOTES.md`](./NOTES.md) for the distilled evidence and applicability
   to AI-DEV-TEAM.
3. Read [`DECISIONS.md`](./DECISIONS.md) before changing contracts, prompts,
   permissions, or orchestration.
4. Read [`PORTABILITY_AND_COST.md`](./PORTABILITY_AND_COST.md) before adding a
   runtime adapter or an automated loop.
5. Add new evidence before proposing a design change that depends on it.

## Research rules

- Prefer primary sources: official documentation, papers, standards, and
  first-party engineering reports.
- Record the source date and the date we accessed it.
- Separate what a source demonstrates from our inference about this project.
- Do not treat a benchmark score as a production reliability guarantee.
- Mark a source as `accepted`, `contextual`, `rejected`, or `needs follow-up`.
- Keep summaries short and link to the original source.

## Current scope

The first corpus covers:

- prompt and context engineering;
- agent loops and harness engineering;
- specialist routing and handoffs;
- maker/checker and evaluator-optimizer workflows;
- state, checkpoints, retries, and resumability;
- evaluations, traces, regression suites, and cost/latency;
- human approval and permission boundaries;
- prompt injection, tool misuse, excessive agency, and supply-chain risk.

Portability across Codex, Claude, and Hermes, plus token and cost controls, is
tracked separately in [`PORTABILITY_AND_COST.md`](./PORTABILITY_AND_COST.md).

## Status

Initial corpus created on August 17, 2026. It is a starting point for the
design review, not a final literature review.
