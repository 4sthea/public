# CLASP v3 Migration Guide — Research-Driven Restructuring

**Date:** 2026-03-14
**Status:** Ready for implementation
**Basis:** Research report on agent persona effectiveness, tool restriction mechanics, and cognitive lane isolation evidence (2025–2026 literature review)

---

## Executive Summary

CLASP v3 applies three research findings to radically simplify the governance ecosystem:

1. **Persona labels are theater on frontier models.** A 162-persona study found persona prompts have negligible effects on task accuracy. "You are a Software Architect" spends tokens for zero accuracy return on Opus 4.6, Sonnet 4.6, or GPT-5.x.

2. **Tool restrictions are the load-bearing constraint.** Hard `allowed_tools` enforcement is the single most important function agents provide — the principle of least privilege applied to AI. This is the ONLY reason to keep separate agent.md files.

3. **Instruction files can replace cognitive posture.** Domain knowledge (architecture reasoning, security review methodology, feature decomposition) lives as on-demand instruction files that any agent invokes when needed.

**Result:** 7 agents → 3, with all institutional knowledge preserved in instruction files.

---

## Agent Changes

### Surviving Agents (3)

| Agent | Tool Restriction | Model | Justification |
|-------|-----------------|-------|---------------|
| **software-engineer** | read, search, agent, edit, todo, execute | Opus 4.6 | Only agent that can modify files and run commands. Ralph Loop self-verification. |
| **code-reviewer** | read, search, agent, todo | o4-mini | Read-only. Different model creates adversarial consensus. Hard tool restriction prevents edits. |
| **thinking-assistant** | read, search, agent, todo | default | Read-only. Prevents premature implementation during planning. Now absorbs architect/teacher domains. |

### Deleted Agents (4) + Knowledge Extraction

| Deleted Agent | Why | Knowledge Preserved In |
|---------------|-----|----------------------|
| **software-architect** | Identical tool set to thinking-assistant (read-only) or engineer (with edit). Persona-based "architectural reasoning" has negligible effect on frontier models. Its cognitive stance was the least valuable part of the definition. | `architecture.instructions.md` (NEW) — architecture decisions, strategy analysis, feature specification |
| **security-reviewer** | Identical tool set to code-reviewer (read-only). Security domain knowledge is procedural, not identity-based. Code-reviewer already reviews adversarially with a different model. | `security-review.instructions.md` (NEW) — security review methodology, common review areas, risk identification |
| **teacher** | Zero unique tool restrictions. Teaching is a reasoning mode, not a mechanical constraint. Any agent can teach when instruction files provide the domain knowledge. | Absorbed into thinking-assistant's expanded authorized domain. Teaching posture guidance in thinking-assistant agent file. |
| **skill-teacher** | Should have been merged into teacher in v2. Identical posture and tool set. | Same as teacher above. |

**Note:** If `learn-coach.agent.md` still exists, delete it too — it was merged into `teacher` which is now absorbed into `thinking-assistant`.

---

## Instruction Changes

### New Instruction Files (3)

| File | Source | Content |
|------|--------|---------|
| `architecture.instructions.md` | software-architect + strategy-analyst + feature-engineer | Architecture decisions, strategy analysis, feature specification — three sections with scope checks, reasoning approaches, and documentation guidance |
| `security-review.instructions.md` | security-reviewer | Security review methodology, common review areas (auth, input, config, data), risk identification patterns |
| `governance.instructions.md` | what-belongs-where + clasp-system-context + artifact ownership | Consolidated CLASP rules: agent roster, artifact ownership table, placement decision tree, dependency read contract, change propagation |

### Deleted Instruction Files (3)

| File | Why |
|------|-----|
| `copilot-lint.instructions.md` | 244 lines of meta-governance describing a structure no agent file matches. The create-* prompts (also deleted) contained equivalent guidance. If linting is needed in the future, it should be a script, not a prompt. |
| `feature-specification.instructions.md` | Folded into `architecture.instructions.md` § Feature Specification |
| `strategy-analysis.instructions.md` | Folded into `architecture.instructions.md` § Strategy Analysis |

### Kept As-Is (12)

- `stack-python.instructions.md` — Python/FastAPI patterns (helps write code)
- `stack-react.instructions.md` — React/TypeScript patterns (helps write code)
- `stack-database.instructions.md` — SQLAlchemy/Alembic patterns (helps write code)
- `code-analysis.instructions.md` — control flow tracing, data flow (helps analyze code)
- `test-strategy.instructions.md` — test pyramid, layering, quality signals
- `test-aaa-pattern.instructions.md` — AAA test structuring
- `documentation.instructions.md` — README/ADR synthesis
- `refactor-plan.instructions.md` — staged refactoring
- `anti-slug-style.instructions.md` — writing style guidance
- `reasoning-routine.instructions.md` — evidence-bound reasoning
- `tech-debt-fix.instructions.md` — debt remediation
- `tech-debt-review.instructions.md` — debt review

---

## Prompt Changes

### Prompt Agent Rewiring

All document-generation prompts route to `software-engineer` because they require file writing (`edit` tool).

| Prompt | Old Agent | New Agent | Instruction Companion |
|--------|-----------|-----------|----------------------|
| generate-feature-specification | software-architect | **software-engineer** | architecture.instructions.md |
| generate-strategy | software-architect | **software-engineer** | architecture.instructions.md |
| generate-software-architecture | software-architect | **software-engineer** | architecture.instructions.md |
| generate-test-architecture | software-architect | **software-engineer** | test-strategy.instructions.md |
| generate-security-review | security-reviewer | **software-engineer** | security-review.instructions.md |

**No agent change needed** (already correctly routed):
- generate-code-analysis → software-engineer
- generate-tech-debt-analysis → software-engineer
- generate-test-changelog → software-engineer
- generate-code-review → code-reviewer
- readme-generation → software-engineer

### Frontmatter Update Required

For each rewired prompt, update only the YAML frontmatter:

```yaml
# Example: generate-feature-specification.prompt.md
---
agent: software-engineer          # was: software-architect
model: Claude Sonnet 4.6 (copilot)
tools: [read, search, agent, edit, todo, vscode, execute]
---
```

```yaml
# Example: generate-security-review.prompt.md
---
agent: software-engineer          # was: security-reviewer
model: Claude Sonnet 4.6 (copilot)
tools: [read, search, agent, edit, todo, vscode, execute]
---
```

### Deleted Prompts (8)

| Prompt | Why |
|--------|-----|
| `create-agent.prompt.md` | Meta-governance — CLASP governing itself. Rarely used. The governance instruction provides equivalent guidance. |
| `create-instructions.prompt.md` | Meta-governance. Same reasoning. |
| `create-prompt.prompt.md` | Meta-governance. Same reasoning. |
| `fix-artifact-from-lint.prompt.md` | Companion to deleted lint infrastructure. |
| `lint-artifacts.prompt.md` | Companion to deleted lint infrastructure. |
| `generate-summary.prompt.md` | Rarely used. Any agent can summarize without a dedicated prompt. |
| `log-user-pitfall.prompt.md` | Minimal value. User pitfalls can be logged manually or via simple instruction. |
| `generate-codebase-components.prompt.md` | One-time inventory task. Not worth maintaining a dedicated prompt. |

### Consolidation

If `generate-strategy.creative.prompt.md` and `generate-software-architecture.creative.prompt.md` still exist as separate files, merge them into their standard counterparts using the style toggle already present in `generate-strategy.prompt.md`:

```yaml
### Style
Choose one (default: standard):
- **standard** — structured, declarative
- **creative** — narrative, explanatory
```

---

## Procedure Changes

### Deleted (1)

| File | Why |
|------|-----|
| `artifact-lint.procedure.md` | Companion to deleted lint infrastructure. Meta-governance for auditing CLASP files. |

### Kept As-Is (2–3)

- `readme-generation.procedure.md`
- `tech-debt-review.procedure.md` (if exists)
- `tech-debt-fix.procedure.md` (if exists)

---

## Template Changes

### Deleted (5)

| File | Why |
|------|-----|
| `agent.template.md` | CLASP scaffold for creating agents. Meta-governance. |
| `instructions.template.md` | CLASP scaffold. Meta-governance. |
| `prompt.template.md` | CLASP scaffold. Meta-governance. |
| `procedure.template.md` | CLASP scaffold. Meta-governance. |
| `guideline.template.md` | Dead template — no guidelines files exist. |

### Kept As-Is (10)

All document templates survive — they're low-cost structural skeletons:

- `code-analysis.template.md`
- `code-review.template.md`
- `feature-specification.template.md`
- `security-review.template.md`
- `software-architecture.template.md`
- `strategy-analysis.template.md`
- `tech-debt-analysis.template.md`
- `software-changelog.template.md`
- `test-architecture.template.md`
- `readme.template.md`

---

## Context Changes

### Deleted (3)

| File | Why | Action |
|------|-----|--------|
| `context-pointers.md` | 70-line index of 5 self-describing files. Redundant. | Delete |
| `clasp-system-context.md` | 300-line CLASP explainer. Valuable for onboarding but loaded into context every time. Key rules migrated to `governance.instructions.md`. | Move to `docs/architecture/` for reference. Delete from `.github/context/`. |
| `what-belongs-where.md` | 120-line decision tree. Key rules migrated to `governance.instructions.md`. | Move to `docs/architecture/` for reference. Delete from `.github/context/`. |

### Kept As-Is (3)

- `codebase-context.md` — project structure, build commands, key decisions
- `shared-context.md` — high-level orientation
- `user-pitfalls.md` — personal learning patterns

---

## Additional Deletions

### Standalone Checklists

Delete if they exist:
- `agent-creation-checklist.md`
- `instruction-file-checklist.md`
- `prompt-creation-checklist.md`

These are meta-checklists for creating CLASP files. The deleted create-* prompts contained equivalent guidance. The governance instruction now covers placement rules.

### Empty Directories

Delete if they exist:
- `.github/guidelines/`
- `.github/rules/`

### Consolidated Training Files

Keep for reference but move out of `.github/` if currently there:
- `research-prompt-templates.md` → `docs/training/`
- `clasp-prompt-training.md` → `docs/training/`

Update any agent references in these files to reflect the 3-agent roster.

---

## Constitution & Enforcement

**No changes.** Both files are already effective and lean:

- `copilot-instructions.md` (~77 lines) — epistemic rules, precedence, mode declaration
- `verification-checklist.md` — anti-hallucination enforcement (the most effective file in the system)

---

## Token Budget Impact

### Before (v2): ~6,085 lines

| Category | Lines | % |
|----------|-------|---|
| Constitution + enforcement | ~450 | 7% |
| Agents (7) | ~600 | 10% |
| Instructions (12+) | ~880 | 14% |
| Prompts (22) | ~2,220 | 36% |
| Procedures (4) | ~255 | 4% |
| Templates (16) | ~800 | 13% |
| Context (6) | ~570 | 9% |
| Auxiliary checklists | ~310 | 5% |

### After (v3): ~3,800 lines (est.)

| Category | Lines | Change |
|----------|-------|--------|
| Constitution + enforcement | ~450 | unchanged |
| Agents (3) | ~280 | −53% |
| Instructions (15) | ~1,050 | +19% (new files add value) |
| Prompts (10) | ~1,000 | −55% |
| Procedures (2-3) | ~170 | −33% |
| Templates (10) | ~500 | −38% |
| Context (3) | ~350 | −39% |

**Net reduction: ~37% fewer governance lines.** More importantly, the ratio shifts from "governance governing itself" to "governance helping write code."

---

## Implementation Sequence

Execute in this order to avoid broken references:

### Phase 1: Add new files
1. Create `architecture.instructions.md`
2. Create `security-review.instructions.md`
3. Create `governance.instructions.md`

### Phase 2: Rewrite surviving agents
4. Replace `software-engineer.agent.md` with v3 version
5. Replace `code-reviewer.agent.md` with v3 version
6. Replace `thinking-assistant.agent.md` with v3 version

### Phase 3: Rewire prompts
7. Update frontmatter on 5 rewired prompts (agent field + tools)
8. Merge creative variants into standard prompts

### Phase 4: Delete
9. Delete 4 agent files: `software-architect`, `security-reviewer`, `teacher`, `skill-teacher` (+ `learn-coach` if exists)
10. Delete 3 instruction files: `copilot-lint`, `feature-specification`, `strategy-analysis`
11. Delete 8 prompts: `create-agent`, `create-instructions`, `create-prompt`, `fix-artifact-from-lint`, `lint-artifacts`, `generate-summary`, `log-user-pitfall`, `generate-codebase-components`
12. Delete 1 procedure: `artifact-lint`
13. Delete 5 templates: `agent`, `instructions`, `prompt`, `procedure`, `guideline`
14. Delete 3 context files: `context-pointers`, move `clasp-system-context` and `what-belongs-where` to `docs/`
15. Delete standalone checklists and empty directories

### Phase 5: Update references
16. Update `clasp-system-context.md` (now in docs/) agent roster table
17. Grep for remaining references to deleted agents/files across all `.github/` files
18. Update any training/consolidated files with new agent roster

---

## Verification Checklist (Post-Migration)

- [ ] Only 3 agent files exist in `.github/agents/`
- [ ] No remaining references to: software-architect, security-reviewer, teacher, skill-teacher, learn-coach, agent-router, code-analyst, tech-writer, feature-engineer, strategy-analyst, test-architect, test-engineer, tech-debt-analyst, tech-debt-resolver
- [ ] All prompts reference one of: software-engineer, code-reviewer, thinking-assistant
- [ ] New instruction files exist: architecture, security-review, governance
- [ ] Deleted instruction files gone: copilot-lint, feature-specification, strategy-analysis
- [ ] No orphaned templates: agent, instructions, prompt, procedure, guideline deleted
- [ ] Context directory has exactly 3 files: codebase-context, shared-context, user-pitfalls
- [ ] Constitution and verification-checklist unchanged
- [ ] All instruction files have valid YAML frontmatter
