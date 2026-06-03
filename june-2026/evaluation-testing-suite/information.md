## What is inside

The suite contains:

| Area                 | Included files                                                                                                                                                        |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Test prompts**     | 16 task definitions plus one rendered Markdown file with all copy/paste prompts                                                                                       |
| **Smoke tests**      | 10 low-effort/high-signal tests for docs, code, security, adherence, traces, OTel, and pairwise judging                                                               |
| **Capability tests** | 6 larger tests for runbooks, Agent Guard, Promptfoo config, trace checker design, and human calibration                                                               |
| **Fixtures**         | README excerpt, Engineer Agent excerpt, prompt-injection fixture, ambiguous request fixture, sample PR diff, OTel sample, trace samples, known-good/known-bad outputs |
| **Rubrics**          | Documentation quality, code quality, harness adherence, trace quality, security, semantic regression                                                                  |
| **Scripts**          | Prompt renderer, deterministic scorer, baseline/candidate comparator, aggregate reporter, trace checker, hook event logger, fixture-test runner                       |
| **Optional tooling** | Promptfoo config for `llm-rubric`, `agent-rubric`, and `select-best`                                                                                                  |
| **Runbooks**         | Before/after workflow, human calibration protocol, source notes, test-suite playbook                                                                                  |

## Why this design

I built the suite around the lowest-effort methods that still give useful signal:

1. **Deterministic gates first**: required strings, forbidden strings, required headings, word-count boundaries, evidence labels, and validation commands.
2. **Pairwise semantic regression second**: baseline vs candidate comparison, but without treating the baseline as ground truth.
3. **Trace/tool behavior third**: essential milestone checks, tool-call sanity, verification behavior, and optional hook/OTel instrumentation.
4. **LLM-as-judge only where needed**: especially for semantic equivalence, documentation quality, and nuanced improvement/worsening.
5. **Human calibration for important changes**: spot-checks for false positives from the judge.

This matches the research direction: Anthropic’s agent-eval guidance defines evaluations around **task → trial → grader → transcript → outcome**, with deterministic, model-based, and human graders; VS Code’s own harness work evaluates solution correctness, agent effort, token efficiency, and latency rather than only final answer quality. ([Anthropic][1])

I also included hooks/trace support because your the project repo already has hook lifecycle surfaces for `SessionStart`, `PreToolUse`, `PostToolUse`, and `Stop`.  VS Code’s official hook and OTel documentation supports this style of lifecycle instrumentation and trace/metric export for agent interactions, tool executions, and token usage. ([Visual Studio Code][2])

The suite is tailored to verified the project context: the project is a dividend-capture platform with a Python/FastAPI backend and React/TypeScript/Vite frontend, and it uses Agent Harness to govern AI-assisted development.   Your Engineer Agent already has a Ralph Loop posture and explicit verification expectations, so several tasks directly test whether a changed harness still preserves that behavior.  

## Recommended first test run

Start with these six smoke tasks:

```text
smoke-doc-001-the-project-readme-summary
smoke-agent-001-engineer-contract-summary
smoke-harness-001-eval-debug-mode-proposal
smoke-adherence-001-insufficient-context-trap
smoke-security-001-prompt-injection-trap
smoke-code-001-fix-dividend-window-fixture
```

Run each once for baseline and once for candidate. For serious agent-instruction changes, run **3–5 trials**. For major Agent Harness/skill changes, run **5–10 trials**. This is important because recent work on agentic evaluation warns that single-run accuracy hides variance, and practitioner sentiment also strongly warns against judging harnesses from one run. ([arXiv][3])

## Basic usage

After unzipping, copy these into the the project repo root:

```powershell
Copy-Item -Recurse -Force .\.github\evals <the project>\.github\evals
Copy-Item -Recurse -Force .\scripts\ai_eval_*.py <the project>\scripts\
Copy-Item -Recurse -Force .\runbooks <the project>\runbooks\ai-evals
```

Then render a prompt:

```bash
python scripts/ai_eval_render_prompt.py \
  --task .github/evals/tasks/smoke/smoke-doc-001-the-project-readme-summary.json \
  --variant baseline \
  --trial 1
```

Paste the rendered prompt into your current Engineer Agent and save the output to the path shown in the prompt.

After changing the agent artifact, run the same task again:

```bash
python scripts/ai_eval_render_prompt.py \
  --task .github/evals/tasks/smoke/smoke-doc-001-the-project-readme-summary.json \
  --variant candidate \
  --trial 1
```

Score both outputs:

```bash
python scripts/ai_eval_score.py \
  --task .github/evals/tasks/smoke/smoke-doc-001-the-project-readme-summary.json \
  --output docs/tmp/ai-evals/runs/manual/baseline/smoke-doc-001-the-project-readme-summary/t01/output.md \
  --variant baseline \
  --trial 1 \
  --out docs/tmp/ai-evals/runs/manual/baseline/smoke-doc-001-the-project-readme-summary/t01/trial-result.json
```

Compare baseline vs candidate:

```bash
python scripts/ai_eval_compare.py \
  --task .github/evals/tasks/smoke/smoke-doc-001-the-project-readme-summary.json \
  --baseline docs/tmp/ai-evals/runs/manual/baseline/smoke-doc-001-the-project-readme-summary/t01/output.md \
  --candidate docs/tmp/ai-evals/runs/manual/candidate/smoke-doc-001-the-project-readme-summary/t01/output.md \
  --out docs/tmp/ai-evals/reports/manual-smoke-doc-001-comparison.md
```

The comparison report includes a deterministic result plus a ready-to-use pairwise semantic judge prompt.

## Important note

The code fixture `smoke-code-001-fix-dividend-window-fixture` is intentionally failing at first. That is deliberate: it tests whether the changed agent can inspect a small bug, fix it, and verify the fix with tests.

I attempted to include YouTube/comment-section sentiment in the research pass, but public extraction was not reliable enough. I therefore did not use YouTube comments as evidence. The practical community signal in the source notes comes mainly from Reddit/HN/GitHub discussions, while the actual methodology is grounded in official docs, recent papers, and reproducible test design.

[1]: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents "https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents"
[2]: https://code.visualstudio.com/docs/copilot/customization/hooks "https://code.visualstudio.com/docs/copilot/customization/hooks"
[3]: https://arxiv.org/abs/2512.06710 "https://arxiv.org/abs/2512.06710"
