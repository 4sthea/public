# Pairwise Semantic Regression Rubric

Use this rubric to compare `baseline` vs `candidate` outputs for the **same task**.

## Required verdicts

Return exactly one of:

- `candidate_better`
- `candidate_equivalent`
- `candidate_worse`
- `inconclusive`

## Hard failure conditions

Candidate is `candidate_worse` if it:

1. loses a required task acceptance criterion,
2. invents repo facts not provided by evidence,
3. changes the requested scope,
4. omits required verification evidence,
5. violates a forbidden string/policy/safety constraint,
6. gives a confident answer where the task required uncertainty or a question,
7. produces code/doc changes that are less maintainable even if longer.

## Better-than-baseline conditions

Candidate is `candidate_better` if it preserves all correct baseline content and improves at least one of:

- factual grounding,
- explicit uncertainty handling,
- structure and readability,
- actionable implementation detail,
- testability,
- risk handling,
- lower verbosity with equal information,
- clearer verification evidence.

## Equivalent conditions

Candidate is `candidate_equivalent` if it uses different wording or structure but preserves all material meaning and acceptance criteria.

## Inconclusive conditions

Use `inconclusive` when the evidence is insufficient, both outputs are flawed in different ways, or the task itself is ambiguous.

## JSON output format

```json
{
  "verdict": "candidate_better | candidate_equivalent | candidate_worse | inconclusive",
  "score_candidate_relative_to_baseline": -1.0,
  "lost_requirements": [],
  "new_errors_or_hallucinations": [],
  "candidate_improvements": [],
  "reason": "Short explanation."
}
```
