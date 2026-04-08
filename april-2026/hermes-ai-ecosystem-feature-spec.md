# Feature Specification: Hermes-Informed Runtime Enhancements for AI ecosystem

**Status:** Draft proposal  
**Audience:** AI ecosystem maintainers / Copilot ecosystem maintainers  
**Primary Goal:** Selectively import the strongest runtime ideas from Hermes Agent into AI ecosystem without weakening AI ecosystem’s epistemic governance model  
**Scope:** Architecture, runtime model, skills, checkpoints, worktree isolation, approvals, plugin seams, evaluation, and rollout  
**Decision Theme:** Borrow Hermes runtime mechanics. Reject Hermes-style unconstrained self-modification of high-authority artifacts.

---

# Table of Contents

- [1. Executive Summary](#1-executive-summary)
- [2. Hermes Agent: Comprehensive Introduction](#2-hermes-agent-comprehensive-introduction)
  - [2.1 What Hermes Is](#21-what-hermes-is)
  - [2.2 What Hermes Does](#22-what-hermes-does)
  - [2.3 What Hermes Is Used For](#23-what-hermes-is-used-for)
  - [2.4 Core Design Philosophy](#24-core-design-philosophy)
  - [2.5 Key Capabilities](#25-key-capabilities)
  - [2.6 Key Systems](#26-key-systems)
  - [2.7 Architecture Overview](#27-architecture-overview)
  - [2.8 Runtime Model](#28-runtime-model)
  - [2.9 Context and Prompt Model](#29-context-and-prompt-model)
  - [2.10 Memory Model](#210-memory-model)
  - [2.11 Skill Model](#211-skill-model)
  - [2.12 Tool and Provider Model](#212-tool-and-provider-model)
  - [2.13 Security Model](#213-security-model)
  - [2.14 Scheduling and Automation Model](#214-scheduling-and-automation-model)
  - [2.15 Delegation and Parallelism](#215-delegation-and-parallelism)
  - [2.16 Self-Improvement and Self-Evolution](#216-self-improvement-and-self-evolution)
  - [2.17 Repository / System Structure](#217-repository--system-structure)
  - [2.18 Advantages](#218-advantages)
  - [2.19 Disadvantages and Risks](#219-disadvantages-and-risks)
  - [2.20 Key Insights Worth Extracting](#220-key-insights-worth-extracting)
  - [2.21 What AI ecosystem Should Explicitly Reject](#221-what-AI ecosystem-should-explicitly-reject)
- [3. AI ecosystem Context and Design Constraints](#3-AI ecosystem-context-and-design-constraints)
- [4. Problem Statement](#4-problem-statement)
- [5. Product Vision](#5-product-vision)
- [6. Goals](#6-goals)
- [7. Non-Goals](#7-non-goals)
- [8. Proposed Feature Set](#8-proposed-feature-set)
  - [8.1 Runtime Profiles for Orchestrator Isolation](#81-runtime-profiles-for-orchestrator-isolation)
  - [8.2 Worktree Execution Lanes](#82-worktree-execution-lanes)
  - [8.3 Checkpoint and Rollback Manager](#83-checkpoint-and-rollback-manager)
  - [8.4 Summary-Only Subagent Contract](#84-summary-only-subagent-contract)
  - [8.5 Trust-Tiered Skill System](#85-trust-tiered-skill-system)
  - [8.6 Capability Packs / Plugin Seams](#86-capability-packs--plugin-seams)
  - [8.7 Approval Policy Engine](#87-approval-policy-engine)
  - [8.8 Context Compression and Handoff Summaries](#88-context-compression-and-handoff-summaries)
  - [8.9 Self-Optimization Lab for Low-Authority Assets](#89-self-optimization-lab-for-low-authority-assets)
  - [8.10 Evaluation Harness for Runtime Changes](#810-evaluation-harness-for-runtime-changes)
- [9. Detailed Requirements](#9-detailed-requirements)
- [10. Architecture Design](#10-architecture-design)
- [11. File and Directory Layout](#11-file-and-directory-layout)
- [12. Orchestrator Changes](#12-orchestrator-changes)
- [13. Skill System Changes](#13-skill-system-changes)
- [14. Hook and Procedure Changes](#14-hook-and-procedure-changes)
- [15. Data Model](#15-data-model)
- [16. Security and Governance](#16-security-and-governance)
- [17. Migration Plan](#17-migration-plan)
- [18. Rollout Plan](#18-rollout-plan)
- [19. Acceptance Criteria](#19-acceptance-criteria)
- [20. Risks, Trade-Offs, and Failure Modes](#20-risks-trade-offs-and-failure-modes)
- [21. Open Questions](#21-open-questions)
- [22. Final Recommendation](#22-final-recommendation)

---

# 1. Executive Summary

Hermes Agent is best understood as a **stateful agent runtime platform** rather than a prompt-governance framework. It provides a broad execution environment for agents: isolated profiles, tools, skills, persistent memory, scheduled tasks, worktrees, checkpoint/rollback, multi-platform messaging, provider routing, and optional self-improvement components. Its strongest ideas are operational, not epistemic.

AI ecosystem, by contrast, is fundamentally an **epistemic governance architecture**. Its main strength is not convenience or feature breadth. Its main strength is artifact discipline: single ownership of rules, bounded authority, verification gates, and explicit separation of cognition from enforcement.

Therefore the right strategic move is **not** to morph AI ecosystem into Hermes. The right move is to selectively import Hermes patterns that improve runtime safety and coordination while preserving AI ecosystem’s stricter authority model.

This specification proposes nine concrete enhancements:

1. Runtime profiles for orchestrator isolation
2. Worktree execution lanes for risky or parallel work
3. Checkpoint/rollback manager for reversible mutation
4. Summary-only subagent contract to reduce context pollution
5. Trust-tiered skill system with promotion controls
6. Capability packs / plugin seams outside core governance
7. Approval policy engine for deterministic and semi-smart command control
8. Context compression and lineage-preserving handoff summaries
9. Separate optimization lab for low-authority assets only

The core principle is simple:

> Import Hermes runtime mechanics. Do not import Hermes-style unrestricted self-modification into AI ecosystem core governance.

---

# 2. Hermes Agent: Comprehensive Introduction

## 2.1 What Hermes Is

Hermes Agent is an open-source, self-hostable AI agent platform built by Nous Research. It is designed to operate as a persistent, tool-using, stateful agent that can live across sessions, platforms, environments, and workflows.

It is not just a chat UI. It is a runtime and execution framework for agents that can:

- call tools
- manage sessions
- remember information across runs
- schedule tasks
- run on multiple backends
- connect to messaging platforms
- delegate sub-work
- load skills on demand
- optionally evolve prompts/skills through a separate optimization pipeline

At a conceptual level, Hermes tries to be:

- an agent shell
- an agent server
- an execution orchestrator
- a memory-capable assistant runtime
- an extensible framework for tools, providers, and skills

## 2.2 What Hermes Does

Hermes provides an environment in which an LLM can act more like a persistent operator than a transient chat model.

In practice it does the following:

- assembles prompt state from persona, memory, skills, and context files
- resolves the correct inference provider and API mode
- executes tool calls
- maintains session history across CLI and gateway use
- compresses context when sessions get large
- caches prompt prefixes where supported
- stores structured session data in SQLite
- uses skills as reusable procedural capability bundles
- schedules future work through cron-like automation
- supports isolated profiles
- supports worktree-based isolation for coding tasks
- can snapshot file state before destructive operations
- exposes multiple extension seams for tools, providers, memory, and plugins

## 2.3 What Hermes Is Used For

Hermes is used as a general agent runtime for scenarios such as:

- coding and repository work
- Linux/server administration
- long-running research tasks
- messaging bots on Telegram/Discord/Slack/other gateways
- scheduled automations and recurring tasks
- personal assistant workflows
- self-hosted multi-platform agent deployments
- experimentation with agent memory, skills, and self-improvement

It is especially attractive to users who want the same agent identity and memory to survive across environments and sessions instead of restarting from scratch each time.

## 2.4 Core Design Philosophy

Hermes is built around a few strong ideas:

### Persistence over statelessness

Hermes assumes that an agent becomes more useful if it can preserve state across time rather than living only inside a single chat session.

### Progressive disclosure over prompt bloat

Skills and subdirectory context files are meant to appear only when relevant rather than being dumped into the system prompt upfront.

### Operational breadth over narrow specialization

Hermes supports many modalities and environments: CLI, APIs, gateways, memory plugins, automation, tools, voice, and integrations.

### Runtime modularity over monolithic hardcoding

Hermes exposes extension seams for providers, plugins, memory providers, and skills.

### Agent continuity over per-task amnesia

Profiles, sessions, checkpoints, and storage are all designed to make the agent feel durable rather than ephemeral.

## 2.5 Key Capabilities

Hermes’ main capabilities can be grouped as follows:

### Core execution

- stateful conversation loop
- tool calling
- provider selection and failover behavior
- conversation persistence
- context compression

### Context shaping

- SOUL.md for durable persona
- AGENTS.md and related context files for project instructions
- progressive subdirectory discovery
- security scanning for context-bearing files

### Skills

- reusable procedural capability bundles
- progressive-disclosure loading
- community-shareable structure
- optional skill creation and improvement behavior

### Memory

- built-in local memory files
- optional memory provider plugins
- cross-session recall
- session database with full-text search
- optional deeper user modeling via Honcho

### Isolation and safety

- isolated profiles
- worktree support
- checkpoint/rollback mechanism
- containerized backends
- dangerous-command approval
- MCP credential filtering

### Automation

- cron-like scheduled tasks
- multi-platform delivery
- persistent shell and command workflows
- gateway operation

### Extensibility

- provider plugins
- memory provider plugins
- skill authoring
- CLI extension
- plugin architecture

## 2.6 Key Systems

The key Hermes systems are:

1. **AIAgent loop** — core orchestration engine
2. **Prompt assembly system** — builds the effective system prompt from persona, context, memory, and skills
3. **Provider runtime resolver** — central provider/auth/runtime selector
4. **Tool runtime / dispatch** — executes tool calls and coordinates tool schemas
5. **Session storage** — SQLite-backed persistence for sessions and messages
6. **Context compression system** — manages long sessions through compression
7. **Prompt caching integration** — provider-aware caching optimization
8. **Checkpoint manager** — snapshots state before destructive operations
9. **Profile system** — creates isolated Hermes environments
10. **Worktree integration** — safe parallel coding and rollback isolation
11. **Skills system** — reusable procedural memory layer
12. **Memory provider plugin system** — pluggable persistent memory backends
13. **Gateway subsystem** — multi-platform agent access and messaging
14. **Cron subsystem** — scheduled automations
15. **Plugin architecture** — user-extendable tools/commands/hooks
16. **Security model** — layered isolation, approval, scanning, and credential boundaries
17. **Optional self-evolution pipeline** — separate repo for optimizing Hermes artifacts

## 2.7 Architecture Overview

At a high level, the architecture looks like this:

1. Entry points feed requests into the central agent runtime.
2. The runtime assembles context and tool schemas.
3. The provider runtime determines which model/provider/API mode to use.
4. The model produces tool calls or text.
5. Tool dispatch executes actions.
6. Session history is persisted.
7. Compression and caching manage long-horizon efficiency.
8. Skills, memory, and context files shape future behavior.
9. Gateways and cron extend the runtime across platforms and time.

### Architectural character

Hermes is architecturally broad rather than narrow. It is less like a single-purpose coding agent and more like a general operating environment for tool-using language agents.

That gives it flexibility, but it also increases complexity and widens the attack surface.

## 2.8 Runtime Model

Hermes uses a central runtime class, `AIAgent`, as the main orchestration engine. That engine is responsible for:

- building the effective prompt
- selecting the provider/API mode
- executing sequential or concurrent tool calls
- maintaining history
- triggering compression
- handling retries and fallback behavior
- tracking iteration budgets
- flushing persistent memory before context loss

This means Hermes’ main logic is concentrated in one large orchestration surface rather than spread across many tiny orchestrators.

### Implication

This makes Hermes powerful and cohesive, but it also makes the core runtime a critical complexity hotspot.

## 2.9 Context and Prompt Model

Hermes uses a layered context model:

### SOUL.md

A durable personality / identity file stored in the Hermes home directory. This is instance-level identity, not project context.

### Project context files

Hermes supports a priority stack of project context files such as `.hermes.md`, `AGENTS.md`, `CLAUDE.md`, and `.cursorrules`, with first-match behavior for primary project context.

### Progressive subdirectory discovery

Subdirectory context files are not injected upfront. They are discovered as the agent navigates the project, reducing prompt bloat and preserving cache stability.

### Prompt assembly

The prompt builder composes personality, tool behavior, memory, skills, context files, and other system-level sections into the final prompt.

### Security scanning

Context-bearing files are scanned for prompt-injection patterns before inclusion.

### Strength

This is a serious runtime-context architecture, not just “paste a system prompt.”

### Weakness

It still creates a broad, mutable prompt surface, which is powerful but governance-heavy.

## 2.10 Memory Model

Hermes’ memory model has multiple layers:

### Built-in local memory

Persistent files such as memory/user state maintained under the Hermes home directory.

### Session database

A SQLite database stores sessions, messages, FTS tables, and schema versioning.

### Full-text retrieval

FTS-backed recall over prior sessions allows Hermes to search its own history.

### Memory provider plugins

External memory systems can be attached through a plugin API.

### Honcho

An optional deeper memory / user-modeling layer intended to build richer long-term understanding.

### Strength

Hermes treats memory as a first-class runtime concern rather than an afterthought.

### Weakness

Memory easily becomes a source of hidden authority. If not bounded carefully, it can silently shape future outputs in ways that are hard to audit.

## 2.11 Skill Model

Hermes positions skills as the preferred way to add new capabilities when the behavior can be expressed using instructions, shell commands, and existing tools.

### Skill characteristics

- reusable
- declarative or semi-procedural
- progressive disclosure
- no need to patch the agent core for many use cases
- community-shareable
- compatible with the wider agent-skills style ecosystem

### Skill vs tool distinction

Hermes explicitly distinguishes between:

- **skill**: instructions + shell commands + existing tool use
- **tool**: precise runtime integration requiring custom code, auth, streaming, or binary/event handling

### Strength

This is a good separation. It keeps many extensions out of the runtime core.

### Weakness

If skills are untrusted, automatically generated, or mutable by the agent itself, they can become a supply-chain and governance risk.

## 2.12 Tool and Provider Model

Hermes uses:

- multiple providers
- multiple API modes
- shared runtime resolution across CLI/gateway/cron/ACP
- tool grouping into toolsets
- MCP integration
- optional external plugins

This makes Hermes adaptable across many environments and model vendors.

### Strength

Centralized runtime provider resolution is good engineering because it avoids duplicating auth/runtime logic across every entrypoint.

### Weakness

Broad provider and tool support increases the surface area for bugs, auth mishaps, and inconsistent behavior between providers.

## 2.13 Security Model

Hermes documents a seven-layer security model:

1. user authorization
2. dangerous command approval
3. container isolation
4. MCP credential filtering
5. context file scanning
6. cross-session isolation
7. input sanitization

### Why this is good

Hermes at least treats security as a runtime systems problem instead of relying on prompts alone.

### Why this is not enough by itself

Layered security on paper is useful, but the real question is enforcement quality, defaults, bypass resistance, and whether critical paths remain deterministic.

## 2.14 Scheduling and Automation Model

Hermes includes scheduled automations using cron-like workflows and delivery to platforms. This lets the agent behave less like a reactive chat bot and more like a proactive system.

### Strength

Useful for recurring workflows, maintenance, reminders, monitoring, and scheduled research.

### Weakness

Scheduled execution widens the blast radius of errors if permissions, prompts, or skills are weak.

## 2.15 Delegation and Parallelism

Hermes supports delegated work through child agents with isolated context, restricted toolsets, and their own terminal sessions.

This is valuable because it gives the system a way to:

- explore parallel workstreams
- isolate subproblems
- keep parent context smaller
- apply different tool restrictions

### Strength

This is one of the strongest runtime patterns in Hermes.

### Weakness

Delegation without strict output contracts can produce context spam, drift, duplicated effort, or hidden assumptions.

## 2.16 Self-Improvement and Self-Evolution

Hermes markets itself heavily around being “self-improving.” There are really two layers here:

### In-core self-improvement style behavior

- nudging itself to persist knowledge
- creating skills from experience
- improving skills during use
- optional deeper memory behavior

### Separate self-evolution repository

A separate repo uses DSPy + GEPA to evolve skills, tool descriptions, prompts, and eventually code, with evaluation and constraint gates.

### Important distinction

The separate optimization repo is more disciplined than the marketing slogan suggests. It is an explicit optimization pipeline, not magic autonomous self-perfection.

### Strength

Treating optimization as a separate pipeline is much safer than letting the runtime rewrite itself unchecked.

### Weakness

“Self-improving” language can lead users to overestimate autonomy, reliability, or safety.

## 2.17 Repository / System Structure

At a functional level, Hermes’ structure can be understood as these major areas:

### Entry surfaces

- CLI
- gateway
- API/server-like entrypoints
- ACP/editor integration
- Python library usage

### Runtime core

- AIAgent loop
- prompt builder
- provider runtime resolution
- tool runtime / dispatch
- session state

### State and persistence

- Hermes home directory
- session database
- logs
- memories
- skills
- cron jobs
- plugin state
- caches

### Extension layers

- skills
- optional skills
- plugins
- providers
- memory provider plugins
- CLI extensions

### Safety / isolation layers

- approval logic
- worktrees
- checkpoints
- container backends
- context scanning

### Optimization / research layers

- trajectory export
- optional RL/training-oriented components
- separate self-evolution repo

## 2.18 Advantages

Hermes has several real advantages:

### 1. Strong runtime completeness

It is unusually complete for an open agent runtime. Profiles, memory, skills, gateways, checkpoints, worktrees, automation, and providers all exist within one ecosystem.

### 2. Practical isolation ideas

Profiles, worktrees, and checkpoints are high-value runtime primitives.

### 3. Good skill/tool distinction

The distinction between skill and tool is clearer than in many other ecosystems.

### 4. Extensibility

Memory providers, plugins, and provider integrations make Hermes adaptable.

### 5. Persistence and continuity

Hermes treats sessions, identity, and memory as durable assets.

### 6. Operational breadth

It can serve as a bot, CLI assistant, automation runner, or coding environment.

### 7. Security awareness

Its docs at least acknowledge key runtime risks such as injection, dangerous commands, and credential leakage boundaries.

## 2.19 Disadvantages and Risks

Hermes also has serious disadvantages:

### 1. Complexity

It is a wide platform with many moving parts. Complexity can create brittleness, config friction, and harder debugging.

### 2. Governance ambiguity

Self-improving skills and persistent memory are powerful, but without strict promotion and trust controls they can undermine reliability.

### 3. Large mutable prompt/state surface

Persona, memory, skills, context files, plugins, and runtime state can all affect outcomes.

### 4. Uneven expectations

The phrase “self-improving” can raise expectations beyond what the actual system guarantees.

### 5. Potential authority leakage

Learned skills or persistent memory may shape output without the kind of explicit audit boundary AI ecosystem requires.

### 6. Broader attack surface

More integrations, platforms, providers, and plugin points mean more security and stability risk.

### 7. Single-runtime concentration

A large central orchestration engine can become a maintenance and reasoning bottleneck.

## 2.20 Key Insights Worth Extracting

The strongest Hermes insights are:

1. isolate runtime state by purpose
2. isolate risky work physically, not just by prompt
3. snapshot before mutation
4. keep subagent outputs compact and structured
5. prefer skills for reusable procedural behavior
6. keep provider resolution centralized
7. treat scheduled execution as a first-class feature
8. separate extension packs from the core runtime
9. progressive disclosure reduces prompt bloat
10. self-optimization belongs in a bounded pipeline, not the live runtime

## 2.21 What AI ecosystem Should Explicitly Reject

AI ecosystem should reject these Hermes-adjacent patterns:

### Unrestricted mutation of core governance artifacts

An agent must never be allowed to rewrite high-authority AI ecosystem artifacts automatically.

### Deep user modeling in authoritative delivery lanes

Operator preference memory should not silently shape code-delivery truth claims.

### “Self-improving” as a blanket trust signal

Optimization must be bounded, benchmarked, and reviewable.

### Capability without promotion controls

Skills, plugins, and candidate improvements must have explicit trust tiers.

---

# 3. AI ecosystem Context and Design Constraints

AI ecosystem is not a generic agent runtime. It is a governed artifact ecosystem centered on:

- constitution-level rules
- explicit authority hierarchy
- verification ownership
- agent scope boundaries
- controlled prompts / instructions / procedures / skills
- truth-over-helpfulness discipline

That means any Hermes-inspired enhancement must satisfy these constraints:

1. it must not blur authority boundaries
2. it must not let mutable memory become hidden policy
3. it must not let low-trust artifacts silently become high-trust artifacts
4. it must not move verification into persona or prompt folklore
5. it must remain auditable and reversible

---

# 4. Problem Statement

AI ecosystem already has strong epistemic governance, but it is comparatively weak in runtime mechanics.

Current pain points include:

- orchestrators may share too much mutable runtime context
- risky or exploratory work may happen in the main checkout
- auto-remediation is useful but insufficiently reversible
- subagent outputs can still pollute parent context
- skills are powerful but lack stronger trust-tier mechanics
- extension seams are present but could be cleaner and more modular
- approval logic is partially deterministic but not yet fully expressed as a first-class policy engine
- context/handoff compression can be improved
- there is no dedicated bounded self-optimization lab for low-authority artifacts

The result is a system that is strong on governance but still improvable on safe execution, isolation, and runtime ergonomics.

---

# 5. Product Vision

Create a **Hermes-informed AI ecosystem runtime layer** that improves:

- isolation
- reversibility
- capability packaging
- execution control
- handoff hygiene
- evaluation

while preserving:

- AI ecosystem’s explicit authority hierarchy
- single ownership of rules
- verification independence
- auditable artifact promotion
- refusal/silence/unknown as valid outcomes

---

# 6. Goals

## Functional goals

- Add isolated runtime lanes per orchestrator
- Support worktree-based risky or parallel execution
- Add automatic checkpoints before dangerous mutation
- Standardize subagent return schemas
- Add trust tiers and promotion flow for skills
- Add capability packs / plugin seams outside AI ecosystem core
- Introduce approval policy engine
- Add lineage-preserving handoff summaries
- Add separate optimization lab for low-authority assets

## Quality goals

- deterministic where safety matters
- reversible mutation
- explicit trust boundaries
- low context pollution
- no hidden authority upgrades
- easy auditability
- incremental adoption
- minimal disruption to existing AI ecosystem artifact taxonomy

---

# 7. Non-Goals

This project does **not** aim to:

- replace AI ecosystem with Hermes
- make AI ecosystem a generic messaging bot platform
- add broad social/chat integrations to core AI ecosystem
- add unrestricted self-editing of core instructions
- centralize all behavior in one monolithic runtime file
- replace existing verification gates with model judgment
- introduce operator-persona memory as a source of delivery truth
- add every Hermes feature just because it exists

---

# 8. Proposed Feature Set

## 8.1 Runtime Profiles for Orchestrator Isolation

### Summary

Introduce Hermes-style profile isolation, adapted for AI ecosystem orchestrators.

### Motivation

Feature, test, QA, and research orchestrators should not implicitly share one mutable state bucket.

### Requirement

Each orchestrator lane gets its own isolated runtime home containing:

- config
- state
- temporary runtime memory
- session lineage
- caches
- logs
- approvals
- optional tool visibility filters

### Example lanes

- `feature`
- `test`
- `qa`
- `research`
- `sparring`
- `candidate-optimization`

### Design rule

Profiles isolate runtime state. They do **not** define authority. Authority still comes from AI ecosystem artifacts.

## 8.2 Worktree Execution Lanes

### Summary

Introduce worktree-backed execution lanes for risky, parallel, or exploratory work.

### Use cases

- feature slice implementation in isolation
- contract review experiments
- test generation trials
- QA auto-remediation
- refactor prototypes
- branch-and-merge multi-agent workflows

### Requirements

- parent orchestrator can request a worktree lane
- worktree lane is tied to a branch and workflow id
- destructive or broad changes must prefer isolated lanes
- merge back requires passing configured gates
- cleanup policy is explicit

### Design rule

Physical isolation is preferred over “please stay in your lane” prompt text.

## 8.3 Checkpoint and Rollback Manager

### Summary

Add cheap checkpointing before dangerous or file-mutating operations.

### Trigger conditions

- file edits
- patch application
- auto-remediation attempts
- destructive shell commands
- batch doc propagation
- migration or config rewrite operations

### Requirements

- checkpoint metadata records workflow id, branch, orchestrator, reason, timestamp
- restore whole lane or single file
- diff preview supported
- checkpoint storage separate from canonical git history

### Design rule

Rollback must be procedural and deterministic, not agent-memory based.

## 8.4 Summary-Only Subagent Contract

### Summary

Standardize subagent outputs to prevent context bloat and leakage.

### Requirements

Subagents return only a normalized summary object:

- `finding_id`
- `category`
- `severity`
- `confidence`
- `evidence`
- `impacted_artifacts`
- `recommended_action`
- `needs_human_decision`
- `status`

### Rules

- no raw transcripts
- no full tool chatter
- no uncontrolled notes dump
- no speculative authority claims without evidence references

### Value

This keeps parent orchestrators small and makes synthesis auditable.

## 8.5 Trust-Tiered Skill System

### Summary

Introduce promotion tiers for skills.

### Proposed tiers

- `core`
- `curated`
- `optional`
- `candidate`
- `deprecated`
- `blocked`

### Rules by tier

#### core

- high authority
- manually maintained
- reviewed
- versioned
- cannot be auto-modified

#### curated

- approved for use
- lower authority than core
- reviewed and benchmarked
- promotion required for entry

#### optional

- installable capability packs
- not core, but allowed
- may have narrower trust scope

#### candidate

- draft / generated / experimental
- can be produced by optimization pipelines
- human review required before promotion

#### deprecated

- still recognized
- discouraged
- migration path should exist

#### blocked

- never load
- known bad or unsafe

### Metadata additions

Each skill should declare:

- trust tier
- owner
- source provenance
- applicability conditions
- required tools
- stop conditions
- evaluation status
- last review date
- promotion history

## 8.6 Capability Packs / Plugin Seams

### Summary

Separate optional domain capabilities from AI ecosystem core.

### Examples

- `AI ecosystem-security-pack`
- `AI ecosystem-frontend-pack`
- `AI ecosystem-finance-pack`
- `AI ecosystem-backstage-pack`
- `AI ecosystem-python-pack`

### Requirements

- capability packs must not override constitution-level rules
- packs may add skills, templates, prompts, and helper procedures
- packs must declare compatibility and trust level
- packs may be enabled per repository or per profile

### Value

Prevents core AI ecosystem from becoming bloated while enabling strong domain specialization.

## 8.7 Approval Policy Engine

### Summary

Promote command approval from ad hoc hook behavior to a first-class policy engine.

### Policy outputs

- `allow`
- `ask`
- `deny`

### Input dimensions

- orchestrator
- profile
- command class
- path scope
- worktree status
- repo trust level
- current phase
- user override
- prior approval memory for safe classes

### Command classes

- read-only
- local mutation
- destructive mutation
- networked mutation
- package install
- git history rewrite
- test/lint/type-check
- deployment / external side effects

### Design rule

Deterministic rules first. Optional learned/smart approval only for borderline `ask` decisions.

## 8.8 Context Compression and Handoff Summaries

### Summary

Add explicit lineage-preserving compression for long orchestrations.

### Requirements

- compress only from bounded source artifacts
- preserve decision lineage
- retain unresolved risks
- retain open findings
- retain acceptance coverage status
- retain rollback anchors
- never compress away blocking evidence

### Handoff artifact

Create standardized handoff summaries between:

- research → feature
- feature → test
- test → QA
- QA → remediation
- optimization lab → human reviewer

## 8.9 Self-Optimization Lab for Low-Authority Assets

### Summary

Create a separate repo or isolated folder/pipeline for optimizing low-authority assets using evaluation loops.

### Allowed optimization targets

- low-authority prompts
- candidate skills
- tool descriptions
- summaries / rubrics
- packaging metadata

### Forbidden targets

- constitution
- verification checklist
- core agent authority files
- promotion policy
- hook safety policy
- canonical core skills

### Required gates

- benchmark task suite
- regression comparison
- semantic-intent preservation check
- human review before promotion
- changelog and rollback support

## 8.10 Evaluation Harness for Runtime Changes

### Summary

Every runtime enhancement must ship with evals.

### Evaluation classes

- code-based graders
- model-based graders
- human spot-review

### Benchmark themes

- context pollution
- rollback correctness
- worktree isolation
- command approval accuracy
- skill trust-tier enforcement
- handoff completeness
- subagent summary quality
- remediation recovery rate

---

# 9. Detailed Requirements

## R1. Runtime profile isolation

The system shall support per-orchestrator runtime homes with isolated state and logs.

## R2. Worktree binding

The system shall support creating, naming, tracking, and destroying worktree-backed execution lanes.

## R3. Checkpoint manager

The system shall create checkpoints before dangerous mutation and allow rollback by id.

## R4. Summary contract enforcement

The system shall reject subagent outputs that do not conform to the normalized findings schema.

## R5. Skill trust tiers

The system shall store and enforce trust-tier metadata for all skills.

## R6. Promotion workflow

The system shall support promotion from candidate → curated and curated → core through explicit review.

## R7. Approval engine

The system shall classify commands using deterministic rules and phase-aware policy.

## R8. Handoff summaries

The system shall generate lineage-preserving handoff documents between orchestrators.

## R9. Optimization lab isolation

The system shall isolate self-optimization workflows from canonical governance files.

## R10. Auditability

The system shall persist enough metadata to reconstruct who changed what, in which lane, under which policy, and with which checkpoint.

---

# 10. Architecture Design

## 10.1 High-Level Design

```text
User / Prompt / Orchestrator
    -> AI ecosystem Artifact Authority Layer
    -> Runtime Profile Resolver
    -> Worktree Lane Manager
    -> Checkpoint Manager
    -> Approval Policy Engine
    -> Worker Agent / Subagent
    -> Summary Normalizer
    -> Verification / Eval Layer
    -> Promotion / Finalization
```

## 10.2 Authority Model

Authority remains unchanged:

1. constitution
2. verification checklist / always-on enforcement
3. instructions
4. agent definitions
5. prompts
6. templates
7. context
8. candidate/generated runtime artifacts

Runtime enhancements must fit under that model, never replace it.

## 10.3 Runtime State Separation

### Canonical artifacts

Governance files under `.github/` or equivalent canonical locations.

### Runtime artifacts

Ephemeral or operational files under `runtime/`, `state/`, `checkpoints/`, `handoffs/`, `logs/`.

### Promotion boundary

No runtime artifact becomes canonical automatically.

---

# 11. File and Directory Layout

Suggested layout:

```text
.github/
├── copilot-instructions.md
├── instructions/
├── agents/
├── prompts/
├── procedures/
├── templates/
├── skills/
│   ├── core/
│   ├── curated/
│   ├── optional/
│   ├── candidate/
│   ├── deprecated/
│   └── blocked/
├── packs/
│   ├── AI ecosystem-security-pack/
│   ├── AI ecosystem-frontend-pack/
│   └── AI ecosystem-finance-pack/
├── runtime/
│   ├── profiles/
│   │   ├── feature/
│   │   ├── test/
│   │   ├── qa/
│   │   ├── research/
│   │   └── sparring/
│   ├── worktrees/
│   ├── checkpoints/
│   ├── handoffs/
│   ├── logs/
│   ├── state/
│   └── evals/
└── optimization-lab/
    ├── candidate-prompts/
    ├── candidate-skills/
    ├── eval-datasets/
    ├── benchmark-results/
    └── promotion-reports/
```

---

# 12. Orchestrator Changes

## 12.1 Feature Orchestrator

### Additions

- profile binding: `feature`
- worktree spawn for risky slices
- checkpoint before mutation
- summary-only subagent consumption
- handoff summary generation for test orchestrator

### Recommended triggers for isolated lane

- more than N files expected to change
- refactor crossing package boundaries
- schema or public contract changes
- migration generation
- high remediation risk

## 12.2 Test Orchestrator

### Additions

- profile binding: `test`
- optional separate worktree for generated tests
- checkpoint before healing iterations
- structured test-gap handoff to QA

## 12.3 QA Orchestrator

### Additions

- profile binding: `qa`
- checkpoint before auto-remediation
- approval engine integration for risky fixes
- structured final report with remediation lineage

## 12.4 Research Orchestrator

### Additions

- profile binding: `research`
- explicit handoff artifact to feature orchestrator
- optional compression summaries for long analysis chains

## 12.5 Sparring Orchestrator

### Additions

- profile binding: `sparring`
- strict summary-only return contract
- zero write access
- ability to run in shared repo or isolated snapshot mode

---

# 13. Skill System Changes

## 13.1 Skill metadata schema

Each skill must include:

```yaml
name:
trust_tier:
owner:
provenance:
status:
applicability:
required_tools:
forbidden_tools:
stop_conditions:
output_contract:
evaluation_status:
last_reviewed:
promotion_history:
```

## 13.2 Skill loading policy

- `core`: always eligible
- `curated`: eligible if relevant
- `optional`: eligible if pack enabled
- `candidate`: never auto-loaded in authoritative lanes
- `deprecated`: only with explicit fallback
- `blocked`: never load

## 13.3 Candidate skill workflow

1. generated or authored in candidate lane
2. evaluated on benchmark set
3. reviewed by human
4. promoted or rejected
5. promotion report stored

---

# 14. Hook and Procedure Changes

## 14.1 Pre-tool hook

- classify command
- consult approval engine
- enforce deny/ask/allow
- optionally trigger checkpoint if command mutates files

## 14.2 Post-tool hook

- update lane state
- attach checkpoint id if created
- record changed files
- update handoff evidence
- optionally auto-format if policy allows

## 14.3 New procedures

### `runtime-profile.initialize.procedure.md`

Sets up the correct profile lane.

### `worktree.spawn.procedure.md`

Creates isolated worktree and binds metadata.

### `checkpoint.create.procedure.md`

Creates checkpoint with reason and lane metadata.

### `handoff.summarize.procedure.md`

Builds bounded lineage-preserving summary.

### `skill.promote.procedure.md`

Formal promotion path for candidate/curated/core.

### `optimization.evaluate.procedure.md`

Runs candidate prompt/skill through eval harness.

---

# 15. Data Model

## 15.1 Lane state record

```json
{
  "workflow_id": "",
  "orchestrator": "",
  "profile": "",
  "branch": "",
  "worktree_path": "",
  "phase": "",
  "checkpoint_ids": [],
  "handoff_ids": [],
  "approval_events": [],
  "status": ""
}
```

## 15.2 Checkpoint record

```json
{
  "checkpoint_id": "",
  "workflow_id": "",
  "orchestrator": "",
  "profile": "",
  "branch": "",
  "worktree_path": "",
  "reason": "",
  "created_at": "",
  "changed_paths": []
}
```

## 15.3 Skill promotion record

```json
{
  "artifact_id": "",
  "from_tier": "",
  "to_tier": "",
  "requested_by": "",
  "reviewed_by": "",
  "benchmark_suite": "",
  "result": "",
  "notes": ""
}
```

---

# 16. Security and Governance

## 16.1 Hard rules

- core governance files are immutable to autonomous optimization
- candidate artifacts cannot auto-promote
- context-bearing runtime artifacts must be scanned before injection
- subagent summaries must cite evidence paths where applicable
- destructive operations require checkpoint and policy classification
- credentials remain scoped by lane and tool visibility rules

## 16.2 Governance boundaries

### High-authority

- constitution
- verification checklist
- canonical agent definitions
- canonical core skills
- promotion policy
- approval policy definitions

### Medium-authority

- curated skills
- reviewed prompts
- reviewed templates
- capability packs

### Low-authority

- runtime summaries
- candidate skills
- optimization outputs
- generated notes
- local temporary memory

## 16.3 Threat model

Major risks include:

- skill supply-chain compromise
- hidden authority upgrades via memory
- worktree merge contamination
- context poisoning through runtime artifacts
- unsafe command approval drift
- self-optimization overfitting or reward hacking

---

# 17. Migration Plan

## Phase 1 — Foundations

- add runtime profiles
- add checkpoint manager
- add summary schema
- add skill trust metadata

## Phase 2 — Safer execution

- add worktree lanes
- add approval policy engine
- update hooks/procedures

## Phase 3 — Better packaging

- add capability packs
- add promotion workflow
- add handoff summaries

## Phase 4 — Optimization lab

- create isolated optimization space
- add low-authority benchmark suite
- enable candidate generation and promotion reviews

---

# 18. Rollout Plan

## Milestone A

Implement profile directories and checkpoint system only.

## Milestone B

Enable worktree isolation for feature remediation and large slices.

## Milestone C

Enforce summary-only subagent returns.

## Milestone D

Add trust-tiered skills and promotion pipeline.

## Milestone E

Add approval policy engine.

## Milestone F

Stand up optimization lab for non-core artifacts.

---

# 19. Acceptance Criteria

## AC1

Each orchestrator can run with isolated runtime state and no unintended cross-contamination.

## AC2

Risky slices can run in isolated worktrees and be merged only after configured gates pass.

## AC3

Every destructive or file-mutating action can be rolled back from a recorded checkpoint.

## AC4

Subagent outputs are normalized and do not spam parent context with raw transcripts.

## AC5

Skills cannot silently move from candidate to authoritative use.

## AC6

Approval decisions are reproducible and policy-driven.

## AC7

Handoff summaries preserve unresolved blockers, evidence, and rollback lineage.

## AC8

Optimization workflows cannot mutate core governance artifacts.

## AC9

Benchmark/eval results demonstrate no regression in verification reliability.

---

# 20. Risks, Trade-Offs, and Failure Modes

## 20.1 More moving parts

Adding profiles, worktrees, checkpoints, and promotion paths increases system complexity.

### Mitigation

Keep each enhancement modular and adopt in phases.

## 20.2 Slower execution

Checkpoints, worktrees, and reviews add overhead.

### Mitigation

Apply only where risk justifies cost.

## 20.3 Metadata burden

Trust tiers and promotion records require discipline.

### Mitigation

Use templates and automation to generate boilerplate metadata.

## 20.4 False confidence

A more sophisticated runtime can create the illusion of correctness.

### Mitigation

Keep verification independent and benchmarked.

## 20.5 Optimization drift

Candidate optimization can overfit benchmarks.

### Mitigation

Use held-out tasks, semantic preservation checks, and human review.

---

# 21. Open Questions

1. Should worktrees be mandatory for all remediation loops or only for risky classes?
2. Should approval memory be global, per profile, or per repository?
3. Should curated skills be allowed in all authoritative lanes or only whitelisted orchestrators?
4. Should handoff summaries be stored in runtime only or optionally promoted to documentation artifacts?
5. How much runtime memory should be allowed in epistemic delivery lanes before it becomes hidden authority?
6. Should candidate optimization live in the same repository or a sibling repository?

---

# 22. Final Recommendation

Adopt Hermes-inspired runtime mechanics selectively.

## Do adopt

- isolated profiles
- worktree execution lanes
- checkpoints and rollback
- summary-only delegation
- skill/tool distinction
- trust-tiered skills
- plugin/capability seams
- phase-aware approval policies
- bounded optimization labs

## Do not adopt

- unconstrained self-editing of canonical AI ecosystem artifacts
- deep user modeling in authoritative delivery lanes
- “self-improving” as a trust shortcut
- broad runtime memory as hidden policy

## Final principle

Hermes is useful to AI ecosystem primarily as a source of **runtime engineering patterns**.

AI ecosystem should remain the source of **epistemic discipline and authority control**.

The correct synthesis is:

> Hermes for runtime isolation, reversibility, and packaging.  
> AI ecosystem for truth discipline, authority boundaries, and governed promotion.
