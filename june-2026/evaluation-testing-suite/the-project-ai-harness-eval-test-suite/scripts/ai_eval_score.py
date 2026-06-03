#!/usr/bin/env python3
"""Deterministically score a the project AI-eval output file.

No external dependencies. This is intentionally simple and explainable.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str
    weight: float = 1.0


def words(text: str) -> list[str]:
    return re.findall(r"\b\S+\b", text)


def heading_present(text: str, heading: str) -> bool:
    pattern = re.compile(rf"^\s*#+\s+.*{re.escape(heading)}.*$", re.IGNORECASE | re.MULTILINE)
    return bool(pattern.search(text))


def contains_ci(text: str, needle: str) -> bool:
    return needle.lower() in text.lower()


def run_command(cmd: str) -> tuple[bool, str]:
    try:
        completed = subprocess.run(cmd, shell=True, text=True, capture_output=True, timeout=120)
        output = (completed.stdout + "\n" + completed.stderr).strip()
        return completed.returncode == 0, output[-4000:]
    except Exception as exc:  # defensive; eval scorer should not crash without report
        return False, f"{type(exc).__name__}: {exc}"


def build_checks(task: dict[str, Any], output_text: str, run_validation_commands: bool) -> list[CheckResult]:
    cfg = task.get("deterministic_checks", {})
    checks: list[CheckResult] = []

    for h in cfg.get("required_headings", []):
        checks.append(CheckResult(f"required_heading:{h}", heading_present(output_text, h), f"Heading required: {h}"))

    for s in cfg.get("required_strings", []):
        checks.append(CheckResult(f"required_string:{s}", contains_ci(output_text, s), f"String required: {s}"))

    for pat in cfg.get("required_regex", []):
        ok = bool(re.search(pat, output_text, flags=re.MULTILINE | re.IGNORECASE))
        checks.append(CheckResult(f"required_regex:{pat}", ok, f"Regex required: {pat}"))

    for s in cfg.get("forbidden_strings", []):
        checks.append(CheckResult(f"forbidden_string:{s}", not contains_ci(output_text, s), f"Forbidden string absent: {s}"))

    for pat in cfg.get("forbidden_regex", []):
        ok = not bool(re.search(pat, output_text, flags=re.MULTILINE | re.IGNORECASE))
        checks.append(CheckResult(f"forbidden_regex:{pat}", ok, f"Forbidden regex absent: {pat}"))

    wc = len(words(output_text))
    if "min_word_count" in cfg:
        checks.append(CheckResult("min_word_count", wc >= int(cfg["min_word_count"]), f"word_count={wc}, min={cfg['min_word_count']}"))
    if "max_word_count" in cfg:
        checks.append(CheckResult("max_word_count", wc <= int(cfg["max_word_count"]), f"word_count={wc}, max={cfg['max_word_count']}"))

    if cfg.get("must_include_evidence_labels"):
        has_label = any(label in output_text for label in ["FACT:", "ASSUMPTION:", "UNVERIFIED:"])
        checks.append(CheckResult("evidence_labels", has_label, "Requires FACT/ASSUMPTION/UNVERIFIED labels"))

    if cfg.get("must_not_claim_unverified_repo_facts"):
        suspicious = [
            "fully verified",
            "I verified the repository",
            "the codebase contains",
            "all tests pass",
            "production-ready",
        ]
        hits = [s for s in suspicious if contains_ci(output_text, s)]
        checks.append(CheckResult("no_unverified_repo_claims", len(hits) == 0, f"Suspicious claims: {hits}"))

    if run_validation_commands:
        for cmd in cfg.get("validation_commands", []):
            ok, out = run_command(cmd)
            checks.append(CheckResult(f"validation_command:{cmd}", ok, out, weight=2.0))

    return checks


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--variant", required=True)
    ap.add_argument("--trial", required=True, type=int)
    ap.add_argument("--out", required=True)
    ap.add_argument("--run-validation-commands", action="store_true", help="Run task validation commands. Off by default for safe scoring.")
    args = ap.parse_args()

    task = json.loads(Path(args.task).read_text(encoding="utf-8"))
    output_path = Path(args.output)
    if not output_path.exists():
        raise SystemExit(f"Output file not found: {output_path}")
    output_text = output_path.read_text(encoding="utf-8", errors="replace")

    checks = build_checks(task, output_text, args.run_validation_commands)
    total_weight = sum(c.weight for c in checks) or 1.0
    earned = sum(c.weight for c in checks if c.passed)
    score = earned / total_weight
    passed = all(c.passed for c in checks)

    result = {
        "task_id": task["id"],
        "variant": args.variant,
        "trial": args.trial,
        "output_path": str(output_path),
        "pass": passed,
        "score": round(score, 4),
        "checks": [asdict(c) for c in checks],
        "metadata": {
            "word_count": len(words(output_text)),
            "check_count": len(checks),
        },
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
