# Judge Calibration Prompt

Use this prompt to calibrate an LLM judge against known-good and known-bad fixture outputs before trusting it on real the project outputs.

Evaluate the following three candidate outputs against the task. One is good, one is borderline, one is a regression. Return a JSON array with a verdict for each.

## Task

Use `.github/evals/tasks/smoke/smoke-doc-001-the-project-readme-summary.json`.

## Candidate files

- `.github/evals/fixtures/outputs/doc-001-candidate-better.md`
- `.github/evals/fixtures/outputs/doc-001-candidate-regression.md`
- `.github/evals/fixtures/outputs/doc-001-baseline-good.md`

## Required output

```json
[
  {"file": "...", "verdict": "candidate_better|candidate_equivalent|candidate_worse|inconclusive", "reason": "..."}
]
```
