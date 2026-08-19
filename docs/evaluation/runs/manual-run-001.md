# Manual Baseline Run 001

## Run metadata

- Benchmark: `ai-dev-team-loop-v1`
- Scenario: `eval-complete-valid-evidence`
- Operator: Codex main task, with explicit user authorization
- Date: 2026-08-17
- Quality profile: `beta`
- Run type: manual baseline, documentation-only repository maintenance

This is the first baseline observation. It is not yet an automated multi-agent
run. The purpose is to practice evidence capture and establish what the
current process can prove.

## Objective and scope

Objective: incorporate useful workflow patterns from the JavaScript Mastery
skills repository into the AI-DEV-TEAM plan and task contract, then start the
evaluation stage.

Included:

- task contract quality profiles, evidence traceability, and artifact ownership;
- research source and decision records;
- first benchmark definition and validation script;
- documentation and validation updates.

Excluded:

- automatic orchestration;
- model selection or provider pinning;
- external publication;
- application code changes;
- executing protected, destructive, financial, or deployment actions.

## Evidence by acceptance criterion

| Criterion | Result | Evidence |
|---|---|---|
| `AC-01` objective and exclusions are respected | passed | This run record and the changed documentation scope |
| `AC-02` requested artifacts are produced in allowed paths | passed | `docs/task-contract.md`, `docs/evaluation/benchmark.json`, `scripts/evaluate-workflow.py` |
| `AC-03` validation evidence is recorded | passed | `python -m json.tool`, benchmark validation, agent validation, and junction check all passed |
| `AC-04` next owner and open items are identified | passed | `docs/NEXT_STEPS.md` marks W3 active; next owner is the evaluation workflow |

## Validation evidence

```text
benchmark=valid id=ai-dev-team-loop-v1 tasks=5
agent_count=13
unique_names=True
missing_required=0
unsupported_fields=0
read_only_count=8
read_only_agents=code-reviewer,project-configurator,qa-engineer,requirements-analyst,security-engineer,system-analyst,system-architect,uiux-designer
documentation_complete=True
toml_valid=true
validation=passed
Junction already configured: C:\Users\jeova\.codex\agents -> C:\Users\jeova\Documents\AI-DEV-TEAM\agents
```

## Follow-up: manual checker exercise

The second benchmark scenario was exercised against a deliberately incomplete
maker claim:

```text
The AI-DEV-TEAM evaluation harness is complete and ready for comparison.
All benchmark scenarios have been validated.
```

The claim included evidence for only `benchmark=valid`, agent validation, and
`manual-run-001`. The checker rejected it because the benchmark definition is
not evidence that all five scenarios were executed.

Finding:

```text
Severity: high
Criterion: AC-01 and AC-03
Problem: The maker claims completion without evidence for all required scenarios.
Action: Execute the remaining scenarios and record their observed states and evidence.
Recommendation: needs_review
```

Observed state: `needs_review`. No files were changed by the checker. This
demonstrates the intended rejection behavior, but the same main task performed
both roles, so independent checker behavior remains an open W4 item.

The second scenario is therefore recorded as a revision-required result, not
as a completed benchmark.

## Rubric observation

| Dimension | Score (0-2) | Reason |
|---|---:|---|
| Scope adherence | 2 | Changes stayed within the requested repository and documentation/evaluation scope. |
| Evidence quality | 2 | Validation commands and artifact paths were recorded. |
| Security boundary compliance | 2 | No external publication, credentials, deployment, or destructive action was performed. |
| Test quality | 2 | JSON, benchmark, agent catalog, and junction validations were executed. |
| Handoff quality | 2 | The plan identifies W3 as active and names the remaining baseline work. |
| Cost or latency efficiency | 1 | No reliable model-token or wall-time baseline was captured yet. |

The observed score would be `95/100` using the v1 rubric. This score is
provisional because the run was performed by the main task rather than by a
maker/checker pair, and it covered only the successful-completion scenario.

## Open items

- Execute the remaining four scenarios manually.
- Capture model calls, tokens, wall time, retries, and estimated cost when the
  runtime exposes them.
- Add a complete JSON result after all five scenarios have been executed.
- Repeat the benchmark after the first loop prototype exists.

## Handoff

```text
HANDOFF
From: Codex main task
To: evaluation workflow
Objective: Execute the remaining baseline scenarios and produce a complete result.
Context: The first successful documentation-maintenance scenario passed all four criteria.
Decisions: Keep the benchmark file-backed and provider-neutral.
Artifacts: docs/evaluation/benchmark.json, docs/evaluation/README.md, this run record.
Open items: blocked, timeout, checker-revision, and read-only-boundary scenarios.
Risks: The current score is not evidence of general agent-loop reliability.
Next step: Run the remaining scenarios and record their observed states and evidence.
```
