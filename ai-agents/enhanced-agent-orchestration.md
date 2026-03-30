# Feature Specification — CLASP Orchestrated Implementation, Testing, and QA System

## Document Control

- **Document Type:** Feature Specification
- **Status:** Proposed
- **Mode:** Epistemic
- **Target System:** CLASP ecosystem in VS Code with GitHub Copilot
- **Feature Name:** Orchestrated Implementation, Testing, and QA System
- **Short Name:** OITQ
- **Primary Objective:** Introduce a robust, production-ready orchestration layer that separates feature implementation, test creation, and QA audit while preserving CLASP’s broad worker-agent model and strict ownership boundaries
- **Primary Beneficiaries:** `feature-orchestrator`, new `test-orchestrator`, new `qa-orchestrator`, existing `sparring-orchestrator`, and the existing worker agents `software-engineer`, `code-reviewer`, and `thinking-assistant`

---

## 1. Executive Recommendation

The strongest design is **not** to create many new specialist editing agents.

The strongest design is:

- keep the current broad worker agents
- add thin workflow orchestrators
- move test and QA expertise into instructions, procedures, templates, and skills
- use subagents only where isolation materially improves quality
- keep `software-engineer` as the sole file-editing and terminal-executing agent
- make `sparring-orchestrator` the escalation path for ambiguity, conflict, or unresolved tradeoffs

### Recommended Topology

Visible or task-level orchestrators:

- `feature-orchestrator`
- `test-orchestrator`
- `qa-orchestrator`
- `sparring-orchestrator` (already exists)

Existing broad worker agents reused internally:

- `software-engineer`
- `code-reviewer`
- `thinking-assistant`

Optional hidden aspect runners only if later needed:

- requirements-traceability lens
- test-quality heuristics lens
- flaky-test / reliability lens
- writing / maintainability lens
- non-functional quality lens

Default recommendation:

implement those aspect runners first as **instructions / skill aspects**, not as permanent agents.

---

## 2. Summary

This feature introduces a coordinated development pipeline for CLASP that separates three concerns that are currently too entangled:

1. **feature implementation**
2. **test design and test implementation**
3. **quality assurance audit and remediation routing**

The intended steady-state workflow is:

    feature specification
      → feature-orchestrator
        → implementation complete
          → test-orchestrator
            → test suite complete
              → qa-orchestrator
                → findings?
                  → yes → route targeted fixes
                  → no  → accept

The new system must also support conflict resolution:

    any orchestrator
      → sparring-orchestrator
        → resolved recommendation
          → resume normal workflow

This design deliberately avoids collapsing implementation, testing, and QA into one “super-agent.”

Instead, it creates:

- a clearer pipeline
- cleaner ownership
- better observability
- more targeted remediation
- stronger test quality
- less risk that low-value or brittle tests are mistaken for quality

---

## 3. Problem Statement

The current feature pipeline already implements code and some tests, but that bundles too many responsibilities into one flow.

Current risks:

- the implementation flow can over-prioritize shipping over test design quality
- tests may be created opportunistically rather than strategically
- QA concerns may be treated as “code review afterthoughts”
- test quantity may be mistaken for test quality
- flaky, brittle, redundant, low-signal, or poorly scoped tests may survive
- remediation may be too broad because findings are not routed by ownership
- disagreements about implementation vs tests vs quality may have no explicit escalation path

The desired future state is a pipeline where:

- implementation is done deliberately
- tests are designed and implemented deliberately
- QA audits both code and tests deliberately
- remediation is targeted to the right owner
- conflict resolution is explicit
- the whole flow remains aligned with CLASP’s authority model

---

## 4. Goals

### 4.1 Functional Goals

1. Separate implementation, testing, and QA into distinct orchestrated stages.
2. Create a dedicated `test-orchestrator` responsible for test planning, selection, creation, and validation.
3. Create a dedicated `qa-orchestrator` responsible for auditing code quality, test quality, and release readiness.
4. Route findings to the correct remediation owner:
   - feature implementation
   - test implementation
   - both
   - or sparring escalation
5. Support a bounded remediation loop until the output converges or a stop condition is hit.
6. Preserve the ability for any orchestrator to call `sparring-orchestrator` when deeper reasoning or conflict resolution is required.

### 4.2 CLASP Alignment Goals

1. Preserve CLASP v3’s broad worker-agent model.
2. Avoid reintroducing many specialized visible agents.
3. Keep procedural logic in procedures and skills.
4. Keep domain expertise in instructions and skill resources.
5. Preserve `software-engineer` as the only editing/execution agent unless CLASP deliberately changes that rule later.
6. Preserve `code-reviewer` as read-only and adversarial.
7. Preserve `thinking-assistant` as read-only and planning-heavy.

### 4.3 Quality Goals

1. Increase test relevance, not just test count.
2. Increase QA audit strength without creating agent chaos.
3. Detect flaky, brittle, redundant, low-value, and misleading tests earlier.
4. Improve requirement-to-test traceability.
5. Improve maintainability and readability of tests and implementation.

---

## 5. Non-Goals

1. Replacing CI or real enforcement infrastructure.
2. Guaranteeing that all bugs are caught before merge.
3. Creating an agent per test type.
4. Making QA the sole owner of security, architecture, or product decisions.
5. Allowing unbounded retry loops.
6. Turning the orchestrators into direct editors.
7. Building a theatrical multi-agent system where every concern becomes a permanent persona.

---

## 6. Research-Informed Design Principles

1. **Balanced test portfolio over dogma**
   - Prefer a balanced portfolio of unit, component, integration, and end-to-end tests.
   - Do not force a rigid single “shape” when the system under test needs a different balance.

2. **Fast narrow tests dominate, broad tests are strategic**
   - Unit and other fast focused tests should usually form the majority.
   - Broader integration and end-to-end tests should exist, but selectively.

3. **Test quality is not test count**
   - Strong tests encode behavior, failure oracles, boundaries, and invariants.
   - Weak tests only exercise code paths.

4. **Flaky tests are a first-class reliability problem**
   - QA must explicitly detect, classify, and quarantine or reject flaky tests.

5. **Mutation testing is a quality signal, not a universal gate**
   - Use mutation testing selectively for critical modules or suspiciously weak test suites.

6. **Property-based testing is powerful but selective**
   - Use it where invariants, input spaces, transformations, or generative edge cases matter.

7. **Large rewrites are drift machines**
   - Findings should route to targeted fixes, not broad rewrites.

8. **Conflict resolution must be explicit**
   - When implementation, test design, and QA concerns disagree, the system should escalate intentionally rather than blur ownership.

---

## 7. System Overview

The orchestrator system has four top-level capabilities:

### 7.1 Feature Orchestrator

Owns:

- implementation planning for a feature slice
- code implementation
- minimal local verification needed to avoid handing broken work downstream
- handoff package for testing

Does not own:

- canonical test strategy
- full test suite design
- final quality audit

### 7.2 Test Orchestrator

Owns:

- test strategy for the feature or slice
- selection of appropriate test types
- creation of test artifacts
- execution and stabilization of those tests
- test evidence package for QA

Does not own:

- product/feature code implementation
- final QA disposition

### 7.3 QA Orchestrator

Owns:

- audit of implementation quality
- audit of test quality
- audit of requirement-to-test traceability
- audit of non-functional and maintainability concerns where in scope
- routing of findings to the correct remediation owner

Does not own:

- direct editing
- architecture arbitration by itself
- product prioritization

### 7.4 Sparring Orchestrator

Owns:

- deep analysis of unresolved conflicts
- explicit tradeoff resolution support
- challenging recommendations through multi-perspective and advanced elicitation methods
- returning a bounded resolution package

Does not own:

- permanent implementation execution
- test ownership
- QA ownership

---

## 8. Recommended Architecture

### 8.1 Top-Level Structure

    User Request / Feature Spec
      → Feature Orchestrator
        → Test Orchestrator
          → QA Orchestrator
            → Remediation Router
              → Feature Orchestrator and/or Test Orchestrator
                → QA Re-check
                  → Accept or Stop

### 8.2 Escalation Path

    Any orchestrator
      → Sparring Orchestrator
        → Resolution Package
          → resume owning workflow

### 8.3 Worker-Agent Execution Model

The orchestrators coordinate.
The worker agents do the actual cognitive and execution work.

Worker responsibilities:

- `software-engineer`
  - only agent allowed to edit files and run terminal commands
  - used by feature and test orchestration for implementation work

- `code-reviewer`
  - read-only adversarial review
  - used by QA orchestration for audit and by feature/test flows for targeted review

- `thinking-assistant`
  - read-only planning and analysis
  - used for decomposition, test strategy reasoning, heuristics selection, and escalation prep

---

## 9. Key Design Decision

## Do not create a separate permanent test-editing agent.

Instead:

- create a **Test Orchestrator**
- let that orchestrator use `software-engineer` under test-specific instructions and procedures

Reason:

- it preserves the current CLASP tool-boundary model
- it avoids splitting editing authority across multiple agents
- it keeps test code and feature code under the same mechanical execution authority
- it prevents agent sprawl where the only real difference is prompt framing

The same logic applies to QA.
QA should be a coordinator and audit capability, not a new editing agent.

---

## 10. Artifact Strategy

The system should be implemented primarily through:

- thin orchestrator agent files
- instructions
- procedures
- skills
- templates
- finding schemas
- targeted prompts

Not through:

- many new specialist worker agents

### 10.1 Recommended New Artifacts

    .github/
    ├── agents/
    │   ├── feature-orchestrator.agent.md
    │   ├── test-orchestrator.agent.md
    │   ├── qa-orchestrator.agent.md
    │   ├── sparring-orchestrator.agent.md
    │   ├── software-engineer.agent.md
    │   ├── code-reviewer.agent.md
    │   └── thinking-assistant.agent.md
    ├── instructions/
    │   ├── test-design.instructions.md
    │   ├── test-selection.instructions.md
    │   ├── test-quality.instructions.md
    │   ├── flaky-test.instructions.md
    │   ├── qa-audit.instructions.md
    │   ├── qa-writing-quality.instructions.md
    │   ├── requirements-traceability.instructions.md
    │   ├── mutation-testing.instructions.md
    │   ├── property-based-testing.instructions.md
    │   ├── e2e-strategy.instructions.md
    │   └── remediation-routing.instructions.md
    ├── procedures/
    │   ├── feature-delivery.procedure.md
    │   ├── test-delivery.procedure.md
    │   ├── qa-audit.procedure.md
    │   └── remediation-loop.procedure.md
    ├── skills/
    │   ├── test-orchestration/
    │   │   └── SKILL.md
    │   ├── qa-orchestration/
    │   │   └── SKILL.md
    │   └── sparring-resolution/
    │       └── SKILL.md
    ├── prompts/
    │   ├── implement-feature.prompt.md
    │   ├── generate-test-plan-and-tests.prompt.md
    │   ├── run-qa-audit.prompt.md
    │   └── resolve-conflict-with-sparring.prompt.md
    ├── templates/
    │   ├── test-plan.template.md
    │   ├── test-findings.template.md
    │   ├── qa-report.template.md
    │   ├── remediation-plan.template.md
    │   └── resolution-package.template.md
    └── context/
        ├── qa-heuristics.md
        ├── test-type-selection-matrix.md
        └── release-quality-gates.md

---

## 11. Orchestrator Definitions

## 11.1 Feature Orchestrator

### Purpose

Take a feature specification and produce a bounded implementation package that is ready for test design and implementation.

### Responsibilities

- read the feature spec
- decompose into slices if needed
- identify impacted code areas
- route coding tasks to `software-engineer`
- perform minimal immediate verification
- emit an implementation package for testing

### Output

Implementation Package:

- feature summary
- changed files
- architecture / design notes
- risks introduced
- assumptions
- testability hooks and seams
- unresolved questions
- local verification evidence

### Must NOT Own

- canonical decision of which full test suite to build
- final QA sign-off

---

## 11.2 Test Orchestrator

### Purpose

Own the design and implementation of the automated test portfolio for the implemented feature.

### Responsibilities

- read the feature spec and implementation package
- map requirements and risk to test types
- decide which tests are needed and which are not
- route test code creation to `software-engineer`
- execute tests
- stabilize brittle tests
- emit a test evidence package for QA

### Core Principle

The test orchestrator is not “write all test types always.”

It is:

- choose the smallest sufficient test portfolio
- prefer fast focused tests when possible
- use broader tests strategically
- include richer methods only where they materially improve confidence

### Output

Test Evidence Package:

- requirement-to-test matrix
- test types selected
- test files created or updated
- execution evidence
- skipped / deferred test types with rationale
- known test risks
- flaky-test status
- optional advanced quality signals

### Must NOT Own

- product feature code beyond test scaffolding/test harness needs
- final QA sign-off

---

## 11.3 QA Orchestrator

### Purpose

Audit the combined output of feature implementation and test implementation, then route findings to the right owner.

### Responsibilities

- audit implementation quality
- audit test relevance and test quality
- audit traceability from spec to tests
- audit writing quality and maintainability of tests
- audit reliability risks including flaky and brittle tests
- classify findings by severity and owner
- route remediation
- re-audit after targeted fixes

### Output

QA Report:

- audit scope
- findings
- severity
- owner
- blocking vs non-blocking
- recommended remediation path
- release disposition

### Must NOT Own

- direct code editing
- silent architecture decisions
- broad rewrites

---

## 11.4 Sparring Orchestrator

### Purpose

Resolve conflicts, ambiguity, or deeper reasoning questions that block progress in feature, test, or QA workflows.

### Responsibilities

- run multi-perspective analysis
- apply advanced elicitation when useful
- explicitly compare alternatives
- return a bounded decision package

### Typical Triggers

- disagreement between implementation and QA
- disagreement between implementation and test strategy
- uncertain test type selection
- brittle test vs valuable test tradeoff
- architecture conflict surfaced late
- unclear remediation path

### Output

Resolution Package:

- problem summary
- perspectives used
- tradeoff analysis
- selected recommendation
- assumptions
- unresolved residual risks

---

## 12. Suggested Aspect Model

Do not create permanent subagents for every QA concern initially.

Instead, model QA as **aspect passes** inside a skill or procedure.

### Recommended QA Aspects

1. **Requirements Traceability Aspect**
   - checks whether each material requirement or acceptance criterion maps to code and tests

2. **Test Strategy Aspect**
   - checks whether selected test types fit the risk and architecture

3. **Test Quality Aspect**
   - checks readability, isolation, determinism, oracle quality, failure clarity, maintainability

4. **Reliability / Flakiness Aspect**
   - checks nondeterminism, timing sensitivity, environment dependence, retry abuse, network dependence

5. **Implementation Quality Aspect**
   - checks maintainability, coupling, naming, error handling, edge cases, code clarity

6. **Non-Functional Quality Aspect**
   - checks relevant performance, accessibility, security, and operational concerns when in scope

7. **Writing / Documentation Aspect**
   - checks whether tests and artifacts explain intent clearly enough for maintenance

### Escalation Rule

If one aspect becomes large, tool-specific, or repeatedly overloaded, only then consider materializing it as a hidden subagent.

---

## 13. When Subagents Are Actually Worth It

A new hidden subagent is justified only if at least one of these is true:

1. it needs a materially different tool profile
2. it needs isolated context because prompt size or cross-talk hurts quality
3. it has a recurring specialized reasoning pattern that is genuinely separable
4. it needs a different model or execution environment
5. it produces a stable artifact with clear reuse value

### Likely Good Future Hidden Subagents

- `traceability-auditor` — read-only, requirement-to-test mapping
- `flakiness-auditor` — read-only, reliability and determinism analysis
- `nonfunctional-qa-auditor` — read-only, performance/accessibility/security in scope
- `test-portfolio-planner` — read-only, complex test strategy selection

### What Should Stay as Instructions / Aspects

- AAA style checks
- naming clarity
- snapshot-test policy
- when to use property-based tests
- when to use mutation testing
- when E2E is justified
- what constitutes brittle test design

---

## 14. Test Orchestrator — Test Type Selection Policy

The test orchestrator must build a test portfolio deliberately.

### Default Preference Order

1. unit tests
2. component tests
3. integration tests
4. contract tests where service boundaries exist
5. end-to-end tests for critical user journeys only
6. property-based tests where invariants or large input spaces matter
7. mutation testing as a selective quality signal
8. performance / load tests where non-functional risk is material
9. accessibility tests where UI changes affect user interaction
10. snapshot / approval tests only when change review remains meaningful

### Test Selection Rules

The orchestrator should prefer:

- the cheapest test that can credibly detect the risk
- the narrowest reliable test that gives sufficient confidence
- broader tests only where interactions are the risk

The orchestrator should avoid:

- adding E2E where unit/integration can cover the same risk
- snapshot tests for highly unstable outputs unless deliberately curated
- mutation testing on every change by default
- property-based tests where there is no stable invariant worth encoding

---

## 15. QA Orchestrator — Audit Dimensions

The QA orchestrator must audit at least the following:

### 15.1 Requirement Coverage

- each material requirement mapped to at least one credible verification mechanism
- each critical acceptance criterion exercised
- explicit note where a requirement is deferred or non-automatable

### 15.2 Test Relevance

- tests correspond to actual risk
- tests are not just implementation-detail lock-in
- unnecessary duplicate tests are identified

### 15.3 Test Quality

- readable names
- understandable failure messages
- clear arrange/act/assert or equivalent structure
- deterministic setup
- meaningful assertions
- low mock abuse
- no brittle timing assumptions
- no hidden shared state dependence

### 15.4 Implementation Quality

- code clarity
- maintainability
- safe handling of edge cases
- no obvious regression risk
- appropriate error handling
- acceptable boundary design

### 15.5 Reliability

- flaky-test risk
- environment-sensitive behavior
- order dependence
- race-condition sensitivity
- test data contamination
- misuse of retries

### 15.6 Writing / Documentation Quality

- test names explain behavior
- comments explain intent, not obvious mechanics
- change logs or notes capture non-obvious test strategy decisions
- generated artifacts are understandable to future maintainers

### 15.7 Non-Functional Quality

In-scope only where relevant:

- performance
- accessibility
- security
- operational supportability

---

## 16. Findings Schema

All QA findings must use a normalized schema.

### Required Fields

- `finding_id`
- `title`
- `severity`
- `category`
- `owner`
- `blocking`
- `evidence`
- `scope`
- `recommended_action`
- `fix_route`
- `confidence`

### Suggested Severity

- `critical`
- `high`
- `medium`
- `low`
- `info`

### Suggested Categories

- `implementation_correctness`
- `implementation_maintainability`
- `test_gap`
- `test_quality`
- `test_brittleness`
- `test_flakiness`
- `traceability_gap`
- `nonfunctional_risk`
- `documentation_quality`
- `needs_sparring`
- `needs_human_decision`

### Owner Values

- `feature-orchestrator`
- `test-orchestrator`
- `both`
- `sparring-orchestrator`
- `human`

### Fix Route Values

- `feature_fix`
- `test_fix`
- `dual_fix`
- `sparring_resolution`
- `human_decision`

---

## 17. Routing Matrix

| Finding Type                                 | Owner                 | Default Route       |
| -------------------------------------------- | --------------------- | ------------------- |
| feature behavior incorrect                   | feature-orchestrator  | feature_fix         |
| missing test for requirement                 | test-orchestrator     | test_fix            |
| brittle / flaky test                         | test-orchestrator     | test_fix            |
| test failure caused by feature defect        | feature-orchestrator  | feature_fix         |
| unclear contract between code and test       | both                  | dual_fix            |
| architecture / strategy conflict             | sparring-orchestrator | sparring_resolution |
| missing product decision                     | human                 | human_decision      |
| poor test readability / maintainability      | test-orchestrator     | test_fix            |
| poor implementation readability              | feature-orchestrator  | feature_fix         |
| non-functional risk with unclear remediation | sparring-orchestrator | sparring_resolution |

---

## 18. End-to-End Workflow

## 18.1 Phase 1 — Feature Implementation

Input:

- feature specification
- constraints
- relevant context

Flow:

- `feature-orchestrator` invokes `thinking-assistant` for decomposition if needed
- `feature-orchestrator` invokes `software-engineer` for implementation
- local implementation verification is run
- implementation package is emitted

Exit Criteria:

- implementation slice completed
- no immediately blocking local errors
- handoff package ready

## 18.2 Phase 2 — Test Design and Test Implementation

Input:

- feature specification
- implementation package
- changed files
- risk profile

Flow:

- `test-orchestrator` invokes `thinking-assistant` for test strategy if needed
- selects test portfolio
- invokes `software-engineer` to implement tests
- runs tests
- stabilizes tests
- emits test evidence package

Exit Criteria:

- selected tests created or updated
- test evidence package complete
- deferred tests explicitly documented

## 18.3 Phase 3 — QA Audit

Input:

- feature spec
- implementation package
- test evidence package
- diffs and results

Flow:

- `qa-orchestrator` runs aspect-based audit
- may invoke `code-reviewer` for adversarial review
- classifies findings
- decides if remediation is required

Exit Criteria:

- no blocking findings remain
- or remediation plan created
- or stop condition reached

## 18.4 Phase 4 — Targeted Remediation

Flow:

- route finding bundle to owner
- owner orchestrator invokes `software-engineer` for minimal fixes
- rerun affected tests/checks only as needed
- return to QA for re-audit

Exit Criteria:

- finding cleared
- or escalated
- or max iterations reached

## 18.5 Phase 5 — Sparring Escalation

Trigger:

- unresolved conflict
- repeated failure without progress
- architecture/test strategy disagreement
- ambiguous QA recommendation
- high-stakes tradeoff

Flow:

- owning orchestrator invokes `sparring-orchestrator`
- receives bounded resolution package
- resumes normal workflow

---

## 19. Remediation Loop Rules

The remediation loop must be bounded.

### Default Bounds

- small change: max 2 QA remediation cycles
- medium change: max 3 QA remediation cycles
- larger change: split work instead of increasing loops indefinitely

### Non-Convergence Signals

Stop and escalate if:

- the same finding repeats twice without material improvement
- the fix increases surface area without reducing blockers
- tests keep changing while the requirement remains unclear
- QA findings are too vague to action safely
- flaky failures prevent trustworthy completion
- sparring resolution still leaves unresolved product or architecture ownership

---

## 20. Test Strategy Requirements

The `test-orchestrator` must produce a test plan or embedded test strategy record containing:

- requirement list
- risk list
- chosen test types
- rejected test types with rationale
- oracle strategy
- environment assumptions
- fixtures and data dependencies
- flakiness risks
- optional advanced test signals

### Optional Advanced Signals

Only when justified:

- mutation score or mutation findings
- property-based test set
- contract compatibility matrix
- performance budget checks
- accessibility checks

---

## 21. QA Audit Requirements

The `qa-orchestrator` must produce a QA report containing:

- audited scope
- summary disposition
- findings by owner
- findings by severity
- evidence excerpts
- traceability gaps
- test quality concerns
- reliability concerns
- remediation routes
- residual non-blocking risks
- final recommendation

Suggested dispositions:

- `pass`
- `pass_with_nonblocking_findings`
- `fix_required`
- `needs_sparring`
- `needs_human_decision`
- `not_ready`

---

## 22. Suggested Skills

### 22.1 `test-orchestration` Skill

Bundles:

- test design instructions
- test selection matrix
- test delivery procedure
- test-plan template
- test findings template

Use for:

- designing and implementing a test portfolio for a feature

### 22.2 `qa-orchestration` Skill

Bundles:

- qa audit instructions
- requirements traceability instructions
- flaky test instructions
- qa audit procedure
- qa report template

Use for:

- auditing implementation + tests and routing remediation

### 22.3 `sparring-resolution` Skill

Bundles:

- multi-perspective orchestration
- advanced elicitation
- comparative decision framing
- resolution template

Use for:

- resolving workflow-blocking conflicts

---

## 23. Suggested Prompts

### `implement-feature.prompt.md`

Wires:

- feature-orchestrator
- feature-delivery procedure
- implementation package output shape

### `generate-test-plan-and-tests.prompt.md`

Wires:

- test-orchestrator
- test-orchestration skill
- test-plan template
- test evidence package output shape

### `run-qa-audit.prompt.md`

Wires:

- qa-orchestrator
- qa-orchestration skill
- qa report template

### `resolve-conflict-with-sparring.prompt.md`

Wires:

- sparring-orchestrator
- sparring-resolution skill
- resolution-package template

---

## 24. Optional Hidden Subagents — Future, Not Default

These should be considered **later**, not in v1.

### `traceability-auditor`

Focus:

- requirement-to-test mapping

### `flakiness-auditor`

Focus:

- reliability risks and deterministic behavior

### `test-portfolio-planner`

Focus:

- complex tradeoffs in selecting test types

### `nonfunctional-qa-auditor`

Focus:

- performance, accessibility, security, operational supportability when scoped in

These should remain hidden and read-only.

---

## 25. Operational Rules

1. `software-engineer` remains the only editor and terminal executor.
2. `code-reviewer` remains read-only.
3. `thinking-assistant` remains read-only.
4. Orchestrators coordinate; they do not become giant editing prompts.
5. QA findings must always be normalized before routing.
6. Remediation must be targeted, not broad.
7. Sparring escalation is a first-class workflow, not an exception path of shame.
8. Unknown or deferred items must remain visible rather than being guessed into completion.

---

## 26. Acceptance Criteria

### 26.1 Functional Acceptance

1. A feature can be implemented through `feature-orchestrator`.
2. Tests can be designed and implemented through `test-orchestrator`.
3. QA can audit both code and tests through `qa-orchestrator`.
4. Findings can be routed to the correct owner.
5. Blocking findings can trigger a bounded remediation loop.
6. Any orchestrator can escalate to `sparring-orchestrator`.
7. The system can stop honestly when no safe progress is possible.

### 26.2 CLASP Acceptance

1. Worker-agent tool boundaries remain intact.
2. Most new expertise lives in instructions and skills, not agent sprawl.
3. Procedures own the lifecycle steps.
4. Templates own output structure.
5. Prompts own task wiring.
6. Orchestrators remain thin enough to be maintainable.

### 26.3 Quality Acceptance

1. Test suites produced by the system are more strategic, not just larger.
2. QA can identify missing, brittle, flaky, or low-value tests.
3. QA findings are actionable and routable.
4. Remediation is targeted and converges on straightforward changes.
5. The system handles disagreements explicitly.

---

## 27. Risks and Mitigations

| Risk                                              | Impact                               | Mitigation                                                       |
| ------------------------------------------------- | ------------------------------------ | ---------------------------------------------------------------- |
| Reintroducing agent sprawl                        | maintenance burden, CLASP regression | keep broad worker agents; put expertise into instructions/skills |
| Test orchestrator writes too many low-value tests | slow suite, false confidence         | require test-selection rationale and rejected test types         |
| QA becomes vague review theater                   | poor remediation                     | normalize findings and route by owner                            |
| Flaky tests poison confidence                     | unreliable pipeline                  | explicit flakiness audit and stop/quarantine rules               |
| Mutation testing overused                         | slow and noisy                       | make it selective, not default                                   |
| E2E overused                                      | brittle suite, slow feedback         | require explicit rationale for E2E                               |
| Orchestrators become god-prompts                  | drift and confusion                  | keep workflow logic in procedures/skills                         |
| Conflict resolution gets buried                   | repeated churn                       | formal sparring escalation path                                  |

---

## 28. Recommended Implementation Sequence

### Phase 1 — Minimal Honest Version

Build:

- `test-orchestrator.agent.md`
- `qa-orchestrator.agent.md`
- `test-orchestration/SKILL.md`
- `qa-orchestration/SKILL.md`
- `test-delivery.procedure.md`
- `qa-audit.procedure.md`
- normalized findings schema
- test-plan template
- QA report template

Reuse:

- existing `software-engineer`
- existing `code-reviewer`
- existing `thinking-assistant`
- existing `sparring-orchestrator`

### Phase 2 — Remediation Loop

Add:

- `remediation-loop.procedure.md`
- routing matrix
- owner-based fix bundles

### Phase 3 — Conflict Resolution Integration

Add:

- direct sparring escalation hooks from all orchestrators
- resolution-package artifact

### Phase 4 — Optional Specialized Read-Only Subagents

Only after repeated evidence of value:

- `traceability-auditor`
- `flakiness-auditor`
- `nonfunctional-qa-auditor`

---

## 29. Explicit Recommendations

1. Create a **Test Orchestrator**, but do not create a new separate editing test-worker agent.
2. Create a **QA Orchestrator**, but keep QA expertise mostly in aspects, skills, and instructions.
3. Keep `software-engineer` as the sole editor.
4. Keep `sparring-orchestrator` as the conflict-resolution engine callable by all orchestrators.
5. Treat subagents as optional optimization, not the core architecture.
6. Build the first version around **clear routing and quality signals**, not maximum autonomy.

---

## 30. Final Recommendation

The production-ready version of this system is **not**:

- feature agent
- test agent
- QA agent
- security agent
- flakiness agent
- readability agent
- traceability agent
- performance agent
- all permanently chatting with each other

The production-ready version is:

- a few orchestrators with clean workflow ownership
- the existing broad worker agents with stable tool boundaries
- reusable skills and procedures
- explicit quality signals
- targeted remediation
- explicit escalation to sparring when needed

That is the version that stays robust without collapsing back into v1-style maintenance burden.
