#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-.}"
mkdir -p "$TARGET/.github" "$TARGET/scripts" "$TARGET/runbooks/ai-evals"
cp -R .github/evals "$TARGET/.github/"
cp scripts/ai_eval_*.py "$TARGET/scripts/"
cp runbooks/*.md "$TARGET/runbooks/ai-evals/"
echo "Installed the project AI eval test suite into $TARGET"
