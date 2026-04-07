# Prompt Rewiring Patches

## How to apply
For each prompt listed below, replace ONLY the YAML frontmatter block (between the `---` delimiters).

---

## generate-feature-specification.prompt.md

BEFORE:
```yaml
---
agent: software-architect
model: Claude Sonnet 4.6 (copilot)
tools: [read, search, agent, search, edit, todo, vscode, execute]
---
```

AFTER:
```yaml
---
agent: software-engineer
model: Claude Sonnet 4.6 (copilot)
tools: [read, search, agent, edit, todo, vscode, execute]
---
```

Also add to Task Instructions section:
```
- Invoke `.github/instructions/architecture.instructions.md` § Feature Specification for domain guidance.
```

---

## generate-strategy.prompt.md

BEFORE:
```yaml
---
agent: software-architect
model: Claude Sonnet 4.6 (copilot)
tools: [read, search, agent, edit, todo]
---
```

AFTER:
```yaml
---
agent: software-engineer
model: Claude Sonnet 4.6 (copilot)
tools: [read, search, agent, edit, todo, vscode, execute]
---
```

Also add to Task Instructions section:
```
- Invoke `.github/instructions/architecture.instructions.md` § Strategy Analysis for domain guidance.
```

---

## generate-software-architecture.prompt.md (if separate from creative variant)

BEFORE:
```yaml
---
agent: software-architect
...
---
```

AFTER:
```yaml
---
agent: software-engineer
model: Claude Sonnet 4.6 (copilot)
tools: [read, search, agent, edit, todo, vscode, execute]
---
```

Also add to Task Instructions section:
```
- Invoke `.github/instructions/architecture.instructions.md` for domain guidance.
```

---

## generate-test-architecture.prompt.md

BEFORE:
```yaml
---
agent: software-architect
model: Claude Sonnet 4.6 (copilot)
tools: [read, search, agent, search, edit, todo, vscode, execute]
---
```

AFTER:
```yaml
---
agent: software-engineer
model: Claude Sonnet 4.6 (copilot)
tools: [read, search, agent, edit, todo, vscode, execute]
---
```

Also add to Task Instructions section:
```
- Invoke `.github/instructions/test-strategy.instructions.md` for domain guidance.
```

---

## generate-security-review.prompt.md

BEFORE:
```yaml
---
agent: security-reviewer
model: Claude Sonnet 4.6 (copilot)
tools: [read, search, agent, search, edit, todo, vscode, execute]
---
```

AFTER:
```yaml
---
agent: software-engineer
model: Claude Sonnet 4.6 (copilot)
tools: [read, search, agent, edit, todo, vscode, execute]
---
```

Also add to Task Instructions section:
```
- Invoke `.github/instructions/security-review.instructions.md` for domain guidance.
```

---

## Note: Duplicate `search` in tool arrays

Several original prompts have `tools: [read, search, agent, search, edit, ...]` with `search` listed twice. The rewired versions fix this to a single `search` entry.
