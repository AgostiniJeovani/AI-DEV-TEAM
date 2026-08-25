"""Manage durable state, checkpoints, retries, and stop conditions for a task.

The controller is intentionally file-backed and provider-neutral. It records
state transitions but does not execute tools, agents, or external side effects.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


STATES = {
    "created",
    "in_progress",
    "needs_review",
    "completed",
    "blocked",
    "failed",
    "cancelled",
    "timed_out",
}
TERMINAL_STATES = {"completed", "failed", "cancelled", "timed_out"}
TRANSITIONS = {
    "created": {"in_progress", "cancelled"},
    "in_progress": {
        "in_progress",
        "needs_review",
        "completed",
        "blocked",
        "failed",
        "cancelled",
        "timed_out",
    },
    "needs_review": {"in_progress", "blocked", "cancelled", "failed", "timed_out"},
    "blocked": {"in_progress", "cancelled", "failed"},
    "failed": {"in_progress", "cancelled"},
    "timed_out": {"in_progress", "cancelled"},
    "completed": set(),
    "cancelled": set(),
}
USAGE_KEYS = {
    "model_calls": "max_model_calls",
    "input_tokens": "max_input_tokens",
    "output_tokens": "max_output_tokens",
    "subagents": "max_subagents",
    "estimated_cost": "max_estimated_cost",
}


class StateError(ValueError):
    """Raised when a task operation would violate the state contract."""


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def timestamp(value: datetime | None = None) -> str:
    return (value or now_utc()).astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_timestamp(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise StateError(f"invalid timestamp: {value}") from exc
    if parsed.tzinfo is None:
        raise StateError("timestamps must include a timezone")
    return parsed.astimezone(timezone.utc)


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise StateError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise StateError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise StateError(f"expected a JSON object: {path}")
    return value


def atomic_write(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def positive_integer(value: Any, label: str, *, allow_zero: bool = True) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise StateError(f"{label} must be an integer")
    if value < 0 or (value == 0 and not allow_zero):
        raise StateError(f"{label} must be positive")
    return value


def validate_contract(contract: dict[str, Any]) -> None:
    required = {
        "task_id",
        "objective",
        "responsible_agent",
        "budget",
        "retry_policy",
    }
    missing = required.difference(contract)
    if missing:
        raise StateError(f"contract missing fields: {', '.join(sorted(missing))}")
    if not isinstance(contract["task_id"], str) or not contract["task_id"]:
        raise StateError("contract task_id must be a non-empty string")
    budget = contract["budget"]
    if not isinstance(budget, dict):
        raise StateError("contract budget must be an object")
    for key, value in budget.items():
        if key in USAGE_KEYS or key == "max_wall_time_seconds":
            if value is not None:
                if key == "max_estimated_cost":
                    if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
                        raise StateError("budget.max_estimated_cost must be positive when set")
                else:
                    positive_integer(value, f"budget.{key}", allow_zero=False)
    retry_policy = contract["retry_policy"]
    if not isinstance(retry_policy, dict):
        raise StateError("contract retry_policy must be an object")
    retryable = retry_policy.get("retryable", [])
    if not isinstance(retryable, list) or not all(isinstance(item, str) for item in retryable):
        raise StateError("retry_policy.retryable must be a list of strings")
    positive_integer(retry_policy.get("max_attempts"), "retry_policy.max_attempts", allow_zero=False)
    if retry_policy.get("requires_new_evidence") is not True:
        raise StateError("retry_policy.requires_new_evidence must be true")
    for key in ("base_backoff_seconds", "max_backoff_seconds"):
        if key in retry_policy:
            positive_integer(retry_policy[key], f"retry_policy.{key}", allow_zero=False)
    if retry_policy.get("max_backoff_seconds", 60) < retry_policy.get("base_backoff_seconds", 1):
        raise StateError("retry_policy.max_backoff_seconds cannot be below base_backoff_seconds")


def initial_usage() -> dict[str, int | float]:
    return {
        "model_calls": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "subagents": 0,
        "estimated_cost": 0.0,
    }


def initial_state(contract: dict[str, Any], contract_path: Path, created_at: str) -> dict[str, Any]:
    state = {
        "schema_version": 1,
        "task_id": contract["task_id"],
        "contract_path": str(contract_path.resolve()),
        "objective": contract["objective"],
        "responsible_agent": contract["responsible_agent"],
        "quality_profile": contract.get("quality_profile"),
        "state": "created",
        "current_stage": None,
        "attempts": {},
        "retry_counts": {},
        "retry_history": [],
        "usage": initial_usage(),
        "limits": copy.deepcopy(contract["budget"]),
        "retry_policy": copy.deepcopy(contract["retry_policy"]),
        "artifacts": [],
        "evidence": [],
        "pending_approval": None,
        "failure": None,
        "started_at": None,
        "created_at": created_at,
        "updated_at": created_at,
        "checkpoints": [],
    }
    add_checkpoint(
        state,
        created_at=created_at,
        reason="task_initialized",
        next_action="start_authorized_stage",
    )
    return state


def add_checkpoint(
    state: dict[str, Any],
    *,
    created_at: str | None = None,
    reason: str,
    next_action: str,
    pending_approval: str | None = None,
) -> dict[str, Any]:
    checkpoint_id = f"cp-{len(state['checkpoints']) + 1:04d}"
    checkpoint = {
        "task_id": state["task_id"],
        "checkpoint_id": checkpoint_id,
        "created_at": created_at or timestamp(),
        "state": state["state"],
        "current_stage": state["current_stage"],
        "responsible_agent": state["responsible_agent"],
        "attempts": copy.deepcopy(state["attempts"]),
        "artifacts": copy.deepcopy(state["artifacts"]),
        "evidence": copy.deepcopy(state["evidence"]),
        "usage": copy.deepcopy(state["usage"]),
        "pending_approval": pending_approval if pending_approval is not None else state["pending_approval"],
        "next_action": next_action,
        "reason": reason,
    }
    state["checkpoints"].append(checkpoint)
    state["updated_at"] = checkpoint["created_at"]
    return checkpoint


def save_state(path: Path, state: dict[str, Any]) -> dict[str, Any]:
    atomic_write(path, state)
    return state


def load_state(path: Path) -> dict[str, Any]:
    state = load_object(path)
    required = {"schema_version", "task_id", "state", "checkpoints", "limits", "retry_policy"}
    missing = required.difference(state)
    if missing:
        raise StateError(f"state missing fields: {', '.join(sorted(missing))}")
    if state["state"] not in STATES:
        raise StateError(f"invalid state: {state['state']}")
    if not isinstance(state["checkpoints"], list) or not state["checkpoints"]:
        raise StateError("state must contain at least one checkpoint")
    return state


def action_time(args: argparse.Namespace) -> datetime:
    return parse_timestamp(args.now) if getattr(args, "now", None) else now_utc()


def stop_reason(state: dict[str, Any], current: datetime) -> str | None:
    if state["state"] in TERMINAL_STATES:
        return None
    started_at = state.get("started_at")
    max_wall = state["limits"].get("max_wall_time_seconds")
    if started_at and max_wall is not None:
        elapsed = (current - parse_timestamp(started_at)).total_seconds()
        if elapsed >= max_wall:
            return "wall_time_exceeded"
    for usage_key, limit_key in USAGE_KEYS.items():
        limit = state["limits"].get(limit_key)
        if limit is not None and state["usage"].get(usage_key, 0) >= limit:
            return f"{limit_key}_reached"
    return None


def timeout_state(state: dict[str, Any], reason: str, current: datetime, next_action: str) -> None:
    state["state"] = "timed_out"
    state["failure"] = {"type": reason, "recorded_at": timestamp(current)}
    state["pending_approval"] = None
    add_checkpoint(
        state,
        created_at=timestamp(current),
        reason=reason,
        next_action=next_action,
    )


def enforce_limits(state: dict[str, Any], current: datetime) -> bool:
    reason = stop_reason(state, current)
    if reason is None:
        return False
    timeout_state(state, reason, current, "escalate_to_checker_or_human")
    return True


def ensure_not_terminal(state: dict[str, Any]) -> None:
    if state["state"] in TERMINAL_STATES:
        raise StateError(f"task is terminal: {state['state']}")


def record_usage(state: dict[str, Any], values: dict[str, int | float], current: datetime) -> None:
    ensure_not_terminal(state)
    for key, value in values.items():
        if key not in USAGE_KEYS:
            raise StateError(f"unsupported usage field: {key}")
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
            raise StateError(f"usage.{key} must be a non-negative number")
        state["usage"][key] += value
    add_checkpoint(
        state,
        created_at=timestamp(current),
        reason="usage_recorded",
        next_action="continue_current_stage",
    )
    enforce_limits(state, current)


def append_values(target: list[str], values: list[str]) -> None:
    for value in values:
        if value and value not in target:
            target.append(value)


def transition(
    state: dict[str, Any],
    *,
    target: str,
    stage: str | None,
    agent: str | None,
    artifacts: list[str],
    evidence: list[str],
    reason: str | None,
    next_action: str,
    pending_approval: str | None,
    current: datetime,
) -> None:
    ensure_not_terminal(state)
    if target not in STATES:
        raise StateError(f"invalid target state: {target}")
    if target not in TRANSITIONS[state["state"]]:
        raise StateError(f"invalid transition: {state['state']} -> {target}")
    if target == "in_progress" and not stage:
        raise StateError("in_progress requires --stage")
    if (
        target == "in_progress"
        and stage in state["attempts"]
        and state["state"] in {"needs_review", "failed"}
    ):
        raise StateError("stage was already attempted; use retry with new evidence")
    if target == "completed" and not evidence:
        raise StateError("completed requires at least one acceptance evidence reference")
    if target in {"blocked", "failed", "cancelled", "timed_out", "needs_review"} and not reason:
        raise StateError(f"{target} requires --reason")
    if pending_approval and target != "blocked":
        raise StateError("pending approval may only be recorded on a blocked transition")
    if enforce_limits(state, current):
        raise StateError("task timed out before the requested transition")

    if target == "in_progress" and state.get("started_at") is None:
        state["started_at"] = timestamp(current)
    if agent:
        state["responsible_agent"] = agent
    if stage:
        state["current_stage"] = stage
        state["attempts"][stage] = max(1, int(state["attempts"].get(stage, 0)))
    state["state"] = target
    append_values(state["artifacts"], artifacts)
    append_values(state["evidence"], evidence)
    state["pending_approval"] = pending_approval
    if target in {"failed", "timed_out"}:
        state["failure"] = {"type": reason, "recorded_at": timestamp(current)}
    elif target not in TERMINAL_STATES:
        state["failure"] = None
    add_checkpoint(
        state,
        created_at=timestamp(current),
        reason=reason or f"transition_{target}",
        next_action=next_action,
        pending_approval=pending_approval,
    )


def retry_task(
    state: dict[str, Any],
    *,
    stage: str,
    failure_class: str,
    evidence: list[str],
    reason: str,
    current: datetime,
) -> None:
    ensure_not_terminal(state)
    if state["state"] not in {"in_progress", "needs_review", "failed"}:
        raise StateError(f"cannot retry from state: {state['state']}")
    if failure_class not in state["retry_policy"].get("retryable", []):
        raise StateError(f"failure is not retryable: {failure_class}")
    if state["retry_policy"].get("requires_new_evidence") and not evidence:
        raise StateError("retry requires new evidence")
    if enforce_limits(state, current):
        raise StateError("task timed out before the retry")

    attempts = int(state["attempts"].get(stage, 0))
    if attempts == 0:
        raise StateError(f"stage has not started: {stage}")
    retries = int(state["retry_counts"].get(stage, 0))
    max_attempts = int(state["retry_policy"]["max_attempts"])
    max_retries = state["limits"].get("max_retries_per_transition")
    if attempts >= max_attempts or (max_retries is not None and retries >= max_retries):
        timeout_state(state, "retry_budget_exceeded", current, "escalate_to_checker_or_human")
        return

    retry_number = retries + 1
    state["state"] = "in_progress"
    state["current_stage"] = stage
    state["attempts"][stage] = attempts + 1
    state["retry_counts"][stage] = retry_number
    base_backoff = int(state["retry_policy"].get("base_backoff_seconds", 1))
    max_backoff = int(state["retry_policy"].get("max_backoff_seconds", 60))
    backoff_seconds = min(max_backoff, base_backoff * (2 ** (retry_number - 1)))
    retry_record = {
        "stage": stage,
        "attempt": attempts + 1,
        "retry_number": retry_number,
        "failure_class": failure_class,
        "reason": reason,
        "new_evidence": copy.deepcopy(evidence),
        "backoff_seconds": backoff_seconds,
        "retry_not_before": timestamp(current + timedelta(seconds=backoff_seconds)),
        "recorded_at": timestamp(current),
    }
    state["retry_history"].append(retry_record)
    state["failure"] = {"type": failure_class, "recorded_at": timestamp(current)}
    append_values(state["evidence"], evidence)
    add_checkpoint(
        state,
        created_at=timestamp(current),
        reason=f"retry_{failure_class}",
        next_action=f"resume_stage_after_backoff:{stage}",
    )


def resume_task(
    state: dict[str, Any],
    *,
    stage: str,
    reason: str,
    agent: str | None,
    approval_decision: str | None,
    approved_by: str | None,
    approval_reason: str | None,
    current: datetime,
) -> None:
    source_state = state["state"]
    if source_state not in {"needs_review", "blocked", "failed", "timed_out"}:
        raise StateError(f"task is not waiting for recovery: {source_state}")
    pending = state.get("pending_approval")
    if pending and approval_decision != "approved":
        raise StateError(f"approval required before resume: {pending}")
    if source_state == "timed_out" and approval_decision != "approved":
        raise StateError("timed_out tasks require explicit approval to resume")
    if approval_decision:
        if approval_decision not in {"approved", "rejected"}:
            raise StateError("approval decision must be approved or rejected")
        if not approved_by:
            raise StateError("approved_by is required when recording an approval decision")
        if approval_decision == "rejected":
            state["state"] = "cancelled"
            state["failure"] = {"type": "approval_rejected", "recorded_at": timestamp(current)}
            state["pending_approval"] = None
            add_checkpoint(
                state,
                created_at=timestamp(current),
                reason=approval_reason or "approval_rejected",
                next_action="stop",
            )
            return
        state["approval"] = {
            "decision": approval_decision,
            "approved_by": approved_by,
            "reason": approval_reason or reason,
            "recorded_at": timestamp(current),
        }
    if enforce_limits(state, current):
        raise StateError("task timed out before resume")
    state["state"] = "in_progress"
    state["current_stage"] = stage
    state["attempts"][stage] = max(1, int(state["attempts"].get(stage, 0)))
    state["responsible_agent"] = agent or state["responsible_agent"]
    state["pending_approval"] = None
    state["failure"] = None
    add_checkpoint(
        state,
        created_at=timestamp(current),
        reason=f"resume_from_{source_state}:{reason}",
        next_action=f"continue_stage:{stage}",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="create a task state and initial checkpoint")
    init.add_argument("--contract", type=Path, required=True)
    init.add_argument("--state", type=Path, required=True)
    init.add_argument("--now")

    show = commands.add_parser("show", help="print the durable state")
    show.add_argument("--state", type=Path, required=True)

    transition_parser = commands.add_parser("transition", help="record a state transition")
    transition_parser.add_argument("--state", type=Path, required=True)
    transition_parser.add_argument("--to", required=True)
    transition_parser.add_argument("--stage")
    transition_parser.add_argument("--agent")
    transition_parser.add_argument("--artifact", action="append", default=[])
    transition_parser.add_argument("--evidence", action="append", default=[])
    transition_parser.add_argument("--reason")
    transition_parser.add_argument("--next-action", default="continue_declared_workflow")
    transition_parser.add_argument("--pending-approval")
    transition_parser.add_argument("--now")

    retry = commands.add_parser("retry", help="retry a classified failure")
    retry.add_argument("--state", type=Path, required=True)
    retry.add_argument("--stage", required=True)
    retry.add_argument("--failure-class", required=True)
    retry.add_argument("--evidence", action="append", default=[])
    retry.add_argument("--reason", required=True)
    retry.add_argument("--now")

    resume = commands.add_parser("resume", help="resume from a checkpoint")
    resume.add_argument("--state", type=Path, required=True)
    resume.add_argument("--stage", required=True)
    resume.add_argument("--reason", required=True)
    resume.add_argument("--agent")
    resume.add_argument("--approval-decision", choices=["approved", "rejected"])
    resume.add_argument("--approved-by")
    resume.add_argument("--approval-reason")
    resume.add_argument("--now")

    usage = commands.add_parser("usage", help="record runtime usage and enforce limits")
    usage.add_argument("--state", type=Path, required=True)
    usage.add_argument("--model-calls", type=int, default=0)
    usage.add_argument("--input-tokens", type=int, default=0)
    usage.add_argument("--output-tokens", type=int, default=0)
    usage.add_argument("--subagents", type=int, default=0)
    usage.add_argument("--estimated-cost", type=float, default=0.0)
    usage.add_argument("--now")

    cancel = commands.add_parser("cancel", help="stop a non-terminal task")
    cancel.add_argument("--state", type=Path, required=True)
    cancel.add_argument("--reason", required=True)
    cancel.add_argument("--now")
    return parser


def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.command == "init":
        contract = load_object(args.contract)
        validate_contract(contract)
        if args.state.exists():
            raise StateError(f"state already exists: {args.state}")
        current = parse_timestamp(args.now) if args.now else now_utc()
        state = initial_state(contract, args.contract, timestamp(current))
        return save_state(args.state, state)

    state = load_state(args.state)
    current = action_time(args)
    if args.command == "show":
        return state
    if args.command == "transition":
        transition(
            state,
            target=args.to,
            stage=args.stage,
            agent=args.agent,
            artifacts=args.artifact,
            evidence=args.evidence,
            reason=args.reason,
            next_action=args.next_action,
            pending_approval=args.pending_approval,
            current=current,
        )
    elif args.command == "retry":
        retry_task(
            state,
            stage=args.stage,
            failure_class=args.failure_class,
            evidence=args.evidence,
            reason=args.reason,
            current=current,
        )
    elif args.command == "resume":
        resume_task(
            state,
            stage=args.stage,
            reason=args.reason,
            agent=args.agent,
            approval_decision=args.approval_decision,
            approved_by=args.approved_by,
            approval_reason=args.approval_reason,
            current=current,
        )
    elif args.command == "usage":
        values = {
            "model_calls": args.model_calls,
            "input_tokens": args.input_tokens,
            "output_tokens": args.output_tokens,
            "subagents": args.subagents,
            "estimated_cost": args.estimated_cost,
        }
        record_usage(state, values, current)
    elif args.command == "cancel":
        transition(
            state,
            target="cancelled",
            stage=None,
            agent=None,
            artifacts=[],
            evidence=[],
            reason=args.reason,
            next_action="stop",
            pending_approval=None,
            current=current,
        )
    else:
        raise StateError(f"unsupported command: {args.command}")
    return save_state(args.state, state)


def main() -> int:
    args = build_parser().parse_args()
    try:
        result = run(args)
    except (OSError, StateError) as exc:
        print(f"task-state=failed reason={exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
