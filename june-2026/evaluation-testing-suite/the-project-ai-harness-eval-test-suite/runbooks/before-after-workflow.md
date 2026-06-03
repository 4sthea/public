# the project AI-Harness Before/After Workflow

## Goal

Measure whether a candidate change to an agent/prompt/instruction/skill is semantically equivalent or better than the baseline under the same task conditions.

## Controls

Keep these fixed for a comparison:

- repository commit or branch,
- model,
- reasoning/effort mode,
- tools enabled,
- task prompt,
- output path pattern,
- trial count,
- judge model if using a judge.

Change exactly one harness artifact at a time where possible.

## Workflow

### 1. Select tasks

Start with 6 smoke tasks:

```text
smoke-doc-001-the-project-readme-summary
smoke-agent-001-engineer-contract-summary
smoke-harness-001-eval-debug-mode-proposal
smoke-adherence-001-insufficient-context-trap
smoke-security-001-prompt-injection-trap
smoke-code-001-fix-dividend-window-fixture
```

### 2. Capture baseline

Render a prompt:

```bash
python scripts/ai_eval_render_prompt.py --task .github/evals/tasks/smoke/smoke-doc-001-the-project-readme-summary.json --variant baseline --trial 1
```

Run the agent and save output to the requested file path.

### 3. Change one harness artifact

Examples:

- edit `.github/agents/engineer.agent.md`,
- edit `.github/instructions/*.instructions.md`,
- edit `.github/skills/*/SKILL.md`,
- edit `.github/prompts/*.prompt.md`.

### 4. Capture candidate

Run the exact same task prompt with `--variant candidate`.

### 5. Score deterministically

```bash
python scripts/ai_eval_score.py --task <task.json> --output <baseline-output.md> --variant baseline --trial 1 --out <baseline-result.json>
python scripts/ai_eval_score.py --task <task.json> --output <candidate-output.md> --variant candidate --trial 1 --out <candidate-result.json>
```

For fixture code tasks, add:

```bash
--run-validation-commands
```

### 6. Compare semantically

```bash
python scripts/ai_eval_compare.py --task <task.json> --baseline <baseline-output.md> --candidate <candidate-output.md> --out <comparison.md>
```

Paste the generated pairwise judge prompt into your fixed judge model.

### 7. Decide

Accept candidate only if:

- no new deterministic failures,
- no forbidden strings or hallucinated repo facts,
- no safety/adherence regression,
- pairwise judge says `candidate_equivalent` or `candidate_better`,
- human spot-check does not disagree for important tasks.

## Trial count

- first experiment: 1 trial per task,
- serious candidate: 3 trials per task,
- merge-critical agent change: 5–10 trials for top smoke tasks.

Do not over-invest in statistics before the tasks themselves are stable.
