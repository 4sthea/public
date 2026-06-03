# the project AI-Harness Test-Suite Playbook

## Goal

Use this suite to answer one practical question:

> Did the candidate agent/prompt/instruction/skill change preserve or improve output quality compared with the baseline?

The suite does not treat the baseline output as truth. It compares both outputs against task acceptance criteria, deterministic checks, rubrics, and optional pairwise semantic judging.

## Recommended first run

Run these six smoke tasks first:

1. `smoke-doc-001-the-project-readme-summary`
2. `smoke-agent-001-engineer-contract-summary`
3. `smoke-harness-001-eval-debug-mode-proposal`
4. `smoke-adherence-001-insufficient-context-trap`
5. `smoke-security-001-prompt-injection-trap`
6. `smoke-code-001-fix-dividend-window-fixture`

These cover hallucination, contract adherence, eval-mode design, insufficient-context handling, prompt-injection resistance, and code-edit verification.

## Before/after protocol

For each task:

1. Check out the baseline commit or use the current agent artifact as baseline.
2. Render the task prompt with `--variant baseline --trial 1`.
3. Run the agent and save its output exactly where the rendered prompt says.
4. Apply exactly one harness artifact change.
5. Render the same task with `--variant candidate --trial 1`.
6. Run the same model, same effort level, same tools, same repo snapshot except the harness artifact change.
7. Score both outputs with `ai_eval_score.py`.
8. Compare with `ai_eval_compare.py`.
9. If deterministic checks pass for both, use the pairwise judge prompt embedded in the comparison report.
10. For important changes, repeat 3–10 trials and aggregate.

## Interpretation

Accept a candidate only if:

- it does not lose required facts or constraints,
- it does not introduce forbidden claims or unsafe actions,
- deterministic score is equal or higher,
- semantic pairwise judge says `equivalent` or `candidate_better`,
- human spot-check does not find a material regression,
- extra tool/token overhead is acceptable.

Reject or revise a candidate if:

- it is more polished but less faithful,
- it guesses where the baseline asked for clarification,
- it removes evidence labels,
- it edits more files than necessary,
- it skips verification,
- it gets a higher judge score but fails deterministic gates.

## Trial count

- Local prompt tweak: 1–3 trials on 6 smoke tasks.
- Agent instruction change: 3–5 trials on all smoke tasks.
- Skill or Agent Harness rule change: 5–10 trials on smoke plus selected capability tasks.
- Merge gate: require zero hard-regression failures.

## Debugging failures

Use failure type to decide what to fix:

| Failure type | Likely cause | Fix location |
|---|---|---|
| Missing required string | output omitted important evidence | prompt/rubric/task acceptance criteria |
| Forbidden string | hallucination or fixture-instruction leakage | agent instruction/security rules |
| No evidence labels | Agent Harness adherence regression | copilot instructions / agent contract |
| Trace missing verification | Ralph Loop regression | engineer agent / hook instrumentation |
| Code fixture tests fail | implementation quality regression | agent execution rules / test-first behavior |
| Pairwise judge says worse | semantic regression despite deterministic pass | agent prompt or task rubric |

## Files to inspect after a run

- Agent output: `docs/tmp/ai-evals/runs/.../output.md`
- Trial score: `docs/tmp/ai-evals/runs/.../trial-result.json`
- Comparison report: `docs/tmp/ai-evals/reports/...comparison.md`
- Aggregated report: `docs/tmp/ai-evals/reports/...aggregate.md`

