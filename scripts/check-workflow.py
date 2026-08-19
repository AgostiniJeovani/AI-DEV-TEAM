"""Apply deterministic and optional independent maker/checker gates."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_submission(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("submission must be a JSON object")
    return value


def check_submission(submission: dict[str, Any]) -> dict[str, Any]:
    required = {"task_id", "maker", "artifacts", "criteria", "scope", "security", "approval", "findings"}
    missing = required.difference(submission)
    if missing:
        raise ValueError(f"submission missing fields: {', '.join(sorted(missing))}")

    criteria = submission["criteria"]
    if not isinstance(criteria, list) or not criteria:
        raise ValueError("criteria must be a non-empty list")
    findings = submission["findings"]
    if not isinstance(findings, list):
        raise ValueError("findings must be a list")

    reasons: list[str] = []
    next_actions: list[str] = []
    outcome = "pass"

    approval = submission["approval"]
    if not isinstance(approval, dict):
        raise ValueError("approval must be an object")
    if approval.get("required") is True and approval.get("granted") is not True:
        outcome = "block"
        reasons.append("required approval is missing")
        next_actions.append("obtain and record the required approval before continuing")

    security = submission["security"]
    scope = submission["scope"]
    if not isinstance(security, dict) or not isinstance(scope, dict):
        raise ValueError("scope and security must be objects")
    if security.get("boundary_ok") is not True:
        outcome = "block"
        reasons.append("security or permission boundary is not satisfied")
        next_actions.append("stop and route the issue to security or the responsible owner")
    if security.get("unknown_side_effect") is True:
        outcome = "block"
        reasons.append("unknown side effect was reported")
        next_actions.append("identify and authorize the side effect before continuing")
    if scope.get("within_scope") is not True:
        outcome = "block"
        reasons.append("submission is outside the declared scope")
        next_actions.append("return to requirements or obtain explicit scope approval")

    missing_evidence = []
    for criterion in criteria:
        if not isinstance(criterion, dict) or not criterion.get("id"):
            raise ValueError("each criterion needs an id")
        if criterion.get("verified") is not True or not criterion.get("evidence"):
            missing_evidence.append(criterion["id"])
    if missing_evidence and outcome != "block":
        outcome = "revise"
        reasons.append("required criteria lack verified evidence: " + ", ".join(missing_evidence))
        next_actions.append("add evidence and verify every listed acceptance criterion")

    for finding in findings:
        if not isinstance(finding, dict):
            raise ValueError("each finding must be an object")
        severity = finding.get("severity")
        if severity in {"critical", "high"}:
            outcome = "block"
            reasons.append(f"{severity} finding: {finding.get('message', 'unspecified')}")
            next_actions.append("resolve the high-impact finding and run the checker again")
        elif severity in {"medium", "low"} and finding.get("correctable") is True and outcome != "block":
            outcome = "revise"
            reasons.append(f"correctable {severity} finding: {finding.get('message', 'unspecified')}")
            next_actions.append("fix the finding and run the checker again")

    if outcome == "pass":
        reasons.append("all required criteria have evidence and no blocking finding remains")
        next_actions.append("continue to the next declared verification gate")

    return {
        "task_id": submission["task_id"],
        "maker": submission["maker"],
        "checker": "deterministic-file-checker-v1",
        "checker_independence": "deterministic_script",
        "outcome": outcome,
        "reasons": reasons,
        "next_actions": next_actions,
        "artifacts_reviewed": submission["artifacts"],
    }


def load_review_report(path: Path, task_id: str) -> dict[str, Any]:
    report = load_submission(path)
    required = {"task_id", "reviewer", "independent", "outcome", "findings"}
    missing = required.difference(report)
    if missing:
        raise ValueError(f"review report missing fields: {', '.join(sorted(missing))}")
    if report["task_id"] != task_id:
        raise ValueError("review report task_id does not match the submission")
    if report["outcome"] not in {"pass", "revise", "block"}:
        raise ValueError("review outcome must be pass, revise, or block")
    if not isinstance(report["independent"], bool):
        raise ValueError("review independent must be true or false")
    if not isinstance(report["findings"], list):
        raise ValueError("review findings must be a list")
    return report


def combine_with_review(result: dict[str, Any], report: dict[str, Any]) -> dict[str, Any]:
    rank = {"pass": 0, "revise": 1, "block": 2}
    deterministic_outcome = result["outcome"]
    reported_review_outcome = report["outcome"]
    review_outcome = reported_review_outcome
    for finding in report["findings"]:
        if not isinstance(finding, dict):
            raise ValueError("each review finding must be an object")
        severity = finding.get("severity")
        if severity in {"critical", "high"}:
            review_outcome = "block"
        elif severity in {"medium", "low"} and finding.get("correctable") is True:
            if rank[review_outcome] < rank["revise"]:
                review_outcome = "revise"
    combined_outcome = max((deterministic_outcome, review_outcome), key=lambda value: rank[value])
    reasons = list(result["reasons"])
    next_actions = list(result["next_actions"])

    if review_outcome == "block":
        reasons.append("independent review reported a blocking finding")
        next_actions.append("resolve the independent review finding before continuing")
    elif review_outcome == "revise":
        reasons.append("independent review reported a correctable finding")
        next_actions.append("address the independent review finding and run the checker again")
    else:
        reasons.append("independent review found no blocking or revision finding")

    warnings = []
    if report["independent"] is not True:
        warnings.append("review report was not independent; treat it as an additional review, not a second opinion")
    if review_outcome != reported_review_outcome:
        warnings.append("deterministic safety rules upgraded the review outcome based on finding severity")

    return {
        **result,
        "checker": "deterministic-file-checker-v1+review-report-v1",
        "checker_independence": "independent_reviewer" if report["independent"] else "non_independent_review",
        "outcome": combined_outcome,
        "reasons": reasons,
        "next_actions": next_actions,
        "warnings": warnings,
        "independent_review": {
            "reviewer": report["reviewer"],
            "reported_outcome": reported_review_outcome,
            "effective_outcome": review_outcome,
            "findings": report["findings"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--submission", type=Path, required=True)
    parser.add_argument("--review-report", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        submission = load_submission(args.submission)
        result = check_submission(submission)
        if args.review_report:
            report = load_review_report(args.review_report, submission["task_id"])
            result = combine_with_review(result, report)
    except ValueError as exc:
        print(f"checker=failed reason={exc}", file=sys.stderr)
        return 1

    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    print(rendered)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
