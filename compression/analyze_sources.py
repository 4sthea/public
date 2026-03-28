#!/usr/bin/env python3
"""
Tiny analyzer for a distillation skill.

Goals
- resolve files recursively
- skip noisy directories
- estimate token volume
- detect likely semantic groupings
- recommend single vs split mode
- emit a compact Markdown report

Works on Windows and macOS with Python 3.9+ and only uses the standard library.

Usage examples
  python analyze_sources.py docs/
  python analyze_sources.py docs/ specs/*.md --json
  python analyze_sources.py . --max-files 200 --output analysis.md
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List, Dict, Tuple


SUPPORTED_EXTS = {
    ".md",
    ".txt",
    ".rst",
    ".yaml",
    ".yml",
    ".json",
}

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".idea",
    ".cursor",
    ".vscode",
    ".claude",
    "_bmad-output",
    "dist",
    "build",
    "coverage",
    ".next",
    ".turbo",
    ".pytest_cache",
}

ROLE_PATTERNS = [
    ("spec", re.compile(r"(spec|requirements|prd|feature|user-story)", re.I)),
    ("architecture", re.compile(r"(adr|architecture|arch|design)", re.I)),
    ("research", re.compile(r"(research|discovery|analysis|notes|findings)", re.I)),
    ("implementation", re.compile(r"(implementation|impl|plan|approach)", re.I)),
    ("testing", re.compile(r"(test|qa|verification|validation)", re.I)),
    ("operations", re.compile(r"(ops|runbook|incident|deploy|observability)", re.I)),
    ("appendix", re.compile(r"(appendix|annex|supplement)", re.I)),
    ("readme", re.compile(r"(^readme$)", re.I)),
    ("changelog", re.compile(r"(changelog|history|release-notes)", re.I)),
]

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.M)
WORD_RE = re.compile(r"\b[\w\-/.:]{2,}\b", re.U)
NUMBER_RE = re.compile(r"\b\d[\d,._%/-]*\b")
TABLEISH_RE = re.compile(r"(\t)|(\|.+\|)|(^\s*[-+|]+\s*$)", re.M)


@dataclass
class FileStat:
    path: str
    role: str
    chars: int
    words: int
    token_estimate: int
    headings: int
    numbers: int
    tableish_lines: int
    top_headings: List[str]
    relative_dir: str


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def estimate_tokens(text: str) -> int:
    # Simple, stable heuristic for English-ish technical text.
    # Good enough for routing, not billing.
    return max(1, math.ceil(len(text) / 4))


def safe_read_text(path: Path) -> str:
    encodings = ("utf-8", "utf-8-sig", "cp1252", "latin-1")
    for enc in encodings:
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
        except OSError:
            break
    return ""


def should_skip_dir(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def iter_candidate_files(inputs: Iterable[str]) -> Iterable[Path]:
    seen: set[Path] = set()

    for raw in inputs:
        p = Path(raw)

        # Glob handling
        if any(ch in raw for ch in "*?[]"):
            for match in Path().glob(raw):
                if match.is_file():
                    rp = match.resolve()
                    if rp not in seen and match.suffix.lower() in SUPPORTED_EXTS:
                        seen.add(rp)
                        yield rp
            continue

        if p.is_file():
            if p.suffix.lower() in SUPPORTED_EXTS:
                rp = p.resolve()
                if rp not in seen:
                    seen.add(rp)
                    yield rp
            continue

        if p.is_dir():
            for root, dirs, files in os.walk(p):
                root_path = Path(root)
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                if should_skip_dir(root_path):
                    continue
                for name in files:
                    fp = root_path / name
                    if fp.suffix.lower() in SUPPORTED_EXTS:
                        rp = fp.resolve()
                        if rp not in seen:
                            seen.add(rp)
                            yield rp


def detect_role(path: Path) -> str:
    stem = path.stem
    rel = str(path).replace("\\", "/")
    for role, rx in ROLE_PATTERNS:
        if rx.search(stem) or rx.search(rel):
            return role
    return "general"


def relative_dir(path: Path, root: Path) -> str:
    try:
        parent = path.parent.resolve().relative_to(root.resolve())
        s = str(parent).replace("\\", "/")
        return s if s else "."
    except Exception:
        return str(path.parent).replace("\\", "/")


def top_headings(text: str, limit: int = 6) -> List[str]:
    return [m.group(2).strip() for m in HEADING_RE.finditer(text)][:limit]


def analyze_file(path: Path, root: Path) -> FileStat:
    text = safe_read_text(path)
    words = len(WORD_RE.findall(text))
    headings = len(HEADING_RE.findall(text))
    nums = len(NUMBER_RE.findall(text))
    tableish = len(TABLEISH_RE.findall(text))

    return FileStat(
        path=str(path).replace("\\", "/"),
        role=detect_role(path),
        chars=len(text),
        words=words,
        token_estimate=estimate_tokens(text),
        headings=headings,
        numbers=nums,
        tableish_lines=tableish,
        top_headings=top_headings(text),
        relative_dir=relative_dir(path, root),
    )


def choose_root(paths: List[Path]) -> Path:
    if not paths:
        return Path(".").resolve()
    common = os.path.commonpath([str(p.resolve()) for p in paths])
    common_path = Path(common)
    return common_path if common_path.is_dir() else common_path.parent


def group_key(fs: FileStat) -> str:
    # Prefer semantic grouping by directory and role.
    if fs.relative_dir != ".":
        return f"{fs.relative_dir} :: {fs.role}"
    return fs.role


def recommend_mode(file_count: int, source_tokens: int, estimated_output_tokens: int) -> Tuple[str, List[str]]: # type: ignore
    reasons: List[str] = []

    if file_count == 0:
        return "none", ["No readable files found."]

    if file_count <= 3 and source_tokens <= 15000:
        mode = "single"
        reasons.append("Small source set heuristic matched (<= 3 files and <= ~15k estimated source tokens).")
    else:
        mode = "split"
        reasons.append("Source set exceeds the small-set heuristic.")