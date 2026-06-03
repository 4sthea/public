# Source Notes for the Eval Suite

**Accessed:** 2026-06-03

This file records the external methods used to design the suite. It is not a citation system for final answers; it is a practical source log for future maintenance.

## Official/product sources

| Source | Date / status | Relevance |
|---|---:|---|
| VS Code, “The Coding Harness Behind GitHub Copilot in VS Code” | 2026-05-15 | Defines harness as context assembly + tools + loop; VSC-Bench measures solution correctness, agent effort, token efficiency, latency; PR harness changes get eval assessment. |
| VS Code Agent Hooks docs | Accessed 2026-06-03; preview docs show 2026 examples | Hooks execute deterministic commands at lifecycle points; useful for audit trails, security policy, post-edit validation. |
| VS Code OpenTelemetry monitoring docs | Accessed 2026-06-03 | Copilot Chat can export traces, metrics, events; includes LLM calls, tool executions, token usage. |
| Anthropic, “Demystifying evals for AI agents” | 2026-01-09 | Defines task/trial/grader/transcript/outcome/harness; recommends code-based, model-based, and human graders; suggests 20–50 starter tasks. |
| GitHub Blog, “Validating agentic behavior when ‘correct’ isn’t deterministic” | 2026-05-06; updated 2026-05-26 | Supports validating essential milestones rather than exact step replay; warns against brittle validation and agent self-assessment. |
| Promptfoo `llm-rubric` docs | Last updated 2026-06-03 | General LLM-as-judge rubric, thresholds, grader pinning. |
| Promptfoo `agent-rubric` docs | Last updated 2026-06-02 | Repo-aware/read-only agentic grader for verifying artifact claims. |
| Promptfoo `select-best` docs | Last updated 2026-06-03 | Compares multiple outputs for prompt/harness variants. |

## Academic sources

| Source | Date | Relevance |
|---|---:|---|
| Claw-Eval: Towards Trustworthy Evaluation of Autonomous Agents | Submitted 2026-04-07, revised 2026-05-07 | Supports trajectory-aware grading, audit logs, environment snapshots, completion/safety/robustness, multiple trials. |
| Configuring Agentic AI Coding Tools: An Exploratory Study | Submitted 2026-02-16, revised 2026-05-08 | Confirms repository-level config artifacts such as context files, skills, subagents, AGENTS.md matter as harness artifacts. |
| AdaRubric | Submitted 2026-03-22, revised 2026-05-10 | Supports task-specific rubrics over fixed generic rubrics. |
| SPEAR: Code-Augmented Agentic Prompt Optimization | Submitted 2026-05-25 | Supports structural error analysis, confusion matrices, rollback on metric regression. |
| Stochasticity in Agentic Evaluations | Submitted 2025-12-07 | Warns that single-run accuracy hides variance; supports multiple trials and stability metrics. |
| REFLECT | Submitted 2026-05-18 | Warns that LLM judges can be unreliable for fine-grained failure detection; supports deterministic checks and calibration. |

## Community / user sentiment

| Source | Date visible in page | Signal |
|---|---:|---|
| Reddit r/LocalLLaMA: same task across GitHub Copilot, Pi, Claude Code, OpenCode | Page shows 2026 and “45m ago” at access | Practitioners explicitly compare harnesses with the same model; comments warn that single-shot comparisons are variance and ask for 10 attempts; users mention token/tool efficiency. |
| Hacker News discussions around coding harnesses | 2026 pages identified | Practitioner discussion aligns with the idea that the harness is a large part of quality, not just model choice. |

## YouTube / comments limitation

I attempted to find and open current YouTube material and comment sections. Public search/fetch access was not reliable enough to extract comment sentiment. Do not treat YouTube comments as a verified source in this suite. Use Reddit/HN/GitHub discussions for community sentiment unless you manually collect video comments yourself.
