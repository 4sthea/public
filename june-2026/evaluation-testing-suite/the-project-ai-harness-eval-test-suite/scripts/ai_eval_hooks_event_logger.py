#!/usr/bin/env python3
"""Minimal VS Code/Copilot hook event logger for eval/debug mode.

Usage from a hook command:
  python scripts/ai_eval_hooks_event_logger.py

It reads hook JSON from stdin and appends one JSONL event to:
  docs/tmp/ai-evals/events/hooks.jsonl

This script intentionally redacts common secret-looking fields.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SECRET_PAT = re.compile(r'(api[_-]?key|token|secret|password|authorization)', re.I)


def redact(obj: Any) -> Any:
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if SECRET_PAT.search(str(k)):
                out[k] = '<redacted>'
            else:
                out[k] = redact(v)
        return out
    if isinstance(obj, list):
        return [redact(v) for v in obj]
    if isinstance(obj, str) and len(obj) > 5000:
        return obj[:5000] + '...<truncated>'
    return obj


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception as exc:
        event = {'parse_error': str(exc), 'raw': sys.stdin.read()[:2000]}

    safe = redact(event)
    safe['_logged_at'] = datetime.now(timezone.utc).isoformat()
    safe['_eval_experiment_id'] = os.environ.get('THE_PROJECT_AI_EVAL_EXPERIMENT_ID', 'manual')
    safe['_eval_variant'] = os.environ.get('THE_PROJECT_AI_EVAL_VARIANT', 'unknown')
    safe['_eval_task_id'] = os.environ.get('THE_PROJECT_AI_EVAL_TASK_ID', 'unknown')

    out = Path('docs/tmp/ai-evals/events/hooks.jsonl')
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('a', encoding='utf-8') as f:
        f.write(json.dumps(safe, ensure_ascii=False) + '\n')

    print(json.dumps({'continue': True}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
