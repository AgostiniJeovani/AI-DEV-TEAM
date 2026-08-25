# Evaluation Harness

This is the final, optional step of the guided path. Use it to compare a
proposed change to the catalog or controlled loop with a measured local
baseline. It is not needed to activate or use the agents.

## What stays in the repository

`benchmark.json` defines five provider-neutral scenarios:

1. successful work with evidence;
2. a checker decision that requires revision;
3. work blocked by input or approval;
4. a retry or budget limit; and
5. a read-only or allowed-path boundary check.

The evaluator checks expected task states, acceptance criteria, scope,
evidence, security boundaries, tests, handoffs, and cost or latency data.
It does not run models or fabricate evidence.

## Validate the benchmark

```powershell
python .\scripts\evaluate-workflow.py `
  --benchmark .\docs\evaluation\benchmark.json `
  --validate-only
```

## Compare a change

Keep measured result files outside version control, for example under
`.evaluation\results\`:

```powershell
python .\scripts\evaluate-workflow.py `
  --benchmark .\docs\evaluation\benchmark.json `
  --baseline .\.evaluation\results\baseline.json `
  --result .\.evaluation\results\candidate.json `
  --label candidate
```

A higher score is evidence to inspect, not automatic permission to adopt a
change. Review the task evidence, safety behavior, cost, and limitations
before a human approves it.
