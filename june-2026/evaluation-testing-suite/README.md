# the project AI-Harness Eval Test Suite

**Created:** 2026-06-03  
**Purpose:** before/after evaluation of the project agent-harness artifacts: agents, prompts, instructions, skills, hooks, Agent Harness rules, and related Markdown/JSON prompt infrastructure.

This pack gives you a practical evaluation suite you can copy into the the project repository and use manually with VS Code + GitHub Copilot, Copilot CLI, Codex, Claude Code, OpenCode, or another coding agent.

It intentionally starts with **low-effort/high-signal checks**:

1. deterministic output gates,
2. task acceptance criteria,
3. prompt-injection and hallucination traps,
4. pairwise before/after semantic regression judging,
5. lightweight trace/tool metrics,
6. optional Promptfoo configuration for `llm-rubric`, `agent-rubric`, and `select-best`.

The old output is **not** treated as gold truth. It is only a comparison anchor. The ground truth is the task spec, acceptance criteria, required evidence, deterministic checks, and rubric.

---

## What is inside

```text
.github/evals/
  README.md
  tasks/
    smoke/*.json
    capability/*.json
  rubrics/*.md
  prompts/*.md
  schemas/*.json
  promptfoo/promptfooconfig.yaml
  fixtures/
    docs/*.md
    diffs/*.diff
    outputs/*.md
    python/*.py
    traces/*.json
    otel/*.jsonl
scripts/
  ai_eval_render_prompt.py
  ai_eval_score.py
  ai_eval_compare.py
  ai_eval_aggregate.py
  ai_eval_run_fixture_tests.py
  ai_eval_hooks_event_logger.py
  ai_eval_trace_check.py
runbooks/
  before-after-workflow.md
  manual-human-calibration.md
  source-notes.md
  test-suite-playbook.md
install.ps1
install.sh
```

For direct copy/paste usage, see `.github/evals/prompts/ALL_RENDERED_TEST_PROMPTS.md`. For a task spreadsheet-style overview, see `.github/evals/tasks/eval-matrix.csv`.

---

## Fastest usage path

### 1. Copy into the project

From this extracted folder, copy the `.github/evals/`, `scripts/`, and `runbooks/` folders into your the project repo root.

PowerShell:

```powershell
Copy-Item -Recurse -Force .\.github\evals <the project>\.github\evals
Copy-Item -Recurse -Force .\scripts\ai_eval_*.py <the project>\scripts\
Copy-Item -Recurse -Force .\runbooks <the project>\runbooks\ai-evals
```

Bash:

```bash
cp -R .github/evals <the project>/.github/
cp scripts/ai_eval_*.py <the project>/scripts/
mkdir -p <the project>/runbooks/ai-evals
cp runbooks/*.md <the project>/runbooks/ai-evals/
```

### 2. Pick a task and render the prompt

```bash
python scripts/ai_eval_render_prompt.py \
  --task .github/evals/tasks/smoke/smoke-doc-001-the-project-readme-summary.json \
  --variant baseline \
  --trial 1
```

Paste the rendered prompt into your selected agent. Save the agent output to the exact output path shown in the prompt.

### 3. Run the same task after changing the agent artifact

Render again with `--variant candidate` and save the new output.

```bash
python scripts/ai_eval_render_prompt.py \
  --task .github/evals/tasks/smoke/smoke-doc-001-the-project-readme-summary.json \
  --variant candidate \
  --trial 1
```

### 4. Score both outputs deterministically

```bash
python scripts/ai_eval_score.py \
  --task .github/evals/tasks/smoke/smoke-doc-001-the-project-readme-summary.json \
  --output docs/tmp/ai-evals/runs/manual/baseline/smoke-doc-001-the-project-readme-summary/t01/output.md \
  --variant baseline \
  --trial 1 \
  --out docs/tmp/ai-evals/runs/manual/baseline/smoke-doc-001-the-project-readme-summary/t01/trial-result.json

python scripts/ai_eval_score.py \
  --task .github/evals/tasks/smoke/smoke-doc-001-the-project-readme-summary.json \
  --output docs/tmp/ai-evals/runs/manual/candidate/smoke-doc-001-the-project-readme-summary/t01/output.md \
  --variant candidate \
  --trial 1 \
  --out docs/tmp/ai-evals/runs/manual/candidate/smoke-doc-001-the-project-readme-summary/t01/trial-result.json
```

### 5. Compare baseline vs candidate

```bash
python scripts/ai_eval_compare.py \
  --task .github/evals/tasks/smoke/smoke-doc-001-the-project-readme-summary.json \
  --baseline docs/tmp/ai-evals/runs/manual/baseline/smoke-doc-001-the-project-readme-summary/t01/output.md \
  --candidate docs/tmp/ai-evals/runs/manual/candidate/smoke-doc-001-the-project-readme-summary/t01/output.md \
  --out docs/tmp/ai-evals/reports/manual-smoke-doc-001-comparison.md
```

The comparison report contains:

- deterministic pass/fail deltas,
- missing/preserved criteria,
- lexical drift indicators,
- pairwise semantic judge prompt you can paste into a strong judge model,
- recommended verdict: `PASS`, `FAIL`, or `INCONCLUSIVE`.

---

## Recommended first 6 tasks

Start with these before adding more:

| Order | Task | Why |
|---:|---|---|
| 1 | `smoke-doc-001-the-project-readme-summary` | catches hallucinated repo facts and missing evidence labels |
| 2 | `smoke-agent-001-engineer-contract-summary` | directly tests the Engineer Agent behavior contract |
| 3 | `smoke-harness-001-eval-debug-mode-proposal` | checks whether new agent instructions improve eval/debug design |
| 4 | `smoke-adherence-001-insufficient-context-trap` | catches guessing and overconfident fabrication |
| 5 | `smoke-security-001-prompt-injection-trap` | catches unsafe obedience to untrusted fixture text |
| 6 | `smoke-code-001-fix-dividend-window-fixture` | checks code edit + verification behavior with deterministic tests |

Run 1–3 trials per task at first. Move to 5–10 trials only for changes you seriously want to merge.

---

## Rule of interpretation

A candidate change is good only if it improves or preserves all hard gates:

```text
candidate_deterministic_pass >= baseline_deterministic_pass
candidate_forbidden_violations == 0
candidate_required_criteria_missing <= baseline_required_criteria_missing
candidate_semantic_verdict in ["equivalent", "better"]
candidate_cost_or_tool_overhead <= allowed_budget
```

Do not accept a change just because the answer is longer, sounds more polished, or has better formatting.

---

## Evidence basis for this suite

The suite is based on the research summarized in `runbooks/source-notes.md`:

- Anthropic-style agent evals: task + trial + grader + transcript + outcome.
- VS Code harness evals: solution correctness, agent effort, token efficiency, latency.
- Promptfoo-style model graders: deterministic assertions first, `llm-rubric`/`agent-rubric`/`select-best` only where nuance is needed.
- GitHub Trust Layer idea: validate essential milestones rather than brittle exact paths.
- Current academic warnings: LLM judges are useful but unreliable without deterministic checks and human calibration.

---

## Import notes

This suite does **not** modify your existing the project agents automatically. It gives you test assets. Import them manually, commit them, then use them to test a later change to an agent/prompt/instruction/skill.

If you already have `.github/evals/`, merge carefully instead of overwriting.
