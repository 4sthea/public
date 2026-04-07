# AI ecosystem — Controlled Layered Authority System for Prompts

> **Version:** v3 — Updated 2026-04-05  
> **Supersedes:** v1 (2026-03-06), v2 (2026-03-10)  
> **Canonical source of truth:** Active files under `.github/`

## What This Document Covers

This document explains the architecture, rationale, advantages, disadvantages, and everyday usage of **AI ecosystem** (Controlled Layered Authority System for Prompts) — the agent-and-artifact governance framework used in this repository to keep AI-generated outputs honest, auditable, and safe to merge.

---

## 1) The Problem AI ecosystem Solves

Large Language Models (LLMs) are probabilistic text continuators. Given a prompt, they predict the most plausible next tokens. They are not truth engines. When evidence is missing and the prompt implicitly demands completion, the model does what it was trained to do: produce fluent, confident-sounding text that fills the gap. In casual chat this is a nuisance; in merged documentation, infrastructure configs, or code reviews it is a hazard. A hallucinated detail — an API endpoint that does not exist, a config key with a wrong default, a security claim without audit evidence — can outlive the conversation that created it, propagate through onboarding docs, and eventually become an unchallenged "fact" in the team's institutional memory.

The root cause is structural, not moral. Models hallucinate because:

1. **Missing evidence** creates a vacuum that completion training fills.
2. **Completion pressure** in the prompt ("be comprehensive", "make it complete") punishes abstention and rewards guessing.
3. **Authority cues** ("ensure correctness", "verify") imply the model can validate its own claims.
4. **Unbounded scope** ("review the entire codebase") makes it impossible to ground every claim.

AI ecosystem exists to remove these pressures systematically. It does not make the model smarter. It reshapes the environment so that honesty is the cheapest path, silence is an acceptable outcome, and uncertainty is visible rather than hidden.

---

## 2) Core Philosophy

AI ecosystem rests on three principles:

- **Truth over helpfulness over speed.** An "Unknown" cell in a table is more valuable than a plausible guess that might be wrong.
- **Single ownership per concern.** Every rule, gate, procedure, and structural decision has exactly one canonical home. Duplicating rules across files causes drift, contradiction, and audit nightmares.
- **Creativity belongs in cognition; authority must not leak.** Agents may reason freely within their scope. But enforcement, verification gates, and output structure are governed by dedicated artifacts that the agent does not own and cannot override.

---

## 3) The Artifact Taxonomy

AI ecosystem separates AI-assisted work into seven artifact types plus two composable additions (skills and instructions). Each has one job and strict boundaries on what it may and may not contain.

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

> For the current roster with model assignments, see `.github/context/AI ecosystem-artifact-freshness.md` and `.github/instructions/AI ecosystem-authoring.instructions.md`.

| Agent                     | Model           | Tools                                    | Purpose                                                                |
| ------------------------- | --------------- | ---------------------------------------- | ---------------------------------------------------------------------- |
| **software-engineer**     | Claude Opus 4.6 | read, search, agent, edit, todo, execute | Implementation + Ralph Loop verification                               |
| **code-reviewer**         | Claude Opus 4.6 | read, search, agent, todo                | Read-only adversarial review + security                                |
| **thinking-partner**      | default         | read, search, agent, todo                | Read-only planning, design, teaching                                   |
| **sparring-orchestrator** | default         | read, search, agent, todo, web           | Multi-perspective analysis orchestrator                                |
| **feature-orchestrator**  | default         | read, search, agent, todo, vscode        | Feature lifecycle coordinator                                          |
| **test-orchestrator**     | default         | read, search, agent, todo, vscode        | Self-healing test generation orchestrator                              |
| **qa-orchestrator**       | default         | read, search, agent, todo, vscode        | Post-delivery quality assurance (4-gate validation + auto-remediation) |
| **research-orchestrator** | default         | read, search, agent, todo, vscode        | Autonomous research-to-spec pipeline (consensus → feature)             |

Tool restrictions are the load-bearing constraint:

- The **software-engineer** is the only agent that can edit files and run terminal commands. It follows the "Ralph Loop": implement → build → test → read output → fix → loop until verified or stuck.
- The **code-reviewer** is read-only and reviews diffs for correctness, safety, maintainability, and security. It provides adversarial consensus — a different perspective on code the software-engineer wrote.
- The **thinking-partner** is read-only and prevents premature implementation during planning. It challenges assumptions, explores alternatives, and designs before anyone writes code.
- The **sparring-orchestrator** invokes hidden partner agents (architecture-partner, implementation-partner, operations-partner, thinking-partner, creative-partner, devils-advocate-partner) for structured multi-perspective analysis and synthesizes one actionable answer.
- The **feature-orchestrator** coordinates the full feature lifecycle (plan → implement → verify → review → remediate → finalize) by routing work to software-engineer, code-reviewer, and thinking-partner. It is read-only — it coordinates but never edits.
- The **test-orchestrator** generates all test artifacts (unit, integration, backtest), runs them, reviews for correctness, and iterates until convergence. Self-healing loop — delegates execution to software-engineer.
- The **qa-orchestrator** validates delivered features through 4 gates: test suite, coverage threshold, regression baselines, and smoke tests. If any gate fails, it auto-remediates by delegating fixes to software-engineer and re-running failed gates (max 3 iterations). Can escalate design concerns to sparring-orchestrator.
- The **research-orchestrator** drives a consensus document through multi-perspective analysis, code review, implementation planning, and feature specification generation — producing an approved spec ready for the feature-orchestrator. Only two manual steps: reading the consensus doc and reviewing the generated spec.

Hidden partner agents (not visible in the agent picker):

| Partner                     | Purpose                                                          |
| --------------------------- | ---------------------------------------------------------------- |
| **architecture-partner**    | System boundaries, coupling, interfaces, design tradeoffs        |
| **implementation-partner**  | Feasibility, complexity, failure points, sequencing              |
| **operations-partner**      | Deployment, observability, safety, rollback, runtime risk        |
| **creative-partner**        | Idea expansion, brainstorming, possibility mapping, steelmanning |
| **devils-advocate-partner** | Stress-testing ideas, exposing flaws, adversarial analysis       |

The **thinking-partner** serves double duty as both a user-visible planning agent and a hidden partner for the sparring orchestrator.

Each agent lists its procedural companions (which `*.instructions.md` files it may invoke), when to use it, when NOT to use it, and agent-specific preflight checks.

> **v1 → v3 migration note:** v1 had 16 specialized agents (Agent Router, Code Analyst, Feature Engineer, Learn Coach, Security Reviewer, Skill Teacher, Software Architect, Strategy Analyst, Tech Debt Analyst, Tech Debt Resolver, Tech Writer, Test Architect, Test Engineer, etc.). v3 consolidated these into a small set of visible agents + hidden partners for orchestration. The specialized knowledge from the retired agents now lives in `*.instructions.md` files that any agent can invoke on demand. This reduced maintenance burden while preserving domain expertise through composable instructions.

> For the current agent roster and tool assignments, see `.github/instructions/AI ecosystem-authoring.instructions.md` → Agent Roster table.
> For current artifact counts, see `.github/context/AI ecosystem-artifact-freshness.md`.

### 3.4 Instructions — `*.instructions.md`

Instructions are on-demand procedural knowledge files. They contain domain-specific conventions, patterns, and rules that agents invoke when their scope matches. Instructions replaced the need for many specialized agents — instead of having a dedicated "Security Reviewer" agent, the software-engineer or code-reviewer can invoke `security-review.instructions.md` when reviewing security.

Instruction files live in `.github/instructions/`. Each uses `applyTo` glob patterns so VS Code automatically attaches them when working in matching files.

> For the current list of instructions and their scopes, see the files on disk in `.github/instructions/`.
> For the current count, see `.github/context/AI ecosystem-artifact-freshness.md`.

### 3.5 Procedures — `*.procedure.md`

Procedures are explicitly invoked playbooks. They contain ordered steps, stop conditions, and propagation passes. A procedure must be read before execution — the contract is "attempt to read the file; STOP if it is missing or unreadable."

Procedure files live in `.github/procedures/`.

> For the current list and count, see `.github/context/AI ecosystem-artifact-freshness.md`.

### 3.6 Wiring — `*.prompt.md`

Prompts are the task-level glue. A prompt selects an agent, references one or more instructions/procedures, declares a template, defines the evidence scope, specifies the output shape, and sets stop conditions.

Prompt files live in `.github/prompts/`. Each prompt selects an agent, references instructions/procedures, declares a template, and sets stop conditions.

> For the current list and count, see `.github/context/AI ecosystem-artifact-freshness.md`.

### 3.7 Structure — `*.template.md`

Templates are interfaces. They define headings, placeholder lists, and section structure — nothing more. Empty sections are explicitly allowed and encouraged, because an empty section with the heading "Unknown" is infinitely more honest than a filled section containing plausible invention.

Available templates:

Template files live in `.github/templates/`. Each defines headings, placeholder lists, and section structure.

> For the current list and count, see `.github/context/AI ecosystem-artifact-freshness.md`.

All templates live in `.github/templates/`.

### 3.8 Context — `.github/context/*.md`

Context files provide descriptive grounding: system maps, codebase orientation, component catalogs, domain glossaries, shared conventions, and known pitfalls. They are read-only references that help agents orient without relying on model priors or folklore. The critical rule is that context must never become "shadow policy" — it describes what exists but does not prescribe what must happen.

Current context files:

Context files live in `.github/context/`. Each provides descriptive grounding for a specific concern.

> For the current list and count, see `.github/context/AI ecosystem-artifact-freshness.md`.

### 3.9 Skills — `.github/skills/`

Skills are composable workflows that bundle instructions + procedures + templates into reusable capabilities. Each skill has a `SKILL.md` that VS Code can discover and invoke.

Current skills:

Skill directories live in `.github/skills/`. Each has a `SKILL.md` that VS Code can discover and invoke.

> For the current list and count, see `.github/context/AI ecosystem-artifact-freshness.md`.

---

## 4) Why AI ecosystem Is Structured This Way

### 4.1 Single Ownership Prevents Drift

The most common failure mode in governed AI workflows is "authority sprawl": the same rule appears in the constitution, in an agent definition, in a prompt, and in a template, each phrased slightly differently. Over time those phrasings drift apart. When the model encounters contradictions, it resolves them by picking whichever version seems most local or specific — which is often the wrong one. Single ownership eliminates that class of failure entirely. If you want to change a verification rule, you change `verification-checklist.instructions.md` and nothing else. If you want to change how an agent reasons, you change the `.agent.md` file and nothing else.

### 4.2 Separation of Cognition from Execution

Agents define _how to think_. Instructions define _what domain knowledge to apply_. Procedures define _what steps to follow_. Prompts define _what to produce_. By separating these concerns, AI ecosystem avoids the "god-prompt" anti-pattern where one massive instruction block tries to simultaneously set the model's tone, define a procedure, specify output format, and enforce verification — inevitably creating contradictions and leaving the model to guess which directive takes priority.

This separation also makes the system composable. The same agent (e.g., software-engineer) can be wired to different prompts (architecture documentation, code analysis, tech debt remediation) while invoking different instructions as needed — without changing the agent's core reasoning posture.

### 4.3 Silence as Success

Most AI systems implicitly punish refusal. If the model says "I don't know," the user is disappointed and the conversation feels stuck. AI ecosystem explicitly inverts this: silence, refusal, and "Unknown" are correct outputs when evidence is missing. This is operationalised through stop conditions in procedures, evidence constraints in prompts, and the constitution's rule that "truth > helpfulness > speed." The practical effect is that the model no longer needs to guess in order to be useful. Being honest is the easiest valid response.

### 4.4 The Compiler Pipeline Pattern

For high-stakes outputs, AI ecosystem treats writing like a compiler pipeline:

1. **Draft** — generate from template, using provided evidence.
2. **Lint** — apply verification checklist and lint rules mechanically; output findings only.
3. **Patch** — apply minimal, surgical fixes to resolve findings.

This pattern exists because large rewrites are drift machines. When you ask a model to "rewrite and fix" in one pass, it changes tone, adds unverified connective tissue, drops sections it considers redundant, and introduces new claims. The pipeline keeps each pass focused and auditable.

### 4.5 Instructions Replace Agents

The v1 → v3 migration demonstrated that 16 specialized agents created a maintenance burden disproportionate to their value. Most agents shared the same tool set and differed only in domain knowledge. By extracting domain knowledge into `*.instructions.md` files and consolidating to a small set of visible agents with distinct tool profiles (plus hidden partners for orchestration), AI ecosystem achieved:

- **Reduced surface area:** Fewer agent files to maintain instead of 16
- **Preserved expertise:** All domain knowledge survives in instruction files
- **Better composability:** Any agent can invoke any instruction when scope matches
- **Clearer tool boundaries:** Edit capability is the meaningful differentiator, not domain label

---

## 5) Authority Flow and Precedence

AI ecosystem defines a strict precedence hierarchy:

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

## 6) Advantages of AI ecosystem

### Reduced Hallucination

By removing completion pressure, bounding evidence scope, centralizing enforcement, and making "Unknown" acceptable, AI ecosystem addresses the structural causes of hallucination rather than relying on vague instructions like "be accurate."

### Auditability

Every claim in a AI ecosystem-generated artifact should be traceable to provided evidence. The separation of facts, assumptions, and recommendations makes review mechanical rather than subjective.

### Composability

Agents, instructions, prompts, templates, and procedures are independent and can be mixed and matched. Adding a new document type requires creating a template and a prompt — the existing agent roster and verification infrastructure are reused without modification.

### Institutional Memory Protection

Merged documentation becomes precedent. Precedent becomes onboarding. AI ecosystem breaks the hallucination cascade by ensuring that only evidence-backed claims survive the pipeline and that gaps remain visible as "Unknown."

### Low Maintenance Footprint (v3)

The v3 consolidation reduced the active maintenance surface by ~60% compared to v1 while preserving all domain expertise in composable instruction files.

> For current artifact counts, see `.github/context/AI ecosystem-artifact-freshness.md`.

---

## 7) Disadvantages and Limitations

### Overhead for Simple Tasks

AI ecosystem adds cognitive overhead. For a quick one-off question or a trivial code change, AI ecosystem is overkill. The system is designed for artifacts that persist and accumulate authority.

### Prompt Sensitivity

AI ecosystem is a safety rail, not autopilot. If a user writes a prompt that says "be comprehensive" and "fill gaps," they have reintroduced the exact completion pressure AI ecosystem was designed to eliminate. The user remains part of the safety boundary.

### Runtime Enforcement via Hooks

AI ecosystem uses Copilot hooks (`.github/hooks/`) for deterministic runtime enforcement. The `PreToolUse` hook evaluates terminal commands against `command-policy.json` and returns allow/ask/deny decisions. The `PostToolUse` hook auto-formats edited files. These hooks enforce behavior within Copilot sessions only — CI gates and non-Copilot shell sessions are not covered.

---

## 8) Everyday Usage Guide

### 8.1 Starting a Task

1. **Identify the task type.** Are you producing a document? Reviewing code? Implementing a feature? Analyzing strategy?
2. **Select the prompt.** Browse `.github/prompts/` for a matching `*.prompt.md`. The prompt name usually makes the intent clear (e.g., `code-review.generate.prompt.md`).
3. **The prompt selects the agent.** You do not need to manually pick an agent when using a prompt. In VS Code's Copilot Chat, you can directly invoke agents by name (e.g., `@software-engineer`, `@code-reviewer`, `@thinking-partner`).
4. **Provide evidence.** Paste or reference the specific files, snippets, or context the task requires.
5. **Let the pipeline run.** The agent reasons, instructions provide domain knowledge, the procedure drives the steps, the template provides structure, and the verification checklist gates the output.

### 8.2 When to Skip AI ecosystem

Not everything needs the full framework:

- **Casual questions** ("what does this function do?") — ask directly.
- **Trivial changes** (rename a variable, fix a typo) — just do it.
- **Exploratory brainstorming** — use `@thinking-partner` without a formal prompt.

Reserve the full pipeline for artifacts that will be merged, shared, or referenced later.

### 8.3 Writing Good Prompts (The Three Knobs)

Every prompt controls three independent dimensions:

| Knob          | What It Governs               | Example                                        |
| ------------- | ----------------------------- | ---------------------------------------------- |
| **Authority** | What may be treated as true   | "Use only provided files; mark unknowns"       |
| **Scope**     | What area is in bounds        | "Only these directories / only these concerns" |
| **Output**    | What shape the artifact takes | "Use template X; leave empty sections"         |

Bad prompts blur these knobs: "Write a complete architecture doc" explodes all three simultaneously. Good AI ecosystem prompts set each one explicitly.

### 8.4 Dangerous Phrases to Avoid

| Phrase                 | Why It Is Dangerous                    | Safer Alternative                                  |
| ---------------------- | -------------------------------------- | -------------------------------------------------- |
| "Be comprehensive"     | Pressures gap-filling                  | "Cover only what evidence supports; list unknowns" |
| "Ensure correctness"   | Implies the model can verify           | "Mark Unknown if not evidenced"                    |
| "Verify everything"    | Unbounded scope + implied omniscience  | "State whether evidence is present"                |
| "As discussed above"   | Treats conversation memory as evidence | "Use only provided text"                           |
| "Assume typical setup" | Authorises invention                   | "State assumptions explicitly; default to unknown" |

### 8.5 Reviewing AI-Generated Artifacts

When reviewing output produced through AI ecosystem:

1. **Check for unsupported claims.** Does the artifact assert facts without quoting evidence?
2. **Check for missing "Unknown" sections.** If a template section is filled but no evidence was provided, the content is likely fabricated.
3. **Check assumption labels.** Are assumptions explicitly marked and their impact noted?
4. **Check template adherence.** Does the output follow the specified template structure?
5. **Check scope boundaries.** Does the output stay within the evidence scope declared in the prompt?

---

## 9) Mode Separation

AI ecosystem defines three operational modes, and every substantial output should declare which one it operates in:

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
├── agents/                          # Cognition contracts
├── instructions/                    # On-demand procedural knowledge + enforcement (verification-checklist)
├── prompts/                         # Task wiring
├── templates/                       # Output structure
├── procedures/                      # Executable playbooks
├── skills/                          # Composable workflows
├── context/                         # Descriptive grounding
└── hooks/                           # Runtime enforcement
```

> For current file counts and rosters, see `.github/context/AI ecosystem-artifact-freshness.md`.
> For individual file listings, browse the directories or run `./scripts/verify-AI ecosystem-freshness.sh`.

---

## 11) Evolution History

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
- `scripts/verify-AI ecosystem-freshness.sh` automates freshness validation

### v3 Maintenance (2026-03-29)

- Split `AI ecosystem-governance.instructions.md` into runtime (always-on, `applyTo: "**"`) + authoring (scoped to `.github/**`)
- Deleted `session-today.instructions.md` (obsolete — replaced by VS Code memory system)
- Created `session.save.prompt.md` for curating conversation learnings into persistent memory
- Full ecosystem audit: fixed missing prompt frontmatter, narrowed over-broad `applyTo` scopes for stack instructions, relocated repo-specific prompt to `divical-api/prompts/`
- Documented Explore subagent (VS Code built-in) in agent roster
- Archived 5 dead-weight files from v1 consolidation

### v3 Expansion (2026-04-04)

- Added test-orchestrator, qa-orchestrator, research-orchestrator (visible) and creative-partner, devils-advocate-partner (hidden)
- Added Claude Opus 4.6 to research pipeline Stage 1 fan-out
- Removed AlphaVantage as a provider (FMP + Mock only)
- Added orchestrator handoff protocol: feature-orchestrator → test-orchestrator → qa-orchestrator
- Test pipeline: 5-phase self-healing loop with assertion policy (locked vs flexible) and financial-logic review aspect
- QA pipeline: 4-gate sequential validation with sparring escalation

### v3 Handoff + Remediation Update (2026-04-05)

- Added explicit `handoffs:` frontmatter fields to feature-orchestrator and test-orchestrator agent files for VS Code Autopilot chaining
- Handoff configuration: `send: true` (auto-submit in Autopilot), `model: Claude Opus 4.6 (copilot)` (explicit model for handoff target)
- QA orchestrator upgraded from diagnostic-only to diagnostic + auto-remediation:
  - Removed "never fixes code" constraint
  - Added remediation loop (max 3 iterations): identify failures → delegate fixes to software-engineer → re-run failed gates
  - New verdict types: PASS (REMEDIATED), PASS WITH CAVEATS (REMEDIATED)
  - Remediation exclusions: coverage warnings (non-blocking), `needs-human-decision` sparring findings, architectural issues
  - QA procedure updated with Step 8 (Auto-Remediation) and Step 9 (Final Verdict)

> For current artifact counts, see `.github/context/AI ecosystem-artifact-freshness.md`.

---

## 12) Summary

AI ecosystem is an engineering architecture for governing AI-assisted work. It separates cognition (agents) from domain knowledge (instructions), execution (procedures and prompts), and enforcement (verification checklist and constitution). Each artifact type has a single responsibility, authority flows through a strict hierarchy, and missing evidence is surfaced rather than hidden.

The v3 architecture achieves this with a deliberately small footprint. The system makes honesty cheap and fabrication expensive — not by asking the model to "be honest," but by structuring the environment so that truthful, bounded outputs are the path of least resistance.

> For current artifact counts and roster, see `.github/context/AI ecosystem-artifact-freshness.md`.

> Creativity belongs in cognition. Discipline belongs in artifacts. Authority must not leak.
