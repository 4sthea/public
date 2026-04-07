# Feature Specification — AI Ecosystem Advanced Elicitation Integration

## Document Control

- **Document Type:** Feature Specification
- **Status:** Proposed
- **Mode:** Epistemic
- **Target System:** AI Ecosystem ecosystem in VS Code with GitHub Copilot
- **Feature Name:** Advanced Elicitation Integration
- **Short Name:** AEI
- **Primary Objective:** Enhance AI Ecosystem’s existing multi-perspective orchestration and thinking workflow with structured second-pass critique using named elicitation methods
- **Intended Audience:** AI Ecosystem maintainers, prompt/agent authors, workflow designers
- **Primary Beneficiaries:** `thinking-assistant`, `sparring-orchestrator`, and any workflow that currently produces a synthesized recommendation

---

## 1. Summary

This feature adds a AI Ecosystem-native advanced elicitation capability to improve the quality, depth, and robustness of idea evaluation, planning, architecture analysis, and strategy synthesis.

The enhancement introduces a structured post-synthesis critique stage that applies one or more named elicitation methods to an already-generated answer, recommendation, or synthesis.

The feature is intended to:

- improve the `thinking-assistant`
- improve the existing multi-perspective orchestration flow
- surface hidden assumptions
- challenge premature conclusions
- improve tradeoff analysis
- improve failure-mode discovery
- reduce shallow “first plausible answer” lock-in

This feature must remain compatible with AI Ecosystem’s current architecture:

- small visible agent surface
- broad agents rather than many narrow agents
- instructions over specialized-agent sprawl
- procedures and skills for reusable workflows
- bounded reasoning with explicit uncertainty
- explicit stop conditions and explicit unknowns

This feature is not intended to create a new family of permanent “thinking lenses” as separate agents.

Instead, it introduces one reusable capability that can be invoked:

- inside `thinking-assistant`
- after synthesis in `sparring-orchestrator`
- optionally in other AI Ecosystem workflows that benefit from deeper second-pass reasoning

---

## 2. Problem Statement

AI Ecosystem’s current multi-perspective orchestration already works well by combining perspectives from multiple agents or subagents and synthesizing the result into a coherent recommendation.

However, even a well-synthesized result can still have weaknesses:

- hidden assumptions remain unchallenged
- the recommendation may converge too quickly
- tradeoffs may remain implicit rather than explicit
- risks may be underexplored
- stakeholder conflict may remain unmodeled
- failure modes may not be surfaced
- a plausible synthesis may be mistaken for a robust one

The current system is good at:

- breadth across perspectives
- structured comparison
- synthesis across viewpoints

The current system is weaker at:

- deliberately attacking the synthesis itself from a named analytical angle
- separating “initial synthesis” from “stress-tested synthesis”
- providing structured second-pass challenge instead of general refinement

This creates a gap:

the system can produce strong first-pass reasoning, but it lacks a reusable, explicit mechanism for forcing deeper analysis through named reasoning methods.

---

## 3. Goals

### 3.1 Functional Goals

1. Introduce a reusable advanced elicitation capability into AI Ecosystem.
2. Allow a generated answer or synthesis to be re-examined using a named analytical method.
3. Improve the quality of outputs from `thinking-assistant`.
4. Improve the robustness of `sparring-orchestrator` outputs by adding a post-synthesis challenge pass.
5. Support dynamic method selection based on task type and likely weakness.
6. Allow one method by default, with optional bounded multi-method sequences where justified.
7. Produce explicit deltas showing what changed after elicitation.
8. Preserve user inspectability and bounded reasoning.

### 3.2 AI Ecosystem Alignment Goals

1. Preserve AI Ecosystem’s broad-agent architecture.
2. Avoid reintroducing many specialist “thinking lens” agents.
3. Keep elicitation behavior as a workflow capability rather than agent proliferation.
4. Place reusable logic in a skill and/or procedure.
5. Keep method knowledge in instructions or data artifacts where appropriate.
6. Preserve explicit uncertainty and honesty when no further improvement is justified.

### 3.3 UX Goals

1. The user should be able to invoke advanced elicitation naturally.
2. The system should not become noisy by default.
3. The user should understand:
   - which method was selected
   - why it was selected
   - what changed
   - whether the recommendation changed
4. The feature should feel like a meaningful deepening pass, not generic polishing.

---

## 4. Non-Goals

1. Creating one new permanent agent per elicitation method.
2. Replacing the existing multi-perspective orchestration.
3. Turning all thought workflows into heavy multi-stage rituals.
4. Automatically applying many elicitation methods in parallel by default.
5. Creating roleplay-heavy or persona-heavy “debate theater.”
6. Treating elicitation output as verified truth rather than improved reasoning.
7. Forcing elicitation on trivial tasks.

---

## 5. Core Design Principles

1. **Second-pass critique, not first-pass generation**
   - Advanced elicitation should operate on an existing answer, synthesis, or recommendation.

2. **Named angle of attack**
   - The system should explicitly state which method is being used.

3. **Method selection is dynamic**
   - The system should choose methods based on context, not on permanent agent identity.

4. **One method by default**
   - The default behavior should be one carefully selected method, not a swarm.

5. **Optional second method only when justified**
   - Multi-method passes should be bounded and complementary.

6. **Delta over repetition**
   - The output should emphasize what changed, not restate everything from scratch.

7. **No agent proliferation**
   - Methods are reasoning tools, not separate enduring agent roles.

8. **Post-synthesis placement**
   - In orchestrated workflows, elicitation should usually happen after perspective synthesis.

9. **Explicit keep/discard discipline**
   - The system should preserve the spirit of “accept, revise, or discard” rather than blindly replacing prior reasoning.

---

## 6. User Stories

### 6.1 Thinking Assistant Deepening

As a user, I want the `thinking-assistant` to challenge its own draft from a named analytical angle so that I get a more robust answer than a generic first pass.

### 6.2 Orchestrator Stress Test

As a user, I want the `sparring-orchestrator` to apply an advanced elicitation method after synthesizing multiple perspectives so that the final recommendation is stress-tested rather than merely averaged.

### 6.3 Assumption Discovery

As a user, I want hidden assumptions in my idea or plan to be surfaced explicitly so that I can make better decisions.

### 6.4 Controlled Depth

As a AI Ecosystem maintainer, I want deeper analysis without adding many new agents so that the system stays maintainable and aligned with AI Ecosystem v3.

---

## 7. Scope

### In Scope

- advanced elicitation capability
- method selection logic
- method registry
- integration into `thinking-assistant`
- integration into `sparring-orchestrator`
- post-synthesis elicitation pass
- optional user-facing method choice
- output delta and recommendation-change reporting
- bounded multi-method sequencing

### Out of Scope

- permanent agent per elicitation method
- autonomous unlimited reasoning loops
- direct code implementation workflows
- hard verification guarantees
- freeform debate theater
- replacing existing review or implementation workflows

---

## 8. Proposed Architecture

## 8.1 Recommended Artifact Set

Minimal recommended first version:

- `.github/skills/advanced-elicitation/SKILL.md`
- `.github/instructions/advanced-elicitation.instructions.md`
- `.github/procedures/advanced-elicitation.procedure.md`
- `.github/context/elicitation-methods.csv` or equivalent registry file
- optional `.github/templates/elicitation-delta.template.md`

Existing artifacts reused:

- `.github/agents/thinking-assistant.agent.md`
- `.github/agents/sparring-orchestrator.agent.md`
- existing orchestration instructions
- existing multi-perspective templates or reporting artifacts

Optional if Copilot orchestration benefits from a hidden callable worker:

- `.github/agents/elicitation-facilitator.agent.md`

## 8.2 Architectural Position

Advanced elicitation should be treated as a reusable workflow capability.

It should sit:

- inside `thinking-assistant` as an optional refinement mode
- after synthesis inside `sparring-orchestrator`
- optionally in other high-value planning/specification flows

It should not become:

- a new visible top-level user-facing agent family
- a replacement for multi-perspective orchestration
- a separate perspective parallel to architecture / implementation / thinking

---

## 9. Recommended Integration Model

## 9.1 Primary Integration

### `sparring-orchestrator`

Recommended default flow:

    perspectives
      → synthesis
        → elicitation method selection
          → elicitation pass
            → refined synthesis
              → final answer

This is the preferred integration point because the elicitation method challenges the combined result rather than only one contributor’s reasoning.

### `thinking-assistant`

Recommended direct-use flow:

    initial answer
      → elicitation method selection
        → elicitation pass
          → refined answer

This supports high-quality standalone use outside orchestrated mode.

## 9.2 Optional Hidden Worker

If the orchestrator implementation is cleaner with a hidden worker, introduce exactly one hidden elicitation worker.

Suggested role:

- inspect synthesized answer
- select best-fit method
- apply one elicitation pass
- return:
  - selected method
  - reason for selection
  - delta
  - whether recommendation changed
  - residual uncertainties

This worker must not become a new freeform “thinking partner.”

---

## 10. Method Model

## 10.1 Method Classes

Elicitation methods should be grouped into a small number of conceptual classes.

### Assumption-Challenging Methods

Used when the answer may rest on unexamined premises.

Examples:

- First Principles Analysis
- Socratic Questioning
- Assumption Surfacing

### Risk / Failure Methods

Used when the answer may sound plausible but hide fragility.

Examples:

- Pre-mortem Analysis
- Failure Mode Analysis
- Red Team vs Blue Team

### Tradeoff / Decision Methods

Used when multiple reasonable options exist and tradeoffs need to be made explicit.

Examples:

- Comparative Analysis Matrix
- Architecture Decision Record style analysis
- Tradeoff matrix

### Stakeholder / Context Methods

Used when different parties are likely to value different outcomes.

Examples:

- Stakeholder Round Table
- Cross-Functional War Room

### Consistency / Robustness Methods

Used when the current answer needs internal coherence checks.

Examples:

- Self-Consistency Validation
- Critical Perspective Challenge

## 10.2 Initial Recommended Method Set

Start with a small curated set:

1. First Principles Analysis
2. Socratic Questioning
3. Pre-mortem Analysis
4. Comparative Analysis Matrix
5. Stakeholder Round Table
6. Architecture Decision Record style tradeoff analysis
7. Red Team vs Blue Team
8. Self-Consistency Validation

This set is large enough to be useful and small enough to stay maintainable.

---

## 11. Method Selection Model

## 11.1 Why Selection Matters

The value of advanced elicitation comes from selecting an angle that meaningfully challenges the current answer.

Selection must therefore depend on:

- task type
- current output type
- likely weakness in the current answer
- user goal
- whether multiple perspectives have already been synthesized

## 11.2 Required Inputs for Selection

The selector should consider:

- task type
- current artifact type
- current recommendation confidence
- observed uncertainty level
- likely weakness class
- whether the answer already includes explicit tradeoffs or risks

## 11.3 Likely Weakness Classes

Suggested weakness classes:

- hidden assumptions
- weak tradeoff analysis
- underexplored failure modes
- stakeholder blindness
- premature convergence
- internal inconsistency
- weak decision rationale

## 11.4 Default Mapping

| Likely Weakness                 | Preferred Method            |
| ------------------------------- | --------------------------- |
| hidden assumptions              | First Principles Analysis   |
| underexplored uncertainty       | Socratic Questioning        |
| fragile recommendation          | Pre-mortem Analysis         |
| unclear tradeoffs               | Comparative Analysis Matrix |
| missing stakeholder impact      | Stakeholder Round Table     |
| architecture decision ambiguity | ADR-style tradeoff analysis |
| overly optimistic answer        | Red Team vs Blue Team       |
| contradictory reasoning         | Self-Consistency Validation |

## 11.5 Selection Output

The selector must produce:

- selected method
- reason for selection
- optional alternative method if uncertainty is high
- whether one or two passes are justified

---

## 12. Execution Model

## 12.1 Standard Single-Method Pass

The default lifecycle is:

    initial answer or synthesis
      → identify likely weakness
        → choose best-fit method
          → apply method
            → compare result to prior answer
              → produce delta
                → keep refined version

## 12.2 Optional Two-Method Sequence

A second method may be applied only when:

- the first pass exposed a deeper unresolved issue
- the second method is complementary rather than redundant
- the additional pass is likely to materially improve the answer
- bounded complexity is preserved

## 12.3 Good Two-Method Sequences

- First Principles → Comparative Analysis Matrix
- Pre-mortem → ADR-style tradeoff analysis
- Stakeholder Round Table → Red Team vs Blue Team
- Socratic Questioning → Self-Consistency Validation

## 12.4 Bad Multi-Method Pattern

The system must avoid:

- three or more elicitation methods in parallel by default
- method chains that restate the same criticism in different words
- forcing second-pass complexity onto trivial tasks

---

## 13. Placement Rules

## 13.1 In `sparring-orchestrator`

Elicitation should occur:

- after perspective synthesis
- before final recommendation is emitted

Why:

- the synthesis is the thing that needs challenging
- elicitation is most valuable when operating on a concrete integrated answer
- it avoids asking each worker perspective to overfit its own angle

## 13.2 In `thinking-assistant`

Elicitation should occur:

- after a substantial draft or recommendation exists
- only when the task benefits from deeper challenge

It should not occur:

- on simple factual or straightforward instructional tasks
- when the output is already intentionally minimal
- when the user clearly wants speed over depth

---

## 14. Trigger Conditions

## 14.1 Automatic Triggers

The system may auto-trigger advanced elicitation when:

- the task is architectural, strategic, or planning-heavy
- the current answer recommends a nontrivial decision
- the recommendation depends on assumptions not yet made explicit
- multiple perspectives converge quickly on a strong recommendation
- the user asks for critique, stress testing, or challenge
- the risk of premature confidence is nontrivial

## 14.2 Manual Triggers

The user may explicitly request:

- “challenge this”
- “stress-test this”
- “use first principles”
- “do a pre-mortem”
- “show stakeholder impact”
- “compare the options explicitly”

## 14.3 Non-Trigger Conditions

Do not trigger elicitation when:

- the task is trivial
- the answer is purely mechanical
- the output is already a structured second-pass critique
- the user explicitly requests a quick direct answer only
- additional depth would create noise without decision value

---

## 15. Required Behavior

## 15.1 `thinking-assistant` Behavior

The `thinking-assistant` shall:

1. produce the initial answer or recommendation
2. detect whether advanced elicitation is warranted
3. either:
   - offer 3 relevant methods to the user, or
   - auto-select one when the user requested challenge/stress test
4. apply the selected method
5. report:
   - selected method
   - reason for selection
   - what changed
   - whether the recommendation changed
   - residual uncertainty

## 15.2 `sparring-orchestrator` Behavior

The `sparring-orchestrator` shall:

1. gather perspective outputs as usual
2. synthesize the perspectives
3. determine whether advanced elicitation is warranted
4. select one method or invoke the elicitation capability
5. apply elicitation to the synthesized result
6. produce:
   - pre-elicitation synthesis summary
   - method used
   - post-elicitation refinement summary
   - final recommendation

## 15.3 Elicitation Capability Behavior

The advanced elicitation capability shall:

1. read the current answer or synthesis
2. identify likely weaknesses
3. select one method by default
4. apply the method explicitly
5. generate a refined answer or refinement delta
6. preserve explicit uncertainty
7. avoid hallucinated facts
8. stop when no material refinement is justified

---

## 16. Output Model

## 16.1 Required Output Fields

Each elicitation run should produce:

- `selected_method`
- `selection_reason`
- `target_artifact`
- `key_challenge`
- `delta_summary`
- `recommendation_changed`
- `refined_recommendation`
- `residual_uncertainties`

## 16.2 Delta-Centric Output

The preferred output style is delta-centric.

It should focus on:

- what the method revealed
- what changed
- whether the overall recommendation shifted

It should avoid:

- unnecessary full restatement of the prior answer
- narrative inflation
- repeating unchanged sections

## 16.3 Example Output Shape

### Selected Method

Pre-mortem Analysis

### Why This Method

The synthesis converged quickly on a strong recommendation but did not explicitly explore how the decision could fail operationally or organizationally.

### What This Method Surfaced

- service boundaries are assumed rather than evidenced
- operational complexity may rise before benefits materialize
- local development speed may drop

### What Changed

The recommendation shifted from “microservices are likely appropriate soon” to “use a modular monolith now and preserve extraction seams.”

### Residual Uncertainties

- actual scaling bottlenecks are still not evidenced
- team ownership model is unclear

---

## 17. Examples

## 17.1 Example — Architecture Decision

### User Request

We have a FastAPI backend and React frontend. Should we stay a modular monolith or move to microservices?

### Orchestrated Flow

1. architecture lens evaluates boundaries
2. implementation lens evaluates delivery cost
3. thinking lens evaluates broader reasoning
4. orchestrator synthesizes
5. advanced elicitation selects Pre-mortem Analysis
6. final recommendation is refined

### Expected Improvement

Before elicitation:

- the answer may conclude “modular monolith” based on initial tradeoffs

After elicitation:

- the system explicitly surfaces likely failure mechanisms
- the final recommendation becomes more justified and more cautious
- the explanation includes evidence of fragility analysis

## 17.2 Example — Product / Strategy Idea

### User Request

We should build a plugin ecosystem for the app. What do you think?

### `thinking-assistant` Flow

1. initial answer produced
2. selector sees hidden assumptions and stakeholder complexity
3. selects Stakeholder Round Table
4. refined answer incorporates:
   - platform owner view
   - external developer view
   - customer view
   - support / operations view

### Expected Improvement

The final answer becomes less generic and more grounded in ecosystem incentives and support burden.

## 17.3 Example — Comparative Choice

### User Request

Which is better for this feature: event sourcing or ordinary CRUD with audit logs?

### Likely Method

Comparative Analysis Matrix or ADR-style tradeoff analysis

### Expected Improvement

The final answer becomes a decision document rather than a loosely argued preference.

---

## 18. User Interaction Modes

## 18.1 Fully Automatic Mode

The system:

- determines elicitation is warranted
- selects the best-fit method
- applies it
- reports the result

Best for:

- orchestrated workflows
- expert users
- stress-test mode

## 18.2 Guided Mode

The system:

- proposes 3 relevant methods
- asks the user to choose one
- applies the chosen method

Best for:

- interactive design sessions
- direct `thinking-assistant` use
- teaching / exploration workflows

## 18.3 Bounded Hybrid Mode

The system:

- auto-selects by default when the user requested stress testing
- otherwise offers a small menu when the answer is exploratory

This is the recommended general mode.

---

## 19. File Responsibilities

| Artifact                                    | Responsibility                                                           | Must NOT Own                                       |
| ------------------------------------------- | ------------------------------------------------------------------------ | -------------------------------------------------- |
| `advanced-elicitation/SKILL.md`             | reusable workflow packaging, entry points, examples, artifact references | global AI Ecosystem rules                          |
| `advanced-elicitation.procedure.md`         | ordered elicitation flow, selection/execution steps, stop conditions     | agent identity, global policy                      |
| `advanced-elicitation.instructions.md`      | reusable elicitation guidance, method use rules, selection heuristics    | workflow ownership, template structure             |
| `elicitation-methods.csv`                   | method registry and metadata                                             | live reasoning, policy                             |
| optional `elicitation-facilitator.agent.md` | hidden callable worker for selection/execution if needed                 | broad planning role, freeform synthesis ownership  |
| `thinking-assistant.agent.md`               | uses elicitation capability where appropriate                            | method registry, full workflow definition          |
| `sparring-orchestrator.agent.md`            | calls elicitation post-synthesis where appropriate                       | method corpus ownership, duplicated workflow logic |

---

## 20. Data Model for Method Registry

Suggested fields for `elicitation-methods.csv`:

- `method_id`
- `method_name`
- `category`
- `best_for`
- `avoid_when`
- `targets`
- `strengths`
- `common_failure_modes`
- `example_prompt_frame`
- `pairable_with`
- `priority`

Example:

    method_id,method_name,category,best_for,avoid_when,targets,strengths,common_failure_modes,example_prompt_frame,pairable_with,priority
    pre_mortem,Pre-mortem Analysis,risk_failure,fragile recommendations and planning decisions,trivial tasks,plans and synthesized recommendations,surfaces failure mechanisms,can become repetitive if risks already explicit,"Assume this fails in 6 months. Why?",adr_matrix,high

---

## 21. Procedure Design

## 21.1 Recommended Procedure Stages

`advanced-elicitation.procedure.md` should contain:

1. identify target artifact
2. classify task type
3. identify likely weakness class
4. select best-fit method
5. optionally present alternatives
6. execute elicitation method
7. compare pre/post result
8. produce delta
9. decide whether a second pass is justified
10. finalize refined output

## 21.2 Required Procedure Rules

- one method by default
- optional second method only when explicitly justified
- no parallel method swarm by default
- preserve explicit assumptions and unknowns
- prefer delta over full rewrite
- stop when no material refinement is produced

---

## 22. Integration with Existing Orchestration

## 22.1 Current Baseline

The multi-perspective orchestrator already:

- invokes multiple agents or lenses
- gathers outputs
- synthesizes a recommendation

## 22.2 Enhancement

Add one new stage:

    perspective gathering
      → synthesis
        → advanced elicitation
          → refined synthesis
            → final answer

## 22.3 Why This Is Better Than More Lenses

Adding more permanent lenses would:

- increase agent complexity
- add maintenance burden
- blur the line between perspective and reasoning method
- move AI Ecosystem back toward specialized-agent sprawl

Adding one elicitation stage instead:

- preserves architecture
- increases depth
- keeps methods dynamic
- improves quality without fragmenting agent roles

---

## 23. Integration with `thinking-assistant`

## 23.1 Enhancement Strategy

Add a capability, not a new identity.

`thinking-assistant` should gain:

- awareness of elicitation triggers
- ability to select or offer methods
- ability to produce refined answers via named second-pass challenge

## 23.2 Suggested Behavior

After a substantial answer, the assistant may say:

- “I can stress-test this from one of several angles.”
- “The main weakness here is likely untested assumptions; First Principles Analysis is the best fit.”

Then it applies the method and returns only the meaningful delta.

---

## 24. Acceptance Criteria

## 24.1 Functional Acceptance

1. A reusable advanced elicitation capability exists as a AI Ecosystem skill and/or procedure-backed workflow.
2. `thinking-assistant` can invoke it when appropriate.
3. `sparring-orchestrator` can invoke it after synthesis.
4. The system can select one method dynamically based on context.
5. The system can explain why the method was selected.
6. The output includes a delta and whether the recommendation changed.
7. The feature supports at least 6–8 high-value methods initially.

## 24.2 AI Ecosystem Acceptance

1. No new family of visible specialist elicitation agents is introduced.
2. The feature does not violate broad-agent AI Ecosystem architecture.
3. Workflow logic primarily lives in skill/procedure artifacts.
4. Method metadata lives outside the agent definitions.
5. Uncertainty remains explicit.

## 24.3 UX Acceptance

1. The feature improves high-value reasoning tasks without making simple tasks noisy.
2. The method used is visible to the user.
3. The refinement feels materially deeper than generic polishing.
4. The system avoids repetitive over-analysis by default.

---

## 25. Success Criteria

The feature is successful if:

1. architectural and strategic answers become more robust and explicit
2. hidden assumptions are surfaced more often
3. failure-mode reasoning improves
4. tradeoff clarity improves
5. the orchestrator’s final recommendations become more defensible
6. the enhancement does not require many new permanent agents

---

## 26. Risks and Mitigations

| Risk                                      | Impact                              | Mitigation                                          |
| ----------------------------------------- | ----------------------------------- | --------------------------------------------------- |
| too many methods added too early          | maintenance burden, noisy selection | start with a small curated set                      |
| method selection feels arbitrary          | weak trust                          | always expose selection reason                      |
| system overuses elicitation               | analysis inflation                  | define clear trigger and non-trigger conditions     |
| multiple methods create overlap           | noise and redundancy                | default to one method, bounded second pass only     |
| new lens agents proliferate               | AI Ecosystem regression             | forbid method-per-agent pattern                     |
| method output becomes verbose restatement | low value                           | require delta-centric reporting                     |
| elicitation is used on trivial tasks      | wasted time                         | restrict by trigger rules                           |
| elicitation is mistaken for verification  | false confidence                    | keep output framed as improved reasoning, not proof |

---

## 27. Phased Rollout

### Phase 1 — Minimal Integration

Deliver:

- `advanced-elicitation/SKILL.md`
- `advanced-elicitation.instructions.md`
- small method registry
- integration into `thinking-assistant`

Goal:

prove the capability is useful in direct planning and idea analysis

### Phase 2 — Orchestrator Integration

Deliver:

- post-synthesis elicitation stage in `sparring-orchestrator`
- delta reporting
- method-selection heuristics

Goal:

improve the final recommendation quality in multi-perspective workflows

### Phase 3 — Refinement

Deliver:

- optional hidden elicitation worker if needed
- two-method bounded sequences
- improved registry metadata
- optional user-choice mode enhancements

Goal:

improve flexibility without increasing agent sprawl

---

## 28. Example File Layout

    .github/
    ├── agents/
    │   ├── thinking-assistant.agent.md
    │   ├── sparring-orchestrator.agent.md
    │   └── elicitation-facilitator.agent.md              # optional, hidden
    ├── instructions/
    │   └── advanced-elicitation.instructions.md
    ├── procedures/
    │   └── advanced-elicitation.procedure.md
    ├── skills/
    │   └── advanced-elicitation/
    │       └── SKILL.md
    ├── context/
    │   └── elicitation-methods.csv
    └── templates/
        └── elicitation-delta.template.md                 # optional

---

## 29. Example Final Output Template

# Advanced Elicitation Result

## 1. Target Artifact

## 2. Selected Method

## 3. Why This Method Was Chosen

## 4. What This Method Challenged

## 5. Delta Summary

## 6. Recommendation Change

## 7. Residual Uncertainties

## 8. Suggested Next Step

---

## 30. Explicit Design Decisions

1. Advanced elicitation is a workflow capability, not a new agent family.
2. The primary value is second-pass critique through named methods.
3. The preferred placement is after synthesis in orchestrated workflows.
4. `thinking-assistant` also gains direct-use access to the same capability.
5. One method is the default.
6. A second method is optional and bounded.
7. Methods are selected dynamically from a registry.
8. Output must emphasize delta and recommendation shift.

---

## 31. Open Questions

1. Should the first implementation auto-select methods by default or prefer user choice?
2. Should `sparring-orchestrator` always run elicitation on strategic tasks, or only when confidence is high?
3. Should the method registry remain a CSV, or should it move into a richer metadata file later?
4. Should the optional hidden elicitation worker exist from the start, or only if direct skill invocation proves awkward?
5. Should the system persist the original and refined synthesis for later comparison?

---

## 32. Recommendation

Implement this feature as:

- one advanced elicitation capability
- one small method registry
- one procedure-backed skill
- integration into both `thinking-assistant` and `sparring-orchestrator`

Do not implement this as:

- two more permanent thinking-assistant lenses
- one agent per method
- a swarm of parallel elicitation workers

The best first version is:

- small
- post-synthesis
- dynamic
- delta-driven
- AI Ecosystem-compatible

That gives you the real value of BMAD’s advanced elicitation model without undermining the architectural discipline you already established in AI Ecosystem.
