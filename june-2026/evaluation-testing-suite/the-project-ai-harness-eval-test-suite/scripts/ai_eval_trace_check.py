#!/usr/bin/env python3
"""Check whether a trace contains essential milestones in order.

This is a lightweight substitute for full dominator analysis.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def is_subsequence(required: list[str], actual: list[str]) -> tuple[bool, list[str]]:
    idx = 0
    missing: list[str] = []
    for req in required:
        found = False
        while idx < len(actual):
            if actual[idx] == req:
                found = True
                idx += 1
                break
            idx += 1
        if not found:
            missing.append(req)
    return not missing, missing


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--trace', required=True)
    ap.add_argument('--required', nargs='+', required=True, help='Required states in order')
    args = ap.parse_args()

    data = json.loads(Path(args.trace).read_text(encoding='utf-8'))
    states = data.get('states', [])
    ok, missing = is_subsequence(args.required, states)
    result = {
        'trace': args.trace,
        'pass': ok,
        'coverage': (len(args.required) - len(missing)) / (len(args.required) or 1),
        'required': args.required,
        'states': states,
        'missing': missing,
    }
    print(json.dumps(result, indent=2))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
