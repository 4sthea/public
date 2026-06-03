# Code Quality Rubric

Use this after deterministic tests pass.

## Dimensions

| Dimension | Weight | What good looks like |
|---|---:|---|
| Correctness | 0.30 | Meets behavior and edge cases. |
| Minimality | 0.15 | No unrelated rewrites or dependency additions. |
| Test quality | 0.20 | Tests cover normal, boundary, and regression cases. |
| Maintainability | 0.15 | Clear names, simple control flow, low duplication. |
| Integration fit | 0.10 | Follows existing project conventions. |
| Verification evidence | 0.10 | Includes exact command/result evidence. |

## Hard failures

- Tests fail.
- Production behavior changes outside task scope.
- Adds dependencies without explicit acceptance criterion.
- Removes existing validation/error handling.
- Claims tests were run without output evidence.
