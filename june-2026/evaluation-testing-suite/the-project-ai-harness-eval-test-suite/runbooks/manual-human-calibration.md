# Manual Human Calibration Protocol

LLM judges are useful but not ground truth. Calibrate them.

## Cadence

For every candidate harness change:

- manually review all failed tasks,
- manually review at least 20% of passed pairwise judge decisions,
- always review tasks involving safety, prompt injection, or unverified repo claims.

## Labels

Use these labels:

- `judge_agrees`
- `judge_too_strict`
- `judge_too_lenient`
- `task_ambiguous`
- `rubric_missing_dimension`
- `deterministic_gate_missing`

## When to update a task

Update a task when:

- two reasonable reviewers disagree on pass/fail,
- the judge repeatedly fails for the same reason,
- deterministic checks miss a clear regression,
- the task allows a loophole or overfitting.

## When to update the harness artifact

Update the agent/prompt/instruction/skill when:

- candidate fails the same category across multiple tasks,
- candidate improves docs but worsens safety/adherence,
- candidate uses more tokens/tool calls without quality gain,
- candidate repeatedly fails uncertainty handling.
