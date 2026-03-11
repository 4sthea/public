# LLM-First CLASP Restructuring Plan

**Date:** 2026-03-06  
**Status:** Complete  
**Source Documents:**
- `docs/research/llm-first-restructuring.md` (v1 — architectural vision)
- `docs/research/llm-first-restructuring-2.md` (v2 — concrete deprecation manifest)

---

## 1. Objective

Transition from the current 16-agent specialist model to a lean Orchestration Quad aligned with VS Code Copilot's native sub-agent capabilities. The restructuring consolidates institutional knowledge from 9 deprecated agents into reusable instruction files, rewires prompts to surviving agents, and updates all context/reference files.

---

## 2. Current State Inventory

### Agents (16 total in `.github/agents/`)

| Agent | Status |
|---|---|
| agent-router | **DEPRECATE** |
| code-analyst | **DEPRECATE** |
| code-reviewer | SURVIVE |
| feature-engineer | **DEPRECATE** |
| learn-coach | SURVIVE |
| security-reviewer | SURVIVE |
| skill-teacher | SURVIVE |
| software-architect | SURVIVE (expanded: absorbs Planner role) |
| software-engineer | SURVIVE (expanded: absorbs Coder role) |
| strategy-analyst | **DEPRECATE** |
| tech-debt-analyst | **DEPRECATE** |
| tech-debt-resolver | **DEPRECATE** |
| tech-writer | **DEPRECATE** |
| test-architect | **DEPRECATE** |
| test-engineer | **DEPRECATE** |
| thinking-assistant | SURVIVE |

### Instructions (7 in `.github/instructions/`)
All survive. New instruction files created to absorb deprecated agent knowledge.

### Procedures (5 in `.github/procedures/`)
- `routing-rules.procedure.md` — **DELETE** (agent-router is deprecated)
- All others survive.

### Prompts (21 in `.github/prompts/`)
Prompts referencing deprecated agents get rewired to surviving agents.

### Templates (16 in `.github/templates/`)
All survive unchanged (Structure layer remains rigid per v1 spec).

### Context (6 in `.github/context/`)
Updated to remove deprecated agent references and register new structure.

---

## 3. Workflow Consolidation Mapping

Per v2 specification §4:

| Deprecated Domain | Absorbing Agent | Mechanism |
|---|---|---|
| Strategy + Features (strategy-analyst, feature-engineer) | **software-architect** | On-demand instruction files |
| Analysis + Documentation (code-analyst, tech-writer) | **software-engineer** | On-demand instruction files |
| Testing (test-architect, test-engineer) | **software-engineer** (execution), **software-architect** (strategy) | Existing + new instruction files |
| Tech Debt (tech-debt-analyst, tech-debt-resolver) | **software-engineer** | Existing instruction files (already covered) |
| Routing (agent-router) | Native VS Code routing | No agent needed |

---

## 4. Execution Steps

### Phase 1: Extract Institutional Knowledge → New Instruction Files

Create instruction files for capabilities not yet covered:

| New Instruction File | Extracted From | Key Logic |
|---|---|---|
| `test-strategy.instructions.md` | test-architect | Test pyramid, layering, contract boundaries, quality signals |
| `feature-specification.instructions.md` | feature-engineer | Requirement decomposition, acceptance criteria, edge cases |
| `code-analysis.instructions.md` | code-analyst | Control flow tracing, data flow analysis, dependency mapping |
| `strategy-analysis.instructions.md` | strategy-analyst | Goal clarification, option analysis, tradeoff evaluation |
| `documentation.instructions.md` | tech-writer | README/ADR structure, documentation synthesis, conservative content |

Already covered (no new files needed):
- test-aaa-pattern.instructions.md ← test-engineer AAA patterns
- tech-debt-fix.instructions.md ← tech-debt-resolver remediation
- tech-debt-review.instructions.md ← tech-debt-analyst/resolver review
- refactor-plan.instructions.md ← tech-debt-resolver refactor planning

### Phase 2: Rewire Prompts to Surviving Agents

| Prompt | Old Agent | New Agent |
|---|---|---|
| fix-artifact-from-lint.prompt.md | code-analyst | software-engineer |
| generate-code-analysis.prompt.md | code-analyst | software-engineer |
| generate-codebase-components.prompt.md | tech-writer | software-engineer |
| generate-feature-specification.prompt.md | feature-engineer | software-architect |
| generate-strategy.creative.prompt.md | strategy-analyst | software-architect |
| generate-strategy.prompt.md | strategy-analyst | software-architect |
| generate-summary.prompt.md | tech-writer | software-engineer |
| generate-tech-debt-analysis.prompt.md | tech-debt-analyst | software-engineer |
| generate-test-architecture.prompt.md | test-architect | software-architect |
| generate-test-changelog.prompt.md | test-engineer | software-engineer |
| lint-artifacts.prompt.md | code-analyst | software-engineer |
| log-user-pitfall.prompt.md | tech-writer | software-engineer |
| readme-generation.prompt.md | tech-writer | software-engineer |

### Phase 3: Delete Deprecated Agent Files

Delete 9 files from `.github/agents/`:
- agent-router.agent.md
- code-analyst.agent.md
- feature-engineer.agent.md
- strategy-analyst.agent.md
- tech-debt-analyst.agent.md
- tech-debt-resolver.agent.md
- tech-writer.agent.md
- test-architect.agent.md
- test-engineer.agent.md

### Phase 4: Delete Obsolete Infrastructure

- `.github/procedures/routing-rules.procedure.md` (agent-router companion)

### Phase 5: Update Surviving Agents

**software-engineer** — expand authorized domain:
- Add: code analysis, testing, tech debt remediation, documentation synthesis
- Add procedural companions for new instruction files
- Remove cross-references to deprecated agents in exclusions

**software-architect** — expand authorized domain:
- Add: strategy analysis, feature specification, test architecture
- Add procedural companions for new instruction files
- Remove cross-references to deprecated agents in exclusions

**code-reviewer** — minor update:
- Remove cross-references to deprecated agents

### Phase 6: Update Context and Reference Files

- `context-pointers.md` — purge deprecated agent references
- `clasp-system-context.md` — update agent roster, remove obsolete references
- `verification-checklist.md` — update agents check section
- `what-belongs-where.md` — reflect consolidated agent structure
- `copilot-lint.instructions.md` — no structural change needed (lint by file type, not agent name)
- `shared-context.md` — no changes needed (does not reference specific agents)

### Phase 7: Reference Integrity Check

Grep for any remaining references to deleted agent names across all `.github/` files.

---

## 5. Risk Assessment

| Risk | Mitigation |
|---|---|
| Surviving agents become overloaded with too many domains | Instruction files keep knowledge modular; agents invoke on-demand |
| Prompts break if agent names don't match VS Code registration | Verify agent names match VS Code `*.agent.md` frontmatter |
| Institutional knowledge lost during deletion | Extract before delete; instruction files preserve procedural logic |
| Templates reference deprecated agents | Templates are structure-only with no agent references (verified) |

---

## 6. What This Plan Does NOT Cover

- Multi-model orchestration (Sonnet/GPT-4o/Gemini routing) — outside VS Code Copilot's current capabilities
- Git Worktree isolation for sub-agents — infrastructure concern, not file restructuring
- Ralph Loop / browser verification — requires tooling setup beyond CLASP file changes
- Agent Sessions view / Mission Control — VS Code extension concern

These are aspirational capabilities from v1/v2 that require tooling beyond the CLASP file system.
