# Specification: VS Code Copilot Skill for LLM-Friendly Repository Refactoring Plans

Generated: 2026-06-08

## 1. Purpose

Create a Visual Studio Code Copilot Agent Skill that audits a repository for **LLM-friendly, token-efficient architecture** and produces a detailed, ranked refactoring plan.

The skill should help agents identify:

- oversized files that create excessive context cost
- over-fragmented code that creates excessive navigation cost
- excessive abstraction and design-pattern overuse
- feature logic scattered across horizontal layers
- generic utility dumping grounds
- weak module boundaries
- generated, vendored, build, coverage, fixture, or snapshot files that pollute AI context
- missing tests or missing local documentation around complex modules
- opportunities to convert code into cohesive feature-oriented modules

The skill should **not** modify code by default. Its primary output is a report and staged refactoring roadmap.

---

## 2. Official VS Code Customization Concepts Used

This specification is aligned with current VS Code Copilot customization concepts:

- Custom instructions define persistent coding standards and architectural rules.
- Prompt files are reusable slash-command prompts for lightweight repeated tasks.
- Agent Skills package multi-step workflows, instructions, scripts, examples, and resources.
- Skills are stored in directories containing a required `SKILL.md` file.
- Project skills can live under `.github/skills/`, `.claude/skills/`, or `.agents/skills/`.
- A skill's `name` must match its parent directory name.
- Skill frontmatter uses a lowercase hyphenated `name` and a specific `description` to help Copilot decide when to load it.
- Skills load progressively: first metadata, then `SKILL.md`, then referenced resources only when needed.
- A skill can be manual-only by setting `disable-model-invocation: true`.
- For very large investigations, `context: fork` can be considered, but it is experimental and should only be enabled deliberately.

Reference documentation:

- VS Code Customization overview: https://code.visualstudio.com/docs/agents/concepts/customization
- VS Code custom instructions: https://code.visualstudio.com/docs/agent-customization/custom-instructions
- VS Code agent skills: https://code.visualstudio.com/docs/agent-customization/agent-skills
- VS Code workspace context: https://code.visualstudio.com/docs/agents/reference/workspace-context
- VS Code optimize AI usage: https://code.visualstudio.com/docs/agents/guides/optimize-usage

---

## 3. Recommended Skill Name and Location

Use a project skill:

```text
.github/skills/repository-refactoring-planner/SKILL.md
```

The parent directory name and frontmatter `name` must match exactly:

```yaml
name: repository-refactoring-planner
```

Recommended default behavior:

```yaml
disable-model-invocation: true
user-invocable: true
```

Reason: a full repository refactoring audit can be context-heavy. It should run only when explicitly requested.

Optional large-repository mode:

```yaml
context: fork
```

Use `context: fork` only when the repository is large and the final report is the only thing that needs to return to the parent conversation. Do not enable this blindly if the user is trying to minimize all token consumption and the repository is small or the audit scope is narrow.

---

## 4. Intended Skill Directory Structure

Minimum version:

```text
.github/skills/repository-refactoring-planner/
  SKILL.md
```

Recommended full version:

```text
.github/skills/repository-refactoring-planner/
  SKILL.md
  resources/
    scoring-rubric.md
    report-template.md
    module-readme-template.md
    refactoring-recipes.md
  scripts/
    collect-code-metrics.py
```

The skill must reference every additional resource from `SKILL.md` using relative Markdown links. Otherwise the agent may not load them.

The optional script should use only the Python standard library unless the repository already has an approved analysis dependency. This keeps the skill portable.

---

## 5. Skill Inputs

The skill should support prompts such as:

```text
/repository-refactoring-planner audit the whole repository and create a ranked refactoring plan
```

```text
/repository-refactoring-planner focus on src/backtesting and src/prediction only
```

```text
/repository-refactoring-planner identify files over 800 LOC and propose feature-oriented splits
```

```text
/repository-refactoring-planner create docs/refactoring/llm-friendly-refactoring-plan.md but do not change source code
```

```text
/repository-refactoring-planner audit context hygiene: generated files, snapshots, build artifacts, and files that should be excluded from Copilot context
```

---

## 6. Skill Outputs

The skill should produce one main report, preferably:

```text
docs/refactoring/llm-friendly-refactoring-plan.md
```

If the user does not want file creation, return the report directly in chat.

The report must include:

1. Executive summary
2. Scope analyzed
3. Repository structure overview
4. Hotspot table
5. Architecture and context-efficiency findings
6. Ranked refactoring roadmap
7. Per-module refactoring plans
8. Test and verification strategy
9. Context-hygiene recommendations
10. Suggested PR sequence
11. Risks and migration notes
12. Open questions or unknowns

---

## 7. Analysis Scope

Analyze source files, tests, configuration, and local documentation.

Include by default:

```text
src/
app/
packages/
plugins/
libs/
tests/
.github/
*.sln
*.csproj
package.json
pnpm-workspace.yaml
tsconfig*.json
pytest.ini
pyproject.toml
```

Exclude by default:

```text
node_modules/
dist/
build/
coverage/
.generated/
generated/
vendor/
.bin/
obj/
bin/
.next/
.nuxt/
.cache/
*.min.js
*.bundle.js
*.map
*.lock when not relevant
large logs
large binary files
large snapshots unless the task is about snapshots
large JSON fixtures unless the task is about fixtures
```

Respect `.gitignore` and project-specific ignore rules.

---

## 8. Repository Inventory Requirements

The skill should first create a lightweight inventory before reading many files.

Collect:

- file path
- extension/language
- line count
- approximate size in bytes
- whether file appears generated/vendor/build/test/source/config/doc
- whether file is ignored or should probably be ignored
- imports/dependencies where cheaply available
- exported symbols where tooling supports it
- test file association if obvious

For large repositories, do not read every file in full. First rank candidates using metadata, path names, line counts, imports, and file names. Then read only the high-value files.

---

## 9. Scoring Rubric

Each candidate file or module receives a score from 0 to 100.

| Dimension | Weight | Indicators |
|---|---:|---|
| Size pressure | 15 | File >400, >800, >1,500, or >5,000 LOC. |
| Responsibility mixing | 20 | Validation, persistence, orchestration, formatting, external calls, and domain rules in one file. |
| Context fan-out | 15 | Many imports, many collaborators, many symbols required to understand one change. |
| Abstraction depth | 10 | Interface/factory/provider/base-class chains without clear payoff. |
| Feature scattering | 15 | One business capability spread across many horizontal folders. |
| Retrieval quality | 10 | Weak names, generic utilities, unclear module ownership. |
| Testability risk | 10 | No nearby tests, hard-to-isolate side effects, hidden global state. |
| Context pollution | 5 | Generated/build/snapshot/fixture files likely included in AI context. |

Priority mapping:

| Score | Priority | Meaning |
|---:|---|---|
| 80-100 | P0 | High-impact refactor. Strong candidate for near-term cleanup. |
| 60-79 | P1 | Important improvement with meaningful maintainability/token benefit. |
| 40-59 | P2 | Worth doing when touching the area. |
| 20-39 | P3 | Minor cleanup. Avoid unless already nearby. |
| 0-19 | No action | Leave as-is unless other evidence appears. |

Do not recommend refactoring solely because of size. A large cohesive parser, schema, or generated file may be acceptable. Explain the reason.

---

## 10. Hotspot Detection Rules

Flag files and modules with any of these characteristics:

### Oversized files

- source file over 800 LOC
- source file over 1,500 LOC
- hand-written source file over 5,000 LOC
- test file that mixes many unrelated test suites

### Mixed concerns

- UI + data fetching + domain rules in one file
- API client + caching + business logic in one file
- persistence + orchestration + formatting in one service
- validation + side effects + external calls in one function

### Feature scattering

- one capability spread across `controllers/`, `services/`, `repositories/`, `models/`, and `utils/` with no local module README
- imports bouncing between unrelated top-level folders for one feature
- tests located far from the feature with unclear naming

### Excessive abstraction

- one interface with one implementation and no test seam or future variation
- factory/provider/resolver chains that simply instantiate one class
- inheritance where composition or a small pure function would be clearer
- abstract base classes with hidden state or required call order

### Generic utility risk

- files named `utils`, `helpers`, `common`, `shared`, or `misc` with unrelated functions
- utility files imported by many modules for unrelated reasons
- utility functions that actually belong to a domain module

### Context pollution

- generated files not isolated
- build outputs committed or visible to workspace indexing
- large snapshots or fixtures included in ordinary context
- lockfile diffs shown during unrelated work

---

## 11. Recommended Refactoring Recipes

### Recipe A: Split a God File

Use when one hand-written file has multiple responsibilities.

Steps:

1. Add or locate characterization tests.
2. Identify cohesive internal sections.
3. Extract pure helpers first.
4. Extract domain types next.
5. Extract external adapters last.
6. Keep one facade or service entry point to preserve callers.
7. Update imports through the module entry point.
8. Run focused tests.
9. Split follow-up behavior changes into later PRs.

Target shape:

```text
feature-name/
  README.md
  index.ts
  FeatureService.ts
  FeatureTypes.ts
  FeaturePolicy.ts
  FeatureAdapter.ts
  feature-name.test.ts
```

### Recipe B: Convert Horizontal Scattering to Feature Module

Use when one capability is scattered across generic layers.

Steps:

1. Identify the actual business capability.
2. Create a feature folder.
3. Move implementation, types, tests, and local docs together.
4. Keep framework entry points thin.
5. Keep infrastructure adapters separate from domain logic.
6. Provide a stable public export file.
7. Update references in small batches.

### Recipe C: Remove Abstraction Theater

Use when indirection increases context cost without reducing change cost.

Steps:

1. Map the abstraction chain.
2. Count implementations and real variation points.
3. Inline single-use factories/providers where safe.
4. Keep interfaces only at external boundaries or real strategy seams.
5. Prefer composition over inheritance.
6. Add tests around public behavior before simplifying.

### Recipe D: Detox Generic Utilities

Use when `utils` or `helpers` files contain unrelated domain logic.

Steps:

1. Group utility functions by domain concept.
2. Move each group into the owning module.
3. Keep only truly generic, stable primitives in shared utilities.
4. Rename functions to domain-specific names where possible.
5. Update imports and tests in small batches.

### Recipe E: Add Module Context Packet

Use when a module is conceptually important but hard to understand.

Add:

```text
README.md
index.ts
local tests
clear type/schema file if needed
```

The README should be concise and explain ownership, invariants, entry points, and verification commands.

### Recipe F: Clean AI Context Pollution

Use when irrelevant files are likely loaded into Copilot context.

Steps:

1. Identify generated/build/vendor/snapshot/fixture files.
2. Check `.gitignore` and VS Code `files.exclude`.
3. Recommend exclusions without hiding source files that developers need.
4. If generated code is required, isolate it and add a stable wrapper.

---

## 12. Required Report Template

The skill should generate reports in this shape:

```markdown
# LLM-Friendly Refactoring Plan

Generated: YYYY-MM-DD
Repository: <repo name or workspace root>
Scope: <analyzed scope>

## 1. Executive Summary

<5-10 bullet summary of highest-impact findings>

## 2. Current Architecture Snapshot

<brief description of top-level folders, major modules, and observed conventions>

## 3. Hotspot Table

| Priority | Score | File/Module | Main Issue | Evidence | Recommendation | Estimated Risk |
|---|---:|---|---|---|---|---|
| P0 | 88 | src/example/LargeService.ts | Mixed concerns + 1,700 LOC | validation, persistence, API calls | Split into feature module with facade | Medium |

## 4. Context-Efficiency Findings

### 4.1 Oversized Files
### 4.2 Over-Fragmented Areas
### 4.3 Excessive Abstraction
### 4.4 Feature Scattering
### 4.5 Generic Utilities
### 4.6 Context Pollution

## 5. Target Architecture

<recommended feature/module structure>

## 6. Refactoring Roadmap

### Phase 0: Safety and Characterization Tests
### Phase 1: Context Hygiene
### Phase 2: Highest-Impact Module Splits
### Phase 3: Utility Detox
### Phase 4: Abstraction Simplification
### Phase 5: Documentation and Export Cleanup

## 7. Per-Module Refactoring Plans

### <Module/File Name>

Current state:
- ...

Proposed target state:
- ...

Step-by-step plan:
1. ...
2. ...
3. ...

Verification:
- ...

Risks:
- ...

## 8. Suggested PR Sequence

| PR | Goal | Files/Modules | Verification | Risk |
|---:|---|---|---|---|
| 1 | Add characterization tests | ... | ... | Low |

## 9. Copilot Execution Prompts

<small prompts the user can give to Copilot for each phase>

## 10. Open Questions

<unknowns that require human decision>
```

---

## 13. Required Evidence Standard

The skill must not make unsupported structural claims.

For every major finding, include evidence such as:

- file path
- approximate LOC
- symbol names
- import/dependency indicators
- examples of mixed responsibilities
- missing nearby test evidence
- directory layout evidence

When the agent has not inspected a file directly, it must label the finding as inferred from metadata.

Use labels:

```text
CONFIRMED: directly inspected file or symbol evidence
INFERRED: based on path, imports, names, line count, or repository structure
UNVERIFIED: plausible but not yet checked
```

---

## 14. Safety and Non-Goals

The skill must not:

- rewrite source code unless explicitly requested
- refactor based only on file size
- enforce design patterns without evidence
- recommend splitting cohesive files into arbitrary tiny files
- recommend merging everything into large LLM-optimized God files
- delete generated files without confirming they are rebuildable
- modify public APIs without migration notes
- mix behavior changes with refactoring in one plan
- claim tests pass unless the command was actually run

The skill should prefer:

- report first
- small PRs
- characterization tests before structural change
- feature-oriented modules
- shallow architecture
- explicit adapters for external systems
- keeping domain code independent of vendor DTOs

---

## 15. Acceptance Criteria

The skill is successful when:

- It produces a ranked refactoring plan with clear priorities.
- It identifies both oversized files and over-fragmented areas.
- It distinguishes cohesive large files from harmful God files.
- It finds unnecessary abstraction chains.
- It recommends feature-oriented module structures where appropriate.
- It identifies context-polluting generated/build/vendor/snapshot files.
- It proposes verification steps before and after refactoring.
- It provides a PR-sized roadmap rather than one huge rewrite.
- It avoids unsupported claims and labels uncertainty.
- It does not modify source code unless explicitly asked.

---

# 16. Ready-to-Use `SKILL.md`

Copy the following content into:

```text
.github/skills/repository-refactoring-planner/SKILL.md
```

```markdown
---
name: repository-refactoring-planner
description: Audit a repository for LLM-friendly, token-efficient architecture and produce a ranked refactoring plan. Use when asked to find oversized files, over-fragmented code, excessive abstraction, weak module boundaries, feature scattering, generic utilities, context pollution, or refactoring opportunities. Does not modify source code unless explicitly requested.
disable-model-invocation: true
user-invocable: true
---

# Repository Refactoring Planner

## Purpose

Use this skill to audit a repository for architecture that is efficient for AI-assisted development and maintainable for humans.

The target architecture is:

```text
feature-oriented modules
+ cohesive files
+ shallow design
+ meaningful names
+ low context fan-out
+ local tests
+ concise module documentation
+ minimal useful abstraction
```

Avoid both extremes:

```text
Bad: 5,000-line God files
Bad: 50 tiny files for one simple feature
Good: 3-8 cohesive files around one feature/module
```

## Default Mode

Produce a report and staged refactoring plan. Do not modify source code unless the user explicitly asks for implementation.

If the user asks for file output, create or update:

```text
docs/refactoring/llm-friendly-refactoring-plan.md
```

If the user asks for chat-only output, return the report in chat.

## Initial Questions

Do not ask clarifying questions unless the task cannot proceed safely. Infer sensible defaults:

- scope: whole repository
- output: `docs/refactoring/llm-friendly-refactoring-plan.md`
- mode: plan only, no source edits
- priority: token efficiency plus maintainability

## Analysis Workflow

1. Inspect repository structure.
2. Respect `.gitignore` and obvious generated/build/vendor directories.
3. Identify languages, package boundaries, and major modules.
4. Build a lightweight inventory before reading many files.
5. Rank files/modules by likely architecture impact.
6. Read only the most relevant files first.
7. Identify hotspots:
   - oversized files
   - mixed responsibilities
   - over-fragmented features
   - excessive abstraction
   - generic utility dumping grounds
   - context pollution
   - missing tests
   - missing local documentation
8. Produce a ranked refactoring roadmap.
9. Include verification commands or test targets where discoverable.
10. Label uncertainty clearly.

## File Size Heuristics

Use these thresholds as guidance:

| Size | Guidance |
|---:|---|
| 0-150 LOC | Fine. Do not split only for size. |
| 150-400 LOC | Preferred range for most hand-written files. |
| 400-800 LOC | Acceptable if cohesive. |
| 800-1,500 LOC | Inspect for mixed responsibilities. |
| 1,500+ LOC | Usually needs a staged split if hand-written business logic. |
| 5,000+ LOC | Strong warning unless generated, vendored, or intentionally isolated. |

Do not recommend refactoring solely because of size. First judge cohesion.

## Scoring Rubric

Score each candidate from 0-100:

| Dimension | Weight | Indicators |
|---|---:|---|
| Size pressure | 15 | >400, >800, >1,500, or >5,000 LOC. |
| Responsibility mixing | 20 | Validation, persistence, orchestration, formatting, external calls, and domain rules in one file. |
| Context fan-out | 15 | Many imports/collaborators needed for one change. |
| Abstraction depth | 10 | Interface/factory/provider/base-class chains without payoff. |
| Feature scattering | 15 | One capability spread across generic horizontal folders. |
| Retrieval quality | 10 | Weak names, generic utilities, unclear ownership. |
| Testability risk | 10 | No nearby tests, hard-to-isolate side effects. |
| Context pollution | 5 | Generated/build/snapshot/fixture files likely included in AI context. |

Priority mapping:

| Score | Priority |
|---:|---|
| 80-100 | P0 |
| 60-79 | P1 |
| 40-59 | P2 |
| 20-39 | P3 |
| 0-19 | No action |

## Refactoring Recipes

### Split a God File

1. Add or locate characterization tests.
2. Identify cohesive sections.
3. Extract pure helpers first.
4. Extract domain types next.
5. Extract external adapters last.
6. Keep one facade or service entry point to preserve callers.
7. Update imports through a module entry point.
8. Run focused tests.

### Convert Horizontal Layers to Feature Module

1. Identify the business capability.
2. Create a feature folder.
3. Move implementation, types, tests, and local docs together.
4. Keep framework entry points thin.
5. Keep infrastructure adapters separate from domain logic.
6. Provide a stable public export file.

### Remove Abstraction Theater

1. Map the abstraction chain.
2. Count actual implementations and variation points.
3. Inline single-use factories/providers where safe.
4. Keep interfaces at external boundaries or real strategy seams.
5. Prefer composition over inheritance.

### Detox Generic Utilities

1. Group helpers by domain concept.
2. Move each group into the owning module.
3. Keep only truly generic primitives in shared utilities.
4. Rename helpers to domain-specific names where possible.
5. Update imports and tests in small batches.

### Add a Module Context Packet

For complex modules, recommend:

```text
README.md
index.ts or equivalent module entry point
local tests
clear type/schema file if needed
```

The README should explain ownership, non-ownership, entry points, invariants, and verification commands.

### Clean AI Context Pollution

Identify files that should probably be ignored or hidden from AI context:

```text
dist/
build/
coverage/
node_modules/
generated/
.generated/
vendor/
*.min.js
*.bundle.js
large snapshots
large fixture JSON
large logs
binary artifacts
```

Recommend `.gitignore` or VS Code `files.exclude` changes, but do not delete files unless explicitly requested.

## Evidence Standard

For every major finding, include evidence:

- file path
- approximate LOC
- relevant symbol names
- import/dependency indicators
- examples of mixed responsibility
- missing or present tests
- related directories

Use these labels:

```text
CONFIRMED: directly inspected file or symbol evidence
INFERRED: based on path, imports, names, line count, or repository structure
UNVERIFIED: plausible but not yet checked
```

## Required Report Format

Generate this structure:

```markdown
# LLM-Friendly Refactoring Plan

Generated: YYYY-MM-DD
Repository: <repo name or workspace root>
Scope: <analyzed scope>

## 1. Executive Summary

## 2. Current Architecture Snapshot

## 3. Hotspot Table

| Priority | Score | File/Module | Main Issue | Evidence | Recommendation | Estimated Risk |
|---|---:|---|---|---|---|---|

## 4. Context-Efficiency Findings

### 4.1 Oversized Files
### 4.2 Over-Fragmented Areas
### 4.3 Excessive Abstraction
### 4.4 Feature Scattering
### 4.5 Generic Utilities
### 4.6 Context Pollution

## 5. Target Architecture

## 6. Refactoring Roadmap

### Phase 0: Safety and Characterization Tests
### Phase 1: Context Hygiene
### Phase 2: Highest-Impact Module Splits
### Phase 3: Utility Detox
### Phase 4: Abstraction Simplification
### Phase 5: Documentation and Export Cleanup

## 7. Per-Module Refactoring Plans

## 8. Suggested PR Sequence

| PR | Goal | Files/Modules | Verification | Risk |
|---:|---|---|---|---|

## 9. Copilot Execution Prompts

## 10. Open Questions
```

## Safety Rules

Do not:

- modify source code unless explicitly requested
- recommend refactoring solely due to file size
- force design patterns without evidence
- split cohesive files into arbitrary tiny files
- merge everything into a large LLM-optimized file
- delete generated files without confirming they are rebuildable
- change public APIs without migration notes
- mix behavior changes with refactoring
- claim tests pass unless the command actually ran

Prefer:

- plan first
- small PR-sized changes
- characterization tests before structural change
- feature-oriented modules
- shallow architecture
- explicit adapters for external systems
- stable public module entry points
- local documentation for non-obvious modules

## Final Response Requirements

When returning results to the user:

- summarize the top 5 findings
- provide the path to the report if a file was created
- list the first 3 recommended PRs
- state what was not analyzed
- state whether source code was changed
```

---

## 17. Optional Resource: `resources/scoring-rubric.md`

Create this file only if you want to keep `SKILL.md` shorter.

```markdown
# Repository Refactoring Planner Scoring Rubric

Score each file/module from 0-100.

| Dimension | Weight | Indicators |
|---|---:|---|
| Size pressure | 15 | >400, >800, >1,500, or >5,000 LOC. |
| Responsibility mixing | 20 | Validation, persistence, orchestration, formatting, external calls, and domain rules in one file. |
| Context fan-out | 15 | Many imports/collaborators needed for one change. |
| Abstraction depth | 10 | Interface/factory/provider/base-class chains without payoff. |
| Feature scattering | 15 | One capability spread across generic horizontal folders. |
| Retrieval quality | 10 | Weak names, generic utilities, unclear ownership. |
| Testability risk | 10 | No nearby tests, hard-to-isolate side effects. |
| Context pollution | 5 | Generated/build/snapshot/fixture files likely included in AI context. |
```

---

## 18. Optional No-Dependency Metrics Script Specification

A simple Python script may be added at:

```text
.github/skills/repository-refactoring-planner/scripts/collect-code-metrics.py
```

Requirements:

- Python standard library only
- no network access
- respect common ignore directories
- output JSON or Markdown
- collect path, extension, byte size, LOC, generated/build/vendor/test/source classification
- optionally count imports for TypeScript, JavaScript, Python, and C# using simple regexes

Pseudocode:

```python
from pathlib import Path
import json
import re

IGNORE_DIRS = {
    'node_modules', 'dist', 'build', 'coverage', '.git', '.next', '.nuxt',
    'bin', 'obj', 'vendor', 'generated', '.generated', '.cache'
}

SOURCE_EXTENSIONS = {'.ts', '.tsx', '.js', '.jsx', '.cs', '.py', '.java', '.go', '.rs'}
TEST_HINTS = ('.test.', '.spec.', 'tests/', '__tests__/', 'Test.cs', 'Tests.cs')

def is_ignored(path: Path) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts)

def classify(path: Path) -> str:
    text = str(path).replace('\\', '/')
    if any(hint in text for hint in TEST_HINTS):
        return 'test'
    if path.suffix in SOURCE_EXTENSIONS:
        return 'source'
    if path.suffix in {'.md', '.mdx'}:
        return 'doc'
    if path.name in {'package.json', 'tsconfig.json', 'pyproject.toml'}:
        return 'config'
    return 'other'

def count_imports(content: str, suffix: str) -> int:
    patterns = {
        '.ts': r'^import\\s|require\\(',
        '.tsx': r'^import\\s|require\\(',
        '.js': r'^import\\s|require\\(',
        '.jsx': r'^import\\s|require\\(',
        '.py': r'^(import|from)\\s+',
        '.cs': r'^using\\s+',
    }
    pattern = patterns.get(suffix)
    if not pattern:
        return 0
    return len(re.findall(pattern, content, flags=re.MULTILINE))

def collect(root: Path):
    rows = []
    for path in root.rglob('*'):
        if not path.is_file() or is_ignored(path):
            continue
        try:
            content = path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        rows.append({
            'path': str(path.relative_to(root)).replace('\\', '/'),
            'extension': path.suffix,
            'bytes': path.stat().st_size,
            'loc': content.count('\\n') + 1,
            'imports': count_imports(content, path.suffix),
            'classification': classify(path),
        })
    return rows

if __name__ == '__main__':
    print(json.dumps(collect(Path.cwd()), indent=2))
```

---

## 19. Recommended Follow-Up Prompt Files

After implementing the skill, consider adding prompt files for execution phases:

```text
.github/prompts/refactor-phase-0-characterization-tests.prompt.md
.github/prompts/refactor-phase-1-context-hygiene.prompt.md
.github/prompts/refactor-phase-2-split-hotspot.prompt.md
.github/prompts/refactor-phase-3-utility-detox.prompt.md
```

These should be lightweight execution prompts that consume the generated refactoring plan and implement one small PR-sized phase at a time.

---

## 20. Example User Workflow

1. Add the instruction file:

```text
.github/instructions/llm-friendly-architecture.instructions.md
```

2. Add the skill:

```text
.github/skills/repository-refactoring-planner/SKILL.md
```

3. Run the audit in VS Code Chat:

```text
/repository-refactoring-planner audit the whole repository and create docs/refactoring/llm-friendly-refactoring-plan.md. Do not change source code.
```

4. Review the generated report manually.

5. Ask Copilot to implement only Phase 0:

```text
Using docs/refactoring/llm-friendly-refactoring-plan.md, implement Phase 0 only. Add characterization tests for the top P0 hotspot. Do not refactor source code yet.
```

6. Then implement one refactoring PR at a time.

---

## 21. Final Recommendation

Use this skill as an **audit and planning tool**, not as an automatic refactoring bot.

The highest-value workflow is:

```text
repository audit
→ ranked refactoring plan
→ characterization tests
→ context hygiene cleanup
→ one P0 module split
→ verify
→ repeat
```

This minimizes token waste, avoids risky broad rewrites, and keeps both humans and agents oriented around clear feature boundaries.
