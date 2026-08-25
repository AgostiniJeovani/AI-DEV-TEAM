"""Run the first narrow, file-backed AI-DEV-TEAM maker/checker workflow.

This controller orchestrates evidence already supplied by a maker. It does not
invoke agents or tools, edit the target repository, publish artifacts, or grant
approval. A runtime adapter remains responsible for those side effects.
"""

from __future__ import annotations

import argparse
import fnmatch
import importlib.util
import json
import os
import sys
import tempfile
import tomllib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from types import ModuleType
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


class WorkflowError(ValueError):
    """Raised when a workflow input or transition violates the loop contract."""


def load_module(filename: str, module_name: str) -> ModuleType:
    specification = importlib.util.spec_from_file_location(module_name, ROOT / "scripts" / filename)
    if specification is None or specification.loader is None:
        raise WorkflowError(f"could not load local module: {filename}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


TASK_STATE = load_module("task-state.py", "ai_dev_team_task_state")
CHECKER = load_module("check-workflow.py", "ai_dev_team_checker")


def timestamp(current: datetime | None = None) -> str:
    return (current or datetime.now(timezone.utc)).astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_timestamp(value: str | None) -> datetime:
    if value is None:
        return datetime.now(timezone.utc)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise WorkflowError(f"invalid timestamp: {value}") from exc
    if parsed.tzinfo is None:
        raise WorkflowError("timestamps must include a timezone")
    return parsed.astimezone(timezone.utc)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise WorkflowError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise WorkflowError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise WorkflowError(f"expected a JSON object: {path}")
    return value


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def relative_path(root: Path, path: Path, *, must_exist: bool = False) -> str:
    resolved_root = root.resolve()
    resolved_path = path.resolve()
    try:
        relative = resolved_path.relative_to(resolved_root)
    except ValueError as exc:
        raise WorkflowError(f"path is outside repository root: {path}") from exc
    if must_exist and not resolved_path.exists():
        raise WorkflowError(f"file not found: {relative.as_posix()}")
    return relative.as_posix()


def artifact_path(root: Path, value: Any, *, must_exist: bool = True) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WorkflowError("artifact paths must be non-empty strings")
    candidate = Path(value)
    if candidate.is_absolute() or ".." in PurePosixPath(value.replace("\\", "/")).parts:
        raise WorkflowError(f"artifact path must be repository-relative: {value}")
    return relative_path(root, root / candidate, must_exist=must_exist)


def matches_allowed_path(path: str, allowed: str) -> bool:
    normalized_path = path.replace("\\", "/")
    normalized_allowed = allowed.replace("\\", "/")
    if normalized_allowed.endswith("/"):
        return normalized_path.startswith(normalized_allowed)
    if any(symbol in normalized_allowed for symbol in "*?["):
        return fnmatch.fnmatchcase(normalized_path, normalized_allowed)
    return normalized_path == normalized_allowed


def agent_mode(root: Path, agent_name: str) -> str:
    path = root / "agents" / f"{agent_name}.toml"
    if not path.exists():
        raise WorkflowError(f"responsible agent is not in the catalog: {agent_name}")
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise WorkflowError(f"invalid agent TOML: {agent_name}") from exc
    return data.get("sandbox_mode", "workspace-write")


def validate_submission_boundary(
    root: Path, contract: dict[str, Any], submission: dict[str, Any]
) -> tuple[list[str], list[str]]:
    findings: list[str] = []
    artifacts: list[str] = []
    if submission.get("task_id") != contract.get("task_id"):
        findings.append("submission task_id does not match the contract")
    if submission.get("maker") != contract.get("responsible_agent"):
        findings.append("submission maker does not match the responsible agent")

    raw_artifacts = submission.get("artifacts")
    if not isinstance(raw_artifacts, list) or not raw_artifacts:
        findings.append("submission must contain at least one artifact")
    else:
        allowed_paths = contract.get("allowed_paths", {}).get("write")
        if not isinstance(allowed_paths, list) or not all(isinstance(item, str) for item in allowed_paths):
            findings.append("contract must declare allowed_paths.write")
            allowed_paths = []
        excluded = contract.get("scope", {}).get("excluded", [])
        if not isinstance(excluded, list):
            excluded = []
        for raw_artifact in raw_artifacts:
            try:
                path = artifact_path(root, raw_artifact)
            except WorkflowError as exc:
                findings.append(str(exc))
                continue
            artifacts.append(path)
            if not any(matches_allowed_path(path, allowed) for allowed in allowed_paths):
                findings.append(f"artifact is outside allowed write paths: {path}")
            if any(matches_allowed_path(path, pattern) for pattern in excluded if isinstance(pattern, str)):
                findings.append(f"artifact is in an excluded scope: {path}")

    try:
        mode = agent_mode(root, str(contract.get("responsible_agent", "")))
    except WorkflowError as exc:
        findings.append(str(exc))
    else:
        if mode == "read-only" and artifacts:
            findings.append("a read-only responsible agent cannot produce writable artifacts")
    return artifacts, findings


def write_handoff(
    path: Path,
    *,
    outcome: str,
    contract: dict[str, Any],
    artifacts: list[str],
    evidence: list[str],
    reasons: list[str],
    next_action: str,
) -> None:
    recipient = contract["responsible_agent"] if outcome == "revise" else "human or next declared workflow owner"
    if outcome == "completed":
        recipient = "user or next declared workflow owner"
    if outcome == "blocked":
        recipient = "human approver or responsible owner"
    content = "\n".join(
        [
            "HANDOFF",
            "From: narrow-loop-controller",
            f"To: {recipient}",
            f"Objective: {contract['objective']}",
            "Context: Repository-local maker submission was checked against the task contract and deterministic checker.",
            f"Decisions: outcome={outcome}; reasons={' | '.join(reasons)}",
            f"Artifacts: {', '.join(artifacts) if artifacts else 'none'}",
            f"Evidence: {', '.join(evidence) if evidence else 'none'}",
            "Open items: none" if outcome == "completed" else "Open items: resolve the recorded findings or approval requirement.",
            "Risks: The controller does not execute agents, enforce runtime sandboxing, or perform external side effects.",
            f"Next step: {next_action}",
            "",
        ]
    )
    atomic_write_text(path, content)


def execute_workflow(
    *,
    root: Path,
    contract_path: Path,
    submission_path: Path,
    state_path: Path,
    report_path: Path,
    handoff_path: Path,
    review_report_path: Path | None,
    current: datetime,
) -> dict[str, Any]:
    root = root.resolve()
    contract_reference = relative_path(root, contract_path, must_exist=True)
    submission_reference = relative_path(root, submission_path, must_exist=True)
    state_reference = relative_path(root, state_path)
    report_reference = relative_path(root, report_path)
    handoff_reference = relative_path(root, handoff_path)
    review_reference = relative_path(root, review_report_path, must_exist=True) if review_report_path else None
    output_references = [state_reference, report_reference, handoff_reference]
    if len(set(output_references)) != len(output_references):
        raise WorkflowError("state, report, and handoff paths must be distinct")
    input_references = {contract_reference, submission_reference}
    if review_reference:
        input_references.add(review_reference)
    overlap = sorted(set(output_references).intersection(input_references))
    if overlap:
        raise WorkflowError(f"output paths cannot overwrite workflow inputs: {', '.join(overlap)}")

    contract = load_json(root / contract_reference)
    try:
        TASK_STATE.validate_contract(contract)
    except TASK_STATE.StateError as exc:
        raise WorkflowError(str(exc)) from exc
    submission = load_json(root / submission_reference)
    if state_path.exists():
        state = TASK_STATE.load_state(state_path)
        if state["task_id"] != contract["task_id"]:
            raise WorkflowError("existing state belongs to a different task")
        if state["state"] != "created":
            raise WorkflowError(f"workflow state must be created for this prototype, got {state['state']}")
    else:
        state = TASK_STATE.initial_state(contract, contract_path, timestamp(current))
        TASK_STATE.save_state(state_path, state)

    artifacts, boundary_findings = validate_submission_boundary(root, contract, submission)
    submission_evidence = [submission_reference]
    TASK_STATE.transition(
        state,
        target="in_progress",
        stage="maker",
        agent=contract["responsible_agent"],
        artifacts=artifacts,
        evidence=submission_evidence,
        reason=None,
        next_action="validate_contract_boundary_then_run_checker",
        pending_approval=None,
        current=current,
    )
    TASK_STATE.save_state(state_path, state)

    checker_result: dict[str, Any] | None = None
    if boundary_findings:
        outcome = "block"
        reasons = boundary_findings
        next_action = "obtain_a_safe_contract_or_route_to_the_responsible_owner"
        pending_approval = None
    else:
        try:
            checker_result = CHECKER.check_submission(submission)
            if review_report_path:
                review = CHECKER.load_review_report(review_report_path, submission["task_id"])
                checker_result = CHECKER.combine_with_review(checker_result, review)
        except ValueError as exc:
            outcome = "failed"
            reasons = [f"checker input is invalid: {exc}"]
            next_action = "repair_the_submission_contract_before_restart"
            pending_approval = None
        else:
            outcome = checker_result["outcome"]
            reasons = checker_result["reasons"]
            pending_approval = "record_required_approval" if (
                outcome == "block" and submission.get("approval", {}).get("required") is True
                and submission.get("approval", {}).get("granted") is not True
            ) else None
            next_action = {
                "pass": "accept_the_handoff_or_run_the_next_declared_gate",
                "revise": "fix_the_checker_findings_and_retry_with_new_evidence",
                "block": "obtain_required_approval_or_resolve_the_blocking_boundary",
            }[outcome]

    report = {
        "workflow": "narrow-repository-maintenance-v1",
        "task_id": contract["task_id"],
        "created_at": timestamp(current),
        "contract": contract_reference,
        "submission": submission_reference,
        "review_report": review_reference,
        "state": state_reference,
        "outcome": outcome,
        "boundary_findings": boundary_findings,
        "checker_result": checker_result,
        "artifacts": artifacts,
        "evidence": [submission_reference, report_reference, handoff_reference],
        "next_action": next_action,
    }
    TASK_STATE.atomic_write(report_path, report)
    write_handoff(
        handoff_path,
        outcome=outcome,
        contract=contract,
        artifacts=artifacts + [report_reference],
        evidence=report["evidence"],
        reasons=reasons,
        next_action=next_action,
    )

    if outcome == "pass":
        TASK_STATE.transition(
            state,
            target="in_progress",
            stage="handoff",
            agent="narrow-loop-controller",
            artifacts=[report_reference, handoff_reference],
            evidence=[report_reference, handoff_reference],
            reason=None,
            next_action="confirm_completion_against_acceptance_evidence",
            pending_approval=None,
            current=current,
        )
        TASK_STATE.transition(
            state,
            target="completed",
            stage=None,
            agent=None,
            artifacts=[],
            evidence=[report_reference, handoff_reference],
            reason=None,
            next_action="stop",
            pending_approval=None,
            current=current,
        )
    elif outcome == "revise":
        TASK_STATE.transition(
            state,
            target="needs_review",
            stage="checker",
            agent="narrow-loop-controller",
            artifacts=[report_reference, handoff_reference],
            evidence=[report_reference, handoff_reference],
            reason="checker_requested_revision",
            next_action=next_action,
            pending_approval=None,
            current=current,
        )
    elif outcome == "block":
        TASK_STATE.transition(
            state,
            target="blocked",
            stage="checker",
            agent="narrow-loop-controller",
            artifacts=[report_reference, handoff_reference],
            evidence=[report_reference, handoff_reference],
            reason="workflow_boundary_or_checker_block",
            next_action=next_action,
            pending_approval=pending_approval,
            current=current,
        )
    else:
        TASK_STATE.transition(
            state,
            target="failed",
            stage="checker",
            agent="narrow-loop-controller",
            artifacts=[report_reference, handoff_reference],
            evidence=[report_reference, handoff_reference],
            reason="invalid_checker_input",
            next_action=next_action,
            pending_approval=None,
            current=current,
        )
    TASK_STATE.save_state(state_path, state)
    report["final_state"] = state["state"]
    report["latest_checkpoint"] = state["checkpoints"][-1]["checkpoint_id"]
    TASK_STATE.atomic_write(report_path, report)
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--submission", type=Path, required=True)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--handoff", type=Path, required=True)
    parser.add_argument("--review-report", type=Path)
    parser.add_argument("--now")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = args.repo_root.resolve()

    def resolve_argument(path: Path) -> Path:
        return path.resolve() if path.is_absolute() else root / path

    try:
        result = execute_workflow(
            root=root,
            contract_path=resolve_argument(args.contract),
            submission_path=resolve_argument(args.submission),
            state_path=resolve_argument(args.state),
            report_path=resolve_argument(args.report),
            handoff_path=resolve_argument(args.handoff),
            review_report_path=resolve_argument(args.review_report) if args.review_report else None,
            current=parse_timestamp(args.now),
        )
    except (OSError, WorkflowError, TASK_STATE.StateError) as exc:
        print(f"workflow=failed reason={exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
