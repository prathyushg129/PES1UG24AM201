"""Check saved coverage counts; optionally supply fresh code/branch JSON paths."""

import json
from pathlib import Path
import sys


def check(path, branches=False):
    report = json.loads(path.read_text(encoding="utf-8"))
    if list(report["files"]) != ["parking_fee.py"]:
        raise SystemExit(f"Unexpected coverage scope in {path}")
    summary = report["files"]["parking_fee.py"]["summary"]
    statements = 100 * summary["covered_lines"] / summary["num_statements"]
    print(f"{path.name}: statements {summary['covered_lines']}/{summary['num_statements']} = {statements:.2f}%")
    if statements < 90:
        raise SystemExit("Statement coverage is below 90%")
    if branches:
        if not summary.get("num_branches"):
            raise SystemExit("No measured branches; rerun with --branch")
        percent = 100 * summary["covered_branches"] / summary["num_branches"]
        print(f"{path.name}: branches {summary['covered_branches']}/{summary['num_branches']} = {percent:.2f}%")
        if percent < 90:
            raise SystemExit("Branch coverage is below 90%")


if __name__ == "__main__":
    base = Path(__file__).resolve().parent
    if len(sys.argv) == 1:
        code_path, branch_path = base / "code_coverage.json", base / "branch_coverage.json"
    elif len(sys.argv) == 3:
        code_path, branch_path = map(Path, sys.argv[1:])
    else:
        raise SystemExit("Usage: python verify_metrics.py [code.json branch.json]")
    check(code_path)
    check(branch_path, branches=True)
    print("PASS: both suites independently meet the 90% thresholds.")
