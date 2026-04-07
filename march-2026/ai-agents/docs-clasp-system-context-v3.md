# AI Ecosystem System Context (v3 Reference)

**Purpose:** Reference document explaining how AI Ecosystem artifacts interact. Moved from `.github/context/` to `docs/architecture/` so it is not auto-loaded into every session — consult on-demand.

**For active governance rules, see:** `.github/instructions/governance.instructions.md`

---

## Mental Model

AI Ecosystem separates **execution capability** (tool restrictions on agents) from **domain knowledge** (instruction files) and **enforcement** (verification checklist + constitution). The system works because tool restrictions are mechanical — they cannot be overridden by prompts or instructions.

### End-to-End Flow

```
User request
↓
Prompt (*.prompt.md) — wires: agent + instructions + templates + output constraints
↓
Agent (*.agent.md) — tool restrictions + scope boundaries
↓
Instruction (*.instructions.md) — on-demand domain knowledge
↓
Template (*.template.md) — structure only; empty sections allowed
↓
Draft artifact
↓
Verification checklist (pass/fail checks)
↓
Ralph Loop (build → test → fix → loop) if execution agent
```

---

## Agent Roster (v3)

| Agent              | Tools                                    | Model    | Purpose                                                                                     |
| ------------------ | ---------------------------------------- | -------- | ------------------------------------------------------------------------------------------- |
| software-engineer  | read, search, agent, edit, todo, execute | Opus 4.6 | Implementation + self-verification. Only agent that can modify files or run commands.       |
| code-reviewer      | read, search, agent, todo                | o4-mini  | Read-only adversarial review. Different model from engineer creates adversarial consensus.  |
| thinking-assistant | read, search, agent, todo                | default  | Read-only planning, design, teaching. Prevents premature implementation during exploration. |

### Why Three Agents

Research (2025–2026) demonstrates that agent value comes from **mechanical constraints** (tool restrictions, model routing, context isolation), not from persona labels. Three agents provide three distinct constraint profiles:

1. **Full capability** (engineer) — can edit and execute
2. **Adversarial read-only** (reviewer) — different model, cannot edit
3. **Exploratory read-only** (thinker) — cannot edit, delays convergence

Domain knowledge (architecture, security, testing, strategy) lives in instruction files that any agent invokes on demand.

---

## Instruction Files as Domain Knowledge

| Instruction File  | Domain                                 | Invoked By                             |
| ----------------- | -------------------------------------- | -------------------------------------- |
| stack-python      | Python/FastAPI patterns                | engineer (auto-attached to \*.py)      |
| stack-react       | React/TypeScript patterns              | engineer (auto-attached to _.tsx/_.ts) |
| stack-database    | SQLAlchemy/Alembic patterns            | engineer (auto-attached to models/)    |
| code-analysis     | Control flow, data flow                | engineer                               |
| test-strategy     | Test pyramid, layering                 | engineer, thinker                      |
| test-aaa-pattern  | AAA test structure                     | engineer                               |
| documentation     | README/ADR synthesis                   | engineer                               |
| refactor-plan     | Staged refactoring                     | engineer, thinker                      |
| architecture      | System design, strategy, features      | engineer, thinker                      |
| security-review   | Security risk identification           | engineer, reviewer                     |
| tech-debt-fix     | Debt remediation                       | engineer                               |
| tech-debt-review  | Debt review                            | engineer, reviewer                     |
| governance        | AI Ecosystem rules, artifact ownership | any (when modifying .github/)          |
| anti-slug-style   | Writing style                          | any                                    |
| reasoning-routine | Evidence-bound reasoning               | any                                    |
