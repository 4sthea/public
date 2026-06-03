#!/usr/bin/env python3
"""Aggregate trial-result JSON files into a Markdown summary."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--results-glob', required=True, help='Example: docs/tmp/ai-evals/runs/manual/**/*.json')
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    files = sorted(Path().glob(args.results_glob))
    rows = []
    for p in files:
        try:
            data = json.loads(p.read_text(encoding='utf-8'))
        except Exception:
            continue
        if 'task_id' not in data:
            continue
        rows.append(data)

    total = len(rows)
    passed = sum(1 for r in rows if r.get('pass'))
    avg_score = sum(float(r.get('score', 0.0)) for r in rows) / (total or 1)

    lines = ['# AI Eval Aggregate Report', '', f'- Results: {total}', f'- Passed: {passed}', f'- Pass rate: {(passed/(total or 1)):.2%}', f'- Average score: {avg_score:.3f}', '', '| Task | Variant | Trial | Pass | Score |', '|---|---|---:|---:|---:|']
    for r in rows:
        lines.append(f"| `{r.get('task_id')}` | {r.get('variant')} | {r.get('trial')} | {r.get('pass')} | {r.get('score')} |")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Wrote {out}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
