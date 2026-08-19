# Evaluation Harness

This folder contains the first provider-neutral benchmark for the AI-DEV-TEAM
loop. It is intentionally small and file-backed. It does not call a model,
publish results, access credentials, or claim that the benchmark represents all
software engineering work.

## What it measures

Each benchmark task has an expected state and acceptance criteria. A result
records the observed state, criterion evidence, six rubric scores, and optional
runtime data.

The score has two parts:

- acceptance criteria: 40 points;
- six rubric dimensions, 10 points each: scope adherence, evidence quality,
  security boundary compliance, test quality, handoff quality, and cost or
  latency efficiency.

The command rejects incomplete or contradictory result files. It can validate a
single result or compare a candidate against a baseline. It never decides that
a task is successful only because an agent says it is done.

## Files

- `benchmark.json`: versioned task scenarios, expected states, criteria, and
  rubric definitions;
- `README.md`: this guide;
- `results/`: local evaluation outputs, ignored by default until a result is
  intentionally versioned.

## Run the benchmark validator

From the repository root:

```powershell
python .\scripts\evaluate-workflow.py --benchmark .\docs\evaluation\benchmark.json --validate-only
```

## Evaluate a result

Create a result JSON using the schema described in the benchmark, then run:

```powershell
python .\scripts\evaluate-workflow.py `
  --benchmark .\docs\evaluation\benchmark.json `
  --result .\docs\evaluation\results\candidate.json `
  --label candidate
```

The result file is evidence supplied by a workflow run. The harness checks its
shape and computes a score; it does not fabricate missing evidence.

## Compare two versions

```powershell
python .\scripts\evaluate-workflow.py `
  --benchmark .\docs\evaluation\benchmark.json `
  --baseline .\docs\evaluation\results\baseline.json `
  --result .\docs\evaluation\results\candidate.json `
  --label candidate
```

An improvement is not accepted only because its score is higher. Review the
criterion evidence, boundary behavior, cost, and known limitations together.
The baseline files are measured outputs, not placeholders that should be
committed before an actual run.

## Manual baseline flow

Until the loop controller exists, run one scenario at a time with the current
agents and rules:

1. Select one task from `benchmark.json`.
2. Create or read its task contract.
3. Give the work only to the responsible agent or human operator.
4. Record each handoff, artifact, command, approval, and failure.
5. Run the validations required by the task's quality profile.
6. Record the observed state and score evidence in `docs/evaluation/runs/`.
7. Repeat the same scenario later with the proposed loop.

The manual run is the baseline, not the target architecture. It tells us how
much coordination, evidence, time, and judgment the current process needs
before automation changes it.

## First benchmark scenarios

The initial set covers:

1. successful completion with evidence;
2. checker findings that require revision;
3. blocked work waiting for input or approval;
4. a task that reaches a retry or budget limit;
5. a read-only and allowed-path boundary check.

The benchmark will be expanded only when the current scenarios produce useful
comparisons. The next stage is to run these scenarios against the current
manual workflow and record the first baseline.
