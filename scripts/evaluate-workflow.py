"""Validate and score file-backed AI-DEV-TEAM workflow evaluations."""

from __future__ import annotations

import argparse
import json
import sys
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


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return value


def validate_benchmark(benchmark: dict[str, Any]) -> dict[str, dict[str, Any]]:
    required = {"benchmark_id", "version", "rubric", "tasks"}
    missing = required.difference(benchmark)
    if missing:
        raise ValueError(f"benchmark missing fields: {', '.join(sorted(missing))}")

    rubric = benchmark["rubric"]
    if not isinstance(rubric, dict):
        raise ValueError("benchmark rubric must be an object")
    dimensions = rubric.get("dimensions")
    if not isinstance(dimensions, list) or not dimensions:
        raise ValueError("benchmark rubric dimensions must be a non-empty list")
    if rubric.get("acceptance_criteria", {}).get("max_points") != 40:
        raise ValueError("acceptance_criteria max_points must be 40 in v1")

    tasks = benchmark["tasks"]
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("benchmark tasks must be a non-empty list")

    by_id: dict[str, dict[str, Any]] = {}
    for task in tasks:
        if not isinstance(task, dict):
            raise ValueError("each benchmark task must be an object")
        task_id = task.get("task_id")
        if not isinstance(task_id, str) or not task_id:
            raise ValueError("each benchmark task needs a non-empty task_id")
        if task_id in by_id:
            raise ValueError(f"duplicate benchmark task_id: {task_id}")
        if task.get("expected_state") not in STATES:
            raise ValueError(f"invalid expected_state for {task_id}")
        criteria = task.get("criteria")
        if not isinstance(criteria, list) or not criteria:
            raise ValueError(f"task {task_id} needs at least one criterion")
        criterion_ids: set[str] = set()
        for criterion in criteria:
            if not isinstance(criterion, dict):
                raise ValueError(f"task {task_id} has an invalid criterion")
            criterion_id = criterion.get("id")
            if not isinstance(criterion_id, str) or not criterion_id:
                raise ValueError(f"task {task_id} has a criterion without an id")
            if criterion_id in criterion_ids:
                raise ValueError(f"task {task_id} has duplicate criterion {criterion_id}")
            criterion_ids.add(criterion_id)
        by_id[task_id] = task
    return by_id


def score_result(result: dict[str, Any], tasks: dict[str, dict[str, Any]]) -> dict[str, Any]:
    result_tasks = result.get("tasks")
    if not isinstance(result_tasks, list) or not result_tasks:
        raise ValueError("result tasks must be a non-empty list")

    dimensions = [
        "scope_adherence",
        "evidence_quality",
        "security_boundary_compliance",
        "test_quality",
        "handoff_quality",
        "cost_latency_efficiency",
    ]
    scores: list[dict[str, Any]] = []
    seen: set[str] = set()

    for observed in result_tasks:
        if not isinstance(observed, dict):
            raise ValueError("each result task must be an object")
        task_id = observed.get("task_id")
        if task_id not in tasks:
            raise ValueError(f"result contains unknown task_id: {task_id}")
        if task_id in seen:
            raise ValueError(f"result contains duplicate task_id: {task_id}")
        seen.add(task_id)
        expected = tasks[task_id]
        if observed.get("state") not in STATES:
            raise ValueError(f"invalid observed state for {task_id}")

        criterion_results = observed.get("criterion_results")
        if not isinstance(criterion_results, list):
            raise ValueError(f"task {task_id} needs criterion_results")
        by_criterion = {item.get("id"): item for item in criterion_results if isinstance(item, dict)}
        expected_ids = {item["id"] for item in expected["criteria"]}
        if set(by_criterion) != expected_ids:
            raise ValueError(f"task {task_id} criterion_results do not match the benchmark")
        passed = sum(1 for item in by_criterion.values() if item.get("passed") is True)
        criteria_points = (passed / len(expected_ids)) * 40

        raw_scores = observed.get("scores")
        if not isinstance(raw_scores, dict):
            raise ValueError(f"task {task_id} needs scores")
        dimension_points = 0.0
        for dimension in dimensions:
            value = raw_scores.get(dimension)
            if not isinstance(value, int) or isinstance(value, bool) or value not in (0, 1, 2):
                raise ValueError(f"task {task_id} score {dimension} must be 0, 1, or 2")
            dimension_points += value * 5

        score = round(criteria_points + dimension_points, 2)
        scores.append(
            {
                "task_id": task_id,
                "expected_state": expected["expected_state"],
                "observed_state": observed["state"],
                "state_match": observed["state"] == expected["expected_state"],
                "criteria_passed": passed,
                "criteria_total": len(expected_ids),
                "score": score,
            }
        )

    missing_tasks = set(tasks).difference(seen)
    if missing_tasks:
        raise ValueError(f"result is missing tasks: {', '.join(sorted(missing_tasks))}")

    total = round(sum(item["score"] for item in scores) / len(scores), 2)
    state_matches = sum(1 for item in scores if item["state_match"])
    return {
        "benchmark_id": result.get("benchmark_id"),
        "label": result.get("label"),
        "task_count": len(scores),
        "average_score": total,
        "state_matches": state_matches,
        "state_match_rate": round(state_matches / len(scores), 3),
        "tasks": scores,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark", type=Path, required=True)
    parser.add_argument("--result", type=Path)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--label", default="candidate")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()

    try:
        benchmark = load_json(args.benchmark)
        tasks = validate_benchmark(benchmark)
        print(f"benchmark=valid id={benchmark['benchmark_id']} tasks={len(tasks)}")
        if args.validate_only:
            return 0
        if args.result is None:
            raise ValueError("--result is required unless --validate-only is used")

        result = load_json(args.result)
        result.setdefault("label", args.label)
        scored = score_result(result, tasks)
        print(json.dumps(scored, indent=2, ensure_ascii=False))

        if args.baseline:
            baseline = load_json(args.baseline)
            baseline.setdefault("label", "baseline")
            baseline_score = score_result(baseline, tasks)
            delta = round(scored["average_score"] - baseline_score["average_score"], 2)
            print(json.dumps({"baseline_average_score": baseline_score["average_score"], "delta": delta}, indent=2))
        return 0
    except ValueError as exc:
        print(f"evaluation=failed reason={exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
