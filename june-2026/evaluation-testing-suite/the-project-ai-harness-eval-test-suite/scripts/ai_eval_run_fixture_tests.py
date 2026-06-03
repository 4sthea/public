#!/usr/bin/env python3
"""Run the controlled Python fixture tests."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    fixture_dir = root / '.github' / 'evals' / 'fixtures' / 'python'
    cmd = [sys.executable, '-m', 'unittest', 'discover', '-s', str(fixture_dir), '-p', 'test_*.py']
    print('Running:', ' '.join(cmd))
    return subprocess.call(cmd, cwd=str(fixture_dir))


if __name__ == '__main__':
    raise SystemExit(main())
