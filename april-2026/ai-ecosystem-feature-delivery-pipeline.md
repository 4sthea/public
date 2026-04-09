# AI Ecosystem Feature Delivery Pipeline: Research → Implementation

> **Last Updated:** April 9, 2026

## Overview

There are **two distinct "swarm" concepts** in this codebase:

1. **The RBI Research Pipeline** (automated, runs in `divical-api` via ARQ cron / GitHub Actions) — this is the "research swarm" that produces a consensus document.
2. **The AI Ecosystem agent orchestration** (VS Code agents) — this is the sequence of orchestrators that turn research output into implemented, tested, reviewed code.

**Manual touch points:** Only **two** in the entire pipeline — reading the consensus document and reviewing the generated feature specification. Everything else runs autonomously.

**Governance infrastructure:** The pipeline is supported by Copilot hooks for runtime enforcement, governance scripts for CI and pre-push validation, JSON schemas for inter-orchestrator data exchange, and RBI pipeline data contracts for research-to-backtest-to-incubation state management.

---

## End-to-End Pipeline Diagram

```mermaid
flowchart TD
    classDef autonomous fill:#2d6a4f,stroke:#1b4332,color:#fff
    classDef manual fill:#e76f51,stroke:#9b2226,color:#fff
    classDef pause fill:#e9c46a,stroke:#f4a261,color:#000
    classDef orchestrator fill:#264653,stroke:#1d3557,color:#fff
    classDef agent fill:#457b9d,stroke:#1d3557,color:#fff
    classDef output fill:#a8dadc,stroke:#457b9d,color:#000

    %% ===== STAGE 0: Research Pipeline =====
    subgraph S0["STAGE 0 — Research Pipeline (Server-Side, Fully Autonomous)"]
        direction TB
        S0_trigger["⚡ Trigger: ARQ Cron (every 3 days)<br/>or POST /api/research/trigger"]:::autonomous
        S0_prompts["Stage 0: Prompt Loading<br/>prompt_loader.py → PipelinePrompts"]:::autonomous
        S0_consol["Stage 1: 2-Step Consolidation<br/>6 LLMs + Claude Opus 4.6 independently<br/>→ Claude 4.6 synthesizes all"]:::autonomous
        S0_feasib["Stage 2: Feasibility<br/>Tavily web search + Claude"]:::autonomous
        S0_swarm["Stage 3: Analyst Swarm + Consensus<br/>Per-analyst model routing<br/>→ Claude as 'senior research director'"]:::autonomous
        S0_extract["Stage 4: Proposal Extraction<br/>LLM → JSON → StrategyProposal rows"]:::autonomous
        S0_out1(["📄 consensus.md"]):::output
        S0_out2(["🗃️ StrategyProposal DB rows<br/>status=approved"]):::output

        S0_trigger --> S0_prompts --> S0_consol --> S0_feasib --> S0_swarm --> S0_extract
        S0_swarm --> S0_out1
        S0_extract --> S0_out2
    end

    %% ===== STAGE 1: Research-to-Spec Orchestrator (Autonomous Chain) =====
    subgraph S1["STAGE 1 — Research-to-Spec Orchestrator (Autonomous)"]
        direction TB
        S1_you["👤 YOU read consensus doc<br/>and trigger research-to-spec prompt"]:::manual

        S1_intake["Phase 1 — Intake<br/>Read consensus + codebase summary<br/>+ domain knowledge"]:::orchestrator

        S1_spar["🤖 sparring.orchestrator<br/>Multi-perspective analysis<br/>Creative approaches, risks,<br/>assumptions, feasibility"]:::agent

        S1_cr["🤖 reviewer<br/>Multi-aspect review of proposals<br/>Breaking changes, security, perf"]:::agent

        S1_se["🤖 engineer<br/>Produce ordered change list<br/>Test strategy, rollback plan"]:::agent
        S1_impl_out(["📄 implementation-plan-YYYY-MM-DD.md"]):::output

        S1_tp["🤖 advisor<br/>Detailed plan: phases, deps,<br/>verification criteria, slicing"]:::agent

        S1_se2["🤖 engineer<br/>Generate feature specification<br/>from template + detailed plan"]:::agent
        S1_spec_out(["📄 feature-spec-YYYY-MM-DD.md"]):::output

        S1_review["👤 MANUAL REVIEW<br/>Approve / Revise / Stop"]:::manual
        S1_revision{{"⏸ Revision loop<br/>(max 3 cycles)"}}:::pause

        S1_you --> S1_intake --> S1_spar --> S1_cr --> S1_se --> S1_impl_out
        S1_impl_out --> S1_tp --> S1_se2 --> S1_spec_out --> S1_review
        S1_review -->|"Revise"| S1_revision
        S1_revision --> S1_se2
    end

    %% ===== STAGE 2: Feature Orchestrator =====
    subgraph S2["STAGE 2 — Feature Orchestrator (10 Phases)"]
        direction TB
        S2_invoke["⚙️ feature.orchestrator<br/>auto-invoked after spec approval"]:::autonomous

        S2_P1["Phase 1 — Intake<br/>Orchestrator reads spec<br/>Extracts scope & confidence"]:::orchestrator
        S2_P1_pause{{"⏸ Pause if<br/>confidence < 80%"}}:::pause

        S2_P2["Phase 2 — Plan<br/>🤖 advisor<br/>Slice decomposition, risks, test strategy"]:::agent
        S2_P2_pause{{"⏸ Pause if unresolved<br/>question blocks slicing"}}:::pause

        S2_P3["Phase 3 — Select Slice<br/>Orchestrator picks next slice<br/>Defines brief & boundaries"]:::orchestrator
        S2_P3_pause{{"⏸ Pause after<br/>every 5 slices"}}:::pause

        S2_P4["Phase 4 — Implement<br/>🤖 engineer<br/>✋ You approve each file edit"]:::agent
        S2_P5["Phase 5 — Verify<br/>🤖 engineer<br/>ruff + pyright + pytest<br/>✋ You approve each command"]:::agent

        S2_P6["Phase 6 — Review<br/>🤖 reviewer<br/>Multi-aspect adversarial review<br/>Blocking vs non-blocking findings"]:::agent

        S2_P7["Phase 7 — Decide<br/>Orchestrator evaluates results"]:::orchestrator
        S2_P7_pause{{"⏸ Pause if needs-human-decision<br/>or spec drift detected"}}:::pause

        S2_P8["Phase 8 — Remediate<br/>🤖 engineer<br/>Surgical fixes for blockers only<br/>(max 3-5 iterations)"]:::agent

        S2_P9["Phase 9 — Post-Delivery Docs<br/>🤖 engineer (gated)<br/>Doc updates + AI Ecosystem audit (detect only)<br/>Skipped if no evidence"]:::agent
        S2_P10["Phase 10 — Finalize<br/>Orchestrator confirms all slices done"]:::orchestrator
        S2_out(["📄 Feature Delivery Report"]):::output

        S2_invoke --> S2_P1
        S2_P1 --> S2_P1_pause
        S2_P1_pause -->|"OK"| S2_P2
        S2_P2 --> S2_P2_pause
        S2_P2_pause -->|"OK"| S2_P3
        S2_P3 --> S2_P3_pause
        S2_P3_pause -->|"OK"| S2_P4
        S2_P4 --> S2_P5
        S2_P5 -->|"fail"| S2_P4
        S2_P5 -->|"pass"| S2_P6
        S2_P6 --> S2_P7
        S2_P7 --> S2_P7_pause
        S2_P7_pause -->|"blocking findings"| S2_P8
        S2_P8 --> S2_P5
        S2_P7_pause -->|"all clear<br/>more slices"| S2_P3
        S2_P7_pause -->|"all clear<br/>no more slices"| S2_P9
        S2_P9 --> S2_P10
        S2_P10 --> S2_out
    end

    %% ===== STAGE 3: Test Orchestrator =====
    subgraph S3["STAGE 3 — Test Orchestrator (Self-Healing Loop)"]
        direction TB
        S3_invoke["⚙️ test.orchestrator<br/>auto-invoked after delivery"]:::autonomous
        S3_scope["Phase 1 — Scope<br/>Extract testable surfaces<br/>from delivery report"]:::orchestrator
        S3_gen["Phase 2 — Generate<br/>🤖 engineer<br/>Unit + integration + backtest tests<br/>✋ You approve edits"]:::agent
        S3_exec["Phase 3 — Execute<br/>🤖 engineer<br/>pytest + coverage<br/>✋ You approve commands"]:::agent
        S3_review["Phase 4 — Review<br/>🤖 reviewer<br/>Test correctness + financial-logic"]:::agent
        S3_heal["Phase 5 — Heal<br/>🤖 engineer<br/>Fix blocking findings<br/>(max 5 iterations)"]:::agent
        S3_out(["📄 Test Generation Report<br/>+ handoff block for QA"]):::output

        S3_invoke --> S3_scope --> S3_gen --> S3_exec
        S3_exec -->|"pass"| S3_review
        S3_review -->|"blocking"| S3_heal
        S3_heal --> S3_exec
        S3_review -->|"clear"| S3_out
    end

    %% ===== STAGE 4: QA Orchestrator =====
    subgraph S4["STAGE 4 — QA Orchestrator (4-Gate Validation + Auto-Remediation)"]
        direction TB
        S4_invoke["⚙️ qa.orchestrator<br/>auto-invoked after tests"]:::autonomous
        S4_G1["Gate 1: Test Suite<br/>ruff + pyright + pytest"]:::orchestrator
        S4_G2["Gate 2: Coverage<br/>Diff-coverage ≥ 50%<br/>Warn < 80%"]:::orchestrator
        S4_G3["Gate 3: Regression<br/>Baseline comparison<br/>(or SKIPPED if none)"]:::orchestrator
        S4_G4["Gate 4: Smoke<br/>Import check + config load<br/>+ route registration"]:::orchestrator
        S4_sparring{{"Sparring Escalation?<br/>>3 failures at boundary<br/>or systematic gaps"}}:::pause
        S4_spar["🤖 sparring.orchestrator<br/>Multi-perspective design analysis<br/>(max 2x per run)"]:::agent
        S4_report["📄 QA Report Generation"]:::orchestrator
        S4_remediate{{"Any gate FAIL?"}}:::pause
        S4_fix["🤖 engineer<br/>Fix gate failures<br/>(max 3 iterations)"]:::agent
        S4_rerun["Re-run failed gates only"]:::orchestrator
        S4_out(["📄 Final QA Report<br/>PASS / PASS WITH CAVEATS /<br/>PASS (REMEDIATED) / FAIL"]):::output

        S4_invoke --> S4_G1 --> S4_G2 --> S4_G3 --> S4_G4 --> S4_sparring
        S4_sparring -->|"triggered"| S4_spar --> S4_report
        S4_sparring -->|"not triggered"| S4_report
        S4_report --> S4_remediate
        S4_remediate -->|"yes"| S4_fix --> S4_rerun
        S4_rerun -->|"still failing, budget left"| S4_fix
        S4_rerun -->|"all pass or budget exhausted"| S4_out
        S4_remediate -->|"no"| S4_out
    end

    %% ===== INTER-STAGE CONNECTIONS =====
    S0_out1 --> S1_you
    S1_review -->|"Approve"| S2_invoke
    S2_out --> S3_invoke
    S3_out --> S4_invoke

    %% ===== LEGEND =====
    subgraph Legend
        direction LR
        L1["Autonomous"]:::autonomous
        L2["Manual / You"]:::manual
        L3["Pause Point"]:::pause
        L4["Orchestrator"]:::orchestrator
        L5["Worker Agent"]:::agent
        L6["Output"]:::output
    end
```

### Legend

| Color                 | Meaning                                       |
| --------------------- | --------------------------------------------- |
| 🟢 Green              | Fully autonomous — no human involved          |
| 🔴 Red/Orange         | Manual step — you act                         |
| 🟡 Yellow diamond     | Pause point — orchestrator stops and asks you |
| 🔵 Dark blue          | Orchestrator decision logic                   |
| 🔵 Medium blue        | Worker agent doing the actual work            |
| 🔵 Light blue rounded | Output artifact passed to the next stage      |

---

## Stage-by-Stage Breakdown

### Stage 0 — Research Pipeline (Fully Autonomous)

Runs entirely server-side. Triggered by `POST /api/research/trigger` or ARQ cron every 3 days.

| Sub-stage                     | What happens                                                                                                                                                                                                 | Output                                                 |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------ |
| **Prompt loading**            | Reads `prompts/research.md`, `feasibility.md`, `consensus.md`, + auto-discovers `prompts/analysts/*.md`                                                                                                      | `PipelinePrompts` object                               |
| **2-step consolidation**      | Concurrent calls to 6 LLMs (GPT-5.4, DeepSeek-v3.2, Gemini-3.1-pro-preview, Minimax-m2.7, Qwen3.6-plus, Claude Opus 4.6) + Claude Opus 4.6 independently, then Claude 4.6 synthesizes all                    | `research-output/research-{ts}/research/research.md`   |
| **Feasibility**               | Tavily web search + feasibility prompt → Claude Opus                                                                                                                                                         | `research-output/research-{ts}/enhanced/enhanced.md`   |
| **Analyst swarm + consensus** | Per-analyst model routing (strategy→Gemini-3.1-pro-preview, risk→Claude Opus, feasibility→GPT-5.4) run in parallel, assembled into findings, then Claude as "senior research director" synthesizes consensus | `research-output/research-{ts}/consensus/consensus.md` |
| **Proposal extraction**       | GLM-5 extracts JSON array of `StrategyProposal` rows from consensus                                                                                                                                          | DB rows with `status="approved"`                       |

**Output:** A consensus document (`consensus.md`) and approved `StrategyProposal` database records.

---

### Stage 1 — Research-to-Spec Orchestrator (Autonomous Chain)

You read the consensus document and invoke the `research.prompt`. From here, the **research.orchestrator** runs 7 phases autonomously, pausing only for the mandatory manual review of the generated specification.

| Phase | Name                    | Who runs it               | What gets passed IN                                 | What comes OUT                                                                       | Autonomous?                                                                                                                                     |
| ----- | ----------------------- | ------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **1** | Intake                  | Orchestrator              | Consensus doc path (or "latest")                    | Consensus highlights, recommendation count, scope assessment                         | **Autonomous** — stops only if no consensus found or no actionable recommendations                                                              |
| **2** | Analyze                 | `sparring.orchestrator`   | Consensus + codebase summary + domain knowledge     | Multi-perspective synthesis: creative approaches, risks, assumptions, feasibility    | **Autonomous** — sparring.orchestrator runs its hidden partners (architecture, implementation, operations, creative, devils-advocate, thinking) |
| **3** | Review                  | `reviewer`                | Consensus + sparring analysis                       | Normalized findings: breaking changes, security, performance, pattern conflicts      | **Autonomous**                                                                                                                                  |
| **4** | Plan (Impl)             | `engineer`                | Consensus + analysis + review findings              | `implementation-plan-YYYY-MM-DD.md`: ordered changes, test strategy, rollback        | **Autonomous**                                                                                                                                  |
| **5** | Plan (Detail) + Specify | `advisor` then `engineer` | Implementation plan → detailed plan → spec template | Detailed execution plan with phases/deps/verification → `feature-spec-YYYY-MM-DD.md` | **Autonomous**                                                                                                                                  |
| **6** | Manual Review           | **YOU**                   | Generated feature specification                     | Approve / Revise / Stop                                                              | **⏸ PAUSE — mandatory manual gate**                                                                                                             |
| **7** | Handoff                 | Orchestrator              | Approved spec path                                  | Structured handoff to feature.orchestrator                                           | **Autonomous**                                                                                                                                  |

**Spec revision loop:** If you select "Revise" during manual review, you provide feedback and the orchestrator re-invokes engineer to update the spec, then presents it again. Maximum 3 revision cycles.

**Output:** Approved feature specification + implementation plan. Feature-orchestrator is auto-invoked.

---

### Stage 2 — Feature Orchestrator (Mostly Autonomous — Pauses at Defined Points)

After you approve the feature spec, the feature.orchestrator is invoked automatically. It runs autonomously through 10 phases:

| Phase  | Name               | Who runs it        | What gets passed IN                                     | What comes OUT                                                          | Autonomous?                                                                                                                                                            |
| ------ | ------------------ | ------------------ | ------------------------------------------------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1**  | Intake             | Orchestrator       | Feature spec file/description                           | Goal statement, scope summary, confidence                               | **Autonomous** unless spec is too vague (confidence < 80%) → **pauses, asks you**                                                                                      |
| **2**  | Plan               | `advisor`          | Feature spec + acceptance criteria                      | Slice plan, dependencies, risks, test strategy                          | **Autonomous** unless unresolved question blocks slice definition → **pauses, asks you**                                                                               |
| **3**  | Select Slice       | Orchestrator       | Slice plan                                              | Slice brief (objective, files, acceptance criteria, verification scope) | **Autonomous** — but **pauses after every 5 slices** and asks you to continue                                                                                          |
| **4**  | Implement          | `engineer`         | Slice brief with scope boundaries                       | Implementation summary, changed files                                   | **Autonomous** (but in non-autopilot mode: **you must accept each file edit** in the VS Code diff view)                                                                |
| **5**  | Verify             | `engineer`         | Verification commands                                   | Pass/fail per lint/types/tests                                          | **Autonomous** (but in non-autopilot: **you must approve each terminal command**)                                                                                      |
| **6**  | Review             | `reviewer`         | Current diff                                            | Normalized findings (blocking / non-blocking)                           | **Autonomous**                                                                                                                                                         |
| **7**  | Decide             | Orchestrator       | Verification results + review findings + spec alignment | Decision: next slice / remediate / stop                                 | **Autonomous** unless: `needs-human-decision` finding → **pauses, asks you**; spec drift detected → **pauses, asks you**; sub-agent error → **pauses, reports to you** |
| **8**  | Remediate          | `engineer`         | Only blocking findings + current diff                   | Surgical fixes, then back to Verify (Phase 5)                           | **Autonomous** (same file-edit/terminal approval as Phase 4/5). Max 3-5 iterations per slice — if convergence fails → **stops and reports**                            |
| **9**  | Post-Delivery Docs | `engineer` (gated) | Evidence of doc/API/schema changes                      | Doc updates, AI Ecosystem audit list                                    | **Autonomous** — skipped entirely if no evidence triggers it. AI Ecosystem audit is detection-only (reports stale artifacts, doesn't fix them)                         |
| **10** | Finalize           | Orchestrator       | All slice results                                       | Feature delivery report                                                 | **Autonomous**                                                                                                                                                         |

> **Non-autopilot note:** The orchestration logic is autonomous (it decides what to do next without asking you). But because you're not using autopilot, VS Code will prompt you to approve every file edit (diff view) and every terminal command (allow/deny).

> **Session state persistence:** At Phase 1 (Intake), the feature.orchestrator writes a workflow state file to `.github/runtime/feature-state/{workflow_id}.state.json`. This file is updated after each phase transition. If a session is interrupted, the orchestrator reads the state file on the next invocation and **resumes from `current_phase`** — skipping completed phases. It validates that the `branch` field matches the current git branch before resuming.

**Output:** Feature Delivery Report

---

### Stage 3 — Test Orchestrator (Self-Healing Loop)

After the feature orchestrator produces its delivery report, the test orchestrator is auto-invoked with the delivery report path.

| Phase | Name     | Who                    | What gets passed IN                                  | What comes OUT                                          | Autonomous?                                                                                                            |
| ----- | -------- | ---------------------- | ---------------------------------------------------- | ------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **1** | Scope    | Orchestrator + Explore | Delivery report (changed files, acceptance criteria) | Testable surfaces, test types needed, locked assertions | **Autonomous**                                                                                                         |
| **2** | Generate | `engineer`             | Scope brief + source code + existing test patterns   | Test files (unit, integration, backtest)                | **Autonomous** (you approve file edits)                                                                                |
| **3** | Execute  | `engineer`             | Test files                                           | Pass/fail, coverage delta                               | **Autonomous** (you approve terminal commands)                                                                         |
| **4** | Review   | `reviewer`             | Generated test code                                  | Review findings (blocking/non-blocking)                 | **Autonomous**                                                                                                         |
| **5** | Heal     | `engineer`             | Only blocking findings + failing tests               | Fixes → back to Execute                                 | **Autonomous**, bounded: max 5 iterations per batch, max 3 per individual test. Stops if thrashing or plateau detected |

**Output:** Test generation report + handoff block for QA orchestrator.

---

### Stage 4 — QA Orchestrator (4-Gate Validation + Auto-Remediation)

Auto-invoked after the test orchestrator. Runs 4 quality gates sequentially — **all gates run regardless of failures**. If any gate fails, the QA orchestrator delegates fixes to `engineer` and re-runs failed gates (max 3 iterations).

| Gate              | What                                          | Threshold                                        | Autonomous?                           |
| ----------------- | --------------------------------------------- | ------------------------------------------------ | ------------------------------------- |
| **1: Test Suite** | `ruff check` + `pyright` + `pytest`           | All exit 0                                       | **Autonomous** (you approve commands) |
| **2: Coverage**   | Diff-coverage of changed lines                | Fail < 50%, Warn < 80%                           | **Autonomous**                        |
| **3: Regression** | Run regression tests against stored baselines | All pass (or gracefully SKIPPED if no baselines) | **Autonomous**                        |
| **4: Smoke**      | Import check, config load, route registration | All exit 0                                       | **Autonomous**                        |

After all 4 gates, it evaluates whether a **sparring escalation** is warranted (e.g., >3 tests fail at same module boundary, systematic coverage gaps). If triggered, it invokes `sparring.orchestrator` (max 2x) for multi-perspective design analysis.

**Auto-remediation:** If any gate failed, the QA orchestrator generates an initial report, then enters a remediation loop:

1. Identifies the specific failures from the report
2. Delegates fixes to `engineer` (e.g., `ruff check --fix` for lint, manual fixes for type/test errors)
3. Re-runs **only the failed gates**
4. Loops until all gates pass or budget exhausted (max 3 iterations)

**Remediation exclusions:** Coverage warnings (50-80%) are non-blocking and do not trigger remediation. Sparring findings flagged as `needs-human-decision` require user review. Failures requiring architectural changes are escalated.

**Output:** Final QA report with per-gate results, remediation log (if applicable), and overall verdict.

| Verdict                        | Condition                                              |
| ------------------------------ | ------------------------------------------------------ |
| PASS                           | All gates pass, none skipped                           |
| PASS WITH CAVEATS              | All gates pass with skips or coverage warnings         |
| PASS (REMEDIATED)              | All gates pass after auto-remediation                  |
| PASS WITH CAVEATS (REMEDIATED) | All gates pass after remediation with warnings/skips   |
| FAIL                           | Gates still failing after remediation budget exhausted |

---

## Your Manual Touch Points (Non-Autopilot Mode)

Only **two** mandatory manual steps in the entire pipeline:

| Step                             | What you do                                                                    |
| -------------------------------- | ------------------------------------------------------------------------------ |
| **After research pipeline runs** | Read the consensus document and trigger the research-to-spec prompt            |
| **Review feature specification** | Review and approve the generated feature spec before the orchestrator delivers |

During execution (non-autopilot VS Code), you will also be prompted to:

| Interaction                 | What happens                                                                                                                         |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **During feature delivery** | Accept/reject each file edit diff, allow/deny each terminal command                                                                  |
| **If orchestrator pauses**  | Answer clarifying questions, approve human-decision items                                                                            |
| **During test generation**  | Same accept/reject for edits and commands                                                                                            |
| **After QA report**         | Review verdict; auto-remediation handles most failures, but `needs-human-decision` items and architectural issues require your input |

---

## Runtime Enforcement: Copilot Hooks

Three Copilot hooks (registered in `.github/hooks/hooks.json`) enforce safety and consistency during every pipeline stage:

### SessionStart Hook

**Trigger:** New Copilot session begins | **Timeout:** 10s

Injects into agent context:

- Current git branch name
- Last 5 commits (one-line format)
- Active workflow state from `.github/runtime/**/*.state.json` (if any), including posture (`exploration`/`delivery`/`hotfix`)

This ensures orchestrators resume mid-pipeline with branch awareness and in-progress state.

### PreToolUse Hook — Command Policy Enforcement

**Trigger:** Before any Copilot tool execution | **Timeout:** 10s

Evaluates terminal commands against `command-policy.json`. Non-terminal tools are always allowed without evaluation.

**Deny rules** (always blocked):

| Pattern                                           | Reason                               |
| ------------------------------------------------- | ------------------------------------ |
| `git reset --hard`                                | Destroys uncommitted work            |
| `git push --force` (without `--force-with-lease`) | Overwrites remote commits            |
| `git clean -fd`                                   | Deletes untracked files irreversibly |
| `rm -rf /` or `rm -rf ..`                         | Catastrophic recursive delete        |
| `:>>/dev/sd*`                                     | Block device overwrite               |

**Ask rules** (require user confirmation):

| Pattern                       | Reason                            |
| ----------------------------- | --------------------------------- |
| `git push --force-with-lease` | Still rewrites remote history     |
| `git checkout -- .`           | Discards all unstaged changes     |
| `git stash drop`              | Permanently discards stash        |
| `rm -r`                       | Recursive delete — confirm target |
| `DROP TABLE/DATABASE/SCHEMA`  | Destructive DDL                   |
| `TRUNCATE TABLE`              | Irreversible data removal         |
| `--no-verify`                 | Bypasses safety hooks             |

### PostToolUse Hook — Auto-Format

**Trigger:** After `create_file`, `replace_string_in_file`, `multi_replace_string_in_file`, or `editFiles` | **Timeout:** 15s

| File Extension                                       | Formatter  | Action                                        |
| ---------------------------------------------------- | ---------- | --------------------------------------------- |
| `.py`                                                | `ruff`     | `ruff format` + `ruff check --fix`            |
| `.ts`, `.tsx`, `.js`, `.jsx`, `.json`, `.css`, `.md` | `prettier` | `prettier --write` (fallback: `npx prettier`) |

Non-blocking — formatter unavailability is silently ignored.

---

## Governance Scripts

Scripts in `scripts/` enforce structural integrity outside Copilot sessions — in CI, pre-push hooks, and manual audits.

### Pre-Push Gate (`pre-push-check.sh`)

Installed as git pre-push hook via `setup-hooks.sh`. Runs automatically on `git push`.

**Two-tier verification:**

1. **Changed files only** — `ruff check` + `pyright` on files changed vs. `origin/master` (fast)
2. **Full scope** — `pyright app/` on entire application directory (mirrors CI)

Tests are excluded (run in CI via pytest). Total time: ~5–10 seconds.

The dual-scope approach was introduced after a CI failure where changed-file-only pyright missed a pre-existing type error exposed by a new import.

### AI Ecosystem Freshness Validator (`verify-AI Ecosystem-freshness.sh`)

| Mode      | Command                                      | Description                                                                                                                                                    |
| --------- | -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Check** | `./scripts/verify-AI Ecosystem-freshness.sh` | Compare on-disk artifact counts against `AI Ecosystem-artifact-freshness.md`                                                                                   |
| **Fix**   | `--fix`                                      | Update freshness table with actual counts + today's timestamp                                                                                                  |
| **Lint**  | `--lint`                                     | Structural audit: applyTo glob validation, cross-reference checks, orphan detection, agent reference validation, skill context path checks, JSON schema syntax |

### Feature Slice Verifier (`verify-feature-slice.sh`)

Full verification gate for backend and/or frontend:

| Component | Lint           | Types          | Tests                 |
| --------- | -------------- | -------------- | --------------------- |
| **API**   | `ruff check .` | `pyright app/` | `pytest tests/ -x -q` |
| **Web**   | `eslint src/`  | `tsc --noEmit` | `npm test -- --run`   |

Usage: `scripts/verify-feature-slice.sh api|web|both`

### Instruction Conflict Detector (`verify-instruction-conflicts.sh`)

Detects overlap zones where 3+ instructions match the same source files. Prevents accidental authority conflicts. Always-on instructions (`applyTo: **`) are noted separately. Informational — always exits 0.

### Repo Map Generator (`generate-repo-map.sh`)

Auto-generates the AI Ecosystem artifact inventory at `.github/context/repo-map.md`. Supports `--check` mode for CI freshness validation.

### Hook Installer (`setup-hooks.sh`)

Installs the git pre-push hook (delegates to `scripts/pre-push-check.sh`). Run once after cloning. Includes safe fallback if pre-push-check.sh is missing.

---

## JSON Schemas (Inter-Orchestrator Contracts)

Three JSON schemas under `.github/schemas/` standardize data exchange between pipeline stages.

### Orchestrator Handoff Schema (`orchestrator-handoff.schema.json`)

Passed between orchestrators in the chain: feature → test → QA.

| Field                    | Type           | Required | Description                                                            |
| ------------------------ | -------------- | -------- | ---------------------------------------------------------------------- |
| `source_orchestrator`    | enum           | Yes      | `"feature-orchestrator"` / `"test-orchestrator"` / `"qa-orchestrator"` |
| `target_orchestrator`    | enum           | Yes      | Handoff target                                                         |
| `workflow_id`            | string         | Yes      | Unique workflow identifier                                             |
| `delivery_report_path`   | string         | Yes      | Path to the report artifact                                            |
| `changed_files`          | string[]       | Yes      | Modified files                                                         |
| `acceptance_criteria`    | string[]       | No       | Spec acceptance criteria                                               |
| `test_directories`       | string[]       | No       | Relevant test directories                                              |
| `verification_summary`   | object         | No       | `{lint, types, tests}` — each `"pass"/"fail"/"skipped"`                |
| `coverage_delta`         | string         | No       | Coverage change                                                        |
| `residual_concerns`      | string[]       | No       | Unresolved non-blocking concerns                                       |
| `context_digest`         | string (≤2000) | No       | Compressed context for next stage                                      |
| `handoff_timestamp`      | datetime       | Yes      | ISO 8601                                                               |
| `completion_status`      | enum           | No       | `"full"` (default) / `"partial"` / `"failed"`                          |
| `completed_deliverables` | string[]       | No       | What was completed (for partial)                                       |
| `incomplete_reason`      | string         | No       | Why delivery was incomplete                                            |

### Workflow State Schema (`workflow-state.schema.json`)

Written to `.github/runtime/feature-state/` for session resumption. Orchestrators read this on invocation and resume from `current_phase` if the `branch` matches.

Key fields: `workflow_id`, `workflow_type` (`feature`/`test`/`qa`), `posture` (`exploration`/`delivery`/`hotfix`), `current_phase` (one of 19 possible phases), `owner_agent`, `branch`, `slice_plan[]`, `verification_status`, `open_findings[]` (with severity: `blocking`/`non-blocking`/`needs-human-decision`), `remediation_count`, `escalation_status`.

### Subagent Response Schema (`subagent-response.schema.json`)

Normalizes output from orchestrator subagent invocations.

| Field              | Type           | Required | Description                               |
| ------------------ | -------------- | -------- | ----------------------------------------- |
| `summary`          | string (≤1000) | Yes      | Self-contained conclusion (≤200 words)    |
| `findings[]`       | array          | Yes      | Normalized findings (see below)           |
| `files_referenced` | string[]       | No       | Files examined                            |
| `status`           | enum           | Yes      | `"pass"` / `"fail"` / `"needs-attention"` |
| `dissenting_view`  | string         | No       | Minority opinion                          |

**Finding fields:** `id`, `title`, `severity` (`critical`/`high`/`medium`/`low`/`info`), `category`, `evidence`, `recommendation`, `confidence` (`high`/`medium`/`low`), `blocking` (boolean).

---

## RBI Pipeline Data Contracts

The Research → Backtest → Incubate pipeline manages strategy lifecycle transitions through typed Pydantic models and SQLAlchemy ORM models. These contracts are documented in detail in `docs/AI Ecosystem-agent-architecture.md` §13.

### Strategy Lifecycle State Machine

```
PROPOSED → APPROVED_FOR_BACKTEST → BACKTESTING
    ↗                                  ↓
BACKTEST_FAILED ←────────────── BACKTEST_PASSED
    ↓                                  ↓
  ARCHIVED                         INCUBATING
    ↑                              ↙       ↘
INCUBATION_FAILED         INCUBATION_PASSED
                                    ↓
                  PROMOTED (to simulation dashboard)
                      ↓
                   ARCHIVED
```

Terminal states: `ARCHIVED`. Retry paths: `BACKTEST_FAILED → PROPOSED`, `INCUBATION_FAILED → PROPOSED`, `PROMOTED → INCUBATING` (drift-detected re-incubation).

### Key Database Models

| Model                     | Table                        | Purpose                                                       |
| ------------------------- | ---------------------------- | ------------------------------------------------------------- |
| `StrategyProposal`        | `strategy_proposals`         | Research pipeline output — approved proposals for backtesting |
| `DiscoveredStrategy`      | `discovered_strategies`      | Backtest-validated strategies with metrics                    |
| `IncubationObservation`   | `incubation_observations`    | Forward-simulation observations during incubation             |
| `StrategyStateTransition` | `strategy_state_transitions` | Audit log of all state changes with metric snapshots          |
| `ProvenanceEntry`         | `provenance_entries`         | Cryptographic audit trail (SHA-256 chain)                     |
| `PipelineRun`             | `pipeline_runs`              | Pipeline execution tracking                                   |

### Research Output Contracts

| Contract              | Location                                           | Key Fields                                                                                            |
| --------------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `ResearchAgentOutput` | `app/services/research/contracts/agent_output.py`  | hypothesis, mechanism, expected_edge, confidence (0–1), citations                                     |
| `StrategySpec`        | `app/services/research/contracts/strategy_spec.py` | name, hypothesis, entry/exit logic types, offset_policy (buy: [−30,0], sell: [0,45]), position_sizing |
| `PipelinePrompts`     | `app/services/research/prompt_loader.py`           | research, codebase_summary, feasibility, consensus, analysts[]                                        |
| `WebSearchResult`     | `app/services/research/web_searcher.py`            | title, url, content, score, published_date                                                            |

### Quality Gates

| Gate             | Threshold | Description              |
| ---------------- | --------- | ------------------------ |
| `MIN_EXPECTANCY` | ≥0.5%     | Average return per trade |
| `MIN_SHARPE`     | ≥0.5      | Sharpe ratio             |
| `MAX_DRAWDOWN`   | ≥−10%     | Maximum drawdown         |
| `MIN_TRADES`     | ≥12       | Minimum trade count      |

**OOS validation** (relaxed): `expectancy > 0` AND `max_drawdown >= −15%` on 30% holdout data.

### Backtest Result Schema

The `_backtest_single()` function returns: `ticker`, `buy_offset`, `sell_offset`, `expectancy`, `sharpe_ratio`, `sortino_ratio`, `max_drawdown`, `win_rate`, `total_trades`, `avg_return_pct`, `in_sample_return`, `out_of_sample_return`, `oos_passed`, `dsr`, `regime_state`, `hmm_state`, `pipeline_run_id`, `meta_label_probability`.

### Pipeline Scheduling (ARQ Cron)

| Job                      | Schedule                                    | Description                            |
| ------------------------ | ------------------------------------------- | -------------------------------------- |
| `run_rbi_sweep`          | Every 6h (00:17, 06:17, 12:17, 18:17)       | Full grid sweep: 238 buy×sell combos   |
| `run_research_pipeline`  | Every 12h (06:42, 18:42) + daily GH Actions | 5-stage LLM research → consensus       |
| `run_proposal_backtests` | Every 3h (03:07, 09:07, 15:07, 21:07)       | Backtest approved proposals            |
| `run_incubation_monitor` | Every 12h (01:33, 13:33)                    | Forward-simulate incubating strategies |
| `cleanup_old_runs`       | Daily at 03:00                              | Clean up expired pipeline runs         |

### Change Propagation Rules

Per `rbi-pipeline.instructions.md`:

| What Changed                | Must Also Update                                        |
| --------------------------- | ------------------------------------------------------- |
| Quality gate thresholds     | `proposal_backtester.py`, RBI dashboard                 |
| `_backtest_single()` schema | All validation/testing code                             |
| `DiscoveredStrategy` fields | Alembic migrations, incubation monitor, API serializers |
| `StrategyState` enum        | `strategy_lifecycle.py`, frontend displays              |
| Prompt files in `prompts/`  | PromptLoader validation                                 |

---

## Skills Used in the Pipeline

Each pipeline stage is driven by a corresponding AI Ecosystem skill. Skills bundle phases, stop conditions, worker agent routing, and templates.

### Feature Delivery Skill (Stage 2)

**10 phases:** Intake → Plan → Select Slice → Implement → Verify → Review → Decide → Remediate → Post-Delivery Docs → Finalize

| Phase              | Worker Agent     | Key Details                                               |
| ------------------ | ---------------- | --------------------------------------------------------- |
| Plan               | advisor          | Slice decomposition, dependency analysis, risk surfacing  |
| Implement          | engineer         | Code changes for current slice only                       |
| Verify             | engineer         | `ruff check` → `pyright` → `pytest`                       |
| Review             | reviewer         | Multi-aspect review across 8 domains                      |
| Remediate          | engineer         | Surgical fixes for blocking findings (max 3–5 iterations) |
| Post-Delivery Docs | engineer (gated) | Doc updates + AI Ecosystem audit (detection-only)         |
| Finalize           | orchestrator     | Write handoff payload → invoke test.orchestrator          |

**Anti-thrashing:** STOP if same finding reappears 2×, scope increases without blockers clearing, verification oscillates, or review returns non-actionable findings.

**Iteration limits:** Max 3 remediations (small) / 5 (medium) per slice. Pause after every 5 slices.

### Test Orchestration Skill (Stage 3)

**5-phase self-healing loop:** Scope → Generate → Execute → Review → Heal

| Phase    | Worker Agent | Key Details                                                           |
| -------- | ------------ | --------------------------------------------------------------------- |
| Scope    | Explore      | Discover test patterns, fixtures, classify unit/integration/backtest  |
| Generate | engineer     | Tests with locked assertions (`# LOCKED: <criteria-ref>`)             |
| Execute  | engineer     | Static analysis + lint + types + tests + coverage                     |
| Review   | reviewer     | Assertion density ≥1/test, negative testing ≥30%, no temporal leakage |
| Heal     | engineer     | Fix blocking findings (max 5 iterations/batch, 3/function)            |

**Convergence rules:** SUCCESS when all pass + no blockers. STOP on: max iterations, thrashing (>50% code change same error), error plateau (no decrease 2 iterations).

### QA Orchestration Skill (Stage 4)

**4 sequential gates + auto-remediation:**

| Gate          | Check                                         | Threshold              |
| ------------- | --------------------------------------------- | ---------------------- |
| 1: Test Suite | `ruff check` + `pyright` + `pytest`           | All exit 0             |
| 2: Coverage   | Diff-coverage of changed lines                | Fail < 50%, Warn < 80% |
| 3: Regression | Regression tests vs. baselines                | All pass (or SKIPPED)  |
| 4: Smoke      | Import check, config load, route registration | All exit 0             |

**Sparring escalation:** Triggered if >3 tests fail at same boundary, contradictory smoke behavior, systematic coverage gaps >50%, or regression drift in untouched area. Invokes sparring.orchestrator (max 2× per run).

**Auto-remediation:** Max 3 iterations: identify failures → delegate to engineer → re-run failed gates. Does NOT auto-remediate: coverage warnings (50–80%), `needs-human-decision` sparring findings, failures requiring architectural changes.

**Verdicts:** PASS | PASS WITH CAVEATS | PASS (REMEDIATED) | PASS WITH CAVEATS (REMEDIATED) | FAIL

### Multi-Aspect Code Review Skill (Used in Stage 2 Phase 6)

**8 review domains** executed in 3 parallel waves:

| Wave | Domains                                                                | Focus                          |
| ---- | ---------------------------------------------------------------------- | ------------------------------ |
| 1    | Architecture & Design (`ARCH`), Security (`SEC`), Performance (`PERF`) | Structural + risk-first        |
| 2    | Code Quality (`QUAL`), LLM Optimization (`LLM`), Testing (`TEST`)      | Quality + coverage             |
| 3    | Type Safety & Correctness (`CORR`), Financial Logic (`FIN`)            | Benefits from wave 1–2 context |

Each domain launches an Explore subagent. Findings follow the normalized schema (`subagent-response.schema.json`).
