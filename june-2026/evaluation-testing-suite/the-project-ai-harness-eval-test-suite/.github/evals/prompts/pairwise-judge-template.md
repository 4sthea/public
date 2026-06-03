# Pairwise Judge Prompt: Baseline vs Candidate

You are evaluating a before/after change to a the project AI-harness artifact.

The **baseline** and **candidate** outputs were produced for the same task. The candidate should be semantically/contextually equivalent or better. The baseline is not gold truth; use the task, criteria, and evidence as ground truth.

## Task

{{task_json}}

## Baseline output

```markdown
{{baseline_output}}
```

## Candidate output

```markdown
{{candidate_output}}
```

## Rubric

{{rubric}}

## Required JSON output

Return only valid JSON:

```json
{
  "verdict": "candidate_better | candidate_equivalent | candidate_worse | inconclusive",
  "score_candidate_relative_to_baseline": 0.0,
  "lost_requirements": [],
  "new_errors_or_hallucinations": [],
  "candidate_improvements": [],
  "evidence": [],
  "reason": ""
}
```
