Specification: CLASP Ecosystem Restructuring (LLM-First Architecture)

1. Architectural Transition Objectives

This specification dictates the mandatory transition from the "Specialized Specialist" model—a fragmented architecture of granular, single-purpose agents—to a high-density "Orchestration Quad" model. This shift is necessitated by the emergence of native sub-agent orchestration within Visual Studio Code and the Copilot CLI. By moving to a multi-agent framework (Orchestrator, Planner, Designer, and Coder), we effectively eliminate "multi-agent pileup" and context fragmentation. This architecture leverages isolated context windows to ensure Specialist reasoning does not pollute the primary session, as evidenced by system benchmarks showing 2,700 lines of code implemented using only 10.8K tokens of the main context window.

LLM-First Principles

* Cognitive Lane Isolation: Sub-agents operate within isolated workspaces powered by Git Worktrees, preventing background tasks from colliding with the local working directory.
* Parallel Execution: The Orchestrator is now authorized to dispatch multiple sub-agents (e.g., parallelizing the Coder across discrete chunks) to significantly reduce wait times for complex initiatives.
* Model Specialization: We utilize Claude Sonnet 4.5 for high-agency orchestration ("The Labrador") while delegating technical execution to GPT-4o Codex and UI/UX reasoning to Gemini 1.5 Pro.


--------------------------------------------------------------------------------


2. Agent Deprecation Manifest

The following entities are hereby deprecated. Their authorized domains and reasoning postures must be extracted into monolithic .instructions.md or .procedure.md files before the source files are purged.

Obsolete Entity	Specific Logic to Extract (Institutional Memory)
Agent Router	Intent classification and task-brief generation logic.
Test Architect	"Test Pyramid" strategy and "Contract Boundary" logic.
Test Engineer	AAA (Arrange-Act-Assert) implementation patterns.
Tech Debt Analyst	"Hotspot Mapping" and "Impact Analysis" reasoning.
Tech Debt Resolver	Staged remediation planning and incremental migration logic.
Strategy Analyst	Roadmapping, prioritization, and platform trade-off analysis.
Feature Engineer	Requirement decomposition and acceptance criteria generation.
Code Analyst	Control Flow Tracing and Data Flow Analysis logic.
Tech Writer	README/ADR/Runbook structure and documentation synthesis logic.


--------------------------------------------------------------------------------


3. Core Orchestration Quad Definition

Orchestrator (The Labrador)

* Primary Model: Claude Sonnet 4.5
* Cognitive Stance: Technical Project Manager (TPM).
* Responsibility: Acts as the high-agency entry point. It manages the mission control interface, delegates to sub-agents, and synthesizes results.
* Hard Constraint: The Orchestrator must not provide line-level implementation instructions to sub-agents. It coordinates "what" to do, but must never micro-manage the "how."

Planner (The Architect)

* Primary Model: GPT-4o
* Cognitive Stance: Solution Architect.
* Responsibility: Performs high-level blueprinting and multi-step reasoning.
* Hard Constraint: The Planner does not write code. Its primary output is a detailed .blueprint.md document passed to the Coder agent.

Designer (The UI/UX Specialist)

* Primary Model: Gemini 1.5 Pro
* Cognitive Stance: Creative Lead.
* Responsibility: Handles all UI/UX, styling, and design system aesthetics.
* Hard Constraint: Possesses full creative autonomy; the Orchestrator must not override its design decisions.

Coder (The Implementer)

* Primary Model: GPT-4o Codex
* Cognitive Stance: Lead Software Engineer.
* Responsibility: Focuses on technical implementation and doc reading via MCP (Context 7).
* Hard Constraint: Instructed to "Question Everything" received from the Orchestrator. It operates in an isolated Git Worktree to ensure environment integrity.


--------------------------------------------------------------------------------


4. Workflow Consolidation & Mapping

The procedural logic from deprecated agents is reassigned to the Quad as follows:

1. Strategy & Features: Strategy Analyst and Feature Engineer logic is absorbed into the Planner workflow for initiative decomposition.
2. Analysis & Review: Code Analyst and Tech Writer logic is transitioned to Coder on-demand skills. Technical documentation is now a post-implementation synthesis step by the Coder.
3. Engineering & Debt: Test Engineer and Tech Debt Resolver logic are consolidated into the Coder agent as specialized procedural skills.
4. Routing Logic Update: The Agent Router is to be deleted. Its intent classification logic is replaced by the Orchestrator’s native intent-to-sub-agent routing.


--------------------------------------------------------------------------------


5. Migration to Monolithic On-Demand Skills

Specialized procedural knowledge is migrated to the .github/instructions/ directory to prevent context bloat.

Skill Transformation Protocol

1. Extract technical steps from test-architect.agent.md and tech-debt-analyst.agent.md.
2. Migrate all .procedure.md files (e.g., tech-debt-review.procedure.md) to the new .github/instructions/ directory.
3. Rewrite instructions to focus on mechanical procedures, stripping away all persona-based language.

Skill Invocation Instructions Sub-agents will no longer use @agent calls (which trigger agent hallucinations). Instead, specialists must be invoked via:

* Slash Commands: Use /test-aaa-pattern or /tech-debt-review for specific workflows.
* File Referencing: Explicitly reference instruction files (e.g., #test-strategy.instructions.md) to ground the Coder's implementation.


--------------------------------------------------------------------------------


6. File System Deletion & Cleanup Instructions

Targeted Deletion Commands The following file paths must be removed to eliminate cognitive drift:

* .github/agents/agent-router.agent.md
* .github/agents/test-architect.agent.md
* .github/agents/test-engineer.agent.md
* .github/agents/tech-debt-analyst.agent.md
* .github/agents/tech-debt-resolver.agent.md
* .github/agents/strategy-analyst.agent.md
* .github/agents/feature-engineer.agent.md
* .github/agents/code-analyst.agent.md
* .github/agents/tech-writer.agent.md

Context Pointer Update Update context-pointers.md and clasp-system-context.md to:

1. Purge all references to the nine obsolete specialist agents.
2. Register the Orchestration Quad hierarchy.
3. Map the new .instructions.md and .procedure.md paths in .github/instructions/.


--------------------------------------------------------------------------------


7. Governance & Verification (The New CLASP)

Epistemic Safeguards The CLASP constitution remains supreme: Truth > Helpfulness > Speed.

* "Unknown" is the mandatory response when evidence is missing.
* Agents must explicitly surface uncertainty to the Orchestrator rather than fabricating connective tissue.

Final Verification Checklist The VS Code agent must execute the following checks post-restructuring:

* [ ] Orchestration Handover: Verify Orchestrator (Sonnet 4.5) correctly delegates to Planner (GPT-4o).
* [ ] Context Isolation: Confirm Coder (Codex) utilizes Git Worktrees for implementation.
* [ ] Skill Invocation: Confirm Coder uses Slash Commands or # referencing for testing logic without calling deprecated agents.
* [ ] Reference Integrity: Ensure no remaining .agent.md, .prompt.md, or .template.md files contain pointers to the deleted specialists.
* [ ] Procedural Continuity: Confirm tech-debt-review.procedure.md is accessible in the new /instructions/ path.
