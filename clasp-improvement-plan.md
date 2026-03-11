# CLASP Ecosystem Improvement Plan v2

**Date:** 2026-03-06
**Status:** Implemented (Phases 1–6 complete)
**Goal:** An AI ecosystem that produces production-ready, high-quality code with minimal hallucination.

---

## 1. Diagnosis: CLASP Optimizes for the Wrong Thing

### The numbers

| Category                   | Files  | Lines      | Serves code quality?                                                          |
| -------------------------- | ------ | ---------- | ----------------------------------------------------------------------------- |
| Constitution + enforcement | 2      | ~450       | Partially (anti-hallucination)                                                |
| Agents                     | 7      | ~600       | Yes (3 code-facing, 4 ancillary)                                              |
| Instructions               | 12     | ~880       | **2 of 12** help write code. Rest are meta-governance or document generation. |
| Prompts                    | 22     | ~2,220     | **0 of 22** help write code. All generate documents.                          |
| Procedures                 | 4      | ~255       | 0 — all govern CLASP artifacts or documents                                   |
| Templates                  | 16     | ~800       | 0 — all structure documents, not code                                         |
| Context                    | 6      | ~570       | 1 (codebase-context.md, currently empty)                                      |
| Auxiliary checklists       | 4      | ~310       | 0 — all govern CLASP artifact creation                                        |
| **Total**                  | **73** | **~6,085** |                                                                               |

### The core problem

CLASP has a **governance-to-code ratio** problem. Of ~6,000 lines of AI governance:

- **~500 lines** directly help the agent write or verify code (verification checklist, code-analysis instructions, test pattern instructions, the software-engineer agent)
- **~2,000 lines** govern CLASP itself (lint rules for markdown artifacts, checklists for creating agents/prompts/instructions, templates for creating more CLASP files, procedures for linting CLASP files, a 300-line document explaining how CLASP works, prompts for creating CLASP artifacts)
- **~2,200 lines** generate documents (22 prompts + 16 templates for changelogs, architecture docs, strategy docs, README generation, etc.)
- **~1,400 lines** are the constitution, context files, and agent definitions

The system spends more tokens **governing itself** than it spends **enabling the agent to write good code**.

### What's missing

Zero instructions about the actual tech stack:

- No Python/FastAPI patterns, error handling, or API design conventions
- No React/TypeScript component patterns, state management, or hook conventions
- No SQLAlchemy/Alembic migration patterns
- No testing patterns specific to this codebase (pytest fixtures, test data, mocking)
- `codebase-context.md` is empty — the one file designed for learned codebase facts has nothing in it

The agent tasked with writing production code in Python/FastAPI/React has **no instruction about how this codebase works**. It has 244 lines about how to lint CLASP markdown files.

### What works

The anti-hallucination framework is sound:

- `verification-checklist.md` — genuinely prevents fabrication. Keep.
- Constitution §3 (Epistemic Rules) — "never fabricate, label claims" works. Keep.
- Constitution §4 (Assumptions Policy) — stops agents from guessing. Keep.
- The reasoning-routine instruction — evidence-bound reasoning prevents confident bullshit. Keep.
- The 7-agent roster — right-sized after the 16→7 consolidation. Keep structure.

### What doesn't work

1. **The software-engineer agent is passive.** It proposes changes and waits for the user to verify. It should run tests, read build output, and fix its own errors before returning.

2. **All agents have identical tool arrays.** A code reviewer can edit files. A thinking assistant can execute shell commands. This blurs responsibility boundaries.

3. **The constitution is bloated.** 301 lines. Only ~40 are epistemic laws. The rest is operational governance that doesn't need rank-1 authority and blocks evolution.

4. **12 instruction files, but none about the codebase.** The agent knows how to structure an Arrange-Act-Assert test, but doesn't know that this project uses pytest, SQLAlchemy, or Alembic.

5. **22 prompts all generate documents, none help write code.** Prompts are the most expensive artifact type (~100 lines each, loaded on invocation). Every prompt produces a markdown document. Not one produces code, runs a migration, scaffolds a component, or deploys anything.

6. **Meta-governance is disproportionate.** 18 files (~1,600 lines) exist solely to govern CLASP artifact creation. For a 7-agent system, this is overhead beyond what adds value.

7. **The lint rules don't match reality.** `copilot-lint.instructions.md` requires sections like `## Success Definition`, `## Output Contract`, and `## Truth & Epistemic Hygiene` in agents — but no actual agent file has these sections. The lint rules describe a fantasy structure.

---

## 2. Strategic Redesign

### Principle: Token budget allocation

Every token loaded into the agent's context is competing with space for actual code, actual error messages, and actual reasoning. Governance tokens should be the minimum needed to prevent hallucination and guide behavior. Everything else should either help the agent write code or not exist.

**Target allocation:**

| Category                                                   | Current % | Target % | Strategy                                                           |
| ---------------------------------------------------------- | --------- | -------- | ------------------------------------------------------------------ |
| Anti-hallucination (constitution, verification, reasoning) | ~8%       | ~10%     | Lean constitution + verification checklist. Slightly more focused. |
| Agent definitions                                          | ~10%      | ~12%     | Stronger posture for software-engineer. Tighter tool arrays.       |
| Stack-specific coding guidance                             | **0%**    | **~25%** | New: Python/FastAPI, React/TS, DB, testing instructions            |
| Codebase context                                           | **0%**    | **~10%** | Populate codebase-context.md with real patterns                    |
| Document generation (prompts + templates)                  | ~50%      | ~25%     | Trim to prompts you actively use. Delete unused templates.         |
| Meta-governance                                            | ~27%      | ~8%      | Consolidate into one reference. Delete checklists for checklists.  |
| Skills (on-demand)                                         | 0%        | ~10%     | Bundle document workflows as skills (zero cost until invoked)      |

### What to keep, change, cut, and add

**Keep as-is:**

- `verification-checklist.md` — the most effective anti-hallucination tool
- `reasoning-routine.instructions.md` — evidence-bound reasoning
- `code-analysis.instructions.md` — helps analyze actual code
- `test-strategy.instructions.md` — helps design tests
- `documentation.instructions.md` — helps write docs when needed
- Agent files: `code-reviewer`, `security-reviewer`, `software-architect`, `thinking-assistant` (with tool array fixes)

**Change:**

- `copilot-instructions.md` — thin to epistemic core (~50 lines)
- `software-engineer.agent.md` — Ralph Loop posture (self-verifying)
- `anti-slug-style.instructions.md` — add `applyTo: "**"` frontmatter, shorten to ~40 lines
- All 7 agent tool arrays — role-appropriate restrictions
- `learn-coach` + `skill-teacher` — merge into one `teacher` agent (they share identical posture patterns)

**Cut (delete or archive):**

- `copilot-lint.instructions.md` (244 lines) — describes a fantasy structure no agent file matches. If kept, rewrite to match actual structure. Or migrate to an on-demand skill.
- `agent-creation-checklist.md`, `instruction-file-checklist.md`, `prompt-creation-checklist.md` — meta-checklists for creating CLASP files. The `create-agent.prompt.md`, `create-instructions.prompt.md`, and `create-prompt.prompt.md` already contain this guidance. Delete the standalone checklists.
- `what-belongs-where.md` — useful concept but 120 lines of decision tree that only matters when creating new CLASP artifacts. Merge key rules into the governance instruction.
- `guideline.template.md` — no guidelines directory, no guideline files exist. Dead template.
- `agent.template.md`, `instructions.template.md`, `prompt.template.md`, `procedure.template.md` — CLASP-creation scaffolds. The create-\* prompts already contain the structure guidance. Delete.
- `.github/guidelines/` and `.github/rules/` — empty directories
- `context-pointers.md` — 70-line index of 5 other files. The files are self-describing. Delete.
- `clasp-system-context.md` — 300-line CLASP explainer. Valuable for onboarding but loaded into context. Move core rules to the governance instruction; archive the explainer to `docs/`.
- Prompts: consolidate `generate-strategy.prompt.md` + `generate-strategy.creative.prompt.md` into one (they differ only in tone). Same for `generate-software-architecture` + `.creative`. Delete `generate-summary.prompt.md` (rarely used).

**Add (the missing piece):**

- `stack-python.instructions.md` — Python/FastAPI patterns, error handling, Pydantic model conventions
- `stack-react.instructions.md` — React/TypeScript component patterns, hook conventions, state management
- `stack-database.instructions.md` — SQLAlchemy patterns, Alembic migration conventions
- Populate `codebase-context.md` with actual codebase facts extracted from the repo
- `SessionStart` hook to inject git branch + recent changes into context

---

## 3. Execution Plan

### Phase 1: Make the Software Engineer Actually Verify Its Work (HIGH impact, LOW effort)

**Change 1: Ralph Loop posture.** Rewrite `software-engineer.agent.md`:

Current Reasoning Posture:

> Reasons pragmatically, favoring minimal, safe changes... Highlights risks and conditional steps when context is incomplete.

New Reasoning Posture:

```
Implements changes and verifies them before returning control. Runs the build,
runs the tests, reads the output. If something fails, reads the error, fixes
the code, and loops. Returns to the user only when the change is verified — or
when stuck and needs human input.

Fallback: if lacking documentation, unable to reproduce an error, or uncertain
about the correct approach — stop and ask. Do not guess. Do not spin.
```

Current Preflight:

> List validation steps as conditional if tests/build tools are not specified.

New Preflight:

```
- Discover and run build/test commands. Evidence of success required before concluding.
- If build/test commands are unknown, check pyproject.toml, package.json, Makefile, or tasks.json.
- Apply verification-checklist.md during work, not as a post-hoc gate.
```

**Change 2: Tool arrays.** Update all 7 agents:

| Agent                | New Tools                                    |
| -------------------- | -------------------------------------------- |
| `software-engineer`  | `[read, search, agent, edit, todo, execute]` |
| `software-architect` | `[read, search, agent, edit, todo]`          |
| `code-reviewer`      | `[read, search, agent, todo]`                |
| `security-reviewer`  | `[read, search, agent, todo]`                |
| `thinking-assistant` | `[read, search, agent, todo]`                |
| `learn-coach`        | `[read, search, agent, todo]`                |
| `skill-teacher`      | `[read, search, agent, todo]`                |

### Phase 2: Give the Agent Stack Knowledge (HIGH impact, MEDIUM effort)

Create instruction files that actually help write code in this codebase:

**`stack-python.instructions.md`** (`applyTo: "**/*.py"`)

- Content: Extract from actual codebase — Pydantic model patterns, FastAPI route patterns, dependency injection, error handling, logging conventions, service layer patterns
- Sources: `divical-api/app/` — read real code, document real patterns

**`stack-react.instructions.md`** (`applyTo: "**/*.{tsx,jsx,ts,js}"`)

- Content: Extract from actual codebase — component structure, hook patterns, state management (whatever is used), API client patterns, styling conventions
- Sources: `divical-web/src/` — read real code, document real patterns

**`stack-database.instructions.md`** (`applyTo: "**/{models,alembic,migrations}/**"`)

- Content: SQLAlchemy model conventions, Alembic migration patterns, session handling, relationship patterns
- Sources: `divical-api/app/models/`, `divical-api/alembic/` — read real code

**Populate `codebase-context.md`:**

- Project structure overview (what lives where)
- Build/test/run commands
- Key architectural decisions (Python backend + React frontend, specific libraries chosen and why)
- Known gotchas from past sessions

### Phase 3: Thin the Constitution (HIGH impact, MEDIUM effort)

Split `copilot-instructions.md` into:

**1. Lean constitution** (`copilot-instructions.md`, ~50 lines):

- §1 Precedence (the hierarchy)
- §3 Epistemic Rules (never fabricate, label claims)
- §4 Assumptions Policy (stop if unsure)
- §9 Mistakes (acknowledge, correct, state which rule was violated)
- §13 Mode Declaration (epistemic vs teaching)
- Pointer to governance instruction for operational rules

**2. Governance instruction** (`clasp-governance.instructions.md`, `applyTo: "**"`):

- Everything operational: mission, clarification policy, reasoning output format, validation requirements, high-impact decisions, artifact ownership, dependency reads, change propagation, preflight discipline
- Merge in the key rules from `what-belongs-where.md` (artifact routing)
- Merge in the core CLASP layering rules from `clasp-system-context.md`

This lets the epistemic core stay stable while operational rules evolve.

### Phase 4: Cut the Dead Weight (MEDIUM impact, LOW effort)

**Delete:**

- `.github/guidelines/` (empty)
- `.github/rules/` (empty)
- `context-pointers.md` (5-file index; files are self-describing)
- `guideline.template.md` (no guidelines exist)
- `agent.template.md`, `instructions.template.md`, `prompt.template.md`, `procedure.template.md` (duplicated in create-\* prompts)
- `agent-creation-checklist.md`, `instruction-file-checklist.md`, `prompt-creation-checklist.md` (duplicated in create-\* prompts)
- `generate-summary.prompt.md` (rarely used)

**Move to `docs/architecture/` (archive, not loaded into context):**

- `clasp-system-context.md` — valuable reference but 300 lines that don't need to be in every conversation. Core rules already live in the governance instruction after Phase 3.
- `what-belongs-where.md` — useful reference after merging key rules into governance instruction

**Merge:**

- `learn-coach.agent.md` + `skill-teacher.agent.md` → `teacher.agent.md` (one teaching agent with expanded scope)
- `generate-strategy.prompt.md` + `generate-strategy.creative.prompt.md` → one prompt with a "style" parameter
- `generate-software-architecture.prompt.md` + `generate-software-architecture.creative.prompt.md` → same

**Fix `copilot-lint.instructions.md`:**

- Either rewrite the lint rules to match the actual agent/prompt/instruction structure, or convert to an on-demand skill. The current 244-line file describes sections that don't exist in actual files — this is the lint rules hallucinating about their own codebase.

### Phase 5: Scope Instructions Properly (MEDIUM impact, LOW effort)

Add frontmatter to the 6 unscoped instruction files so they only load when relevant:

| File                               | Frontmatter                                                                |
| ---------------------------------- | -------------------------------------------------------------------------- |
| `anti-slug-style.instructions.md`  | `applyTo: "**"` (always-on)                                                |
| `copilot-lint.instructions.md`     | `description: "Use when linting CLASP artifacts"` (on-demand only)         |
| `refactor-plan.instructions.md`    | `description: "Use when designing refactor plans"` (on-demand only)        |
| `tech-debt-fix.instructions.md`    | `description: "Use when implementing tech debt fixes"` (on-demand only)    |
| `tech-debt-review.instructions.md` | `description: "Use when reviewing tech debt remediation"` (on-demand only) |
| `test-aaa-pattern.instructions.md` | `applyTo: "**/*test*,**/*spec*"` (when editing tests)                      |

### Phase 6: Bundle Document Workflows as Skills (MEDIUM impact, MEDIUM effort)

Convert document-generation workflows into on-demand skills. Zero context cost until invoked.

| Skill           | Bundles                                           | Invoked via      |
| --------------- | ------------------------------------------------- | ---------------- |
| `artifact-lint` | lint procedure + lint rules                       | `/artifact-lint` |
| `tech-debt`     | review + fix procedures + instructions + template | `/tech-debt`     |
| `readme-gen`    | readme procedure + template + doc instructions    | `/readme-gen`    |

After migration, delete the source instruction/procedure files (they're now inside the skill).

### Phase 7: Optional Improvements (LOW priority)

- Add `model:` frontmatter to `code-reviewer` (different model from engineer for adversarial review)
- Add `## Mode` to prompts (Epistemic for all except `learn-skill` which is Teaching)
- Add `SessionStart` hook to inject git branch + recent changes
- Add `PostToolUse` hook for auto-formatting
- Create Evidence Ledger template for auditability

---

## 4. Priority Summary

| #   | Action                                          | Impact on code quality                              | Effort | Do when      |
| --- | ----------------------------------------------- | --------------------------------------------------- | ------ | ------------ |
| 1   | Ralph Loop posture for software-engineer        | **HIGH** — agent verifies its own work              | LOW    | **Now**      |
| 2   | Tighten agent tool arrays                       | MEDIUM — clearer agent responsibilities             | LOW    | **Now**      |
| 3   | Stack-specific instructions (Python, React, DB) | **HIGH** — agent knows the codebase patterns        | MEDIUM | **Now**      |
| 4   | Populate codebase-context.md                    | **HIGH** — agent knows project structure + commands | MEDIUM | **Now**      |
| 5   | Constitution thinning                           | HIGH — unblocks operational evolution               | MEDIUM | **Next**     |
| 6   | Delete dead weight (12+ files)                  | MEDIUM — less noise in context                      | LOW    | **Next**     |
| 7   | Scope instruction frontmatter                   | MEDIUM — context window savings                     | LOW    | **Next**     |
| 8   | Merge duplicate agents + prompts                | MEDIUM — less confusion                             | LOW    | **Next**     |
| 9   | Fix or rewrite lint rules                       | LOW — only matters when linting CLASP               | MEDIUM | **Later**    |
| 10  | Bundle document workflows as skills             | MEDIUM — zero-cost loading                          | MEDIUM | **Later**    |
| 11  | Lifecycle hooks                                 | LOW-MEDIUM — nice automation                        | MEDIUM | **Later**    |
| 12  | Model frontmatter                               | LOW — adversarial diversity                         | LOW    | **Optional** |
| 13  | Evidence Ledger template                        | LOW — auditability                                  | MEDIUM | **Defer**    |

---

## 5. Risk Assessment

| Risk                                                          | Likelihood | Mitigation                                                                                           |
| ------------------------------------------------------------- | ---------- | ---------------------------------------------------------------------------------------------------- |
| Ralph Loop causes agent to spin on unfixable errors           | Medium     | Fallback clause: "if stuck, stop and ask."                                                           |
| Stack instructions become stale as codebase evolves           | Medium     | Include directive for software-engineer to update codebase-context.md when it discovers new patterns |
| Constitution thinning weakens operational rule compliance     | Medium     | Governance instruction gets `applyTo: "**"` — auto-attached to every conversation at rank 2          |
| Tool restrictions block legitimate agent work                 | Medium     | Test common workflows. Add tools back if needed.                                                     |
| Deleting meta-governance files makes CLASP harder to maintain | Low        | The create-\* prompts already contain the scaffold guidance. Archive deleted files to `docs/`.       |
| Lint rules rewrite is wasted effort                           | Medium     | Only rewrite if you actively use the lint workflow. Otherwise convert to on-demand skill.            |

---

## 6. What the Previous Plan Got Right (Preserved)

The v1 plan produced valid analysis on these topics. Key conclusions are preserved in this rewrite:

- **Finding 7 (Ralph Loop posture):** Correct. Highest-impact single change. → Phase 1
- **Finding 8 (tool arrays):** Correct. All agents have identical bloated arrays. → Phase 1
- **Finding 11 (constitution scope violation):** Correct. The file violates its own §10. → Phase 3
- **Finding 2 (instruction scoping):** Correct. 6 files lack frontmatter, waste context. → Phase 5
- **Finding 10 (self-updating reconsidered):** Correct. Viable after constitution thinning at the governance layer.
- **Finding 9 (orchestrator):** Correct to defer. VS Code native routing is sufficient for now.
- **Skills, hooks, model selection re-evaluations:** All valid. Integrated into Phases 6-7.

### What the previous plan missed

1. **Zero stack-specific guidance.** The most impactful gap isn't a CLASP structural issue — it's that the agent has no knowledge of Python/FastAPI/React patterns. This is now Phase 2.

2. **Governance-to-code ratio.** The plan focused on restructuring governance (lint rules, mode declarations, skill migration) without questioning whether the governance itself is proportionate. ~2,000 lines of CLASP meta-governance for a 7-agent system is overhead.

3. **Lint rules vs reality.** The plan treated `copilot-lint.instructions.md` as a valid document needing better scoping. The rules describe sections that don't exist in any actual agent file — the lint rules themselves hallucinate.

4. **Teacher agent duplication.** `learn-coach` and `skill-teacher` have near-identical postures, identical tool arrays, and overlapping domains. The plan proposed tightening tools but not merging.

5. **Template bloat.** 16 templates, 5 of which exist solely to scaffold more CLASP files. The create-\* prompts already embed the structure guidance.

6. **Empty context files.** `codebase-context.md` and `codebase-components.md` are both empty placeholders. The system designed for codebase knowledge capture was never populated.
