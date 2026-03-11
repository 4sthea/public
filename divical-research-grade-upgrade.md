# Divical Improvement Specification

## Moon-Dev-Inspired, Simulation-First Upgrade Plan for VSCode + GitHub Copilot

**Status:** Implemented (all 9 slices — see `research-grade-upgrade-implementation-plan.md`)  
**Audience:** GitHub Copilot agents, software engineer, architecture/refactoring agents  
**Scope:** `divical-api/`, `divical-web/`, docs, tests, CI  
**Primary goal:** Improve prediction correctness, research rigor, and implementation safety for a dividend-capture simulation platform  
**Non-goal:** Real-money trade execution

---

## 1. Purpose

This specification defines how to improve Divical in a way that is:

- technically realistic for the current codebase
- compatible with the current FastAPI + React + ARQ architecture
- useful for GitHub Copilot agents to implement incrementally
- aligned with Divical’s actual domain constraints (stocks, BDCs, dividend capture, simulation/prediction only)
- inspired by the useful parts of Moon Dev’s RBI philosophy without copying the parts that do not fit Divical

This is **not** a request to turn Divical into a crypto HFT system, browser agent swarm, or autonomous live trading bot.

---

## 2. Executive Assessment

## 2.1 What is already strong

Divical already has a strong foundation:

- provider abstraction
- cache-aware market data retrieval
- a substantial ML layer
- quantile enrichment
- a research pipeline with proposal evaluation
- an Agent Guard layer for LLM safety
- an RBI-style background process
- a React UI and WebSocket progress model

That is already more structured than the average “AI quant app” held together by vibes and terminal fumes.

## 2.2 What is still weak

The current architecture still has several high-impact gaps:

1. **Prediction labels are still vulnerable to look-ahead noise**
2. **Temporal leakage risk is not fully closed**
3. **Main-pipeline backtest validation is not rigorous enough**
4. **Small-data overfitting remains a core structural constraint**
5. **Rate/regime awareness exists, but is not yet treated as a first-class experimental axis**
6. **The main orchestration path is too large and hard to evolve safely**
7. **Operational maturity is behind research ambition**
   - missing automated tests
   - missing CI depth
   - missing observability
   - SQLite still too weak for concurrent research-heavy workflows
8. **The RBI loop is not yet a strong experiment system**
   - strategy discovery exists
   - proposal evaluation exists
   - proposal backtesting exists
   - but experiment lineage, evidence tracking, and simulation-forward validation need to be formalized

## 2.3 Strategic conclusion

The next phase should **not** be “add more AI.”
It should be:

- improve the scientific rigor of the prediction pipeline
- formalize the research/backtest/incubation lifecycle
- reduce architectural entropy
- make research outputs auditable and comparable
- keep implementation bounded and simulation-first

---

## 3. Design Stance

## 3.1 Core principle

Divical should evolve into a **research-grade, simulation-first strategy laboratory** for dividend stocks.

That means:

- research ideas are cheap
- backtests are reproducible
- forward simulation is explicit
- implementation is gated
- AI assists, but does not get to freestyle reality into existence

## 3.2 Adapt Moon Dev selectively

Adopt these ideas:

- RBI mindset: Research → Backtest → Incubate
- multi-agent research specialization
- consensus gating
- continuous idea generation
- strategy ranking via evidence, not persuasion
- simulation-forward validation before promotion

Do **not** adopt these yet:

- autonomous arbitrary code generation for novel strategies
- `while True` research daemons inside the app runtime
- live order routing
- microstructure/tick-data execution logic
- unrestricted self-debugging code loops
- AI-generated strategy code executed without a bounded DSL or template

---

## 4. Product Goal for This Upgrade

Transform Divical from:

> “A strong dividend-capture prediction app with research features”

into:

> “A reproducible, evidence-driven strategy discovery and simulation platform for dividend stocks, with safe AI-assisted research and a hardened experimental backbone.”

---

## 5. Success Criteria

The upgrade is successful when all of the following are true:

1. New strategy ideas can be discovered, backtested, and compared through a reproducible experiment pipeline.
2. The main ML pipeline uses cleaner labels and stronger temporal validation.
3. Forward simulation / incubation is a first-class status, separate from historical backtest approval.
4. All major research outputs have machine-readable evidence and lineage.
5. The research pipeline can safely ingest untrusted text without bypassing Agent Guard.
6. The system can be evolved without further bloating `RunExecutor` into a cathedral of pain.
7. The repo has a minimum viable safety net:
   - unit tests
   - integration tests
   - CI
   - structured experiment logging
   - observability hooks

---

## 6. Non-Goals

The following are explicitly out of scope for this specification:

- broker integration
- real-money trading
- options execution
- HFT / order book strategies
- live authenticated browsing agents
- auto-merge from research to implementation
- fully autonomous AI-generated strategy code execution without bounded templates

---

## 7. Fact / Assumption Boundary

## 7.1 Verified baseline from the uploaded docs

The uploaded docs support the following baseline:

- Divical uses a FastAPI backend and React frontend.
- Divical has a 13-model ensemble and quantile enrichment.
- Divical documents a research pipeline with Sentinel, Sentiment, Academic Scout, and Synthesizer agents.
- Divical documents a proposal evaluator and proposal backtester.
- Divical documents Agent Guard as the prompt-injection defense layer.
- Divical documents active risks: look-ahead labels, temporal leakage risk, weak observability, SQLite limitations, and limited backtest validation.

## 7.2 Not treated as verified facts here

The following are not assumed as truth unless already supported by the uploaded docs:

- the exact internals of Moon Dev’s private implementations
- claims that a specific Moon Dev technique is already fully implemented in Divical unless the uploaded docs say so
- any claim that “institutional-grade” automatically means scientifically validated

---

## 8. High-Level Improvement Themes

This specification is organized around seven improvement themes:

1. **Platform Hardening**
2. **Prediction Correctness**
3. **Regime / Factor Intelligence**
4. **RBI Lifecycle Hardening**
5. **Research Governance and Safety**
6. **Architecture Refactoring**
7. **UX for Strategy Discovery and Simulation**

---

# 9. Epic A — Platform Hardening

## Objective

Establish the minimum operational foundation needed before expanding autonomous research further.

## Problem

The docs explicitly identify operational debt:

- no automated test suite
- no meaningful observability
- SQLite unsuitable for concurrent production-like workloads
- limited validation visibility

If this is not fixed, research velocity will outpace correctness.

## Required Changes

### A1. Introduce a minimum viable test strategy

Create test coverage at four layers:

- **unit tests**
  - feature engineering helpers
  - label generation
  - risk scoring
  - scheduling algorithm
  - Agent Guard detectors and validators
- **integration tests**
  - provider abstraction + cache
  - run execution with mock provider
  - research pipeline with mocked LLM responses
- **contract tests**
  - backend Pydantic ↔ frontend TypeScript shape alignment
  - provider interface conformance
- **system tests**
  - create portfolio → start run → receive progress → view results
  - research proposal → evaluator → backtester → dashboard

### A2. Add CI gates

Add GitHub Actions workflows for:

- Python lint + type check + tests
- frontend build + tests
- schema and docs validation
- optional nightly experiment regression job

### A3. Move research-heavy paths to PostgreSQL

Keep SQLite for quick local dev if desired, but define PostgreSQL as the authoritative runtime for:

- concurrent research pipeline execution
- proposal storage
- experiment lineage
- forward simulation artifacts
- richer reporting queries

### A4. Add observability primitives

Implement:

- structured run IDs
- experiment IDs
- proposal IDs
- strategy candidate IDs
- JSON logs for all RBI stages
- metrics counters/timers for:
  - proposal counts
  - approval rates
  - backtest pass rates
  - incubation pass rates
  - LLM validation failures
  - Agent Guard blocks/quarantines

## Suggested Files

### Backend

- `app/observability/metrics.py` _(new)_
- `app/observability/tracing.py` _(new)_
- `app/testing/` _(new helpers)_
- `tests/unit/...`
- `tests/integration/...`
- `tests/system/...`

### CI

- `.github/workflows/ci.yml`
- `.github/workflows/research-regression.yml`

## Acceptance Criteria

- CI blocks merges on failing tests
- backend and frontend both have automated tests
- PostgreSQL is supported end-to-end for research flows
- every research/backtest/incubation event emits machine-readable identifiers
- the system can answer: “why was this strategy approved?”

---

# 10. Epic B — Prediction Correctness Overhaul

## Objective

Improve the scientific quality of the prediction pipeline before adding more strategic complexity.

## Problem

The current system still documents a high-impact label problem and potential temporal leakage. That makes model sophistication less trustworthy than it looks.

## Required Changes

### B1. Replace global-extremum labels with cleaner targets

Current issue:

- training labels are based on hindsight-optimal minima/maxima

Replace with configurable label families:

1. **smoothed-offset labels**
   - derive buy/sell targets from smoothed price curves
2. **percentile-based labels**
   - buy near lower percentile of pre-ex window
   - sell near upper percentile of post-ex window
3. **return-conditioned pair labels**
   - label candidate `(buy_offset, sell_offset)` pairs by profitability instead of “exact optimal day”

### B2. Split “offset prediction” from “trade viability”

Introduce explicit dual-stage inference:

- **Stage 1:** trade viability classifier
  - “Is this candidate worth taking?”
- **Stage 2:** timing estimator
  - “If yes, what buy/sell timing range is reasonable?”

This makes the system less brittle than forcing exact-day regression on noisy labels.

### B3. Enforce point-in-time feature construction

Create a strict rule:

- any feature used for a historical sample must be reconstructable from information available at that historical timestamp

This includes:

- market context
- rate context
- fundamentals
- sentiment
- ticker context
- regime state

Introduce a validation mode that fails if a feature depends on future information.

### B4. Add walk-forward / temporal CV as default evaluation mode

Replace or supplement simple split logic with:

- rolling-origin validation
- walk-forward evaluation
- calibration-by-window tracking
- per-regime performance slices

### B5. Add baseline-first evaluation

Every major ML change must be compared against:

- deterministic baseline strategy
- current production ensemble
- new experimental model

Do not allow “fancy model beats air” as evidence.

## Suggested Files

### New

- `app/ml/labels.py`
- `app/ml/sample_builder.py`
- `app/ml/evaluation/temporal_validation.py`
- `app/ml/evaluation/baselines.py`
- `app/ml/evaluation/metrics.py`
- `app/ml/evaluation/calibration_report.py`

### Existing to refactor

- `app/ml/features.py`
- `app/ml/model_manager.py`
- `app/ml/meta_labeler.py`
- `app/services/run_executor.py`

## Data Model Changes

Add experiment/result tables for:

- label version
- feature snapshot version
- training window
- validation window
- baseline comparison
- calibration metrics

## Acceptance Criteria

- label generation is versioned
- a model artifact can be tied to a specific label strategy
- temporal CV is the default experiment path
- feature leakage checks exist and fail closed
- each model run produces comparable metrics versus deterministic baselines

---

# 11. Epic C — Regime and Factor Intelligence

## Objective

Treat rate sensitivity and market regime as core explanatory variables, not side decorations.

## Problem

The docs repeatedly emphasize rate sensitivity, regime awareness, and BDC-specific structure. Divical already has regime logic and factor-aware components, but they are not yet formalized as a coherent experiment system.

## Required Changes

### C1. Formalize factor inputs

Promote these to first-class, versioned features:

- BIZD / sector proxy returns
- SPY / market returns
- treasury yield changes
- yield curve shape
- VIX or volatility proxy
- credit-spread proxy if available
- earnings proximity
- dividend surprise / consistency features

### C2. Distinguish static regime rules from learned regime models

Support two regime modes:

1. **Rule-based regime**
   - current deterministic implementation
2. **Learned regime**
   - hidden-state / clustering / HMM-like or similar experimental regime models

Important:

- do not replace the current rule-based mode blindly
- compare learned regimes against rule-based regimes empirically

### C3. Add regime-conditioned evaluation

Every backtest and simulation report should show:

- performance by regime
- confidence by regime
- drawdown by regime
- recovery time by regime
- false-positive rate by regime

### C4. Dynamic model weighting

Use recent accuracy and regime-conditioned performance to adapt ensemble weights.

This must be evidence-driven and versioned, not magical hand-tuning.

## Suggested Files

### New

- `app/strategies/regime_models.py`
- `app/ml/evaluation/regime_report.py`
- `app/ml/weights/dynamic_weighting.py`

### Existing

- `app/strategies/regime.py`
- `app/strategies/ensemble.py`
- `app/services/market_context.py`
- `app/ml/model_manager.py`

## Acceptance Criteria

- rule-based and learned regime modes can be compared side by side
- experiment reports include regime slices
- dynamic weighting can be turned on/off by config
- regime metadata is stored with predictions and backtests

---

# 12. Epic D — RBI Lifecycle Hardening

## Objective

Turn the current research pipeline into a proper experiment lifecycle:
**Research → Backtest → Incubate → Simulate Review**

## Problem

The current docs describe research, proposal evaluation, proposal backtesting, and even `incubating` status. That is good. But the lifecycle needs stronger contracts, lineage, and forward-simulation semantics.

## Required Changes

### D1. Rename the operational meaning of “I”

For Divical, the “I” phase must mean:

- **Incubate**
- **Forward simulation**
- **Shadow-mode validation**

Not live deployment.

### D2. Add explicit strategy lifecycle states

At minimum:

- `proposed`
- `approved_for_backtest`
- `backtesting`
- `backtest_failed`
- `backtest_passed`
- `incubating`
- `incubation_failed`
- `incubation_passed`
- `promoted_to_simulation_dashboard`
- `archived`

### D3. Add experiment lineage

For each strategy candidate, record:

- proposal source
- originating agents
- source materials
- strategy hypothesis
- parameter space
- backtest configuration
- validation windows
- incubation window
- promotion rationale

### D4. Introduce a bounded strategy definition format

Do **not** start with arbitrary AI-generated Python code.

Instead, define a strategy proposal DSL or structured template such as:

- entry logic type
- exit logic type
- offset policy
- filters
- factor modifiers
- risk gates
- position-sizing policy for simulation
- required inputs
- unsupported requirements

Only strategies representable in this bounded format may be auto-backtested in V1.

### D5. Add incubation / forward simulation

When a strategy passes backtest gates:

- simulate it on newly arriving market data
- compare predicted outcomes vs realized outcomes
- track confidence drift
- require a minimum incubation horizon before promotion

### D6. Build an evidence ledger

Each strategy should have machine-readable evidence such as:

- backtest metrics
- regime slices
- calibration quality
- incubation performance
- failure cases
- why the evaluator swarm approved it

## Suggested Files

### New

- `app/research/contracts/strategy_spec.py`
- `app/research/contracts/evidence_ledger.py`
- `app/research/contracts/experiment_manifest.py`
- `app/research/incubation/forward_simulator.py`
- `app/research/incubation/incubation_evaluator.py`

### Existing

- `app/services/research/orchestrator.py`
- `app/services/research/agents.py`
- `app/services/research/strategy_evaluator.py`
- `app/services/research/proposal_backtester.py`
- `app/workers/rbi_pipeline.py`

## DB Changes

Add or extend tables for:

- experiment manifest
- incubation observations
- approval decisions
- evaluator votes
- evidence ledger
- strategy state transitions

## Acceptance Criteria

- a discovered strategy has a complete lifecycle record
- no strategy is promoted without backtest + incubation evidence
- auto-backtesting only consumes bounded strategy specs
- the dashboard can show why a strategy is in its current state

---

# 13. Epic E — Research Governance and Safety

## Objective

Keep the research loop useful without letting untrusted content, LLM drift, or vague proposals poison the system.

## Problem

Divical already has Agent Guard and a research pipeline. Good. The next step is not “more agent freedom.” The next step is stronger contracts and stricter research outputs.

## Required Changes

### E1. Standardize agent output contracts

Every research agent must emit structured outputs with fields like:

- `hypothesis`
- `mechanism`
- `required_inputs`
- `assumptions`
- `expected_edge`
- `risk_factors`
- `evaluation_plan`
- `unsupported_claims`
- `confidence`
- `citations_or_source_refs`

### E2. Add proposal quality filters

Reject proposals that are:

- too vague
- not testable with current data
- dependent on unsupported inputs
- incompatible with stock/dividend simulation
- merely a rephrasing of an existing strategy
- impossible to evaluate point-in-time

### E3. Add strategy deduplication and novelty scoring

Before backtesting a proposal:

- compare against existing strategies
- cluster similar hypotheses
- avoid backtesting duplicates with cosmetic renaming

### E4. Extend Agent Guard coverage

Ensure Agent Guard is applied consistently to:

- external research text
- agent-to-agent outputs
- evaluator inputs
- any user-supplied free text used by the research pipeline

### E5. Add proposal explainability snapshots

Store compact reasoning summaries:

- why this proposal exists
- what it depends on
- what would falsify it

## Suggested Files

### New

- `app/services/research/proposal_quality.py`
- `app/services/research/proposal_deduper.py`
- `app/services/research/contracts.py`
- `app/services/research/novelty.py`

### Existing

- `app/agent_guard/...`
- `app/services/research/agents.py`
- `app/services/research/strategy_evaluator.py`

## Acceptance Criteria

- every proposal is machine-testable or rejected
- duplicate proposals are detected
- unsupported strategies are filtered before backtesting
- agent outputs are structured and validated

---

# 14. Epic F — Architecture Refactoring

## Objective

Reduce change risk and make Copilot-guided implementation safer.

## Problem

The onboarding docs explicitly call out `RunExecutor` as a high-complexity hotspot and `PortfolioDetailPage.tsx` as a frontend kitchen sink. Large orchestration files are where correctness goes to die wearing a fake smile.

## Required Changes

### F1. Decompose `RunExecutor`

Split into explicit phase services:

- `Phase1DataFetcher`
- `Phase2Predictor`
- `Phase3HistoricalStrategist`
- `Phase4FuturePredictor`
- `Phase5QuantileEnricher`
- `RunPersistenceService`
- `RunProgressReporter`

### F2. Extract experiment evaluation concerns from `ModelManager`

Move non-core responsibilities out of `ModelManager`:

- evaluation
- calibration reports
- dynamic weights
- validation
- experiment metadata

### F3. Decompose `PortfolioDetailPage.tsx`

Split into:

- portfolio overview
- stock list / cards
- holdings section
- dividend calendar
- strategy configuration dialog
- run launcher
- news / research panel

### F4. Centralize defaults and config schemas

Eliminate drift between:

- backend defaults
- frontend defaults
- docs examples

Generate or validate shared config shapes where feasible.

## Suggested Files

### Backend

- `app/services/run_phases/` _(new package)_
- `app/services/run_executor.py` _(thin coordinator after refactor)_

### Frontend

- `src/pages/portfolio-detail/`
- `src/components/portfolio/`
- `src/lib/config-schema.ts` or generated types

## Acceptance Criteria

- `RunExecutor` becomes orchestration-only
- business logic is testable outside the top-level runner
- `PortfolioDetailPage.tsx` is reduced to composition
- backend/frontend config drift is measurably reduced

---

# 15. Epic G — Strategy Discovery UX and Simulation UX

## Objective

Make the RBI system understandable and useful to a human reviewer.

## Problem

A research engine without a good review surface becomes a markdown landfill with ambitions.

## Required Changes

### G1. Upgrade the RBI dashboard

Add views for:

- proposals
- backtests
- incubating strategies
- promoted simulation strategies
- rejected strategies
- evidence details

### G2. Add side-by-side comparisons

Allow comparison of:

- baseline strategy
- current production strategy
- new candidate strategy

Across:

- return
- Sharpe/Sortino
- drawdown
- win rate
- exposure time
- regime breakdown
- calibration

### G3. Add confidence decomposition

Expose where confidence came from:

- ensemble agreement
- meta-labeler score
- quantile calibration
- regime penalty
- sentiment gate
- evaluator confidence

### G4. Add shadow-mode analytics

For strategies blocked or rejected by the swarm:

- log the hypothetical outcome
- show whether the gate helped or hurt

This is how you learn whether the AI guardrails add value or just ceremonial incense.

## Suggested Files

### Frontend

- `src/pages/RBIDashboardPage.tsx`
- `src/components/rbi/ProposalTable.tsx`
- `src/components/rbi/EvidencePanel.tsx`
- `src/components/rbi/ComparisonView.tsx`
- `src/components/rbi/IncubationTimeline.tsx`

### Backend

- `app/api/routes/strategies.py`
- `app/api/routes/research.py`
- `app/services/reporting/` _(new)_

## Acceptance Criteria

- a reviewer can understand a candidate strategy without reading logs
- blocked/rejected decisions are inspectable
- incubation state is visible
- strategy comparisons are available in the UI

---

# 16. Recommended Implementation Order

## Phase 0 — Guardrails and infrastructure

1. tests
2. CI
3. PostgreSQL support for research-heavy flows
4. observability primitives

## Phase 1 — Correctness first

5. point-in-time sample builder
6. label versioning and cleaner labels
7. temporal CV and baseline comparison
8. experiment manifests and evidence ledger

## Phase 2 — RBI hardening

9. bounded strategy proposal format
10. proposal quality filter and dedupe
11. incubation / forward simulation
12. lifecycle state model

## Phase 3 — architecture cleanup

13. `RunExecutor` decomposition
14. `PortfolioDetailPage` decomposition
15. config/default unification

## Phase 4 — higher-order modeling

16. regime-conditioned evaluation
17. dynamic weights
18. richer factor set
19. optional learned regime experiments

## Phase 5 — advanced strategy families

20. pre-ex run-up strategy branch
21. multi-horizon blending
22. portfolio-level scheduling improvements

---

# 17. Prioritization Matrix

## Highest priority

These should be implemented before any bigger Moon-Dev-style autonomy push:

- platform hardening
- label cleanup
- temporal leakage control
- temporal CV
- evidence ledger
- incubation / forward simulation
- `RunExecutor` decomposition

## Medium priority

- dynamic weights
- proposal dedupe
- richer factor modeling
- dashboard improvements
- comparison analytics

## Lower priority / experimental

- learned regime models
- online learning
- arbitrary strategy code generation
- options-dependent strategy branches
- advanced microstructure ideas

---

# 18. Suggested New Data Model Additions

## Strategy experiment models

### `ExperimentManifest`

Tracks:

- strategy candidate ID
- label version
- feature version
- training window
- validation window
- backtest parameters
- evaluator vote summary

### `EvidenceLedger`

Tracks:

- metrics
- failure modes
- regime slices
- calibration results
- incubation stats
- source references

### `IncubationObservation`

Tracks:

- simulated entry/exit timestamps
- predicted outcome
- realized outcome
- confidence drift
- block/approve decision effects

### `StrategyStateTransition`

Tracks:

- from_state
- to_state
- timestamp
- actor
- rationale

---

# 19. Suggested Copilot Work Breakdown

Use Copilot/agents to implement in bounded vertical slices, not one giant heroic prompt.

## Slice 1

Test foundation + CI

## Slice 2

Point-in-time feature reconstruction + leakage checks

## Slice 3

Label versioning + smoothed/percentile labels

## Slice 4

Temporal CV + evaluation reports

## Slice 5

Experiment manifest + evidence ledger

## Slice 6

Proposal quality filter + bounded proposal schema

## Slice 7

Incubation / forward simulator

## Slice 8

`RunExecutor` phase extraction

## Slice 9

RBI dashboard upgrade

Each slice should end with:

- code
- tests
- docs
- migration notes if applicable

---

# 20. Implementation Rules for Copilot Agents

## Required rules

1. Do not assume live trading.
2. Do not introduce broker APIs.
3. Do not implement autonomous code execution from LLM strategy proposals.
4. Prefer bounded schemas over free-form text.
5. Every research-stage decision must be auditable.
6. Every ML experiment must be reproducible.
7. New models must beat deterministic baselines or remain experimental.
8. No feature may use future data in historical samples.
9. Preserve provider abstraction.
10. Preserve Agent Guard boundaries.

## Stop conditions

Stop and escalate if:

- required data is not point-in-time reconstructable
- a proposed strategy depends on unsupported data sources
- a new model has no measurable win over the baseline
- a feature requires real trading despite simulation-only scope
- a prompt/agent workflow would bypass Agent Guard or evidence logging

---

# 21. Definition of Done

This specification is considered implemented when:

- Divical can discover, backtest, incubate, and compare strategies through a reproducible RBI lifecycle
- the main prediction pipeline has cleaner labels and stronger temporal validation
- experiment lineage and evidence are first-class data
- the research pipeline is structured, deduplicated, and safely bounded
- `RunExecutor` is decomposed into testable services
- the RBI dashboard exposes proposal → backtest → incubation → promotion flow
- CI, tests, and observability exist at a meaningful baseline level

---

# 22. Final Recommendation

The correct next move is **not** to imitate Moon Dev literally.

The correct next move is to build the version of RBI that fits Divical’s reality:

- stock-based, not crypto-HFT
- simulation-first, not live-trading
- evidence-first, not autonomous-code-first
- bounded and testable, not “the agent vibes were immaculate”

That path gives Divical a far better chance of becoming genuinely useful instead of merely sounding sophisticated in a README.
