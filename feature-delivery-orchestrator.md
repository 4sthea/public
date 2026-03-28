# Feature Specification — CLASP Feature Delivery Orchestrator

## Document Control

- **Document Type:** Feature Specification
- **Status:** Proposed
- **Mode:** Epistemic
- **Target System:** CLASP ecosystem in VS Code with GitHub Copilot
- **Feature Name:** Feature Delivery Orchestrator
- **Short Name:** FDO
- **Primary Outcome:** Enable one orchestrator to drive a bounded implementation lifecycle from feature specification to implementation, verification, review, remediation, and final completion
- **Intended Audience:** CLASP maintainers, prompt/agent authors, workflow designers

---

## 1. Summary

The Feature Delivery Orchestrator is a CLASP-native orchestration capability for implementing a feature specification through a controlled multi-phase lifecycle.

It is designed to:

- read a feature specification
- plan and decompose the work
- route implementation to the existing implementation agent
- run required verification checks
- invoke a thorough multi-aspect code review
- convert review findings into structured remediation tasks
- loop through fix → verify → review until either:
  - the feature is complete and verified, or
  - a bounded stop condition is reached

The orchestrator is not a new “god agent.”

It is a coordination layer that sits above the existing CLASP agents and relies on:

- existing broad agents
- explicit procedures
- a reusable skill
- structured findings
- bounded loop control
- mechanical verification

This feature preserves CLASP’s v3 design principles:

- small visible agent surface
- single ownership per concern
- separation of cognition from execution
- instructions over agent sprawl
- verification as a separate concern
- explicit stop conditions instead of fake completion

---

## 2. Problem Statement

CLASP currently supports planning, implementation, code review, and reusable skills, but these are still mostly invoked as separate capabilities.

The missing capability is a reusable lifecycle coordinator that can take a feature specification and drive the full development loop:

1. understand the requested feature
2. produce a plan or slice decomposition
3. implement the feature
4. run verification
5. review the result from multiple aspects
6. remediate blocking findings
7. repeat until convergence or bounded failure

Without this feature, the user or prompt author must manually chain multiple tasks together and manually decide:

- when implementation is ready for review
- whether review findings are blocking
- what should be fixed next
- when to stop
- how to keep the lifecycle coherent

That causes:

- repeated prompt glue
- inconsistent lifecycle behavior
- review findings that are too vague to remediate
- over-correction and drift
- unclear stop conditions
- avoidable agent sprawl if each lifecycle stage becomes a separate top-level visible agent

---

## 3. Goals

### 3.1 Functional Goals

1. Accept a feature specification as the primary input.
2. Decompose the requested work into one or more implementable slices.
3. Route implementation to the existing implementation agent.
4. Run required mechanical verification after implementation.
5. Invoke multi-aspect code review after verification.
6. Convert review findings into structured remediation tasks.
7. Loop only on blocking failures or unresolved required work.
8. Produce a final completion summary with evidence of checks run and residual concerns.

### 3.2 CLASP Alignment Goals

1. Preserve the three-agent CLASP model instead of reintroducing many visible specialist agents.
2. Keep lifecycle logic in a procedure/skill rather than bloating agent files.
3. Preserve single ownership:
   - agents own cognitive posture
   - instructions own domain knowledge
   - procedures own ordered steps
   - prompts own wiring
   - templates own structure
   - verification remains external to the agent
4. Keep review separate from implementation.
5. Preserve “Unknown” and “stop” as valid outcomes.

### 3.3 UX Goals

1. The user should invoke one visible orchestrator.
2. The orchestrator should call existing worker agents as hidden helpers.
3. The user should receive one coherent lifecycle status view instead of disconnected intermediate outputs.
4. The lifecycle should be inspectable without becoming noisy.

---

## 4. Non-Goals

1. Replacing the current CLASP three-agent architecture.
2. Turning the orchestrator into a direct code-editing agent.
3. Allowing uncontrolled recursive subagent graphs.
4. Guaranteeing complete autonomous delivery for every feature.
5. Eliminating the need for human judgment in ambiguous product or architecture decisions.
6. Replacing CI, test infrastructure, or real enforcement mechanisms.
7. Turning review findings into large, unconstrained rewrites.

---

## 5. Core Design Principles

1. **One visible coordinator, multiple hidden workers**
   - The user interacts with one lifecycle orchestrator.
   - Worker agents remain bounded and mostly hidden.

2. **Lifecycle logic belongs in a skill/procedure**
   - The orchestrator should delegate according to a defined procedure.
   - The agent file should not become a giant embedded workflow.

3. **Implementation and review must remain separate**
   - The implementation agent writes and edits code.
   - The reviewer reviews.
   - The orchestrator decides what happens next.

4. **Mechanical verification before adversarial review**
   - Basic checks should run before code review where possible.
   - Review should not waste time on obviously broken code that has not passed basic checks.

5. **Remediation must be surgical**
   - The fix loop should address blocking findings, not restart the feature from scratch.

6. **Bounded convergence**
   - The loop must have clear success conditions and clear stop conditions.
   - Endless autonomous retry is not acceptable.

7. **Small artifact surface**
   - Build the smallest implementation that can carry the orchestration honestly.

---

## 6. User Stories

### 6.1 Feature Delivery

As a developer, I want to give a feature specification to one orchestrator and have it drive planning, implementation, testing, and review so I do not have to manually route every phase.

### 6.2 Controlled Remediation

As a maintainer, I want review findings to be routed back into implementation in a structured and minimal way so the system converges instead of rewriting blindly.

### 6.3 CLASP Governance

As a CLASP maintainer, I want this capability implemented without violating single ownership and without reintroducing specialized-agent sprawl.

### 6.4 Safe Failure

As a user, I want the system to stop honestly when evidence is missing, checks are flaky, or the loop is not converging, rather than pretending the feature is done.

---

## 7. Scope

### In Scope

- one visible lifecycle orchestrator agent
- reuse of existing broad CLASP agents
- lifecycle procedure
- feature-delivery skill
- normalized review findings
- bounded remediation loop
- verification command integration
- success and stop conditions
- final lifecycle status summary

### Out of Scope

- automatic merge to main
- autonomous product decisions without evidence
- CI/CD orchestration beyond verification invocation
- organization-wide agent distribution design
- cloud-agent-specific deployment details
- advanced worktree isolation design
- dynamic creation of new agents at runtime

---

## 8. Proposed CLASP Artifact Architecture

## 8.1 Recommended New Artifacts

Minimal recommended first version:

- `.github/agents/feature-delivery-orchestrator.agent.md`
- `.github/skills/feature-delivery/SKILL.md`
- `.github/procedures/feature-delivery.procedure.md`
- `.github/prompts/implement-feature-lifecycle.prompt.md`
- `.github/templates/feature-delivery-report.template.md`
- `.github/instructions/feature-delivery.instructions.md`
- `scripts/verify-feature-slice.sh`

### Existing Artifacts Reused

- `.github/agents/software-engineer.agent.md`
- `.github/agents/code-reviewer.agent.md`
- `.github/agents/thinking-assistant.agent.md`
- existing stack instructions
- existing test strategy instructions
- existing code review skill or review instructions
- existing governance and CLASP instructions

---

## 8.2 Artifact Ownership

| Artifact                                 | Owns                                                                                     | Must NOT Own                                                     |
| ---------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `feature-delivery-orchestrator.agent.md` | orchestration posture, routing policy, loop control, stop/escalation conditions          | detailed workflow steps, verification rubric, code review rubric |
| `feature-delivery.procedure.md`          | ordered lifecycle phases, iteration semantics, handoff rules, required outputs per phase | global rules, template headings, verification policy             |
| `feature-delivery.instructions.md`       | lifecycle-specific conventions, remediation guidance, finding normalization rules        | global enforcement, output template                              |
| `implement-feature-lifecycle.prompt.md`  | task wiring, input expectations, agent selection, output mode                            | global governance, verification gates                            |
| `feature-delivery-report.template.md`    | final report headings and placeholders                                                   | policy, steps, routing logic                                     |
| `scripts/verify-feature-slice.sh`        | mechanical verification commands and exit status                                         | reasoning, agent policy                                          |
| existing worker agents                   | bounded cognition within their existing lane                                             | lifecycle ownership, final stop decisions                        |

---

## 9. Agent Model

## 9.1 Visible Agent

### Feature Delivery Orchestrator

Responsibilities:

- read the incoming feature specification
- determine whether lifecycle orchestration is appropriate
- invoke planning if needed
- select the next slice of work
- route implementation to `software-engineer`
- trigger verification
- route review to `code-reviewer`
- classify findings
- decide whether remediation is required
- repeat until convergence or stop condition
- produce the final lifecycle report

Constraints:

- must not edit files directly
- must not run arbitrary implementation itself if CLASP keeps edit authority solely with `software-engineer`
- must not embed all lifecycle logic in the agent file
- must not reinterpret non-blocking findings as blocking without evidence
- must not suppress unknowns or failed checks

## 9.2 Worker Agents

### `thinking-assistant`

Use for:

- plan synthesis
- task decomposition
- risk surfacing
- acceptance criteria clarification
- identifying missing evidence
- deciding sensible slice boundaries

Must not:

- implement code
- declare the feature done
- override verification outcomes

### `software-engineer`

Use for:

- implementing a slice
- editing files
- running verification commands
- applying remediation fixes
- producing implementation status and command outputs

Must not:

- perform final lifecycle stop decisions
- self-certify review completeness
- expand scope beyond the assigned slice without explicit instruction

### `code-reviewer`

Use for:

- adversarial review
- security, correctness, maintainability, test quality, and related review concerns
- returning normalized findings with severity and evidence

Must not:

- directly edit implementation
- own the overall lifecycle loop
- turn vague preferences into blocking defects

---

## 10. Execution Model

The lifecycle runs as a bounded state machine owned by the orchestrator.

## 10.1 High-Level State Flow

    Intake
      → Plan / Clarify
        → Select Slice
          → Implement
            → Verify
              → Review
                → Decision
                  → Remediate
                    → Verify
                      → Review
                        → Decision
                          → Finalize

## 10.2 State Definitions

### State 1 — Intake

Input:

- feature specification
- referenced files or directories
- acceptance criteria if provided
- constraints if provided

Actions:

- confirm the task is suitable for lifecycle orchestration
- detect missing critical inputs
- extract explicit acceptance criteria
- identify whether the feature must be split into slices

Output:

- lifecycle start record
- clarified goal statement
- initial scope summary
- missing-information list if applicable

### State 2 — Plan / Clarify

Agent:

- `thinking-assistant`

Actions:

- analyze the feature spec
- identify dependencies and likely affected areas
- propose slice boundaries
- identify testing approach
- identify risks and unknowns

Output:

- slice plan
- dependency/risk summary
- test strategy summary
- unresolved questions

### State 3 — Select Slice

Owner:

- orchestrator

Actions:

- choose the next smallest meaningful slice
- define the implementation objective for the slice
- define the local acceptance criteria for the slice
- define the verification scope for the slice

Output:

- current slice brief

### State 4 — Implement

Agent:

- `software-engineer`

Actions:

- modify only the files required by the current slice
- follow relevant stack instructions
- keep changes focused
- summarize what changed
- run designated verification commands if allowed in the same phase

Output:

- changed files
- implementation summary
- command log
- unresolved implementation issues

### State 5 — Verify

Mechanism:

- `scripts/verify-feature-slice.sh`
- or equivalent explicit command sequence

Required baseline:

- format/lint
- type checking if applicable
- tests relevant to the slice
- broader tests only if the feature or repo policy requires them

Actions:

- execute verification commands
- collect pass/fail results
- normalize command outcomes

Output:

- verification result
- failed commands
- failing files/tests
- raw command output location or summary

### State 6 — Review

Agent:

- `code-reviewer`

Actions:

- review the current diff and changed behavior
- use multi-aspect review guidance
- classify findings by severity and actionability
- distinguish blocking from non-blocking
- identify “needs human decision” issues

Output:

- normalized finding set

### State 7 — Decision

Owner:

- orchestrator

Actions:

- combine verification status and review findings
- decide one of:
  - proceed to next slice
  - remediate current slice
  - finalize feature
  - stop and escalate

Output:

- loop decision record

### State 8 — Remediate

Agent:

- `software-engineer`

Input restrictions:

- current blocking findings only
- failed verification outputs only
- current diff and relevant files only

Actions:

- apply minimal fixes
- preserve already-correct behavior
- avoid unrelated rewrites
- rerun verification

Output:

- remediation summary
- updated command results
- notes on unresolved blockers

### State 9 — Finalize

Owner:

- orchestrator

Actions:

- confirm all slices are done
- confirm required checks passed
- confirm no unresolved blocking findings remain
- record residual non-blocking concerns and assumptions
- produce a final lifecycle report

Output:

- completion report

---

## 11. Loop Semantics

## 11.1 When the Loop Repeats

Repeat the implementation loop when any of the following is true:

- required verification fails
- blocking review findings exist
- acceptance criteria for the current slice are not met
- the current slice is incomplete but still bounded

## 11.2 When the Loop Must NOT Repeat

Do not automatically repeat when:

- only non-blocking style concerns remain
- the next action requires a product decision
- the same blocker repeats without progress
- required context is missing
- verification is flaky and cannot be trusted
- the issue is outside the current slice’s allowed scope

## 11.3 Maximum Iterations

Recommended defaults:

- small feature: max 3 remediation loops
- medium feature: max 5 remediation loops
- large feature: split into more slices rather than raising iteration caps

The orchestrator must stop and report when the maximum iteration count is reached.

## 11.4 Anti-Thrashing Rules

The orchestrator must treat the loop as non-convergent if:

- the same blocking finding reappears unchanged twice
- code changes increase scope without reducing blockers
- verification failures move around without stabilizing
- the review returns broad, non-actionable findings repeatedly

In these cases, the orchestrator must stop and surface the reason.

---

## 12. Findings Normalization Schema

Review and verification outputs must be normalized into a shared schema so remediation is targeted.

## 12.1 Required Fields

Each finding must contain:

- `id`
- `title`
- `severity`
- `category`
- `scope`
- `evidence`
- `required_action`
- `confidence`
- `blocking`

## 12.2 Suggested Severity Levels

- `critical`
- `high`
- `medium`
- `low`
- `info`

## 12.3 Suggested Categories

- `functional`
- `test`
- `security`
- `maintainability`
- `reliability`
- `performance`
- `operational`
- `style`
- `needs-human-decision`

## 12.4 Blocking Rules

By default, these should be blocking:

- failed required verification
- correctness defects
- security defects
- missing required tests where policy requires them
- regressions against explicit acceptance criteria

By default, these should not be blocking unless policy says otherwise:

- minor naming/style preferences
- speculative refactor suggestions
- low-confidence opinions without evidence

## 12.5 Example Finding Record

    - id: CR-004
      title: Missing authorization check in update endpoint
      severity: high
      category: security
      scope: backend/api/users.py
      evidence: Endpoint updates user data without verifying ownership
      required_action: Add ownership or role-based authorization guard and test
      confidence: high
      blocking: true

---

## 13. Verification Model

## 13.1 Mechanical Verification Priority

The lifecycle must prefer mechanical verification before adversarial review whenever possible.

Recommended baseline order:

1. formatter / lint
2. type check
3. targeted tests
4. broader tests if needed
5. adversarial review

## 13.2 Verification Script

Suggested script responsibility:

- run required commands in a stable order
- stop on failure or continue with structured collection, depending on desired mode
- return machine-readable exit behavior
- emit short summaries that the orchestrator can interpret

## 13.3 Verification Modes

- `slice-only`: verify only the current slice’s relevant checks
- `feature-wide`: verify all checks required by the full feature
- `repo-gate`: broader checks required before final completion

Initial version should support at least:

- `slice-only`
- `feature-wide`

---

## 14. Inputs

## 14.1 Required Inputs

- feature specification
- target area or files/directories
- acceptance criteria or equivalent feature intent
- allowed evidence scope

## 14.2 Optional Inputs

- architecture constraints
- performance constraints
- security constraints
- test expectations
- rollout constraints
- migration requirements
- slice-size preference

## 14.3 Input Quality Requirements

The orchestrator must stop or ask for clarification when:

- the feature specification is too vague to define a slice
- the acceptance criteria are absent and cannot be inferred safely
- the relevant code area is not identified and cannot be located from evidence
- required referenced files are missing or unreadable

---

## 15. Outputs

## 15.1 Primary Output

A final lifecycle report containing:

- request summary
- scope summary
- slice history
- implementation summary
- verification evidence
- review findings summary
- remediation history
- completion status
- residual risks / non-blocking concerns
- explicit unknowns
- recommended next step

## 15.2 Intermediate Outputs

- plan summary
- current slice brief
- implementation summary
- verification summary
- normalized finding set
- remediation summary
- stop reason if halted

---

## 16. Prompt Wiring

## 16.1 Recommended Prompt

`implement-feature-lifecycle.prompt.md`

Responsibilities:

- select the orchestrator
- declare evidence scope
- declare the expected output template
- attach the lifecycle procedure
- attach relevant stack and testing instructions
- define stop conditions

## 16.2 Prompt Requirements

The prompt must:

- name the orchestrator explicitly
- reference the lifecycle procedure
- reference the final report template
- define whether the task is:
  - planning only
  - implementation only
  - full lifecycle
- define whether review remediation is enabled
- define whether the task is slice-bounded or feature-wide

---

## 17. Procedure Design

## 17.1 Procedure Responsibilities

`feature-delivery.procedure.md` should define:

- phase order
- required artifacts per phase
- how slice boundaries are determined
- how verification results are interpreted
- how findings are normalized
- loop entry and exit conditions
- stop conditions
- finalization requirements

## 17.2 Procedure Must Include

- preflight
- lifecycle phases
- loop rules
- failure handling
- escalation handling
- final report generation

## 17.3 Procedure Must NOT Include

- global CLASP governance
- agent definitions
- hardcoded repo-specific facts unless parameterized
- template structure

---

## 18. Skill Design

## 18.1 Skill Name

`feature-delivery`

## 18.2 Skill Responsibility

Package the lifecycle capability into a reusable CLASP workflow that can bundle:

- lifecycle instructions
- lifecycle procedure
- final report template
- example invocations
- optional verification script references

## 18.3 Why This Should Be a Skill

This is not a one-off prompt.

It is a reusable lifecycle capability with:

- ordered phases
- loop control
- reusable artifacts
- evolving examples
- likely future expansion

That fits the CLASP skill model better than hiding everything in a prompt or agent.

---

## 19. Recommended File Layout

    .github/
    ├── agents/
    │   ├── feature-delivery-orchestrator.agent.md
    │   ├── software-engineer.agent.md
    │   ├── code-reviewer.agent.md
    │   └── thinking-assistant.agent.md
    ├── instructions/
    │   ├── feature-delivery.instructions.md
    │   ├── implementation-remediation.instructions.md
    │   └── review-findings-normalization.instructions.md
    ├── procedures/
    │   └── feature-delivery.procedure.md
    ├── prompts/
    │   └── implement-feature-lifecycle.prompt.md
    ├── templates/
    │   └── feature-delivery-report.template.md
    └── skills/
        └── feature-delivery/
            └── SKILL.md

    scripts/
    └── verify-feature-slice.sh

---

## 20. Agent Example — Orchestrator

    ---
    name: Feature Delivery Orchestrator
    description: Orchestrates planning, implementation, verification, review, and remediation for a feature specification
    tools: ['agent', 'read', 'search', 'todo', 'vscode']
    agents: ['software-engineer', 'code-reviewer', 'thinking-assistant']
    ---

    You are a lifecycle coordinator for CLASP.

    Your responsibilities:
    - determine whether full lifecycle orchestration is appropriate
    - invoke planning when needed
    - select the next smallest meaningful slice
    - route implementation to software-engineer
    - ensure verification is run
    - route adversarial review to code-reviewer
    - normalize findings into blocking and non-blocking outcomes
    - loop only when required
    - stop honestly when not converging or when evidence is missing

    Constraints:
    - do not edit files directly
    - do not embed the whole procedure here
    - do not suppress failed checks
    - do not let review findings expand scope unnecessarily
    - do not mark the feature complete if blocking findings remain

Note:

The actual lifecycle logic should still live in the procedure and skill.

---

## 21. Review Integration

## 21.1 Existing Multi-Aspect Review Skill

The code review stage should reuse the existing multi-aspect review capability rather than creating a new review ontology.

The orchestrator should treat review as:

- a structured evidence-producing stage
- not as a freeform opinion generator

## 21.2 Required Review Output

The reviewer must provide:

- a normalized finding set
- not just prose comments

If current review output is too narrative, it must be adapted.

## 21.3 Required Review Questions

The code review phase should, at minimum, cover:

- correctness
- regression risk
- test adequacy
- security
- maintainability
- operational concerns where relevant

---

## 22. Remediation Design

## 22.1 Remediation Objective

Fix only what is required to clear:

- failed required checks
- blocking findings
- acceptance-criteria gaps

## 22.2 Remediation Input Contract

The remediation pass should receive:

- current slice brief
- current diff summary
- failed commands and outputs
- blocking findings only
- explicit “do not change” boundaries where needed

## 22.3 Remediation Guardrails

- do not rewrite unrelated areas
- do not “improve” code outside the blocking scope
- do not restart implementation from scratch unless the orchestrator explicitly approves that
- do not widen architecture unless the blocker requires it and the orchestrator authorizes it

---

## 23. Stop Conditions

The orchestrator must stop and report rather than continue looping when any of the following is true:

1. required files or context are missing
2. the feature specification is too vague for safe slicing
3. max iteration count is reached
4. the same blocking issue repeats without progress
5. verification is flaky and completion cannot be trusted
6. a product or architecture decision is required
7. the necessary change exceeds the allowed scope
8. the review output is too vague to remediate safely
9. the implementation phase cannot complete due to external dependency issues
10. no further safe automatic progress is possible

---

## 24. Success Criteria

The lifecycle may mark a feature as complete only when all of the following are true:

1. the feature’s acceptance criteria are satisfied within the allowed evidence scope
2. required verification passes
3. no blocking findings remain
4. no unresolved “needs-human-decision” items block delivery
5. the final report explicitly lists any remaining non-blocking concerns or assumptions

---

## 25. Acceptance Criteria for the Feature Itself

## 25.1 Functional Acceptance

1. A user can invoke one visible orchestrator with a feature specification.
2. The orchestrator can call the existing three broad CLASP agents as needed.
3. The orchestrator can execute or trigger verification between implementation and review.
4. The orchestrator can process normalized review findings.
5. The orchestrator can loop through remediation at least once.
6. The orchestrator can produce a final lifecycle report.

## 25.2 CLASP Acceptance

1. No lifecycle procedure logic is duplicated into the constitution.
2. No verification policy is embedded into worker agents.
3. The orchestrator does not become a direct editing super-agent unless CLASP explicitly changes that rule.
4. Existing agent boundaries remain meaningful.
5. The feature adds minimal visible-agent surface.

## 25.3 Quality Acceptance

1. The remediation loop converges on straightforward features.
2. The orchestrator stops honestly on non-convergent cases.
3. The review output is actionable enough to drive remediation.
4. The final report is auditable and bounded.

---

## 26. Risks and Mitigations

| Risk                                                | Impact                               | Mitigation                                                    |
| --------------------------------------------------- | ------------------------------------ | ------------------------------------------------------------- |
| Orchestrator becomes a god-prompt in agent form     | authority sprawl, maintenance burden | move lifecycle logic into procedure/skill; keep agent minimal |
| Review findings are too vague                       | non-convergent remediation           | enforce normalized finding schema                             |
| Implementation rewrites too much during remediation | drift, new bugs                      | constrain remediation to blocking findings only               |
| Loop repeats endlessly                              | wasted time, false confidence        | hard iteration caps and anti-thrashing rules                  |
| Worker agents start owning lifecycle policy         | boundary erosion                     | keep stop decisions in orchestrator only                      |
| Too many new specialist agents are added            | CLASP regression                     | reuse existing 3 broad agents and instructions                |
| Verification is expensive                           | slow iteration                       | support slice-bounded verification modes                      |
| Human decisions get buried                          | false autonomy                       | explicit `needs-human-decision` category                      |

---

## 27. Phased Rollout

## Phase 1 — Minimal Working Version

Deliver:

- `feature-delivery-orchestrator.agent.md`
- `feature-delivery.procedure.md`
- `feature-delivery/SKILL.md`
- `implement-feature-lifecycle.prompt.md`
- `verify-feature-slice.sh`

Reuse:

- existing 3 agents
- existing review capability

Goal:

prove the loop works for small features

## Phase 2 — Structured Reporting

Deliver:

- `feature-delivery-report.template.md`
- finding normalization instruction file
- remediation instruction file

Goal:

improve auditability and convergence

## Phase 3 — Expansion

Possible additions:

- slice policy tuning
- optional operations-focused review expansion
- optional handoff into background execution
- optional worktree isolation
- optional PR summary generation

Goal:

expand only after the minimal lifecycle is reliable

---

## 28. Example Invocation

### Example User Request

    @feature-delivery-orchestrator
    Implement the feature specification in docs/specs/add-user-archiving.md.
    Use the full lifecycle:
    - planning
    - implementation
    - verification
    - code review
    - remediation if needed
    Stop if the loop does not converge.

### Expected Lifecycle Behavior

1. orchestrator reads the feature spec
2. thinking-assistant decomposes the work
3. orchestrator selects the first slice
4. software-engineer implements that slice
5. verification script runs
6. code-reviewer reviews the current result
7. orchestrator decides:
   - continue to next slice
   - remediate
   - stop
8. final report is generated when finished or halted

---

## 29. Example Final Report Shape

# Feature Delivery Report

## 1. Request Summary

## 2. Scope and Constraints

## 3. Slice Plan

## 4. Slice Execution History

## 5. Verification Results

## 6. Review Findings Summary

## 7. Remediation History

## 8. Final Status

## 9. Residual Non-Blocking Concerns

## 10. Unknowns / Assumptions

## 11. Recommended Next Step

---

## 30. Explicit Design Decisions

1. The orchestrator is a coordinator, not a coder.
2. Existing broad CLASP agents are reused rather than replaced.
3. Lifecycle logic lives in procedure/skill artifacts.
4. Review findings must be normalized to enable remediation.
5. Verification must occur before completion.
6. The loop must be bounded and honest.

---

## 31. Open Questions

1. Should the orchestrator always require a formal feature specification file, or may it accept an inline specification?
2. Should verification default to slice-only or feature-wide mode?
3. Should the final completion report be mandatory for all runs or only for full-lifecycle runs?
4. Should the remediation loop ever be allowed to widen scope automatically?
5. Should the lifecycle support optional human approval checkpoints between review and remediation?

---

## 32. Recommendation

Implement the smallest honest version first:

- one visible orchestrator
- existing three broad agents reused as workers
- one lifecycle procedure
- one skill
- one verification script
- one normalized findings schema

Do not start by creating additional specialist agents.
Do not place the workflow inside the agent definition.
Do not allow unbounded autonomous retry.

The first version should optimize for:

- convergence
- observability
- bounded scope
- CLASP compatibility

rather than maximum automation.
