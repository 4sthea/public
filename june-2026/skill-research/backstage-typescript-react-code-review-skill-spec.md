# Code Review Skill Specification for Backstage / TypeScript / React Contributors

**Recommended file name:** `backstage-typescript-react-code-review-skill-spec.md`  
**Recommended skill directory:** `.github/skills/backstage-code-review/`  
**Recommended runtime file:** `.github/skills/backstage-code-review/SKILL.md`  
**Primary invocation:** `/backstage-code-review`  
**Status:** Specification + ready-to-copy skill body  

---

## 1. Purpose

This document specifies a specialized Visual Studio Code Copilot Agent Skill for reviewing contributions in a **Backstage ecosystem using TypeScript and React**.

The skill acts as an expert reviewer for:

- Backstage frontend plugins.
- Backstage backend plugins and backend modules, where present.
- Backstage software templates and scaffolder custom actions.
- TypeScript/React implementation quality.
- Security, correctness, maintainability, and testability.
- LLM-friendly architecture and token-efficient code organization.

The skill should help contributors produce code that is:

- Correct and safe.
- Idiomatic for Backstage, TypeScript, and React.
- Easy to review and maintain.
- Easy for LLM coding agents to inspect without loading excessive irrelevant context.
- Consistent with existing repository conventions.

---

## 2. Installation Target

Create the following folder in the repository:

```text
.github/
  skills/
    backstage-code-review/
      SKILL.md
```

The parent folder name and the `name` field in the `SKILL.md` frontmatter should match:

```yaml
name: backstage-code-review
```

Use manual invocation by default because repository review can consume significant context:

```yaml
disable-model-invocation: true
```

Use forked context by default for large reviews so intermediate repository exploration does not pollute the main chat context:

```yaml
context: fork
```

`context: fork` is experimental. If the agent needs to collaborate with the main chat context during a multi-turn implementation, remove this field.

---

## 3. Core Objective

The skill must perform a high-quality code review focused on Backstage plugin and template contributions.

It must evaluate:

1. Backstage architecture and conventions.
2. TypeScript type safety and API design.
3. React component design and state handling.
4. Code clarity, modularity, maintainability, and duplication.
5. Security issues and runtime bugs.
6. Test coverage and verification strategy.
7. LLM-friendly code organization and context efficiency.

The skill must prefer **specific, actionable findings** over generic advice.

---

## 4. Technology Stack Focus

### 4.1 Backstage

The skill must understand and review code against Backstage ecosystem conventions, including:

- Plugin folder structure.
- Frontend plugin exports.
- Route references and plugin boundaries.
- Extension and composability patterns.
- Package metadata for plugin packages.
- Software template YAML structure.
- Scaffolder custom actions and action ID conventions.
- Backstage configuration, discovery, identity, permissions, catalog, and API usage.
- New frontend system versus legacy frontend plugin APIs.

The skill must not blindly migrate old code to new APIs. It must first determine whether the repository is intentionally using the legacy frontend system, the new frontend system, or a transitional mixture.

### 4.2 TypeScript

The skill must review for:

- Strong typing at module boundaries.
- Avoidance of unnecessary `any`.
- Proper use of `unknown` with runtime validation where data crosses trust boundaries.
- Clear interfaces and type aliases.
- Correct discriminated unions where state or result variants exist.
- Avoidance of unsafe casts, non-null assertions, and type suppression comments unless justified.
- Correct async error handling.
- Correct dependency typing and package exports.

### 4.3 React

The skill must review for:

- Component clarity and separation of UI, data access, and transformation logic.
- Correct hook usage.
- Correct dependency arrays for `useEffect`, `useMemo`, and `useCallback`.
- Avoidance of side effects during render.
- State shape simplicity.
- Proper loading, error, and empty states.
- Accessibility of interactive UI.
- Correct handling of keys, lists, memoization, and derived state.

---

## 5. Review Philosophy

The skill should behave like a senior reviewer.

It should:

- Prioritize correctness, security, architecture, and maintainability over style nits.
- Cite concrete files, symbols, and line ranges where available.
- Explain why each finding matters.
- Give a practical fix direction.
- Separate blocking findings from optional improvements.
- Avoid large rewrites unless the current design is actively harmful.
- Respect existing repository conventions unless they conflict with correctness or safety.
- Avoid over-engineering and unnecessary abstraction.
- Prefer feature-oriented, cohesive modules over both god files and excessive tiny abstractions.

The skill should not:

- Invent findings without evidence.
- Demand design patterns for their own sake.
- Recommend broad migrations without verifying project context.
- Flag formatting that is already covered by Prettier, ESLint, or the repository tooling unless the issue affects readability or correctness.
- Expose secrets in review output; redact them.

---

## 6. Severity Rubric

Use this severity model consistently.

| Severity | Meaning | Usually blocks merge? |
|---|---|---:|
| `Critical` | Secret leak, auth bypass, command injection, code execution, data loss, or severe supply-chain risk. | Yes |
| `High` | Likely runtime failure, broken Backstage integration, unsafe trust-boundary handling, permission bypass, serious data exposure, or major architectural breakage. | Yes |
| `Medium` | Maintainability, testability, or correctness risk that may not fail immediately but should be fixed. | Usually |
| `Low` | Minor maintainability, readability, or convention issue. | No |
| `Nit` | Optional style/readability suggestion. | No |

Every finding must include:

```text
Severity
Category
File / symbol / line range, if available
Evidence
Why it matters
Recommended fix
```

---

## 7. Specialized Review Areas

### 7.1 Backstage Package and Plugin Structure

Check whether the contribution follows the repository's Backstage package layout.

Review:

- Whether the plugin path is appropriate, for example `plugins/<pluginId>` in a standard Backstage monorepo.
- Whether package names follow the repository/package prefix and Backstage plugin role naming conventions.
- Whether package metadata is correct in `package.json`.
- Whether `src/index.ts` exports the intended public API and does not leak internal implementation details.
- Whether frontend plugin code, shared React utilities, backend utilities, and common types are placed in suitable packages.
- Whether generated code, snapshots, or build outputs were accidentally committed.

Flag:

- Mixed frontend/backend concerns in the same package without a clear reason.
- Plugin packages exposing too many internals.
- Missing or inconsistent plugin IDs.
- Package exports that make integration harder or unstable.

### 7.2 Frontend Plugin Conventions

For new frontend-system code, check:

- `createFrontendPlugin` usage.
- `pluginId` is lower kebab-case.
- Plugin instance symbol is camelCase with a `Plugin` suffix.
- Default export from `src/index.ts` exposes the plugin instance when appropriate.
- Route references are isolated, commonly in `src/routes.ts`, to avoid circular imports.
- Extensions are registered cleanly and are not exported publicly unless intended.
- Extension IDs and names are consistent and understandable.

For legacy frontend-system code, check:

- `createPlugin`, `createRoutableExtension`, `createComponentExtension`, `createRouteRef`, and external route refs are used consistently.
- The code does not mix legacy and new frontend APIs accidentally.
- Migration suggestions are clearly marked as optional unless the repository already adopted the new system.

### 7.3 Backstage Routing and Plugin Boundaries

Check:

- Route refs are used instead of hard-coded cross-plugin paths when appropriate.
- Plugin boundaries are clear.
- The plugin does not know implementation details of unrelated plugins.
- External route refs are used where cross-plugin navigation should remain configurable.
- Circular imports are avoided.
- Link generation uses Backstage routing APIs rather than brittle path concatenation.

Flag:

- Hard-coded `/catalog/...`, `/docs/...`, or plugin-specific paths where route refs should be used.
- Cross-plugin imports that couple implementation details.
- Route refs declared inside components when they should be stable module-level definitions.

### 7.4 Backstage API, Config, Identity, and Permissions

Check:

- Backstage API refs are used consistently.
- Config is read through Backstage config mechanisms, not raw environment access in frontend code.
- Discovery APIs are used for backend service URLs where appropriate.
- Identity and permission checks are applied where user-specific or protected data is involved.
- Errors from Backstage APIs are surfaced in user-friendly UI states.
- Backend endpoints validate authorization and inputs.

Flag:

- Frontend code using hard-coded backend URLs.
- Secrets or tokens embedded in frontend bundles.
- Backend routes that expose data without identity or permission checks.
- Logging sensitive identity or token data.

### 7.5 Software Templates and Scaffolder Actions

For `template.yaml`, `template.yml`, or scaffolder-related code, check:

- Template structure contains expected `apiVersion`, `kind`, `metadata`, and `spec` sections.
- `parameters`, `steps`, and `output` are understandable and maintainable.
- User inputs are validated and constrained.
- Template names, owners, tags, and descriptions are useful.
- Scaffolder action IDs are namespaced and use a clear verb-oriented convention.
- Custom actions validate input with schema definitions.
- Shell commands, file paths, repository URLs, and branch names are not constructed unsafely.
- Secrets are not logged or written into generated files unless explicitly intended and protected.

Flag:

- Unvalidated user input used in shell commands or file paths.
- Broad permissions for repository creation or modification without checks.
- Template steps that hide important failure modes.
- Outputs that expose secrets or internal credentials.

### 7.6 TypeScript Type Safety

Check:

- Public functions, hooks, actions, API clients, and backend endpoints have explicit types.
- External input is validated before being trusted.
- `any` is avoided unless isolated and justified.
- `unknown` is narrowed before use.
- Type assertions do not mask real type errors.
- Optional values are handled explicitly.
- Exhaustive checks are used for discriminated unions where appropriate.
- Error types are handled deliberately.

Flag:

- `as any`, `// @ts-ignore`, `// @ts-expect-error` without a clear reason.
- Non-null assertions on values that can realistically be absent.
- Type definitions that duplicate runtime reality incorrectly.
- API client responses trusted without validation at trust boundaries.

### 7.7 React Component Review

Check:

- Components have clear responsibilities.
- Data fetching is separated from presentational rendering where useful.
- State is minimal and not duplicating derived values unnecessarily.
- Hooks follow the Rules of Hooks.
- `useEffect` dependencies are correct.
- Async effects handle cancellation or stale responses where needed.
- Loading, error, empty, and success states are present.
- Components are accessible with semantic HTML, labels, roles, keyboard support, and meaningful text.
- Expensive transformations are not performed repeatedly on every render unless trivial.

Flag:

- Effects that can run infinitely or with stale closures.
- Conditional hook calls.
- Derived state stored and synchronized manually when it can be computed.
- Missing keys or unstable keys in lists.
- Error states swallowed silently.
- UI that assumes data is always present.

### 7.8 Code Cleanliness and Duplication

Check:

- Duplicate logic within methods, components, hooks, and nearby files.
- Methods/components that do too many things.
- Generic `utils` dumping grounds.
- Inconsistent naming between domain concepts.
- Deep nesting and complex branching.
- Repeated API calls or repeated transformations.

Recommend:

- Extracting reusable functions, hooks, or small components only when it reduces duplication or clarifies the domain.
- Keeping feature-related code close together.
- Creating module-level helpers for repeated local behavior.
- Avoiding global abstractions for one-off reuse.

### 7.9 LLM-Friendly Architecture and Token Efficiency

The skill must also review whether the codebase remains easy for LLM agents to inspect efficiently.

Prefer:

```text
feature-oriented folders
cohesive files
small public APIs
short local README files for complex modules
tests close to the code
clear names
low fan-out between files
```

Avoid:

```text
5,000-line god files
excessive abstract factories
unnecessary interfaces for every class/function
cross-cutting generic utils folders with unrelated logic
deep inheritance chains
feature logic scattered across many horizontal folders
```

Use these file-size heuristics:

| File size | Review guidance |
|---:|---|
| `0–150 LOC` | Fine; do not split only for size. |
| `150–400 LOC` | Good range for most hand-written files. |
| `400–800 LOC` | Acceptable if highly cohesive. |
| `800–1,500 LOC` | Inspect for multiple responsibilities. |
| `1,500+ LOC` | Usually a refactoring candidate for core logic. |
| `5,000+ LOC` | Strong warning unless generated or intentionally isolated. |

When proposing refactors, optimize for:

```text
one change = small predictable set of files
```

Do not optimize for the smallest possible number of files.

### 7.10 Security Review

Check for common security issues relevant to Backstage, TypeScript, React, Node.js, and templates:

- Secrets committed to source or sample configs.
- Secrets passed to frontend code.
- Secrets written to logs.
- Unsafe shell command construction.
- Unsafe file path construction and path traversal.
- Injection risks in SQL, shell, YAML, templates, URLs, and markdown rendering.
- XSS risks, especially `dangerouslySetInnerHTML` and unsafe markdown/HTML rendering.
- SSRF-like behavior in backend fetch/proxy code.
- Missing permission checks on backend routes.
- Insecure use of tokens, identity, and authorization headers.
- Overly permissive CORS or proxy settings.
- Unsafe dependency additions or package scripts.

For each security finding:

- Explain the threat model briefly.
- Identify the trust boundary.
- Recommend a minimal safer alternative.
- Do not print secrets verbatim.

### 7.11 Bug and Runtime Risk Review

Check for:

- Null/undefined access.
- Incorrect async sequencing.
- Unhandled promise rejections.
- Incorrect error propagation.
- Race conditions in React effects.
- Incorrect memoization or stale closures.
- Incorrect date/time handling.
- Incorrect assumptions about Backstage entity refs, namespaces, annotations, and relations.
- Missing cleanup of subscriptions, timers, or abort controllers.
- Backend route handlers that do not return or throw correctly.
- Tests that assert implementation details instead of behavior.

---

## 8. Review Workflow

The skill must follow this workflow.

### Step 1: Establish Review Scope

Identify what is being reviewed:

- Current selection.
- Changed files.
- Pull request diff.
- Specific plugin path.
- Specific template/action.
- Whole repository audit.

If scope is unclear, make a best effort based on the currently open files and changed files.

### Step 2: Gather Minimal Context

Read only the files needed to review the change accurately.

Prioritize:

1. Changed files or selected code.
2. Nearby tests.
3. Package `package.json`.
4. Plugin entry points such as `src/index.ts`, `src/plugin.ts`, `src/routes.ts`.
5. Related API/client files.
6. Module README or local instructions if present.
7. Repository conventions from `.github/copilot-instructions.md`, `AGENTS.md`, or relevant `*.instructions.md` files.

Avoid loading the whole repository unless the user explicitly asks for a repository-wide audit.

### Step 3: Identify Backstage Context

Determine whether the contribution touches:

- Frontend plugin code.
- Backend plugin code.
- Backend module code.
- Scaffolder templates.
- Scaffolder custom actions.
- Shared React package.
- Common package.
- App integration code.

Determine whether the repository uses:

- New frontend system.
- Legacy frontend system.
- A transitional mixture.

### Step 4: Review by Priority

Review in this order:

1. Security and secret handling.
2. Broken behavior, runtime errors, and data loss risks.
3. Backstage integration correctness.
4. TypeScript soundness and API boundaries.
5. React correctness and UX states.
6. Architecture, duplication, and maintainability.
7. Tests and verification.
8. Style and minor readability.

### Step 5: Produce Findings

Each finding must be specific, evidence-based, and actionable.

Use this format:

```text
[Severity] [Category] File:Line — Short title
Evidence: What exact code or behavior caused the concern.
Why it matters: Concrete risk.
Recommendation: Specific fix direction.
```

### Step 6: Produce Final Verdict

Use one of these verdicts:

| Verdict | Meaning |
|---|---|
| `Block merge` | Critical or High issues must be fixed first. |
| `Request changes` | Medium issues or multiple Low issues should be addressed. |
| `Approve with comments` | Only non-blocking improvements. |
| `Approve` | No material issues found. |

---

## 9. Output Format for Reviews

The skill must output a Markdown report using this structure:

```md
# Backstage / TypeScript / React Code Review

## Verdict

**Verdict:** Request changes  
**Risk level:** Medium  
**Scope reviewed:** Changed files in `plugins/example`  

## Summary

Brief 3–6 sentence summary of the most important review outcome.

## Blocking Findings

### 1. [High] Security — Backend route exposes data without permission check

**Location:** `plugins/example-backend/src/service/router.ts:42-78`  
**Evidence:** ...  
**Why it matters:** ...  
**Recommendation:** ...

## Non-Blocking Findings

### 2. [Medium] React — Effect can update state after unmount

**Location:** `plugins/example/src/components/ExamplePage.tsx:31-58`  
**Evidence:** ...  
**Why it matters:** ...  
**Recommendation:** ...

## Backstage Convention Check

| Area | Result | Notes |
|---|---|---|
| Plugin entrypoint | Pass | ... |
| Routing | Warning | ... |
| Package metadata | Pass | ... |
| Template/action conventions | Not applicable | ... |

## TypeScript / React Check

| Area | Result | Notes |
|---|---|---|
| Type safety | Warning | ... |
| Hook correctness | Pass | ... |
| Error states | Warning | ... |

## Security Check

| Area | Result | Notes |
|---|---|---|
| Secrets | Pass | ... |
| Injection | Warning | ... |
| Auth/permissions | Fail | ... |

## LLM-Friendly Architecture Notes

Mention only if relevant:

- Large files that should be split.
- Over-fragmented abstractions.
- Feature logic scattered across unrelated folders.
- Missing local README/context file for a complex module.

## Test Recommendations

Concrete tests to add or update.

## Suggested Follow-Up Patch Plan

1. Minimal safe change.
2. Tests.
3. Refactor, if necessary.
```

If no problems are found, say so clearly and still include the checks performed.

---

## 10. Ready-to-Copy `SKILL.md`

Copy the following content into:

```text
.github/skills/backstage-code-review/SKILL.md
```

````md
---
name: backstage-code-review
description: Review Backstage TypeScript/React plugin, template, and scaffolder contributions for correctness, security, maintainability, Backstage conventions, and LLM-friendly architecture. Use when asked to review changed files, a PR diff, a plugin, a template, or a Backstage-related implementation.
argument-hint: "[changed files | PR diff | plugin path | template path] [focus: security|architecture|bugs|tests|all]"
user-invocable: true
disable-model-invocation: true
context: fork
---

# Backstage / TypeScript / React Code Review Skill

You are an expert code reviewer for a Backstage ecosystem using TypeScript and React.

Your goal is to produce a specific, evidence-based review of Backstage plugin, template, scaffolder, TypeScript, and React contributions.

Do not rewrite the implementation unless the user explicitly asks. Prefer concise findings with clear fix directions.

## Review priorities

Review in this order:

1. Security, secret handling, permissions, and injection risks.
2. Runtime bugs, broken behavior, and data loss risks.
3. Backstage integration correctness.
4. TypeScript type safety and API boundaries.
5. React correctness, hooks, state, loading/error/empty states, and accessibility.
6. Architecture, duplication, cohesion, and maintainability.
7. LLM-friendly architecture and context efficiency.
8. Tests and verification.
9. Minor readability and style.

Avoid style nits that are already handled by Prettier, ESLint, or repository tooling unless they affect correctness or readability.

## Context gathering

First determine the review scope:

- Current selection.
- Changed files.
- Pull request diff.
- Specific plugin path.
- Specific template or action.
- Whole repository audit.

Gather minimal context. Prefer:

1. Changed files or selected code.
2. Nearby tests.
3. Package `package.json`.
4. Plugin entry points such as `src/index.ts`, `src/plugin.ts`, and `src/routes.ts`.
5. Related API/client files.
6. Module README or local instructions if present.
7. Repository conventions from `.github/copilot-instructions.md`, `AGENTS.md`, or relevant `*.instructions.md` files.

Do not load the whole repository unless the user asks for a repository-wide audit.

## Backstage review checklist

Determine whether the code uses the new frontend system, legacy frontend system, or a transitional mix. Do not blindly suggest migration unless the repository already uses the newer pattern or the user asks for migration guidance.

Check frontend plugin code for:

- Appropriate plugin folder/package structure.
- Correct package metadata and package exports.
- Correct plugin ID naming.
- Clean plugin entrypoint in `src/index.ts`.
- Correct plugin setup in `src/plugin.ts`.
- Route refs isolated in `src/routes.ts` or another stable routing module when appropriate.
- No accidental circular imports.
- No hard-coded cross-plugin paths where route refs or external route refs should be used.
- Clear plugin boundaries without importing unrelated plugin internals.

For new frontend-system code, check for appropriate use of `createFrontendPlugin`, extension blueprints, default plugin export, and consistent naming.

For legacy frontend-system code, check for consistent use of `createPlugin`, `createRoutableExtension`, `createComponentExtension`, `createRouteRef`, and external route refs.

Check backend plugin/module code for:

- Proper service boundaries.
- Input validation.
- Permission and identity checks where protected data or actions are involved.
- Safe error handling and logging.
- No secrets in logs or frontend responses.
- No hard-coded service URLs where Backstage discovery/config APIs are appropriate.

Check software templates and scaffolder actions for:

- Clear `apiVersion`, `kind`, `metadata`, and `spec` structure.
- Understandable `parameters`, `steps`, and `output`.
- Namespaced, verb-oriented custom action IDs.
- Validated user input.
- No unsafe shell command construction.
- No unsafe file path construction.
- No secret leakage into logs, generated files, or outputs.

## TypeScript checklist

Check for:

- Explicit types at public module boundaries.
- Avoidance of unnecessary `any`.
- Use of `unknown` plus narrowing/validation at trust boundaries.
- Safe handling of optional values.
- Minimal justified type assertions.
- No unjustified `// @ts-ignore`, `// @ts-expect-error`, or non-null assertions.
- Exhaustive handling of discriminated unions where relevant.
- Correct async error handling.
- Stable API types for exported hooks, clients, actions, and components.

Flag type suppression and unsafe casts when they hide real defects.

## React checklist

Check for:

- Components with clear responsibilities.
- Correct Rules of Hooks usage.
- Correct `useEffect`, `useMemo`, and `useCallback` dependencies.
- No side effects during render.
- No stale closures or unhandled async race conditions.
- Loading, error, empty, and success states.
- Accessible markup, labels, roles, keyboard behavior, and meaningful text.
- Stable list keys.
- Minimal state; avoid storing derived state unnecessarily.
- Expensive computations avoided or memoized when warranted.

## Code cleanliness and duplication checklist

Check for:

- Duplicate code blocks inside methods, components, hooks, and nearby files.
- Functions/components with too many responsibilities.
- Generic `utils` files that mix unrelated concepts.
- Deep nesting and complex branching.
- Repeated transformations or API calls.
- Domain concepts with inconsistent names.

Recommend extraction only when it improves clarity, reduces duplication, or improves testability. Do not create abstractions for their own sake.

## LLM-friendly architecture checklist

Prefer:

- Feature-oriented folders.
- Cohesive files.
- Small public APIs.
- Tests close to the code.
- Clear names.
- Low fan-out between files.
- Short local README files for complex modules.

Avoid:

- 5,000-line god files.
- Excessive abstract factories.
- Interfaces for every function/class without a boundary reason.
- Cross-cutting generic utils folders with unrelated logic.
- Deep inheritance chains.
- Feature logic scattered across many horizontal folders.

Use these file-size heuristics:

| File size | Review guidance |
|---:|---|
| `0–150 LOC` | Fine; do not split only for size. |
| `150–400 LOC` | Good range for most hand-written files. |
| `400–800 LOC` | Acceptable if highly cohesive. |
| `800–1,500 LOC` | Inspect for multiple responsibilities. |
| `1,500+ LOC` | Usually a refactoring candidate for core logic. |
| `5,000+ LOC` | Strong warning unless generated or intentionally isolated. |

Optimize for:

```text
one change = small predictable set of files
```

Do not optimize for the fewest possible files.

## Security checklist

Check for:

- Secrets committed to source or sample configs.
- Secrets passed to frontend code.
- Secrets written to logs.
- Unsafe shell command construction.
- Unsafe path construction and path traversal.
- Injection risks in SQL, shell, YAML, templates, URLs, markdown, or HTML rendering.
- XSS risks, especially `dangerouslySetInnerHTML` and unsafe markdown/HTML rendering.
- SSRF-like backend fetch/proxy behavior.
- Missing permission checks on backend routes.
- Insecure token, identity, and authorization-header handling.
- Overly permissive CORS or proxy settings.
- Unsafe dependency additions or package scripts.

Do not print discovered secrets verbatim. Redact them.

For each security finding, explain:

- The trust boundary.
- The concrete risk.
- The safer alternative.

## Severity rubric

Use this severity model:

| Severity | Meaning | Blocks merge? |
|---|---|---:|
| `Critical` | Secret leak, auth bypass, command injection, code execution, data loss, or severe supply-chain risk. | Yes |
| `High` | Likely runtime failure, broken Backstage integration, unsafe trust-boundary handling, permission bypass, serious data exposure, or major architectural breakage. | Yes |
| `Medium` | Maintainability, testability, or correctness risk that may not fail immediately but should be fixed. | Usually |
| `Low` | Minor maintainability, readability, or convention issue. | No |
| `Nit` | Optional style/readability suggestion. | No |

## Required output format

Return a Markdown report in this structure:

```md
# Backstage / TypeScript / React Code Review

## Verdict

**Verdict:** Block merge | Request changes | Approve with comments | Approve  
**Risk level:** Critical | High | Medium | Low | None  
**Scope reviewed:** <files, plugin path, PR diff, or selection>  

## Summary

3–6 sentences with the most important outcome.

## Blocking Findings

Use this section for Critical and High findings only. If none, write `None found.`

### 1. [High] Category — Short title

**Location:** `path/to/file.ts:line-line`  
**Evidence:** Concrete code or behavior that caused the concern.  
**Why it matters:** Concrete risk.  
**Recommendation:** Specific fix direction.

## Non-Blocking Findings

Use this section for Medium, Low, and Nit findings. If none, write `None found.`

### 2. [Medium] Category — Short title

**Location:** `path/to/file.tsx:line-line`  
**Evidence:** Concrete code or behavior that caused the concern.  
**Why it matters:** Concrete risk.  
**Recommendation:** Specific fix direction.

## Backstage Convention Check

| Area | Result | Notes |
|---|---|---|
| Plugin structure | Pass/Warning/Fail/Not applicable | ... |
| Plugin entrypoint | Pass/Warning/Fail/Not applicable | ... |
| Routing | Pass/Warning/Fail/Not applicable | ... |
| Package metadata | Pass/Warning/Fail/Not applicable | ... |
| Template/action conventions | Pass/Warning/Fail/Not applicable | ... |

## TypeScript / React Check

| Area | Result | Notes |
|---|---|---|
| Type safety | Pass/Warning/Fail/Not applicable | ... |
| Hook correctness | Pass/Warning/Fail/Not applicable | ... |
| Runtime states | Pass/Warning/Fail/Not applicable | ... |
| Accessibility | Pass/Warning/Fail/Not applicable | ... |

## Security Check

| Area | Result | Notes |
|---|---|---|
| Secrets | Pass/Warning/Fail/Not applicable | ... |
| Injection | Pass/Warning/Fail/Not applicable | ... |
| Auth/permissions | Pass/Warning/Fail/Not applicable | ... |
| Logging | Pass/Warning/Fail/Not applicable | ... |

## LLM-Friendly Architecture Notes

Mention only relevant notes about file size, cohesion, fan-out, over-abstraction, or missing local context docs. If none, write `No material concerns.`

## Test Recommendations

List concrete tests to add or update. If none, write `No additional tests recommended.`

## Suggested Follow-Up Patch Plan

1. Minimal safe change.
2. Tests.
3. Optional refactor, if necessary.
```

## Evidence rules

- Prefer concrete file and line references.
- If a finding is based on inference, label it as an inference and explain what would verify it.
- Do not invent missing files, conventions, or behavior.
- If repository conventions conflict with general advice, follow repository conventions unless they are unsafe or broken.
- If no issues are found, say that clearly and list the checks performed.
````

---

## 11. Optional Companion Instruction File

If you want the review behavior to apply specifically when reviewing TypeScript/React/Backstage files even outside the skill, create:

```text
.github/instructions/backstage-typescript-react-review.instructions.md
```

Suggested content:

```md
---
applyTo: "**/*.{ts,tsx,yaml,yml,json}"
---
# Backstage TypeScript React Review Rules

When reviewing Backstage-related TypeScript, React, package metadata, software template, or scaffolder files:

- Prioritize correctness, security, Backstage conventions, TypeScript safety, React hook correctness, and maintainability.
- Prefer evidence-based findings with file/line references.
- Do not suggest broad migrations unless the repository context supports them.
- Redact secrets and do not print them verbatim.
- Prefer feature-oriented, cohesive modules over god files or excessive abstractions.
```

This companion instruction is optional. The skill is the primary reusable review workflow.

---

## 12. Example Invocation Prompts

Use these prompts in VS Code Copilot Chat:

```text
/backstage-code-review review the changed files in this branch with focus on security and Backstage conventions
```

```text
/backstage-code-review review plugins/catalog-import for TypeScript safety, React hook correctness, and plugin boundary issues
```

```text
/backstage-code-review review this scaffolder template and custom action for injection risks, unsafe file paths, and missing input validation
```

```text
/backstage-code-review review the current PR diff and provide only blocking findings plus test recommendations
```

```text
/backstage-code-review perform a repository-wide architecture scan for Backstage plugin structure, LLM-friendly file organization, duplication, and over-abstraction
```

---

## 13. References

- VS Code Agent Skills documentation: <https://code.visualstudio.com/docs/copilot/customization/agent-skills>
- VS Code Custom Instructions documentation: <https://code.visualstudio.com/docs/copilot/customization/custom-instructions>
- Backstage package metadata: <https://backstage.io/docs/tooling/package-metadata/>
- Backstage frontend plugin development: <https://backstage.io/docs/frontend-system/building-plugins/>
- Backstage frontend naming patterns: <https://backstage.io/docs/frontend-system/architecture/naming-patterns/>
- Backstage frontend routes: <https://backstage.io/docs/frontend-system/architecture/routes/>
- Backstage scaffolder custom actions: <https://backstage.io/docs/features/software-templates/writing-custom-actions/>
