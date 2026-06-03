# the project AI-Harness Evals

This folder contains the task catalog, rubrics, prompt templates, schemas, and fixtures for before/after evaluation of the project agent-harness artifacts.

## Evaluation pattern

For each task:

1. render the task prompt,
2. run baseline agent artifact,
3. save output,
4. run candidate agent artifact under the same conditions,
5. save output,
6. score both with deterministic gates,
7. compare baseline vs candidate,
8. optionally run pairwise LLM judge and human spot-check.

## Minimal task lifecycle

```bash
python scripts/ai_eval_render_prompt.py --task .github/evals/tasks/smoke/<task>.json --variant baseline --trial 1
python scripts/ai_eval_score.py --task .github/evals/tasks/smoke/<task>.json --output <baseline-output.md> --variant baseline --trial 1 --out <baseline-result.json>
python scripts/ai_eval_render_prompt.py --task .github/evals/tasks/smoke/<task>.json --variant candidate --trial 1
python scripts/ai_eval_score.py --task .github/evals/tasks/smoke/<task>.json --output <candidate-output.md> --variant candidate --trial 1 --out <candidate-result.json>
python scripts/ai_eval_compare.py --task .github/evals/tasks/smoke/<task>.json --baseline <baseline-output.md> --candidate <candidate-output.md> --out <comparison-report.md>
```

## Categories

- `documentation`: Markdown/spec/runbook output quality
- `agent_contract`: behavior of agents, instructions, skills, hooks
- `code_fixture`: controlled code-edit task with deterministic tests
- `security_adherence`: prompt injection and unsafe instruction traps
- `trace_quality`: tool/trace/milestone analysis
- `review_quality`: code/doc review quality

## Verdict policy

- `PASS`: deterministic gates pass and pairwise judgment is equivalent/better.
- `FAIL`: hard gate failure, lost requirement, hallucinated repo claim, unsafe action, or worse candidate.
- `INCONCLUSIVE`: deterministic gates pass but semantic judgment is unclear, or there is high run-to-run variance.
