#!/usr/bin/env python3
"""Aggregate bug-fixing results from all languages into a single report."""

import json
import os
import sys
from datetime import datetime


def aggregate_results(results_dir: str) -> dict:
    """Aggregate results from all language evaluators."""
    aggregated = {
        "timestamp": datetime.now().isoformat(),
        "languages": {},
        "overall": {"total_scenarios": 0, "total_passed": 0, "total_failed": 0},
    }

    for lang in ["python", "java", "typescript"]:
        result_file = os.path.join(results_dir, f"{lang}_results.json")
        if os.path.isfile(result_file):
            with open(result_file) as f:
                aggregated["languages"][lang] = json.load(f)
        else:
            aggregated["languages"][lang] = {"status": "not_run"}

    for lang, data in aggregated["languages"].items():
        if "passed" in data:
            aggregated["overall"]["total_scenarios"] += data.get("total", 0)
            aggregated["overall"]["total_passed"] += data.get("passed", 0)
            aggregated["overall"]["total_failed"] += data.get("failed", 0)

    total = aggregated["overall"]["total_scenarios"]
    passed = aggregated["overall"]["total_passed"]
    aggregated["overall"]["pass_rate"] = round(passed / total * 100, 2) if total > 0 else 0

    return aggregated


def main():
    results_dir = sys.argv[1] if len(sys.argv) > 1 else "data"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "data/aggregated_report.json"

    report = aggregate_results(results_dir)

    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Report written to {output_file}")
    print(f"Overall pass rate: {report['overall']['pass_rate']}%")


if __name__ == "__main__":
    main()
