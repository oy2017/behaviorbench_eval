#!/usr/bin/env python3
"""Print the saved results using BehaviorBench's OWN renderer.

This deliberately contains no metric logic. It loads each saved JSON, rebuilds
the program's ``EvaluationResult`` objects, and calls the program's own
``.summary()`` — the same method ``behaviorbench-eval`` calls to print results
to the console during a run (main.py:208).

So the output below is what the program itself reports: every metric key, every
metadata key, verbatim. Nothing is selected, averaged, or reformatted here.

Usage:
    uv run python outputs/openrouter/show_results.py > RESULTS.txt
"""
import glob
import json
import os
import sys

from behaviorbench.eval.base import EvaluationResult

RAW_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tencent", "hy3")


def main():
    files = sorted(glob.glob(os.path.join(RAW_DIR, "*.json")))
    if not files:
        sys.exit(f"no result JSONs found in {RAW_DIR}")

    n_tasks = 0
    for path in files:
        blob = json.load(open(path))
        print("=" * 78)
        print(f"FILE: {os.path.basename(path)}")
        print(f"run at: {blob.get('timestamp', '?')}")
        settings = blob.get("inference_settings")
        if settings:
            print(f"inference settings: {json.dumps(settings)}")
        print("=" * 78)
        for task in blob["tasks"]:
            result = EvaluationResult(
                task_name=task["task_name"],
                metrics=task.get("metrics", {}),
                metadata=task.get("metadata", {}),
            )
            print(result.summary())   # <- the program's own rendering
            print()
            n_tasks += 1

    print("=" * 78)
    print(f"{len(files)} result files, {n_tasks} tasks")


if __name__ == "__main__":
    main()
