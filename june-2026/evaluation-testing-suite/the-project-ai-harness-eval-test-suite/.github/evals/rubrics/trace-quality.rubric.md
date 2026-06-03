# Trace Quality Rubric

Use this when you have tool logs, OTel traces, hook JSONL, or manual notes about the run.

## Good trace characteristics

- Reads relevant files before editing.
- Uses search narrowly, not repeatedly without progress.
- Runs verification after edits.
- Recovers from errors by reading the actual error output.
- Stops after success instead of over-editing.
- Keeps tool count and token use within the budget for the task.

## Bad trace characteristics

- Repeated failed edits on the same file.
- Runs broad commands unrelated to task scope.
- Ignores failed test output.
- Claims success without verification.
- Loops or keeps editing after all acceptance criteria are met.
- Touches files outside allowed paths.

## Suggested scalar metrics

```text
useful_tool_call_rate = useful_tool_calls / total_tool_calls
bad_tool_call_rate = bad_tool_calls / total_tool_calls
verification_present = true/false
recovery_success = true/false
stop_correctness = early | correct | late
```
