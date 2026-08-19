# Scripts

Validation and maintenance scripts for the catalog. They should be safe,
deterministic, and must not publish changes or access credentials.

Run `validate-agents.py` before versioning or activating a new agent version.

Run `evaluate-workflow.py --benchmark ..\docs\evaluation\benchmark.json
--validate-only` to validate the first file-backed evaluation benchmark. See
[`docs/evaluation/README.md`](../docs/evaluation/README.md) for result format,
scoring, and baseline comparison.

Run `check-workflow.py --submission <file.json>` to apply the deterministic
maker/checker gate. It returns `pass`, `revise`, or `block` and never edits the
maker's artifacts. The contract and examples are in
[`docs/maker-checker.md`](../docs/maker-checker.md).

Add `--review-report <file.json>` when a separate reviewer has produced an
independent report. The script combines the hard deterministic checks with the
review outcome and preserves the reviewer's findings.
