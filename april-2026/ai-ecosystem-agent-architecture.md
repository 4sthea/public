# AI Ecosystem — Controlled Layered Authority System for Prompts

> **Version:** v3 — Updated 2026-04-09  
> **Supersedes:** v1 (2026-03-06), v2 (2026-03-10)  
> **Canonical source of truth:** Active files under `.github/`

## What This Document Covers

This document explains the architecture, rationale, advantages, disadvantages, and everyday usage of **AI Ecosystem** (Controlled Layered Authority System for Prompts) — the agent-and-artifact governance framework used in this repository to keep AI-generated outputs honest, auditable, and safe to merge. It includes detailed coverage of all artifact types, hooks, enforcement scripts, skills, JSON schemas, and the complete RBI pipeline data contracts.

---

## 1) The Problem AI Ecosystem Solves

Large Language Models (LLMs) are probabilistic text continuators. Given a prompt, they predict the most plausible next tokens. They are not truth engines. When evidence is missing and the prompt implicitly demands completion, the model does what it was trained to do: produce fluent, confident-sounding text that fills the gap. In casual chat this is a nuisance; in merged documentation, infrastructure configs, or code reviews it is a hazard. A hallucinated detail — an API endpoint that does not exist, a config key with a wrong default, a security claim without audit evidence — can outlive the conversation that created it, propagate through onboarding docs, and eventually become an unchallenged "fact" in the team's institutional memory.

The root cause is structural, not moral. Models hallucinate because:

1. **Missing evidence** creates a vacuum that completion training fills.
2. **Completion pressure** in the prompt ("be comprehensive", "make it complete") punishes abstention and rewards guessing.
3. **Authority cues** ("ensure correctness", "verify") imply the model can validate its own claims.
4. **Unbounded scope** ("review the entire codebase") makes it impossible to ground every claim.

AI Ecosystem exists to remove these pressures systematically. It does not make the model smarter. It reshapes the environment so that honesty is the cheapest path, silence is an acceptable outcome, and uncertainty is visible rather than hidden.

---

## 2) Core Philosophy

AI Ecosystem rests on three principles:

- **Truth over helpfulness over speed.** An "Unknown" cell in a table is more valuable than a plausible guess that might be wrong.
- **Single ownership per concern.** Every rule, gate, procedure, and structural decision has exactly one canonical home. Duplicating rules across files causes drift, contradiction, and audit nightmares.
- **Creativity belongs in cognition; authority must not leak.** Agents may reason freely within their scope. But enforcement, verification gates, and output structure are governed by dedicated artifacts that the agent does not own and cannot override.

---

## 3) The Artifact Taxonomy

AI Ecosystem separates AI-assisted work into seven artifact types plus two composable additions (skills and instructions). Each has one job and strict boundaries on what it may and may not contain.

### 3.1 Constitution — `copilot-instructions.md`

The constitution is the supreme authority layer. It contains the global epistemic laws that every agent, prompt, and procedure must obey: non-fabrication rules, precedence order, the assumptions policy, the dependency-read contract, mode declarations, and change-propagation requirements. It is deliberately short and stable. Nothing task-specific lives here. If a rule is truly universal — "never fabricate", "label assumptions", "stop if required context is unreadable" — it belongs in the constitution and nowhere else.

Key sections in the current constitution:

| Section                          | What It Governs                                             |
| -------------------------------- | ----------------------------------------------------------- |
| Precedence                       | Strict artifact hierarchy — no exceptions                   |
| Epistemic Rules                  | FACT / ASSUMPTION / UNVERIFIED OPINION labeling             |
| Assumptions Policy               | No silent assumptions; stop if correctness-affecting        |
| Mistakes                         | Acknowledge, correct, cite violated constraint              |
| Mode Declaration                 | Epistemic default for "truthy" artifacts                    |
| Pre-Response Verification        | Verify repo-specific claims or state "Not verified"         |
| Post-Implementation Verification | `ruff check` → `pyright` → `pytest` after every code change |
| Operational Rules                | Direct, critical advisor; max 2 clarification questions     |

### 3.2 Enforcement — `verification-checklist.instructions.md`

The verification checklist is the single owner of pass/fail criteria, promoted to an always-on instruction file (`applyTo: "**"`) for reliable injection. Before any repo-specific fact can be asserted (file existence, symbol names, config values, dependency usage, test coverage), the checklist requires gathering direct evidence: opened files, search results, directory listings, or user-provided snippets. Without evidence, the only acceptable output is "Not verified in provided context."

### 3.3 Cognition — `*.agent.md`

Agents are thinking contracts. Each agent defines a reasoning posture (how to think), an authorized domain (what topics are in scope), hard exclusions (what to refuse), and preflight checks (what to confirm before starting). Agents do **not** contain procedures, output paths, verification gates, or tool invocations. They describe cognitive stance, not mechanical steps.

**v3 Agent Roster:**

> For the current roster with model assignments, see `.github/context/AI Ecosystem-artifact-freshness.md` and `.github/instructions/AI Ecosystem-authoring.instructions.md`.

| Agent                     | Model           | Tools                                    | Purpose                                                                |
| ------------------------- | --------------- | ---------------------------------------- | ---------------------------------------------------------------------- |
| **engineer**              | Claude Opus 4.6 | read, search, agent, edit, todo, execute | Implementation + Ralph Loop verification                               |
| **reviewer**              | Claude Opus 4.6 | read, search, agent, todo                | Read-only adversarial review + security                                |
| **advisor**               | default         | read, search, agent, todo                | Read-only planning, design, teaching                                   |
| **sparring.orchestrator** | default         | read, search, agent, todo, web           | Multi-perspective analysis orchestrator                                |
| **feature.orchestrator**  | default         | read, search, agent, todo, vscode        | Feature lifecycle coordinator                                          |
| **test.orchestrator**     | default         | read, search, agent, todo, vscode        | Self-healing test generation orchestrator                              |
| **qa.orchestrator**       | default         | read, search, agent, todo, vscode        | Post-delivery quality assurance (4-gate validation + auto-remediation) |
| **research.orchestrator** | default         | read, search, agent, todo, vscode        | Autonomous research-to-spec pipeline (consensus → feature)             |

Tool restrictions are the load-bearing constraint:

- The **engineer** is the only agent that can edit files and run terminal commands. It follows the "Ralph Loop": implement → build → test → read output → fix → loop until verified or stuck.
- The **reviewer** is read-only and reviews diffs for correctness, safety, maintainability, and security. It provides adversarial consensus — a different perspective on code the engineer wrote.
- The **advisor** is read-only and prevents premature implementation during planning. It challenges assumptions, explores alternatives, and designs before anyone writes code.
- The **sparring.orchestrator** invokes hidden partner agents (architect, implementation, operations, advisor, creative-thinker, critical-thinker) for structured multi-perspective analysis and synthesizes one actionable answer.
- The **feature.orchestrator** coordinates the full feature lifecycle (plan → implement → verify → review → remediate → finalize) by routing work to engineer, reviewer, and advisor. It is read-only — it coordinates but never edits.
- The **test.orchestrator** generates all test artifacts (unit, integration, backtest), runs them, reviews for correctness, and iterates until convergence. Self-healing loop — delegates execution to engineer.
- The **qa.orchestrator** validates delivered features through 4 gates: test suite, coverage threshold, regression baselines, and smoke tests. If any gate fails, it auto-remediates by delegating fixes to engineer and re-running failed gates (max 3 iterations). Can escalate design concerns to sparring.orchestrator.
- The **research.orchestrator** drives a consensus document through multi-perspective analysis, code review, implementation planning, and feature specification generation — producing an approved spec ready for the feature.orchestrator. Only two manual steps: reading the consensus doc and reviewing the generated spec.

Hidden partner agents (not visible in the agent picker):

| Partner              | Purpose                                                          |
| -------------------- | ---------------------------------------------------------------- |
| **architect**        | System boundaries, coupling, interfaces, design tradeoffs        |
| **implementation**   | Feasibility, complexity, failure points, sequencing              |
| **operations**       | Deployment, observability, safety, rollback, runtime risk        |
| **creative-thinker** | Idea expansion, brainstorming, possibility mapping, steelmanning |
| **critical-thinker** | Stress-testing ideas, exposing flaws, adversarial analysis       |

The **advisor** serves double duty as both a user-visible planning agent and a hidden partner for the sparring orchestrator.

Each agent lists its procedural companions (which `*.instructions.md` files it may invoke), when to use it, when NOT to use it, and agent-specific preflight checks.

> **v1 → v3 migration note:** v1 had 16 specialized agents (Agent Router, Code Analyst, Feature Engineer, Learn Coach, Security Reviewer, Skill Teacher, Software Architect, Strategy Analyst, Tech Debt Analyst, Tech Debt Resolver, Tech Writer, Test Architect, Test Engineer, etc.). v3 consolidated these into a small set of visible agents + hidden partners for orchestration. The specialized knowledge from the retired agents now lives in `*.instructions.md` files that any agent can invoke on demand. This reduced maintenance burden while preserving domain expertise through composable instructions.

> For the current agent roster and tool assignments, see `.github/instructions/AI Ecosystem-authoring.instructions.md` → Agent Roster table.
> For current artifact counts, see `.github/context/AI Ecosystem-artifact-freshness.md`.

### 3.4 Instructions — `*.instructions.md`

Instructions are on-demand procedural knowledge files. They contain domain-specific conventions, patterns, and rules that agents invoke when their scope matches. Instructions replaced the need for many specialized agents — instead of having a dedicated "Security Reviewer" agent, the engineer or reviewer can invoke `security-review.instructions.md` when reviewing security.

Instruction files live in `.github/instructions/`. Each uses `applyTo` glob patterns so VS Code automatically attaches them when working in matching files.

Current instruction roster (17 files):

| Instruction              | `applyTo` Scope                                                       | Purpose                                                                    |
| ------------------------ | --------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `advanced-elicitation`   | Advisor/sparring/thinker agents & elicitation prompts                 | Method selection heuristics for named thinking patterns                    |
| `architecture`           | _(on-demand)_                                                         | System-level architecture decisions, tradeoffs, feature decomposition      |
| `AI Ecosystem-authoring` | `.github/**`                                                          | AI Ecosystem artifact ownership, routing, maintenance rules                |
| `documentation`          | `docs/**/*.md,**/README.md,**/ADR*`                                   | Technical documentation synthesis guidance                                 |
| `elicitation-techniques` | Elicitator agent & requirements-elicitation skill                     | Question taxonomy, quality rules, viewpoint sweep                          |
| `feature-delivery`       | Feature delivery skill, prompts, agents                               | Lifecycle conventions, remediation guidance, slice management              |
| `multi-aspect-review`    | `**/*review*`                                                         | Structured multi-aspect code review with normalized findings               |
| `rbi-pipeline`           | `divical-api/app/workers/**`, `services/research/**`, `strategies/**` | RBI pipeline implicit contracts, change-propagation rules                  |
| `refactor-plan`          | _(on-demand)_                                                         | Refactor plan design guidance                                              |
| `runbook`                | `**` (always-on)                                                      | Curated operational runbook — max 10 entries with "Do instead" actions     |
| `security-review`        | _(on-demand)_                                                         | Security risk identification in code, configs, infrastructure              |
| `sparring-orchestration` | Sparring/thinker agents & multi-perspective prompts                   | Multi-perspective analysis orchestration rules                             |
| `stack-python`           | `divical-api/**/*.py`                                                 | Python/FastAPI backend conventions                                         |
| `stack-react`            | `divical-web/**/*.{tsx,jsx,ts,js}`                                    | React/TypeScript frontend conventions                                      |
| `state-management`       | `.github/agents/*-orchestrator*`                                      | Workflow state persistence and session resumption protocol                 |
| `testing`                | `**/*test*,**/*spec*`                                                 | Test strategy, architecture, structuring conventions                       |
| `verification-checklist` | `**` (always-on)                                                      | Anti-fabrication enforcement — verification gates for repo-specific claims |

Two instructions are **always-on** (`applyTo: "**"`): `runbook` and `verification-checklist`. These inject into every agent session regardless of file context.

> For the current list of instructions and their scopes, see the files on disk in `.github/instructions/`.
> For the current count, see `.github/context/AI Ecosystem-artifact-freshness.md`.

### 3.5 Skills — `skills/*/SKILL.md`

Skills are self-contained, composable workflows. Each skill bundles ordered steps, stop conditions, worker agent routing, and required context into a single `SKILL.md` file. Skills replaced the former `*.procedure.md` artifact type — all procedure content has been absorbed into skills.

Skill files live in `.github/skills/*/`.

Current skill roster (11 skills + shared assets):

| Skill                        | Purpose                                                                                     | Worker Agents                        | Key Output                                         |
| ---------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------ | -------------------------------------------------- |
| **advanced-elicitation**     | Apply named thinking patterns as second-pass critique                                       | None (invoking agent drives)         | Delta-centric analysis                             |
| **AI Ecosystem-compression** | Reduce token cost of frequently-injected instruction/context files via lossless compression | Explore                              | Compressed files + token savings report            |
| **compaction**               | Compress workflow context at phase boundaries to preserve working memory                    | None (orchestrator drives)           | Session carryover files                            |
| **distillator**              | Lossless LLM-optimized distillation of source documents into dense context                  | Explore                              | Single distillate or split folder with `_index.md` |
| **feature-delivery**         | 10-phase autonomous feature lifecycle from spec to verified implementation                  | advisor, engineer, reviewer, Explore | Feature delivery report + handoff payload          |
| **multi-aspect-code-review** | 8-domain parallel code review using Explore subagents                                       | Explore (one per domain)             | Consolidated review report with scorecard          |
| **qa-orchestration**         | 4-gate quality validation with auto-remediation and sparring escalation                     | engineer, sparring.orchestrator      | QA report with per-gate results                    |
| **readme-gen**               | Generate or update README files from code evidence                                          | Explore                              | Markdown README                                    |
| **requirements-elicitation** | Interactive requirements discovery via structured questioning                               | Explore (optional)                   | Requirements canvas + elicitation ledger           |
| **tech-debt**                | Review documented debt items and design remediation plans                                   | None (invoking agent drives)         | Tech debt analysis document                        |
| **test-orchestration**       | Self-healing test generation with 5-phase convergence loop                                  | Explore, engineer, reviewer          | Test generation report + handoff for QA            |

**Shared assets** live in `.github/skills/shared/assets/` and are consumed by multiple skills:

| Asset                                    | Used By                                    |
| ---------------------------------------- | ------------------------------------------ |
| `compression-rules.md`                   | AI Ecosystem-compression, distillator      |
| `feature-specification.template.md`      | feature-delivery, requirements-elicitation |
| `multi-perspective-analysis.template.md` | sparring contexts                          |
| `security-review.template.md`            | security review contexts                   |
| `software-architecture.template.md`      | architecture contexts                      |
| `strategy-analysis.template.md`          | strategy contexts                          |

**Skill dependency graph:**

```
requirements-elicitation
        ↓
  feature-delivery
    ↙       ↘
test-       multi-aspect-
orchestration  code-review
    ↓
qa-orchestration

Standalone skills (no dependencies):
  advanced-elicitation, AI Ecosystem-compression, compaction,
  distillator, readme-gen, tech-debt
```

#### Skill Detail: feature-delivery (10 Phases)

1. **Intake** — Read spec, confirm suitability, extract acceptance criteria
2. **Plan** — Analyze feature, propose slices, identify dependencies and risks
3. **Select Slice** — Choose smallest meaningful slice, define objective
4. **Implement** — Engineer implements only current slice changes
5. **Verify** — `ruff check` → `pyright` → `pytest` (lint, types, tests)
6. **Review** — Multi-aspect code review with normalized findings
7. **Decide** — Evaluate results: next slice / remediate / stop
8. **Remediate** — Surgical fixes for blocking findings only (max 3–5 iterations)
9. **Post-Delivery Docs** — Update affected docs, AI Ecosystem audit (detection-only)
10. **Finalize** — Confirm completion, write handoff payload, invoke test.orchestrator

Iteration limits: 3 remediations (small) / 5 (medium) per slice, pause after every 5 slices.

Anti-thrashing: STOP if same blocking finding reappears unchanged 2×, scope increases without reducing blockers, verification oscillates, or review returns broad non-actionable findings repeatedly.

#### Skill Detail: multi-aspect-code-review (8 Domains)

Review domains with execution waves:

| Wave | Domain                    | ID Prefix | Focus                                   |
| ---- | ------------------------- | --------- | --------------------------------------- |
| 1    | Architecture & Design     | `ARCH`    | Boundaries, coupling, interfaces        |
| 1    | Security                  | `SEC`     | Vulnerabilities, auth, data exposure    |
| 1    | Performance               | `PERF`    | Bottlenecks, resource usage             |
| 2    | Code Quality & Principles | `QUAL`    | SOLID, DRY, naming, readability         |
| 2    | LLM Optimization          | `LLM`     | Token cost, prompt efficiency           |
| 2    | Testing                   | `TEST`    | Coverage, assertion quality, edge cases |
| 3    | Type Safety & Correctness | `CORR`    | Type errors, logic bugs, data flow      |
| 3    | Financial Logic           | `FIN`     | BDC-specific calculations, tax rules    |

Supports `--skip {domains}` and `--only {domains}` for selective review.

#### Skill Detail: test-orchestration (5 Phases)

1. **Scope** — Discover test patterns, fixtures; classify as unit/integration/backtest
2. **Generate** — Engineer generates tests; locked assertions marked `# LOCKED: <criteria-ref>`
3. **Execute** — Static analysis + canary validation (backtest) + lint/types/tests + coverage
4. **Review** — Reviewer checks assertion density ≥1/test, negative testing ≥30%, no temporal leakage
5. **Heal** — Fix blocking findings only (max 5 iterations per batch, 3 per function)

Convergence: all tests pass + no blocking findings = SUCCESS. Thrashing or plateau = STOP.

#### Skill Detail: qa-orchestration (4 Gates)

| Gate          | Check                                         | Threshold              |
| ------------- | --------------------------------------------- | ---------------------- |
| 1: Test Suite | `ruff check` + `pyright` + `pytest`           | All exit 0             |
| 2: Coverage   | Diff-coverage of changed lines                | Fail < 50%, Warn < 80% |
| 3: Regression | Regression tests against baselines            | All pass (or SKIPPED)  |
| 4: Smoke      | Import check, config load, route registration | All exit 0             |

Auto-remediation: max 3 iterations of fix → re-run failed gates. Sparring escalation if >3 tests fail at same boundary or systematic coverage gaps. Verdicts: PASS, PASS WITH CAVEATS, PASS (REMEDIATED), FAIL.

#### Skill Detail: requirements-elicitation (Adaptive Phases)

1. **Problem Framing** — Socratic + First Principles: situation, current state, what solved looks like
2. **Assumption Mining** — Challenge assumptions, identify real constraints
3. **Solution Space Exploration** — 2–3 approaches with tradeoffs
4. **Requirements Crystallization** — Functional requirements, quality concerns, error handling
5. **Scope & Risk Check** — Pre-mortem: failure modes, out-of-scope items, confidence
6. **Validation Gate** — Coverage check (9 categories), contradiction check, user confirmation

Uses `vscode_askQuestions` as primary interaction mechanism. Target: 6–10 question rounds. Outputs: requirements canvas + elicitation ledger.

> For the current list and count, see `.github/context/AI Ecosystem-artifact-freshness.md`.

### 3.6 Wiring — `*.prompt.md`

Prompts are the task-level glue. A prompt selects an agent, references one or more instructions/skills, declares a template, defines the evidence scope, specifies the output shape, and sets stop conditions.

Prompt files live in `.github/prompts/`. Each prompt selects an agent, references instructions/skills, declares a template, and sets stop conditions.

> For the current list and count, see `.github/context/AI Ecosystem-artifact-freshness.md`.

### 3.7 Structure — `*.template.md`

Templates are interfaces. They define headings, placeholder lists, and section structure — nothing more. Empty sections are explicitly allowed and encouraged, because an empty section with the heading "Unknown" is infinitely more honest than a filled section containing plausible invention.

Templates live inside skill folders as `skills/<name>/assets/*.template.md`. Skill-owned templates colocate with their owning skill. Cross-cutting templates shared by multiple consumers live in `skills/shared/assets/`.

> For the current list and count, see `.github/context/AI Ecosystem-artifact-freshness.md`.

### 3.8 Context — `.github/context/*.md`

Context files provide descriptive grounding: system maps, codebase orientation, component catalogs, domain glossaries, shared conventions, and known pitfalls. They are read-only references that help agents orient without relying on model priors or folklore. The critical rule is that context must never become "shadow policy" — it describes what exists but does not prescribe what must happen.

Current context files (9):

| File                                 | Purpose                                                                                                   |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| `assertion-policy.md`                | Runtime claims validation — assertion categories and failure modes                                        |
| `AI Ecosystem-artifact-freshness.md` | Canonical registry of mutable AI Ecosystem artifact inventories (counts, rosters, model assignments)      |
| `codebase-context.md`                | Project orientation and known pitfalls — referenced in `copilot-instructions.md`                          |
| `elicitation-methods.md`             | Curated question patterns and discovery workflows for requirements elicitation                            |
| `pipeline-architecture.md`           | Research → Backtest → Incubate pipeline reference (cross-referenced in `rbi-pipeline.instructions.md`)    |
| `repo-map.md`                        | Complete artifact file tree and organization reference — auto-generated by `scripts/generate-repo-map.sh` |
| `review-finding-schema.md`           | Normalized finding structure for multi-aspect code review                                                 |
| `shared-context.md`                  | Common architectural vocabulary and definitions                                                           |
| `temporal-rules.md`                  | Time-dependent behaviors, schedules, and TTLs for the system                                              |

> For the current list and count, see `.github/context/AI Ecosystem-artifact-freshness.md`.

---

## 4) Why AI Ecosystem Is Structured This Way

### 4.1 Single Ownership Prevents Drift

The most common failure mode in governed AI workflows is "authority sprawl": the same rule appears in the constitution, in an agent definition, in a prompt, and in a template, each phrased slightly differently. Over time those phrasings drift apart. When the model encounters contradictions, it resolves them by picking whichever version seems most local or specific — which is often the wrong one. Single ownership eliminates that class of failure entirely. If you want to change a verification rule, you change `verification-checklist.instructions.md` and nothing else. If you want to change how an agent reasons, you change the `.agent.md` file and nothing else.

### 4.2 Separation of Cognition from Execution

Agents define _how to think_. Instructions define _what domain knowledge to apply_. Procedures define _what steps to follow_. Prompts define _what to produce_. By separating these concerns, AI Ecosystem avoids the "god-prompt" anti-pattern where one massive instruction block tries to simultaneously set the model's tone, define a procedure, specify output format, and enforce verification — inevitably creating contradictions and leaving the model to guess which directive takes priority.

This separation also makes the system composable. The same agent (e.g., engineer) can be wired to different prompts (architecture documentation, code analysis, tech debt remediation) while invoking different instructions as needed — without changing the agent's core reasoning posture.

### 4.3 Silence as Success

Most AI systems implicitly punish refusal. If the model says "I don't know," the user is disappointed and the conversation feels stuck. AI Ecosystem explicitly inverts this: silence, refusal, and "Unknown" are correct outputs when evidence is missing. This is operationalised through stop conditions in procedures, evidence constraints in prompts, and the constitution's rule that "truth > helpfulness > speed." The practical effect is that the model no longer needs to guess in order to be useful. Being honest is the easiest valid response.

### 4.4 The Compiler Pipeline Pattern

For high-stakes outputs, AI Ecosystem treats writing like a compiler pipeline:

1. **Draft** — generate from template, using provided evidence.
2. **Lint** — apply verification checklist and lint rules mechanically; output findings only.
3. **Patch** — apply minimal, surgical fixes to resolve findings.

This pattern exists because large rewrites are drift machines. When you ask a model to "rewrite and fix" in one pass, it changes tone, adds unverified connective tissue, drops sections it considers redundant, and introduces new claims. The pipeline keeps each pass focused and auditable.

### 4.5 Instructions Replace Agents

The v1 → v3 migration demonstrated that 16 specialized agents created a maintenance burden disproportionate to their value. Most agents shared the same tool set and differed only in domain knowledge. By extracting domain knowledge into `*.instructions.md` files and consolidating to a small set of visible agents with distinct tool profiles (plus hidden partners for orchestration), AI Ecosystem achieved:

- **Reduced surface area:** Fewer agent files to maintain instead of 16
- **Preserved expertise:** All domain knowledge survives in instruction files
- **Better composability:** Any agent can invoke any instruction when scope matches
- **Clearer tool boundaries:** Edit capability is the meaningful differentiator, not domain label

---

## 5) Authority Flow and Precedence

AI Ecosystem defines a strict precedence hierarchy:

1. `copilot-instructions.md` (constitution) — supreme
2. `*.instructions.md` (auto-attached conventions) — high
3. `*.agent.md` (cognition contracts) — medium
4. `*.prompt.md` (task wiring) — low
5. `*.template.md` (structure only) — minimal
6. `.github/context/*.md` (descriptive grounding) — minimal

Higher ranks always win. If the constitution says "never fabricate" and a prompt says "be comprehensive," the constitution prevails. This is not advisory — it is a hard rule.

The end-to-end flow for a typical task:

```
User request
  → Prompt (selects agent, instructions, template, output shape)
    → Agent (sets reasoning posture, tool access, scope)
      → Instructions (domain-specific knowledge, conventions)
        → Procedure (explicit steps, stop conditions, propagation)
          → Template (structural skeleton)
            → Draft artifact
              → Verification checklist (pass/fail)
                → Surgical fixes
```

### Artifact Ownership Table

| Artifact                                 | Owns                                                  | Must NOT Contain                             |
| ---------------------------------------- | ----------------------------------------------------- | -------------------------------------------- |
| `copilot-instructions.md`                | Global epistemic rules and precedence                 | Task steps, output paths, local conventions  |
| `verification-checklist.instructions.md` | Pass/fail enforcement and gating logic (always-on)    | Procedural steps, creative text              |
| `*.agent.md`                             | Tool restrictions, scope, exclusions, stop conditions | Procedures, output locations, persona labels |
| `*.instructions.md`                      | On-demand procedural knowledge                        | Correctness checks, quality bars             |
| `*.prompt.md`                            | Task wiring: agent, instructions, output shape, mode  | Global rules, verification logic             |
| `*.template.md`                          | Headings and placeholders (empty sections allowed)    | Procedural steps, enforcement, policy        |
| `.github/context/*.md`                   | Descriptive grounding (maps, invariants, pointers)    | Hidden policy, procedures, enforcement       |

---

## 6) Advantages of AI Ecosystem

### Reduced Hallucination

By removing completion pressure, bounding evidence scope, centralizing enforcement, and making "Unknown" acceptable, AI Ecosystem addresses the structural causes of hallucination rather than relying on vague instructions like "be accurate."

### Auditability

Every claim in a AI Ecosystem-generated artifact should be traceable to provided evidence. The separation of facts, assumptions, and recommendations makes review mechanical rather than subjective.

### Composability

Agents, instructions, prompts, templates, and procedures are independent and can be mixed and matched. Adding a new document type requires creating a template and a prompt — the existing agent roster and verification infrastructure are reused without modification.

### Institutional Memory Protection

Merged documentation becomes precedent. Precedent becomes onboarding. AI Ecosystem breaks the hallucination cascade by ensuring that only evidence-backed claims survive the pipeline and that gaps remain visible as "Unknown."

### Low Maintenance Footprint (v3)

The v3 consolidation reduced the active maintenance surface by ~60% compared to v1 while preserving all domain expertise in composable instruction files.

> For current artifact counts, see `.github/context/AI Ecosystem-artifact-freshness.md`.

---

## 7) Disadvantages and Limitations

### Overhead for Simple Tasks

AI Ecosystem adds cognitive overhead. For a quick one-off question or a trivial code change, AI Ecosystem is overkill. The system is designed for artifacts that persist and accumulate authority.

### Prompt Sensitivity

AI Ecosystem is a safety rail, not autopilot. If a user writes a prompt that says "be comprehensive" and "fill gaps," they have reintroduced the exact completion pressure AI Ecosystem was designed to eliminate. The user remains part of the safety boundary.

### Runtime Enforcement via Hooks

AI Ecosystem uses Copilot hooks (`.github/hooks/`) for deterministic runtime enforcement. Three hooks are registered in `hooks.json`:

| Hook             | Trigger                             | Timeout | Purpose                                                                         |
| ---------------- | ----------------------------------- | ------- | ------------------------------------------------------------------------------- |
| **SessionStart** | New Copilot session begins          | 10s     | Inject git branch, recent commits, and active workflow state into agent context |
| **PreToolUse**   | Before any Copilot tool execution   | 10s     | Evaluate terminal commands against `command-policy.json`; return allow/ask/deny |
| **PostToolUse**  | After any Copilot file-editing tool | 15s     | Auto-format edited files based on extension                                     |

Each hook has Unix (`.sh`) and Windows (`.ps1`) implementations.

#### PreToolUse — Command Policy Enforcement

The PreToolUse hook is the core safety rail. It intercepts terminal commands before execution and evaluates them against `command-policy.json`:

**Evaluation flow:**

1. Read JSON from stdin (`tool_name` + `tool_input`)
2. If tool is NOT `run_in_terminal`, `execute_command`, or `terminal` → **allow** (non-terminal tools are always safe)
3. Extract command string from `tool_input.command` / `.cmd` / `.input`
4. Match against **deny** patterns first (always blocked):

| Pattern                                           | Reason                                               |
| ------------------------------------------------- | ---------------------------------------------------- |
| `git reset --hard`                                | Destroys uncommitted work and rewrites history       |
| `git push --force` (without `--force-with-lease`) | Can overwrite remote commits                         |
| `git clean -fd`                                   | Deletes untracked files and directories irreversibly |
| `rm -rf /` or `rm -rf ..`                         | Recursive force-delete of root or parent paths       |
| `:>>/dev/sd*`                                     | Overwriting block devices                            |

5. Match against **ask** patterns (require user confirmation):

| Pattern                       | Reason                                           |
| ----------------------------- | ------------------------------------------------ |
| `git push --force-with-lease` | Safer but still rewrites remote history          |
| `git checkout -- .`           | Discards all unstaged changes                    |
| `git stash drop`              | Permanently discards a stash entry               |
| `rm -r`                       | Recursive delete — confirm target is intentional |
| `DROP TABLE/DATABASE/SCHEMA`  | Destructive database DDL                         |
| `TRUNCATE TABLE`              | Irreversible data removal                        |
| `--no-verify`                 | Bypasses safety hooks                            |

6. Default: **allow**

#### PostToolUse — Auto-Format

Triggered after `create_file`, `replace_string_in_file`, `multi_replace_string_in_file`, or `editFiles`:

| Extension                                            | Formatter  | Action                                               |
| ---------------------------------------------------- | ---------- | ---------------------------------------------------- |
| `.py`                                                | `ruff`     | `ruff format <file>` + `ruff check --fix <file>`     |
| `.ts`, `.tsx`, `.js`, `.jsx`, `.json`, `.css`, `.md` | `prettier` | `prettier --write <file>` (fallback: `npx prettier`) |

Non-blocking — formatter unavailability or errors are silently ignored.

#### SessionStart — Context Injection

Injects into the agent's context at session start:

- Current git branch name
- Last 5 commits (one-line format)
- Active workflow state from `.github/runtime/**/*.state.json` (if any), including the workflow posture (`exploration`, `delivery`, `hotfix`)

This ensures agents resume with awareness of the current branch, recent history, and any in-progress orchestrator workflows.

---

## 8) Everyday Usage Guide

### 8.1 Starting a Task

1. **Identify the task type.** Are you producing a document? Reviewing code? Implementing a feature? Analyzing strategy?
2. **Select the prompt or agent.** Browse `.github/prompts/` for a matching `*.prompt.md` (e.g., `spar.prompt.md` for multi-perspective analysis), or invoke an agent directly by name (e.g., `@engineer`, `@reviewer`, `@advisor`). Most document generation tasks can be handled by asking the engineer to fill a specific template.
3. **Provide evidence.** Paste or reference the specific files, snippets, or context the task requires.
4. **Let the pipeline run.** The agent reasons, instructions provide domain knowledge, skills drive the steps, the template provides structure, and the verification checklist gates the output.

### 8.2 When to Skip AI Ecosystem

Not everything needs the full framework:

- **Casual questions** ("what does this function do?") — ask directly.
- **Trivial changes** (rename a variable, fix a typo) — just do it.
- **Exploratory brainstorming** — use `@advisor` without a formal prompt.

Reserve the full pipeline for artifacts that will be merged, shared, or referenced later.

### 8.3 Writing Good Prompts (The Three Knobs)

Every prompt controls three independent dimensions:

| Knob          | What It Governs               | Example                                        |
| ------------- | ----------------------------- | ---------------------------------------------- |
| **Authority** | What may be treated as true   | "Use only provided files; mark unknowns"       |
| **Scope**     | What area is in bounds        | "Only these directories / only these concerns" |
| **Output**    | What shape the artifact takes | "Use template X; leave empty sections"         |

Bad prompts blur these knobs: "Write a complete architecture doc" explodes all three simultaneously. Good AI Ecosystem prompts set each one explicitly.

### 8.4 Dangerous Phrases to Avoid

| Phrase                 | Why It Is Dangerous                    | Safer Alternative                                  |
| ---------------------- | -------------------------------------- | -------------------------------------------------- |
| "Be comprehensive"     | Pressures gap-filling                  | "Cover only what evidence supports; list unknowns" |
| "Ensure correctness"   | Implies the model can verify           | "Mark Unknown if not evidenced"                    |
| "Verify everything"    | Unbounded scope + implied omniscience  | "State whether evidence is present"                |
| "As discussed above"   | Treats conversation memory as evidence | "Use only provided text"                           |
| "Assume typical setup" | Authorises invention                   | "State assumptions explicitly; default to unknown" |

### 8.5 Reviewing AI-Generated Artifacts

When reviewing output produced through AI Ecosystem:

1. **Check for unsupported claims.** Does the artifact assert facts without quoting evidence?
2. **Check for missing "Unknown" sections.** If a template section is filled but no evidence was provided, the content is likely fabricated.
3. **Check assumption labels.** Are assumptions explicitly marked and their impact noted?
4. **Check template adherence.** Does the output follow the specified template structure?
5. **Check scope boundaries.** Does the output stay within the evidence scope declared in the prompt?

---

## 9) Mode Separation

AI Ecosystem defines three operational modes, and every substantial output should declare which one it operates in:

- **Epistemic (truth-first):** For artifacts that become sources of truth — code reviews, security reviews, changelogs. "Unknown" is a correct output. Claims must be evidence-backed.
- **Teaching (understanding-first):** For onboarding docs, architecture explainers, strategy narratives. Analogies and narrative are allowed. Inference is allowed only if labeled as an assumption.
- **Style-only:** Reformatting or rewriting for readability. No new claims may be introduced.

The critical rule: **mode must be declared, not inferred.** Default is Epistemic for any output that could become a source of truth.

---

## 10) File Map

The complete `.github/` directory structure is organized as follows:

```
.github/
├── copilot-instructions.md          # Constitution (supreme authority)
├── agents/                          # Cognition contracts (9 visible + 5 hidden)
│   ├── engineer.agent.md
│   ├── reviewer.agent.md
│   ├── advisor.agent.md
│   ├── elicitator.agent.md
│   ├── sparring.orchestrator.agent.md
│   ├── feature.orchestrator.agent.md
│   ├── test.orchestrator.agent.md
│   ├── qa.orchestrator.agent.md
│   ├── research.orchestrator.agent.md
│   ├── architect.agent.md           # Hidden partner
│   ├── implementation.agent.md      # Hidden partner
│   ├── operations.agent.md          # Hidden partner
│   ├── creative-thinker.agent.md    # Hidden partner
│   └── critical-thinker.agent.md    # Hidden partner
├── instructions/                    # On-demand procedural knowledge (17 files)
│   ├── runbook.instructions.md                 # Always-on (applyTo: **)
│   ├── verification-checklist.instructions.md  # Always-on (applyTo: **)
│   ├── stack-python.instructions.md
│   ├── stack-react.instructions.md
│   ├── testing.instructions.md
│   ├── rbi-pipeline.instructions.md
│   └── ... (11 more)
├── prompts/                         # Task wiring (5 files)
│   ├── compress.prompt.md
│   ├── research.prompt.md
│   ├── save.prompt.md
│   ├── spar.prompt.md
│   └── teach.prompt.md
├── skills/                          # Self-contained composable workflows (11 skills)
│   ├── advanced-elicitation/
│   ├── AI Ecosystem-compression/
│   ├── compaction/
│   ├── distillator/
│   ├── feature-delivery/            # + assets/feature-delivery-report.template.md
│   ├── multi-aspect-code-review/    # + aspects/ (10 aspect definitions) + assets/
│   ├── qa-orchestration/            # + assets/qa-report.template.md
│   ├── readme-gen/                  # + assets/readme.template.md
│   ├── requirements-elicitation/    # + assets/ (canvas + ledger templates)
│   ├── shared/                      # Cross-cutting templates (6 files)
│   ├── tech-debt/                   # + assets/tech-debt-analysis.template.md
│   └── test-orchestration/
├── context/                         # Descriptive grounding (9 files)
│   ├── AI Ecosystem-artifact-freshness.md
│   ├── codebase-context.md
│   ├── pipeline-architecture.md
│   ├── repo-map.md
│   └── ... (5 more)
├── schemas/                         # JSON schemas (3 files)
│   ├── orchestrator-handoff.schema.json
│   ├── subagent-response.schema.json
│   └── workflow-state.schema.json
├── hooks/                           # Runtime enforcement (3 hook events)
│   ├── hooks.json                   # Hook registry
│   ├── command-policy.json          # PreToolUse policy rules
│   ├── pre-tool-use.sh / .ps1
│   ├── post-format.sh / .ps1
│   └── session-start.sh / .ps1
└── runtime/                         # Ephemeral workflow state
    └── feature-state/*.state.json
```

> For current file counts and rosters, see `.github/context/AI Ecosystem-artifact-freshness.md`.
> For individual file listings, browse the directories or run `./scripts/verify-AI Ecosystem-freshness.sh`.

---

## 11) JSON Schemas

AI Ecosystem defines three JSON schemas under `.github/schemas/` that standardize data exchange between orchestrators, subagents, and workflow state persistence.

### 11.1 Orchestrator Handoff Schema (`orchestrator-handoff.schema.json`)

Defines the payload passed between orchestrators in the pipeline chain (feature → test → QA).

| Field                    | Type     | Required | Description                                                             |
| ------------------------ | -------- | -------- | ----------------------------------------------------------------------- |
| `source_orchestrator`    | enum     | Yes      | `"feature-orchestrator"`, `"test-orchestrator"`, or `"qa-orchestrator"` |
| `target_orchestrator`    | enum     | Yes      | Target orchestrator for the handoff                                     |
| `workflow_id`            | string   | Yes      | Unique workflow identifier                                              |
| `delivery_report_path`   | string   | Yes      | Path to the delivery/test/QA report                                     |
| `changed_files`          | string[] | Yes      | Files modified during the phase                                         |
| `acceptance_criteria`    | string[] | No       | Acceptance criteria from the spec                                       |
| `test_directories`       | string[] | No       | Test directories relevant to this delivery                              |
| `verification_summary`   | object   | No       | `{lint, types, tests}` each `"pass"/"fail"/"skipped"`                   |
| `coverage_delta`         | string   | No       | Coverage change description                                             |
| `residual_concerns`      | string[] | No       | Unresolved non-blocking concerns                                        |
| `iteration_log`          | string   | No       | Summary of iteration history                                            |
| `context_digest`         | string   | No       | Compressed context (≤2000 chars)                                        |
| `handoff_timestamp`      | datetime | Yes      | ISO 8601 timestamp                                                      |
| `completion_status`      | enum     | No       | `"full"` (default), `"partial"`, or `"failed"`                          |
| `completed_deliverables` | string[] | No       | What was completed (for partial handoffs)                               |
| `incomplete_reason`      | string   | No       | Why delivery was incomplete                                             |

### 11.2 Workflow State Schema (`workflow-state.schema.json`)

Defines the persistent state file written by orchestrators to `.github/runtime/`. Enables session resumption after interruption.

| Field                       | Type     | Required | Description                                                                                                                                                                                                                                                            |
| --------------------------- | -------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `workflow_id`               | string   | Yes      | Unique workflow identifier                                                                                                                                                                                                                                             |
| `workflow_type`             | enum     | Yes      | `"feature"`, `"test"`, or `"qa"`                                                                                                                                                                                                                                       |
| `posture`                   | enum     | No       | `"exploration"` (default: `"delivery"`), `"delivery"`, `"hotfix"`                                                                                                                                                                                                      |
| `current_phase`             | enum     | Yes      | One of: `intake`, `plan`, `select-slice`, `implement`, `verify`, `review`, `decide`, `remediate`, `post-delivery-docs`, `finalize`, `generate`, `execute`, `review-tests`, `iterate`, `gate-test-suite`, `gate-coverage`, `gate-regression`, `gate-smoke`, `qa-report` |
| `previous_phase`            | string   | No       | Phase transitioned from                                                                                                                                                                                                                                                |
| `owner_agent`               | enum     | Yes      | Owning orchestrator                                                                                                                                                                                                                                                    |
| `branch`                    | string   | No       | Git branch (validated on resume)                                                                                                                                                                                                                                       |
| `spec_path`                 | string   | No       | Path to the feature spec                                                                                                                                                                                                                                               |
| `slice_plan`                | array    | No       | Array of `{index, objective, files_in_scope[], status}`                                                                                                                                                                                                                |
| `current_slice_index`       | int      | No       | Active slice                                                                                                                                                                                                                                                           |
| `changed_files`             | string[] | No       | Accumulated changed files                                                                                                                                                                                                                                              |
| `verification_status`       | object   | No       | `{lint, types, tests}` each `"pass"/"fail"/"pending"/"skipped"`                                                                                                                                                                                                        |
| `open_findings`             | array    | No       | Array of `{id, severity, description, source_phase}` — severity: `"blocking"/"non-blocking"/"needs-human-decision"`                                                                                                                                                    |
| `remediation_count`         | int      | No       | Current remediation iteration count                                                                                                                                                                                                                                    |
| `max_remediations`          | int      | No       | Budget limit                                                                                                                                                                                                                                                           |
| `last_transition_reason`    | string   | No       | Human-readable reason for last phase change                                                                                                                                                                                                                            |
| `escalation_status`         | enum     | No       | `"none"` (default), `"paused"`, `"stopped"`, `"needs-human"`                                                                                                                                                                                                           |
| `residual_concerns`         | string[] | No       | Accumulated non-blocking concerns                                                                                                                                                                                                                                      |
| `created_at` / `updated_at` | datetime | Yes      | Timestamps                                                                                                                                                                                                                                                             |

### 11.3 Subagent Response Schema (`subagent-response.schema.json`)

Normalizes the response format from orchestrator subagent invocations (e.g., Explore, reviewer, advisor).

| Field              | Type                 | Required | Description                                |
| ------------------ | -------------------- | -------- | ------------------------------------------ |
| `summary`          | string (≤1000 chars) | Yes      | Self-contained conclusion (≤200 words)     |
| `findings`         | array                | Yes      | Array of normalized findings (see below)   |
| `files_referenced` | string[]             | No       | Files the subagent examined                |
| `status`           | enum                 | Yes      | `"pass"`, `"fail"`, or `"needs-attention"` |
| `dissenting_view`  | string               | No       | Minority opinion if applicable             |

**Finding schema** (each entry in `findings[]`):

| Field            | Type    | Description                                           |
| ---------------- | ------- | ----------------------------------------------------- |
| `id`             | string  | Sequential ID (e.g., `ARCH-001`)                      |
| `title`          | string  | Short finding title                                   |
| `severity`       | enum    | `"critical"`, `"high"`, `"medium"`, `"low"`, `"info"` |
| `category`       | string  | Review domain (e.g., "Architecture", "Security")      |
| `evidence`       | string  | Support for the finding                               |
| `recommendation` | string  | Suggested action                                      |
| `confidence`     | enum    | `"high"`, `"medium"`, `"low"`                         |
| `blocking`       | boolean | Whether this blocks progress                          |

---

## 12) Governance Scripts

The `scripts/` directory contains verification, validation, and maintenance scripts that support the AI Ecosystem governance lifecycle. These scripts enforce structural integrity outside of Copilot sessions — in CI, pre-push hooks, and manual audits.

### 12.1 Script Inventory

| Script                             | Purpose                                                             | Trigger                   | Exit Codes               |
| ---------------------------------- | ------------------------------------------------------------------- | ------------------------- | ------------------------ |
| `pre-push-check.sh`                | Fast pre-push gate: ruff lint + pyright type-check on changed files | Git pre-push hook (auto)  | 0=OK, non-zero=fail      |
| `setup-hooks.sh`                   | Install git pre-push hook into `.git/hooks/`                        | Manual (once after clone) | 0=OK                     |
| `verify-AI Ecosystem-freshness.sh` | Validate AI Ecosystem artifact counts against freshness table       | CI gate / manual          | 0=OK, 1=mismatch         |
| `verify-feature-slice.sh`          | Full verification gate: lint + types + tests for API and/or web     | CI / manual               | 0=OK, 1=fail             |
| `verify-instruction-conflicts.sh`  | Detect overlapping `applyTo` patterns across instructions           | Manual                    | 0=always (informational) |
| `generate-repo-map.sh`             | Auto-generate AI Ecosystem artifact inventory map                   | Manual / `--check` in CI  | 0=OK, 1=stale            |
| `capture-prompt-baseline.sh`       | Create prompt metadata snapshots for regression analysis            | Manual                    | 0=OK                     |
| `gen_model_list.py`                | Generate OpenRouter model table from API dump                       | Manual                    | 0=OK                     |
| `generate_research_report.py`      | Run research pipeline standalone                                    | Manual                    | 0=OK                     |

### 12.2 Pre-Push Gate (`pre-push-check.sh`)

The primary CI-prevention script. Installed as a git pre-push hook via `setup-hooks.sh`.

**Two-tier verification:**

1. **Changed files only** — ruff lint + pyright type-check on files changed vs. `origin/master`
2. **Full scope** — pyright on entire `app/` directory (mirrors CI behavior)

Tests are excluded from the pre-push check — they run in CI via pytest. This keeps pre-push fast (5–10 seconds).

The dual-scope approach was introduced after a CI failure where changed-file-only pyright missed a pre-existing type error exposed by a new import.

### 12.3 AI Ecosystem Freshness Validator (`verify-AI Ecosystem-freshness.sh`)

Three modes of operation:

| Mode      | Command                                             | What It Does                                                                                                                                                               |
| --------- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Check** | `./scripts/verify-AI Ecosystem-freshness.sh`        | Count artifacts on disk, compare against `AI Ecosystem-artifact-freshness.md`                                                                                              |
| **Fix**   | `./scripts/verify-AI Ecosystem-freshness.sh --fix`  | Update freshness table with actual counts + today's timestamp                                                                                                              |
| **Lint**  | `./scripts/verify-AI Ecosystem-freshness.sh --lint` | Structural audit: applyTo glob validation, cross-reference validation, orphan detection, agent reference validation, skill context path validation, JSON schema validation |

The `--lint` mode is the most thorough — it validates that every `applyTo` pattern matches at least one file, every `.github/` cross-reference points to an existing file, and no agents or instructions are orphaned.

### 12.4 Feature Slice Verifier (`verify-feature-slice.sh`)

Runs the full verification gate independently for backend and/or frontend:

| Component               | Step 1 (Lint)  | Step 2 (Types) | Step 3 (Tests)        |
| ----------------------- | -------------- | -------------- | --------------------- |
| **API** (`divical-api`) | `ruff check .` | `pyright app/` | `pytest tests/ -x -q` |
| **Web** (`divical-web`) | `eslint src/`  | `tsc --noEmit` | `npm test -- --run`   |

Usage: `scripts/verify-feature-slice.sh api`, `scripts/verify-feature-slice.sh web`, or `scripts/verify-feature-slice.sh both`.

### 12.5 Instruction Conflict Detector (`verify-instruction-conflicts.sh`)

Identifies "overlap zones" where 3+ instructions match the same source files. This prevents accidental authority conflicts where multiple instructions compete.

Process:

1. Scan all `*.instructions.md` for `applyTo` frontmatter
2. Expand brace patterns, match against source files via `git ls-files`
3. Build reverse map: source file → matching instructions
4. Report zones with 3+ overlapping instructions

Always-on instructions (`applyTo: **`) are noted separately and not counted toward overlap thresholds.

---

## 13) RBI Pipeline Data Contracts

The Research → Backtest → Incubate (RBI) pipeline uses Pydantic models and SQLAlchemy ORM models as its data contracts. Changes to these contracts require coordinated updates across the pipeline per the change-propagation rules in `rbi-pipeline.instructions.md`.

### 13.1 Research Output Contracts

**`ResearchAgentOutput`** (`app/services/research/contracts/agent_output.py`):

| Field                | Type      | Constraints     |
| -------------------- | --------- | --------------- |
| `hypothesis`         | str       | `min_length=10` |
| `mechanism`          | str       | `min_length=10` |
| `required_inputs`    | list[str] |                 |
| `assumptions`        | list[str] |                 |
| `expected_edge`      | str       | `min_length=5`  |
| `risk_factors`       | list[str] |                 |
| `evaluation_plan`    | str       | `min_length=5`  |
| `unsupported_claims` | list[str] |                 |
| `confidence`         | float     | `0.0 – 1.0`     |
| `citations`          | list[str] |                 |

### 13.2 Strategy Specification Contracts

**`StrategySpec`** (`app/services/research/contracts/strategy_spec.py`):

| Field                      | Type             | Constraints                                             |
| -------------------------- | ---------------- | ------------------------------------------------------- |
| `name`                     | str              | `1–200 chars`                                           |
| `hypothesis`               | str              | `20–2000 chars`                                         |
| `entry_logic`              | `EntryLogicType` | `FIXED_OFFSET`, `SMOOTHED_SIGNAL`, `PERCENTILE_TRIGGER` |
| `exit_logic`               | `ExitLogicType`  | `FIXED_OFFSET`, `TRAILING_STOP`, `PERCENTILE_TRIGGER`   |
| `offset_policy`            | `OffsetPolicy`   | Buy: `[-30, 0]`, Sell: `[0, 45]`, max ≥ min validated   |
| `ticker_filters`           | list[str]        |                                                         |
| `factor_modifiers`         | list[str]        |                                                         |
| `risk_gates`               | list[str]        |                                                         |
| `position_sizing`          | str              | Default: `"equal_weight"`                               |
| `required_inputs`          | list[str]        |                                                         |
| `unsupported_requirements` | list[str]        |                                                         |
| `confidence`               | float            | `0.0 – 1.0`                                             |
| `citations`                | list[str]        |                                                         |

### 13.3 Prompt Loading Contracts

**`PipelinePrompts`** (`app/services/research/prompt_loader.py`):

| Field              | Type                  | Source                                                     |
| ------------------ | --------------------- | ---------------------------------------------------------- |
| `research`         | str                   | `prompts/research.md` (required)                           |
| `codebase_summary` | str                   | `prompts/codebase-summary.md` (required)                   |
| `feasibility`      | str                   | `prompts/feasibility.md` (required)                        |
| `consensus`        | str                   | `prompts/consensus.md` (required)                          |
| `analysts`         | list[`AnalystPrompt`] | Auto-discovered from `prompts/analysts/*.md` (≥1 required) |

Each `AnalystPrompt` has: `name`, `system`, `prompt`, `source_path`.

### 13.4 Proposal Extraction Contracts

**Allowed proposal keys** (`app/services/research/consensus_to_proposals.py`):

```
title, rationale, expected_improvement, risk_assessment, tickers,
buy_offset_min, buy_offset_max, sell_offset_min, sell_offset_max,
confidence, tax_constraints, execution_filters, risk_flags
```

Optional structured fields:

- `tax_constraints`: `{requires_qualified: bool, min_hold_days: int, tax_sensitivity: "LOW"/"MEDIUM"/"HIGH"}`
- `execution_filters`: `{min_volume: int, max_spread_bps: int, avoid_illiquid_dates: bool}`
- `risk_flags`: list of strings (e.g., `["sector_concentration", "interest_rate_sensitivity", "credit_risk"]`)

### 13.5 Database Models

**`StrategyProposal`** (`app/models/database.py`):

| Column                 | Type         | Description                                                                                              |
| ---------------------- | ------------ | -------------------------------------------------------------------------------------------------------- |
| `id`                   | UUID         | Primary key                                                                                              |
| `title`                | String(200)  | Proposal title                                                                                           |
| `source`               | String(50)   | `"academic"`, `"news"`, `"synthetic"`, `"combined"`                                                      |
| `rationale`            | Text         |                                                                                                          |
| `parameters`           | JSON         | Extracted strategy parameters                                                                            |
| `expected_improvement` | Text         |                                                                                                          |
| `risk_assessment`      | Text         |                                                                                                          |
| `swarm_votes`          | JSON         | List of model votes                                                                                      |
| `consensus_decision`   | String       | `"pending"`, `"approved"`, `"rejected"`, `"needs_modification"`                                          |
| `consensus_confidence` | Float        | 0–1                                                                                                      |
| `aggregate_scores`     | JSON         | Aggregated voting scores                                                                                 |
| `pipeline_run_id`      | String(36)   | FK to pipeline run                                                                                       |
| `status`               | String(20)   | `"proposed"`, `"approved"`, `"backtesting"`, `"incubating"`, `"implemented"`, `"rejected"`, `"archived"` |
| `created_at`           | DateTime(tz) |                                                                                                          |

**`DiscoveredStrategy`** (`app/models/database.py`):

| Column                  | Type       | Description                                              |
| ----------------------- | ---------- | -------------------------------------------------------- |
| `id`                    | UUID       | Primary key                                              |
| `ticker`                | String(10) | BDC ticker (indexed)                                     |
| `buy_offset`            | int        | Negative days before ex-date (−15 to −1)                 |
| `sell_offset`           | int        | Positive days after ex-date (1 to 20)                    |
| `expectancy`            | float      | Mean return per trade                                    |
| `sharpe_ratio`          | float      | Risk-adjusted return                                     |
| `sortino_ratio`         | float      | Downside-only risk                                       |
| `max_drawdown`          | float      | Worst drawdown                                           |
| `win_rate`              | float      | Profitable trade percentage                              |
| `total_trades`          | int        |                                                          |
| `avg_return_pct`        | float      | Expectancy as percentage                                 |
| `in_sample_return`      | float      | Sum of all returns                                       |
| `out_of_sample_return`  | float      | OOS validation result                                    |
| `oos_passed`            | bool       | Default: False                                           |
| `regime_state`          | String(50) | `BULL`, `BEAR`, `HIGH_VOL`, `RATE_SHOCK`                 |
| `hmm_state`             | int        | HMM state (0–2)                                          |
| `status`                | String(20) | `"candidate"`, `"validated"`, `"promoted"`, `"rejected"` |
| `state`                 | String(40) | `StrategyState` enum value                               |
| `strategy_candidate_id` | String(42) | Unique, indexed                                          |
| `experiment_id`         | String(40) | FK to experiment, indexed                                |

**`IncubationObservation`** (`app/models/experiments.py`):

| Column                     | Type          | Description       |
| -------------------------- | ------------- | ----------------- |
| `id`                       | int           | Auto-increment PK |
| `incubation_id`            | String(60)    | Indexed           |
| `strategy_candidate_id`    | String(60)    | Indexed           |
| `observation_date`         | date          |                   |
| `simulated_entry_date`     | date          |                   |
| `simulated_exit_date`      | date          |                   |
| `predicted_buy_offset`     | int           |                   |
| `predicted_sell_offset`    | int           |                   |
| `predicted_return`         | Decimal(12,6) |                   |
| `realized_return`          | Decimal(12,6) |                   |
| `confidence_at_prediction` | float         |                   |
| `confidence_drift`         | float         |                   |
| `ticker`                   | String(10)    |                   |
| `entry_price`              | float         |                   |
| `exit_price`               | float         |                   |
| `dividend_amount`          | float         |                   |
| `gross_return`             | float         |                   |
| `net_return`               | float         |                   |
| `profitable`               | bool          |                   |
| `skipped`                  | bool          | Default: False    |
| `skip_reason`              | String(200)   |                   |

**`StrategyStateTransition`** (`app/models/experiments.py`):

| Column                  | Type       | Description                                  |
| ----------------------- | ---------- | -------------------------------------------- |
| `id`                    | int        | Auto-increment PK                            |
| `strategy_candidate_id` | String(60) | Indexed                                      |
| `from_state`            | String(50) | Previous `StrategyState`                     |
| `to_state`              | String(50) | New `StrategyState`                          |
| `actor`                 | String(50) | e.g., `"RBIPipeline"`, `"IncubationMonitor"` |
| `rationale`             | Text       | Reason for transition                        |
| `timestamp`             | DateTime   |                                              |
| `incubation_trades`     | int        | Metric snapshot (nullable)                   |
| `incubation_win_rate`   | float      | Metric snapshot (nullable)                   |
| `incubation_expectancy` | float      | Metric snapshot (nullable)                   |
| `incubation_sharpe`     | float      | Metric snapshot (nullable)                   |

**`ProvenanceEntry`** (`app/models/experiments.py`) — Cryptographic audit trail:

| Column                  | Type       | Description                                                                                                                                                       |
| ----------------------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                    | int        | Auto-increment PK                                                                                                                                                 |
| `strategy_candidate_id` | String(60) | Indexed                                                                                                                                                           |
| `entry_type`            | String(50) | `"origin"`, `"backtest_pass"`, `"backtest_fail"`, `"gate_decision"`, `"regime_tag"`, `"incubation_obs"`, `"state_transition"`, `"drift_detected"`, `"meta_label"` |
| `actor`                 | String(80) | Service/worker name                                                                                                                                               |
| `payload`               | JSON       | Structured decision data                                                                                                                                          |
| `parent_hash`           | String(64) | SHA-256 of previous entry (chain integrity)                                                                                                                       |
| `content_hash`          | String(64) | SHA-256 of this entry                                                                                                                                             |
| `pipeline_run_id`       | String(60) | Indexed                                                                                                                                                           |
| `created_at`            | DateTime   |                                                                                                                                                                   |

### 13.6 Strategy State Machine

**`StrategyState`** enum (`app/models/strategy_lifecycle.py`):

```
PROPOSED → APPROVED_FOR_BACKTEST → BACKTESTING → BACKTEST_PASSED → INCUBATING → INCUBATION_PASSED → PROMOTED
                                              ↘ BACKTEST_FAILED → ARCHIVED / PROPOSED (retry)
                                                                          INCUBATION_FAILED → ARCHIVED / PROPOSED (retry)
                                                                          PROMOTED → ARCHIVED / INCUBATING (re-incubate on drift)
```

Legal transitions enforced by `transition()` function — raises `ValueError` on illegal transitions and records `StrategyStateTransition` to the database.

### 13.7 Quality Gates & Financial Constants

| Constant             | Value        | Description                           |
| -------------------- | ------------ | ------------------------------------- |
| `TRANSACTION_COST`   | 0.001 (0.1%) | Round-trip transaction cost           |
| `DIVIDEND_TAX_RATE`  | 0.25         | Default dividend tax rate             |
| `QUALIFIED_TAX_RATE` | 0.15         | Qualified dividend tax rate           |
| `MIN_HOLD_DAYS`      | 61           | Days for qualified dividend treatment |
| `MIN_EXPECTANCY`     | 0.005 (0.5%) | Minimum average return per trade      |
| `MIN_SHARPE`         | 0.5          | Minimum Sharpe ratio                  |
| `MAX_DRAWDOWN`       | −0.10 (−10%) | Maximum acceptable drawdown           |
| `MAX_DD_OOS`         | −0.15 (−15%) | Maximum drawdown for OOS (relaxed)    |
| `MIN_TRADES`         | 12           | Minimum number of trades              |
| `OOS_RATIO`          | 0.3 (30%)    | Out-of-sample holdout ratio           |
| `BUY_OFFSET_RANGE`   | (−15, −2)    | Business days before ex-date          |
| `SELL_OFFSET_RANGE`  | (1, 20)      | Business days after ex-date           |

**Quality gate function** (`_passes_quality_gates`):

```
expectancy >= 0.005 AND sharpe_ratio >= 0.5 AND max_drawdown >= -0.10 AND total_trades >= 12
```

**OOS validation** (`_validate_oos`):

```
expectancy > 0 AND max_drawdown >= -0.15
```

### 13.8 Backtest Result Structure

The `_backtest_single()` function returns a dict with this shape:

| Key                      | Type       | Description                              |
| ------------------------ | ---------- | ---------------------------------------- |
| `ticker`                 | str        | BDC ticker symbol                        |
| `buy_offset`             | int        | Days before ex-date                      |
| `sell_offset`            | int        | Days after ex-date                       |
| `expectancy`             | float      | Mean return per trade                    |
| `sharpe_ratio`           | float      | Risk-adjusted return                     |
| `sortino_ratio`          | float      | Downside-only risk                       |
| `max_drawdown`           | float      | Worst drawdown                           |
| `win_rate`               | float      | Profitable trade percentage              |
| `total_trades`           | int        | Number of trades                         |
| `avg_return_pct`         | float      | Expectancy as percentage                 |
| `in_sample_return`       | float      | Sum of all returns                       |
| `out_of_sample_return`   | float      | OOS validation result                    |
| `oos_passed`             | bool       | OOS gate result                          |
| `dsr`                    | float      | Dividend Sharpe Ratio                    |
| `regime_state`           | str / None | `BULL`, `BEAR`, `HIGH_VOL`, `RATE_SHOCK` |
| `hmm_state`              | int / None | HMM state (0–2)                          |
| `pipeline_run_id`        | str        | Pipeline run identifier                  |
| `meta_label_probability` | float      | MetaLabeler confidence (0–1)             |

### 13.9 Change Propagation Rules

Per `rbi-pipeline.instructions.md`, changes to these contracts require coordinated updates:

| What Changed                | Must Also Update                                        |
| --------------------------- | ------------------------------------------------------- |
| Quality gate thresholds     | `proposal_backtester.py`, RBI dashboard                 |
| `_backtest_single()` schema | All validation/testing code                             |
| `DiscoveredStrategy` fields | Alembic migrations, incubation monitor, API serializers |
| `StrategyState` enum        | `strategy_lifecycle.py`, frontend displays              |
| Prompt files in `prompts/`  | PromptLoader validation                                 |

---

## 14) Evolution History

### v1 (2026-03-06) — Initial Architecture

- 16 specialized agents, each occupying a distinct cognitive lane
- Agent Router for intent classification
- Over 20 prompts, 16 templates, 5 procedures
- Comprehensive but high maintenance burden

### v2 (2026-03-10) — Consolidation Plan

- Identified that most agents shared tool sets and differed only in domain knowledge
- Proposed extracting domain knowledge into instruction files
- Planned agent consolidation

### v3 (2026-03-14) — Current State

- Consolidated to a small set of visible agents + hidden partners for multi-perspective analysis
- Instruction files carry all domain expertise via `applyTo` patterns
- ~60% reduction in maintenance surface
- Skills added as composable workflow bundles
- Post-implementation verification gate mandatory (ruff + pyright + pytest)
- Deterministic hook enforcement (PreToolUse command blocking)
- Externalized review aspects with normalized finding schema
- Freshness table and pointer-pattern governance to prevent doc drift
- `scripts/verify-AI Ecosystem-freshness.sh` automates freshness validation

### v3 Maintenance (2026-03-29)

- Split `AI Ecosystem-governance.instructions.md` into runtime (always-on, `applyTo: "**"`) + authoring (scoped to `.github/**`)
- Deleted `session-today.instructions.md` (obsolete — replaced by VS Code memory system)
- Created `save.prompt.md` for curating conversation learnings into persistent memory
- Full ecosystem audit: fixed missing prompt frontmatter, narrowed over-broad `applyTo` scopes for stack instructions, relocated repo-specific prompt to `divical-api/prompts/`
- Documented Explore subagent (VS Code built-in) in agent roster
- Archived 5 dead-weight files from v1 consolidation

### v4 Consolidation (2026-04-08)

- Merged `AI Ecosystem-governance.instructions.md` unique rules back into `copilot-instructions.md` (eliminated duplication)
- Demoted `architecture-workflows.instructions.md` to `.github/context/pipeline-architecture.md` (reference material, not behavioral rules)
- Merged `stack-database.instructions.md` into `stack-python.instructions.md` (eliminated ~70% overlap)
- Merged `test-aaa-pattern.instructions.md` + `test-strategy.instructions.md` → `testing.instructions.md`
- Eliminated `code-analysis.instructions.md` (default LLM behavior, no unique value)
- Compressed `rbi-pipeline.instructions.md` from 125 to ~45 lines (kept contracts + constants, moved reference to context)
- Compressed `verification-checklist.instructions.md` and `runbook.instructions.md`
- Moved AI Ecosystem-specific runbook entries to `AI Ecosystem-authoring.instructions.md`
- Narrowed `documentation.instructions.md` scope from `**/*.md` to `docs/**/*.md,**/README.md,**/ADR*`
- Net: 21 → 16 instruction files, ~35% line reduction, ~66% backend edit session reduction

### v3 Expansion (2026-04-04)

- Added test.orchestrator, qa.orchestrator, research.orchestrator (visible) and creative-thinker, critical-thinker (hidden)
- Added Claude Opus 4.6 to research pipeline Stage 1 fan-out
- Removed AlphaVantage as a provider (FMP + Mock only)
- Added orchestrator handoff protocol: feature.orchestrator → test.orchestrator → qa.orchestrator
- Test pipeline: 5-phase self-healing loop with assertion policy (locked vs flexible) and financial-logic review aspect
- QA pipeline: 4-gate sequential validation with sparring escalation

### v3 Handoff + Remediation Update (2026-04-05)

- Added explicit `handoffs:` frontmatter fields to feature.orchestrator and test.orchestrator agent files for VS Code Autopilot chaining
- Handoff configuration: `send: true` (auto-submit in Autopilot), `model: Claude Opus 4.6 (copilot)` (explicit model for handoff target)
- QA orchestrator upgraded from diagnostic-only to diagnostic + auto-remediation:
  - Removed "never fixes code" constraint
  - Added remediation loop (max 3 iterations): identify failures → delegate fixes to engineer → re-run failed gates
  - New verdict types: PASS (REMEDIATED), PASS WITH CAVEATS (REMEDIATED)
  - Remediation exclusions: coverage warnings (non-blocking), `needs-human-decision` sparring findings, architectural issues
  - QA procedure updated with Step 8 (Auto-Remediation) and Step 9 (Final Verdict)

> For current artifact counts, see `.github/context/AI Ecosystem-artifact-freshness.md`.

---

## 15) Summary

AI Ecosystem is an engineering architecture for governing AI-assisted work. It separates cognition (agents) from domain knowledge (instructions), execution (procedures and prompts), and enforcement (verification checklist and constitution). Each artifact type has a single responsibility, authority flows through a strict hierarchy, and missing evidence is surfaced rather than hidden.

The v3 architecture achieves this with a deliberately small footprint. The system makes honesty cheap and fabrication expensive — not by asking the model to "be honest," but by structuring the environment so that truthful, bounded outputs are the path of least resistance.

> For current artifact counts and roster, see `.github/context/AI Ecosystem-artifact-freshness.md`.

> Creativity belongs in cognition. Discipline belongs in artifacts. Authority must not leak.
