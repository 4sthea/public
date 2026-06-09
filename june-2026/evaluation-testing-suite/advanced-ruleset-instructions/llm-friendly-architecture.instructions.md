---
name: 'LLM-Friendly Architecture and Token Efficiency'
description: 'Repository-wide architecture rules for token-efficient AI-assisted development: cohesive modules, shallow design, low context fan-out, and maintainable refactoring.'
applyTo: '**'
---

# LLM-Friendly Architecture and Token Efficiency Instructions

## Purpose

Use these rules when creating, editing, reviewing, or refactoring code in this repository.

The goal is **not** to optimize for one huge file and not to optimize for pattern-heavy enterprise architecture. The goal is:

> Make each coding task require the smallest predictable set of relevant files while keeping the code maintainable for humans.

Optimize for:

- cohesive, retrievable modules
- shallow architecture
- meaningful names
- low context fan-out
- small change surfaces
- executable tests
- concise local documentation
- minimal but useful abstraction

Do not optimize for:

- 5,000-line God files
- excessive micro-files
- design-pattern theater
- generic utility dumping grounds
- broad rewrites without tests
- forcing the agent to inspect many unrelated files for a small change

---

## Core Architecture Principle

Prefer **retrievable cohesive context** over physical colocation.

A file or module is good for AI-assisted development when an agent can quickly answer:

1. Where is the relevant logic?
2. What does this module own?
3. What does it explicitly not own?
4. Which files are needed for this change?
5. Which tests verify the behavior?

When choosing between competing designs, prefer the design that minimizes:

```text
irrelevant context + required navigation + abstraction depth
```

---

## File Size and Complexity Budget

Treat these as default thresholds, not hard laws:

| Size | Guidance |
|---:|---|
| 0-150 LOC | Fine. Do not split only for size. |
| 150-400 LOC | Preferred range for most hand-written files. |
| 400-800 LOC | Acceptable if the file is highly cohesive. |
| 800-1,500 LOC | Review for multiple responsibilities. Refactor when the file mixes concerns. |
| 1,500+ LOC | Usually too large for core business logic. Plan a staged split. |
| 5,000+ LOC | Strong warning sign unless generated, vendored, or intentionally isolated. |

Also watch for:

- functions that mix validation, persistence, orchestration, formatting, and external calls
- classes with multiple unrelated reasons to change
- files that require scrolling through unrelated sections to understand one behavior
- repeated private helper clusters that indicate hidden submodules
- files where tests are hard to locate or absent

A cohesive 700-line parser can be acceptable. A 700-line service that mixes API calls, UI mapping, caching, persistence, validation, business rules, and logging is not acceptable.

---

## Preferred Module Shape

Prefer **feature-first vertical folders** over broad horizontal folders when working on business features.

Preferred:

```text
src/backtesting/
  README.md
  index.ts
  BacktestRunner.ts
  WalkForwardSplitter.ts
  TradeSimulator.ts
  MetricsCalculator.ts
  BacktestTypes.ts
  backtesting.test.ts
```

Usually worse when the feature is scattered:

```text
src/controllers/
src/services/
src/repositories/
src/models/
src/helpers/
src/utils/
```

Horizontal folders are acceptable for framework-required layers, shared platform code, or very small apps. For feature work, prefer colocating implementation, types, tests, and local documentation near the feature.

---

## Module Boundary Rules

Each non-trivial module should have:

- one clear owner responsibility
- one obvious public entry point, usually `index.ts`, `__init__.py`, or a similarly idiomatic facade
- local tests or clearly referenced tests
- a short `README.md` when the module has non-obvious behavior, invariants, or workflows
- explicit adapters for external systems
- names that match domain concepts rather than technical vagueness

A complex module README should usually be 50-150 lines and answer:

```text
What does this module own?
What does it not own?
What are the main entry points?
What invariants must not be broken?
How is it tested?
What are the most common extension points?
```

---

## Design Pattern Policy

Use design patterns only when they reduce coupling, reduce context needed for a change, or make variation explicit.

Prefer these patterns when they fit naturally:

| Pattern | Use when |
|---|---|
| Strategy | There are multiple algorithms behind one stable interface. |
| Adapter | External APIs, vendors, databases, or framework details should not leak into domain logic. |
| Facade | A module needs one simple public entry point over several internal files. |
| Pipeline | Data transformation stages are explicit and testable. |
| Command / Handler | A use case should be executable, testable, and isolated. |
| Ports and Adapters | External systems change independently of domain logic. |

Avoid these unless there is clear evidence they help:

| Pattern / habit | Why to avoid |
|---|---|
| Abstract factory everywhere | Adds indirection and files without reducing change cost. |
| Interface for every class | Creates navigation overhead unless there are multiple implementations or test seams. |
| Repository for every tiny model | Adds boilerplate and hides simple persistence logic. |
| Deep inheritance | Forces agents to inspect base classes, overrides, and implicit behavior. |
| Generic `utils` buckets | Mix unrelated concepts and harm semantic retrieval. |
| Pattern-first refactoring | Solves imagined problems instead of current coupling. |

---

## Refactoring Triggers

Propose a refactoring plan when you find any of these:

- a file over 800 LOC with multiple responsibilities
- a file over 1,500 LOC that is not generated or vendored
- a feature scattered across many horizontal folders without a local map
- many unrelated imports in a single file
- circular dependencies or bidirectional feature dependencies
- a generic utility file with unrelated helpers
- a service that mixes orchestration, persistence, domain rules, external calls, and formatting
- duplicated logic that would be safer as a named domain function or strategy
- missing tests around code that will be split
- generated, vendored, build, coverage, or large snapshot files visible to the AI context

Do not refactor only because a file is large. First determine whether the file is cohesive.

---

## Refactoring Procedure

When refactoring, prefer staged, behavior-preserving changes:

1. Identify the smallest relevant module or feature boundary.
2. Locate existing tests and add characterization tests when behavior is unclear.
3. Extract pure functions or cohesive helper groups first.
4. Split by domain responsibility, not by arbitrary technical layer.
5. Add or update a local module README if the boundary is non-obvious.
6. Update public exports through the module entry point.
7. Run the narrowest relevant tests first, then broader tests.
8. Keep each refactoring PR small enough to review.

Avoid large unverified rewrites. Do not combine refactoring with unrelated behavior changes unless explicitly requested.

---

## Context Hygiene Rules

Keep irrelevant files out of AI context and repository search when possible.

Prefer excluding or hiding:

```text
dist/
build/
coverage/
node_modules/
.generated/
generated/
vendor/
*.min.js
*.bundle.js
large snapshots
large fixture JSON files
large logs
binary artifacts
```

Use the repository's ignore and editor settings consistently. Generated code should be isolated and clearly labeled. Hand-written code should not import from generated internals unless there is a stable wrapper.

---

## Agent Editing Rules

Before editing code:

- identify the feature/module being changed
- identify the smallest set of files required
- avoid pulling unrelated large files into the working context
- inspect tests before changing behavior
- preserve existing public APIs unless the task explicitly includes API migration

While editing code:

- prefer explicit names over clever abstractions
- keep the architecture shallow
- add abstractions only at real seams
- avoid new generic `utils` files
- avoid making one file the new dumping ground
- keep imports directional and understandable
- colocate tests with the module where idiomatic for the project

After editing code:

- run or name the most relevant verification command
- state which files changed and why
- mention any follow-up refactoring separately
- do not claim full repository safety unless the relevant tests/build actually ran

---

## Preferred Examples

Preferred module-local design:

```text
src/prediction/
  README.md
  index.ts
  PredictionService.ts
  PredictionStrategy.ts
  strategies/
    SsaPredictionStrategy.ts
    GruPredictionStrategy.ts
    LightGbmPredictionStrategy.ts
  PredictionTypes.ts
  prediction.test.ts
```

Avoid feature scattering without a map:

```text
src/services/PredictionService.ts
src/models/PredictionDto.ts
src/repositories/PredictionRepository.ts
src/factories/PredictionStrategyFactory.ts
src/helpers/PredictionUtils.ts
src/utils/DateUtils.ts
```

Preferred adapter boundary:

```text
src/data-providers/fmp/
  README.md
  index.ts
  FmpClient.ts
  FmpDividendCalendarAdapter.ts
  FmpPriceHistoryAdapter.ts
  FmpTypes.ts
  fmp.test.ts
```

Avoid external API leakage:

```text
src/backtesting/BacktestRunner.ts imports raw FMP response DTOs directly
```

---

## PR Acceptance Checklist

A change is architecturally acceptable when most of these are true:

- The changed files belong to one clear feature/module.
- The change does not introduce a new God file.
- The change does not introduce unnecessary interfaces, factories, or inheritance.
- The module boundary is clearer after the change.
- The relevant tests are present or a test gap is explicitly reported.
- Generated/build/vendor artifacts are not part of the meaningful diff.
- The agent can explain the change by referencing a small number of files.
- New names improve semantic search and human navigation.
- The code is easier to verify than before.

---

## Default Recommendation

When uncertain, choose:

```text
feature-oriented module
+ 3-8 cohesive files
+ one simple public entry point
+ local tests
+ short local README for complex behavior
+ minimal abstraction
```

Avoid both extremes:

```text
Bad: one 5,000-line file
Bad: 50 tiny files for one simple feature
Good: a small cohesive module with clear ownership
```
