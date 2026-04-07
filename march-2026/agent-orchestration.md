# Feature Specification — AI Ecosystem Multi-Perspective Orchestration for GitHub Copilot in VS Code

## Document Control

- **Feature Name:** AI Ecosystem Multi-Perspective Orchestration
- **Short Name:** AI Ecosystem MPO
- **Status:** Proposed
- **Mode:** Epistemic
- **Primary Goal:** Add a minimal, AI Ecosystem-compatible way to orchestrate multiple bounded perspectives in Copilot Chat without reintroducing specialized-agent sprawl
- **Primary Audience:** AI Ecosystem maintainers, GitHub Copilot custom-agent authors, VS Code workflow designers

---

## 1. Summary

AI Ecosystem currently consolidates cognition into 3 broad agents and pushes specialized expertise into instructions, prompts, procedures, templates, and context artifacts. This feature adds a new orchestration capability that lets one AI Ecosystem coordinator agent invoke 2–4 bounded worker perspectives as Copilot subagents and then synthesize the result into one structured answer.

This feature is intended to capture the useful part of "party mode" while staying compatible with AI Ecosystem v3:

- keep the visible agent surface small
- avoid persona theater
- preserve single ownership per concern
- preserve strict authority separation
- support multi-perspective stress testing for planning, architecture, review, and tradeoff analysis

The result should feel like:

- one visible coordinator
- several narrowly scoped hidden helpers
- one final structured synthesis

It must not become:

- a return to 16+ specialized first-class agents
- freeform roleplay
- a mechanism for bypassing AI Ecosystem verification rules
- a vague "everyone talks" workflow without deterministic orchestration

---

## 2. Problem Statement

AI Ecosystem v3 deliberately reduced the maintenance burden by consolidating many specialized agents into 3 broad agents and moving expertise into instruction files. That solved maintenance and authority-sprawl problems, but it also removed an ergonomic pattern that can be useful in some tasks: explicit multi-perspective contention.

Current gap:

- AI Ecosystem can already do planning and review
- AI Ecosystem can already use instructions instead of specialist agents
- AI Ecosystem does not yet have a clean, reusable way to force structured disagreement across perspectives inside Copilot Chat

Example gap:

- "Should we keep the FastAPI backend as a modular monolith or split into services?"
- "Review this implementation plan from architecture, delivery, and security angles."
- "Challenge this feature specification with product, implementation, and operational concerns."

Today this can be approximated ad hoc in a prompt, but that is fragile and inconsistent.

---

## 3. Goals

### 3.1 Functional Goals

1. Provide a reusable orchestration pattern for multi-perspective analysis.
2. Keep the visible UX simple: one coordinator, one final structured answer.
3. Allow the coordinator to delegate to hidden worker agents as Copilot subagents.
4. Make the set of allowed worker agents explicit and bounded.
5. Support at least these use cases:
   - design tradeoffs
   - architecture review
   - feature-plan critique
   - implementation strategy critique
   - adversarial pre-implementation challenge
6. Produce outputs that distinguish:
   - perspective findings
   - agreements
   - disagreements
   - unresolved questions
   - recommended next step

### 3.2 AI Ecosystem Goals

1. Preserve the v3 consolidation principle.
2. Keep domain expertise in instructions, not in a growing roster of visible specialized agents.
3. Preserve authority flow:
   - constitution
   - instructions
   - agent
   - prompt
   - template
   - context
4. Ensure the feature can be introduced as:
   - a small number of `.agent.md` files
   - optional supporting instruction files
   - optional prompt file(s)
   - optional template file(s)

### 3.3 UX Goals

1. The user should invoke one visible agent or one prompt.
2. The worker agents should usually stay hidden from the picker.
3. The user should still be able to inspect subagent runs in Copilot Chat if desired.
4. The final answer should read like structured debate, not like an incoherent transcript.

---

## 4. Non-Goals

1. Recreating theatrical BMAD-style persona simulation.
2. Reintroducing many first-class specialized visible agents.
3. Creating a recursive subagent graph by default.
4. Using orchestration for implementation-by-default.
5. Replacing existing AI Ecosystem prompts, procedures, or verification with agent chatter.
6. Claiming runtime enforcement that does not exist.

---

## 5. User Stories

### 5.1 Planning

As a developer, I want one AI Ecosystem agent to challenge a feature idea from multiple angles so that I see the main tradeoffs before implementation begins.

### 5.2 Architecture

As a maintainer, I want architecture, implementation, and operational perspectives on a proposed change so that I can identify hidden coupling and delivery risk.

### 5.3 Review

As a reviewer, I want a coordinator to ask distinct worker perspectives for critique so that the final output contains explicit disagreements instead of one blended opinion.

### 5.4 AI Ecosystem Governance

As a AI Ecosystem maintainer, I want this capability implemented with minimal artifact sprawl so that it does not undermine the v3 consolidation.

---

## 6. Core Concept

The feature introduces one coordinator agent that runs a bounded set of hidden worker agents as Copilot subagents.

The coordinator:

- is visible to the user
- chooses the relevant perspectives
- delegates isolated subtasks
- collects results
- renders the final structured answer

The workers:

- are not normally visible in the picker
- each have a narrow concern
- do not own global rules
- return compact findings only

This is a coordination pattern, not a new ontology for AI Ecosystem.

---

## 7. Scope

### In Scope

- coordinator custom agent
- 2–4 worker custom agents
- optional AI Ecosystem instructions for orchestration behavior
- optional prompt for feature-spec or strategy use
- examples for Copilot Chat usage
- explicit output format
- acceptance criteria

### Out of Scope

- automatic CI enforcement
- dynamic worker creation at runtime
- freeform multi-agent conversation transcript generation
- deep recursive nesting
- replacing the 3 broad AI Ecosystem agents with many specialist visible agents

---

## 8. Proposed Architecture

## 8.1 Recommended AI Ecosystem Placement

Minimal recommended artifact set:

- `.github/agents/multi-perspective-coordinator.agent.md`
- `.github/agents/architecture-lens.agent.md`
- `.github/agents/implementation-lens.agent.md`
- `.github/agents/operations-lens.agent.md` (optional)
- `.github/instructions/multi-perspective-review.instructions.md`
- `.github/prompts/generate-multi-perspective-analysis.prompt.md` (optional)
- `.github/templates/multi-perspective-analysis.template.md` (optional)

### Why this shape

- coordinator and worker invocation behavior belongs in agent files
- reusable orchestration heuristics belong in an instruction file
- task wiring belongs in a prompt file
- response structure belongs in a template file

This keeps single ownership intact.

---

## 8.2 High-Level Flow

    User request
      → prompt or direct coordinator invocation
        → coordinator agent
          → selects 2–4 relevant worker agents
            → worker subagents perform isolated analysis
              → worker results returned to coordinator
                → coordinator synthesis
                  → final structured answer

---

## 8.3 Copilot-Specific Behavior

Expected Copilot behavior:

- the main visible agent uses the `agent` tool
- the coordinator restricts allowed subagents using `agents: [...]`
- worker agents use `user-invocable: false` so they remain subagent-only
- subagent calls appear in Copilot Chat as collapsible tool calls
- users can expand them to inspect details if needed

This means the visible experience is:

- one user message
- one coordinator response
- optional visible subagent call blocks in the chat timeline

---

## 9. Design Constraints

1. Must fit AI Ecosystem v3’s small visible-agent philosophy.
2. Must not duplicate verification logic into agent files.
3. Must not place output structure rules into worker agents if a template exists.
4. Must not place global epistemic rules into local orchestration files.
5. Must allow "Unknown" and abstention when evidence is missing.
6. Must not silently invent repo-specific claims.
7. Must be usable in read-only planning mode.

---

## 10. Required Behavior

## 10.1 Coordinator Behavior

The coordinator shall:

1. Decide whether multi-perspective orchestration is actually needed.
2. Avoid spawning workers for trivial or single-perspective tasks.
3. Select 2–4 relevant workers based on the request.
4. Pass each worker a narrow subtask.
5. Ask each worker for a compact, bounded response.
6. Merge results into a structured final answer.
7. Surface agreements, disagreements, unknowns, and next actions.
8. Refuse to treat worker outputs as verified facts if evidence is absent.

## 10.2 Worker Behavior

Each worker shall:

1. Focus only on its own concern.
2. Return concise analysis, not implementation steps unless asked.
3. Avoid making claims outside the provided evidence.
4. Mark assumptions explicitly.
5. Return findings in a stable shape so the coordinator can synthesize reliably.

## 10.3 Output Behavior

The final response shall contain:

- selected perspectives
- perspective findings
- agreements
- disagreements
- unresolved questions
- recommendation
- confidence / evidence status

---

## 11. Recommended Perspective Set

Minimal default set:

1. Architecture Lens
2. Implementation Lens

Recommended practical set:

1. Architecture Lens
2. Implementation Lens
3. Operations Lens

Optional future lenses:

- Security Lens
- Product Lens
- Test Strategy Lens
- Performance Lens
- Migration Lens

Important AI Ecosystem rule:

These are perspectives, not first-class domain empires.

They should stay small and bounded.

---

## 12. File-Level Responsibilities

| Artifact                                        | Responsibility                                                      | Must Not Own                                          |
| ----------------------------------------------- | ------------------------------------------------------------------- | ----------------------------------------------------- |
| `multi-perspective-coordinator.agent.md`        | delegation policy, worker selection, synthesis contract             | global epistemic policy, verification checklist logic |
| `*-lens.agent.md`                               | narrow perspective reasoning                                        | templates, enforcement, global rules                  |
| `multi-perspective-review.instructions.md`      | reusable orchestration heuristics, selection rules, synthesis rules | tool restrictions, global rules                       |
| `generate-multi-perspective-analysis.prompt.md` | task wiring, output mode, evidence scope, file references           | enforcement, agent cognition                          |
| `multi-perspective-analysis.template.md`        | headings and placeholders                                           | steps, policy, correctness logic                      |

---

## 13. Minimal Implementation Plan

## Phase 1 — Minimal Read-Only Version

Deliver:

- 1 visible coordinator
- 2 hidden workers
- no prompt file
- no dedicated template
- direct chat usage only

Goal:

Prove the orchestration works in Copilot Chat.

Suggested workers:

- Architecture Lens
- Implementation Lens

## Phase 2 — AI Ecosystem-Native Integration

Deliver:

- orchestration instruction file
- optional prompt file
- optional template file
- optional third worker

Goal:

Make the feature reusable and consistent across tasks.

## Phase 3 — Targeted Expansion

Deliver only if Phase 2 proves useful:

- operations lens
- security lens
- explicit feature-spec prompt wiring

Goal:

Expand only where a clear reuse case exists.

---

## 14. Agent File Examples

These are illustrative examples, not the only valid wording.

## 14.1 Coordinator Agent

    ---
    name: Multi-Perspective Coordinator
    description: Orchestrates bounded AI Ecosystem perspectives and synthesizes the result
    tools: ['agent', 'read', 'search']
    agents: ['Architecture Lens', 'Implementation Lens', 'Operations Lens']
    ---

    You are a coordinator agent for AI Ecosystem.

    Purpose:
    - run bounded perspective analysis when the task benefits from structured disagreement
    - keep the visible UX simple
    - synthesize one final answer

    Rules:
    - do not use subagents for trivial tasks
    - select only 2-4 relevant perspectives
    - ask each worker for:
      - position
      - biggest risk
      - recommendation
      - unknowns / assumptions
    - synthesize into:
      - perspectives used
      - agreements
      - disagreements
      - unresolved questions
      - recommendation
      - confidence / evidence status

    Constraints:
    - do not invent repository facts
    - do not treat worker output as automatically verified
    - preserve AI Ecosystem truth-first behavior
    - do not roleplay
    - do not output raw worker transcripts unless explicitly requested

## 14.2 Architecture Lens Worker

    ---
    name: Architecture Lens
    description: Evaluates boundaries, coupling, extraction seams, and long-term maintainability
    user-invocable: false
    tools: ['read', 'search']
    ---

    Evaluate the task only from an architecture perspective.

    Return:
    - Position:
    - Biggest risk:
    - Recommendation:
    - Unknowns / assumptions:

    Stay narrow. Do not discuss implementation details unless they directly affect architecture.

## 14.3 Implementation Lens Worker

    ---
    name: Implementation Lens
    description: Evaluates implementation complexity, delivery risk, and local maintainability
    user-invocable: false
    tools: ['read', 'search']
    ---

    Evaluate the task only from an implementation perspective.

    Return:
    - Position:
    - Biggest risk:
    - Recommendation:
    - Unknowns / assumptions:

    Stay narrow. Do not generalize into architecture unless required by the evidence.

## 14.4 Operations Lens Worker

    ---
    name: Operations Lens
    description: Evaluates operational complexity, deployment risk, observability, and support burden
    user-invocable: false
    tools: ['read', 'search']
    ---

    Evaluate the task only from an operations perspective.

    Return:
    - Position:
    - Biggest risk:
    - Recommendation:
    - Unknowns / assumptions:

    Stay narrow. Focus on runtime complexity and maintenance burden.

---

## 15. Optional AI Ecosystem Instruction File Example

    ---
    applyTo: '**'
    description: Rules for AI Ecosystem multi-perspective orchestration
    ---

    # Multi-Perspective Review

    Use this only when the task benefits from structured disagreement or bounded multi-angle analysis.

    ## When to Use
    - architecture tradeoffs
    - feature strategy review
    - implementation plan critique
    - pre-implementation risk surfacing

    ## When NOT to Use
    - trivial tasks
    - direct code edits
    - pure summarization
    - tasks with a clearly single-perspective answer

    ## Perspective Selection Rules
    - prefer 2 perspectives by default
    - use 3 when the tradeoff is high impact
    - use 4 only when the added perspective changes the likely decision
    - avoid perspective inflation

    ## Synthesis Rules
    The final answer must separate:
    - what perspectives agree on
    - where they disagree
    - what is unknown
    - what should happen next

    ## Epistemic Rules
    - unknown is a valid result
    - assumptions must be labeled
    - no repo-specific fact may be asserted without evidence

---

## 16. Optional Prompt File Example

    ---
    name: generate-multi-perspective-analysis
    description: Run AI Ecosystem multi-perspective analysis on a planning or design question
    tools: ['agent', 'read', 'search']
    ---

    Use the Multi-Perspective Coordinator.

    Task:
    Analyze the provided problem from multiple bounded perspectives.

    Scope:
    - use only the provided files and explicitly referenced context
    - mark unknowns explicitly
    - do not infer missing repository facts

    Output:
    Use the multi-perspective analysis structure.

    Stop Conditions:
    - if the required evidence is missing and the answer would otherwise rely on invention
    - if the user request is too broad to ground
    - if the task is actually trivial and does not need orchestration

---

## 17. Optional Template Example

    # Multi-Perspective Analysis

    ## 1. Request Summary

    ## 2. Perspectives Used

    ## 3. Perspective Findings

    ### 3.1 Architecture Lens

    ### 3.2 Implementation Lens

    ### 3.3 Operations Lens

    ## 4. Agreements

    ## 5. Disagreements

    ## 6. Unknowns and Assumptions

    ## 7. Recommendation

    ## 8. Suggested Next Step

---

## 18. Example User Flows

## 18.1 Direct Agent Invocation

User:

    @Multi-Perspective Coordinator
    We have a FastAPI backend and React frontend.
    Should our MVP remain a modular monolith or move to microservices?
    Use architecture and implementation perspectives.

Expected internal behavior:

1. coordinator recognizes multi-perspective analysis is appropriate
2. coordinator invokes Architecture Lens and Implementation Lens
3. workers return compact findings
4. coordinator synthesizes

Expected final response shape:

    Perspectives Used:
    - Architecture Lens
    - Implementation Lens

    Architecture Lens:
    Position: Prefer a modular monolith.
    Biggest risk: Premature service split may increase interface and deployment complexity.
    Recommendation: Preserve extraction seams now, split later only if evidence demands it.
    Unknowns / assumptions: Current scalability bottlenecks are not evidenced.

    Implementation Lens:
    Position: Prefer a modular monolith for the MVP.
    Biggest risk: Microservices would likely slow delivery.
    Recommendation: Keep one deployable unit and enforce module boundaries.
    Unknowns / assumptions: Existing deployment pain is not yet evidenced.

    Agreements:
    - Start with a modular monolith
    - Keep extraction seams explicit

    Disagreements:
    - None material

    Recommendation:
    Stay with a modular monolith for the MVP and document service extraction boundaries now.

## 18.2 Feature Specification Critique

User:

    @Multi-Perspective Coordinator
    Review this feature plan from architecture, implementation, and operations perspectives.
    Focus on hidden coupling, delivery risk, and runtime burden.

Expected result:

- 3 worker runs
- one coordinator synthesis
- clear separation between agreement, disagreement, and unknowns

---

## 19. Example Copilot Chat UX

What the user is likely to see in Copilot Chat:

    You:
    Review this plan from architecture and implementation perspectives.

    Copilot:
    [Subagent: Architecture Lens] Searching codebase...
    [Subagent: Implementation Lens] Reading files...

    Perspectives Used:
    - Architecture Lens
    - Implementation Lens

    Architecture Lens:
    ...

    Implementation Lens:
    ...

    Agreements:
    ...

    Disagreements:
    ...

    Recommendation:
    ...

Important note:

The "party" effect is created by the coordinator’s output formatting and synthesis logic, not by a literal many-speaker chat room.

---

## 20. Acceptance Criteria

## 20.1 Functional Acceptance

1. A user can select one visible coordinator agent in Copilot Chat.
2. The coordinator can invoke at least 2 worker agents as subagents.
3. Worker agents are hidden from the normal picker.
4. The coordinator restricts allowed subagents explicitly.
5. The final answer includes:
   - perspectives used
   - each perspective’s findings
   - agreements
   - disagreements
   - recommendation
   - unknowns / assumptions
6. The output remains coherent when only 2 perspectives are used.

## 20.2 AI Ecosystem Acceptance

1. No global epistemic rules are duplicated into local orchestration files.
2. No verification-checklist logic is moved into worker agents.
3. The feature does not increase the visible AI Ecosystem first-class agent surface beyond what is justified.
4. Perspective expertise remains narrow and composable.
5. Unknown remains an allowed output.

## 20.3 UX Acceptance

1. Subagent runs are inspectable in Copilot Chat.
2. The default user experience is still one visible coordinator.
3. The final output is more useful than a plain blended answer for design-tradeoff tasks.

---

## 21. Failure Modes and Mitigations

| Failure Mode                               | Risk                        | Mitigation                                         |
| ------------------------------------------ | --------------------------- | -------------------------------------------------- |
| Too many worker agents                     | noise, maintenance, drift   | hard-cap default at 2–3 workers                    |
| Workers become mini-empires                | AI Ecosystem sprawl returns | keep workers narrow and hidden                     |
| Coordinator overuses subagents             | latency, complexity         | define "when NOT to use" clearly                   |
| Perspectives collapse into the same answer | wasted orchestration        | give each worker a sharply bounded concern         |
| Worker outputs treated as verified facts   | false confidence            | coordinator must preserve evidence status          |
| Roleplay takes over                        | style over substance        | forbid persona theater in coordinator instructions |
| Local files duplicate global rules         | authority drift             | enforce single ownership during review             |

---

## 22. Tradeoffs

### Benefits

- better structured disagreement
- better surfacing of tradeoffs
- useful for planning without premature implementation
- AI Ecosystem-compatible if kept minimal

### Costs

- added setup complexity
- more files than a single prompt
- possible overuse on tasks that do not need orchestration
- still no hard runtime enforcement

---

## 23. Recommendation

Implement this feature in the smallest viable AI Ecosystem shape:

- 1 visible coordinator agent
- 2 hidden workers initially
- 1 optional instruction file after proving the pattern useful
- no dedicated procedure unless repeated step logic becomes substantial

Start with:

- Architecture Lens
- Implementation Lens

Add Operations Lens only if it demonstrably changes decisions in real tasks.

Do not start with a large worker roster.

---

## 24. Explicit Decisions

1. This feature is a coordination pattern, not a return to specialized-agent sprawl.
2. The visible surface should remain small.
3. The coordinator owns orchestration and synthesis.
4. Workers own only bounded perspective reasoning.
5. AI Ecosystem authority and verification remain where they already belong.

---

## 25. Open Questions

1. Should this be exposed primarily as:
   - a visible coordinator agent
   - a prompt
   - or both?
2. Should the first AI Ecosystem-native version include an operations lens immediately or defer it?
3. Should there be a dedicated template for multi-perspective analysis, or should the coordinator render directly?
4. Should this feature remain read-only only, or later support a follow-up handoff into implementation?

---

## 26. Suggested First Cut

If you want the smallest credible implementation, build exactly this:

- `multi-perspective-coordinator.agent.md`
- `architecture-lens.agent.md`
- `implementation-lens.agent.md`

Then test with these prompts:

1. "Should we keep a modular monolith or split into services?"
2. "Challenge this implementation plan from architecture and implementation perspectives."
3. "Review this feature spec for hidden coupling and delivery risk."

If those three feel useful, only then add:

- `multi-perspective-review.instructions.md`
- `operations-lens.agent.md`

That is the lowest-risk path.
