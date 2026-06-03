#!/usr/bin/env python3
"""Render a the project AI-eval task prompt for manual use with an agent."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True, help="Path to task JSON")
    ap.add_argument("--variant", required=True, choices=["baseline", "candidate", "comparison"])
    ap.add_argument("--trial", required=True, type=int)
    ap.add_argument("--template", default=".github/evals/prompts/run-task-template.md")
    args = ap.parse_args()

    task_path = Path(args.task)
    task = json.loads(load_text(task_path))
    template = load_text(Path(args.template))
    output_path = task["variant_safe_output_path"].replace("{variant}", args.variant).replace("{trial}", f"{args.trial:02d}")

    rendered = template
    rendered = rendered.replace("{{task_id}}", task["id"])
    rendered = rendered.replace("{{variant}}", args.variant)
    rendered = rendered.replace("{{trial}}", str(args.trial))
    rendered = rendered.replace("{{output_path}}", output_path)
    rendered = rendered.replace("{{task_prompt}}", task["prompt"])
    rendered = rendered.replace("{{acceptance_criteria}}", "\n".join(f"- {c}" for c in task.get("acceptance_criteria", [])))
    rendered = rendered.replace("{{deterministic_checks}}", json.dumps(task.get("deterministic_checks", {}), indent=2, ensure_ascii=False))

    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
