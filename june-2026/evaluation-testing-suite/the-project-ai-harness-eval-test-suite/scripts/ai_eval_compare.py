#!/usr/bin/env python3
"""Compare baseline vs candidate output for one task.

This script performs deterministic checks and renders a pairwise judge prompt.
It does not call an LLM. Paste the judge prompt into your chosen judge model or Promptfoo.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
from pathlib import Path
from typing import Any

from ai_eval_score import build_checks, words


def pass_rate(checks):
    return sum(1 for c in checks if c.passed) / (len(checks) or 1)


def missing(checks):
    return [c.name for c in checks if not c.passed]


def load(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def render_judge_prompt(task: dict[str, Any], baseline: str, candidate: str) -> str:
    template_path = Path('.github/evals/prompts/pairwise-judge-template.md')
    rubric_path = Path('.github/evals/rubrics/semantic-regression-pairwise.rubric.md')
    template = template_path.read_text(encoding='utf-8') if template_path.exists() else '{{task_json}}\n{{baseline_output}}\n{{candidate_output}}\n{{rubric}}'
    rubric = rubric_path.read_text(encoding='utf-8') if rubric_path.exists() else task.get('pairwise_rubric', '')
    return (template
            .replace('{{task_json}}', json.dumps(task, indent=2, ensure_ascii=False))
            .replace('{{baseline_output}}', baseline[:20000])
            .replace('{{candidate_output}}', candidate[:20000])
            .replace('{{rubric}}', rubric))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--task', required=True)
    ap.add_argument('--baseline', required=True)
    ap.add_argument('--candidate', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    task = json.loads(load(Path(args.task)))
    baseline = load(Path(args.baseline))
    candidate = load(Path(args.candidate))

    b_checks = build_checks(task, baseline, run_validation_commands=False)
    c_checks = build_checks(task, candidate, run_validation_commands=False)
    b_rate = pass_rate(b_checks)
    c_rate = pass_rate(c_checks)

    b_missing = set(missing(b_checks))
    c_missing = set(missing(c_checks))
    newly_missing = sorted(c_missing - b_missing)
    newly_fixed = sorted(b_missing - c_missing)

    b_wc = len(words(baseline))
    c_wc = len(words(candidate))
    diff = '\n'.join(difflib.unified_diff(
        baseline.splitlines(), candidate.splitlines(),
        fromfile='baseline', tofile='candidate', lineterm=''
    ))
    diff_excerpt = diff[:8000]

    if newly_missing:
        verdict = 'FAIL'
    elif c_rate < b_rate:
        verdict = 'FAIL'
    elif c_rate == 1.0 and c_rate >= b_rate:
        verdict = 'INCONCLUSIVE'  # semantic judge still needed
    else:
        verdict = 'INCONCLUSIVE'

    judge_prompt = render_judge_prompt(task, baseline, candidate)

    report = f"""# AI Eval Comparison Report

## Task

- ID: `{task['id']}`
- Title: {task.get('title', '')}

## Deterministic Summary

| Metric | Baseline | Candidate | Delta |
|---|---:|---:|---:|
| Pass rate | {b_rate:.2%} | {c_rate:.2%} | {(c_rate-b_rate):+.2%} |
| Word count | {b_wc} | {c_wc} | {c_wc-b_wc:+d} |
| Missing checks | {len(b_missing)} | {len(c_missing)} | {len(c_missing)-len(b_missing):+d} |

## Newly Missing Checks

{chr(10).join('- ' + x for x in newly_missing) if newly_missing else 'None.'}

## Newly Fixed Checks

{chr(10).join('- ' + x for x in newly_fixed) if newly_fixed else 'None.'}

## Deterministic Verdict

`{verdict}`

Deterministic scoring cannot prove semantic equivalence. Use the pairwise judge prompt below for the final semantic verdict.

## Diff Excerpt

```diff
{diff_excerpt}
```

## Pairwise Semantic Judge Prompt

```markdown
{judge_prompt}
```
"""

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding='utf-8')
    print(f'Wrote {out}')
    return 0 if verdict != 'FAIL' else 1


if __name__ == '__main__':
    raise SystemExit(main())
