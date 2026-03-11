# Research-Grade Upgrade — Implementation Plan

> **Status: IMPLEMENTED** — All 9 slices complete. 112 tests passing. CI green.

**Source spec:** `docs/features/divical-research-grade-upgrade.md`
**Target agent:** Software Engineer
**Scope:** 9 implementation slices, broken into atomic coding tasks
**Branching:** Each slice should be a separate branch off `master`

---

## Implementation Summary

| Slice     | Name                                                  | Status         | Tests   |
| --------- | ----------------------------------------------------- | -------------- | ------- |
| 1         | Test Foundation + CI Hardening                        | ✅ Implemented | 15      |
| 2         | Observability Primitives                              | ✅ Implemented | 8       |
| 3         | Point-in-Time Feature Reconstruction + Leakage Checks | ✅ Implemented | 9       |
| 4         | Label Versioning + Cleaner Labels                     | ✅ Implemented | 14      |
| 5         | Temporal CV + Baseline Evaluation                     | ✅ Implemented | 10      |
| 6         | Experiment Manifest + Evidence Ledger                 | ✅ Implemented | 14      |
| 7         | Proposal Quality + Bounded Strategy Schema            | ✅ Implemented | 16      |
| 8         | RunExecutor Decomposition                             | ✅ Implemented | 12      |
| 9         | Incubation / Forward Simulation                       | ✅ Implemented | 14      |
| **Total** |                                                       |                | **112** |

---

## How to Use This Plan

Each **Slice** is an independent vertical of work that produces shippable code + tests.
Within each slice, **Tasks** are ordered sequentially — complete them one at a time.

Tasks marked `[EXISTING]` modify existing files. Tasks marked `[NEW]` create new files.
Every task ends with a **Done-when** gate — the minimum condition to move on.

---

## Slice 1 — Test Foundation + CI Hardening ✅

**Goal:** Establish the safety net that all subsequent slices depend on.

### Existing state

- Tests exist in `divical-api/tests/` (agent_guard suite, plus 5 research/ML test files)
- CI exists at `.github/workflows/ci.yml` (ruff + compileall + pytest, 28 lines)
- No frontend tests
- No test directory structure beyond flat files + agent_guard/

### Task 1.1 — Restructure test directories `[NEW]`

Create the directory scaffold for organized tests:

```
tests/
  unit/
    ml/
      __init__.py
    services/
      __init__.py
    strategies/
      __init__.py
    __init__.py
  integration/
    __init__.py
  system/
    __init__.py
  conftest.py          (keep existing, extend)
  agent_guard/         (keep existing)
```

Create `__init__.py` files for each new directory. Do not move existing tests yet — that happens in later tasks.

**Done-when:** `pytest` still passes with the new directories present. All `__init__.py` files exist.

### Task 1.2 — Add unit test helpers and fixtures `[NEW]`

Create `tests/unit/conftest.py` with:

- A `mock_market_context()` fixture returning a `MarketContext` with realistic defaults
- A `mock_ticker_context()` fixture returning a `TickerContext` with realistic defaults
- A `sample_strategy_options()` fixture returning a `StrategyOptions` with safe defaults
- A `sample_trading_options()` fixture returning a `TradingOptions` with safe defaults

Import the real dataclasses/models from `app.ml.features` and `app.models.domain`.

**Done-when:** Fixtures can be imported and instantiated in a trivial test. `pytest tests/unit/` passes.

### Task 1.3 — Add unit tests for feature engineering `[NEW]`

Create `tests/unit/ml/test_features.py`:

- Test `MarketContext.to_features()` returns expected key count and value ranges
- Test `TickerContext.to_features()` returns expected key count and value ranges
- Test that `FeatureExtractor` (if it has a standalone method) produces deterministic output for fixed input
- Test edge cases: zero/None fields don't crash `to_features()`

**Done-when:** At least 4 passing tests in `test_features.py`.

### Task 1.4 — Add unit tests for strategy base/ensemble `[NEW]`

Create `tests/unit/strategies/test_ensemble.py`:

- Test `EnsembleAggregator` with mocked model predictions produces a combined result
- Test that missing predictions (empty list) are handled without crash
- Test weight application if configurable

Create `tests/unit/strategies/test_regime.py`:

- Test regime classification with known inputs
- Test boundary conditions (e.g., threshold values)

**Done-when:** At least 3 passing tests across these files.

### Task 1.5 — Add integration test for run execution `[NEW]`

Create `tests/integration/test_run_executor.py`:

- Use the Mock provider (already exists in `app/providers/`)
- Create a `RunExecutor` with 1 ticker and default options
- Patch or mock the ML model layer to return dummy predictions
- Assert the executor completes without error and produces a `StrategyResult`

**Done-when:** 1 passing integration test that exercises the full RunExecutor flow with mocked data.

### Task 1.6 — Harden CI workflow `[EXISTING]`

Modify `.github/workflows/ci.yml`:

- Add `pyright` type checking step (install pyright, run `pyright divical-api/app/`)
- Add a frontend step: checkout → `npm ci` → `npm run build` → `npm run lint` (in `divical-web/`)
- Add test coverage reporting with `pytest --cov=app --cov-report=term-missing`
- Set `fail-fast: false` on matrix to see all failures

**Done-when:** CI runs backend lint + typecheck + tests + frontend build + lint. Merge-blocking on failure.

### Task 1.7 — Add frontend build smoke test `[NEW]`

Create `divical-web/src/__tests__/App.test.tsx` (or similar):

- Render `<App />` wrapped in required providers (QueryClient, BrowserRouter)
- Assert it mounts without throwing

Add vitest config if not present:

- Add `vitest` + `@testing-library/react` + `jsdom` to devDependencies in `package.json`
- Add test script to `package.json`: `"test": "vitest run"`
- Add vitest config in `vite.config.ts` or separate `vitest.config.ts`

**Done-when:** `npm test` passes with 1 smoke test. CI includes this step.

---

## Slice 2 — Observability Primitives ✅

**Goal:** Every research/backtest/run event emits structured, machine-readable identifiers. Answers "why was this strategy approved?" become possible.

### Task 2.1 — Create observability module `[NEW]`

Create `divical-api/app/observability/__init__.py` and `divical-api/app/observability/metrics.py`:

Define a `MetricsCollector` class (or simple module-level functions) that tracks counters:

- `proposal_created`
- `proposal_approved`
- `proposal_rejected`
- `backtest_started`
- `backtest_passed`
- `backtest_failed`
- `incubation_started`
- `incubation_passed`
- `incubation_failed`
- `agent_guard_blocked`
- `agent_guard_quarantined`

Use structlog for structured JSON log emission. Each event gets a `run_id`, `experiment_id`, `proposal_id`, or `strategy_id` as applicable. Store counters in a simple dict for now (no external metrics backend yet).

**Done-when:** `MetricsCollector` can be imported, `increment("proposal_created", run_id=...)` emits a structlog event. Unit test confirms emission.

### Task 2.2 — Create structured ID generation `[NEW]`

Create `divical-api/app/observability/ids.py`:

Define ID generators for:

- `experiment_id` — UUID prefixed with `exp-`
- `proposal_id` — UUID prefixed with `prop-`
- `strategy_candidate_id` — UUID prefixed with `strat-`
- `incubation_id` — UUID prefixed with `inc-`

Each returns a string. These will be used by later slices to tag records.

**Done-when:** Functions importable and produce unique, prefixed IDs. Unit test confirms format.

### Task 2.3 — Wire metrics into research orchestrator `[EXISTING]`

Modify `divical-api/app/services/research/orchestrator.py`:

- Import `MetricsCollector`
- Emit `proposal_created` when a new proposal is generated
- Emit `proposal_approved` / `proposal_rejected` after evaluation
- Emit `backtest_started`, `backtest_passed`, `backtest_failed` at the right lifecycle points
- Add `experiment_id` to the `ResearchRunResult` dataclass

**Done-when:** Running the research pipeline emits structured log events with IDs. Existing tests still pass.

### Task 2.4 — Wire metrics into Agent Guard pipeline `[EXISTING]`

Modify `divical-api/app/agent_guard/pipeline.py`:

- Import `MetricsCollector`
- Emit `agent_guard_blocked` when a message is blocked
- Emit `agent_guard_quarantined` when a message is quarantined
- Include the triggering detector name in the log

**Done-when:** Agent Guard tests still pass. Blocked/quarantined events emit structured logs.

---

## Slice 3 — Point-in-Time Feature Reconstruction + Leakage Checks ✅

**Goal:** Every feature used for a historical sample is reconstructable from information available at that timestamp. Leakage is caught, not hoped away.

### Task 3.1 — Add point-in-time validation to FeatureExtractor `[EXISTING]`

Modify `divical-api/app/ml/features.py`:

Add a `validate_point_in_time(sample_date: date, features: dict) -> list[str]` function:

- Check that no feature key references data after `sample_date`
- Return a list of violation descriptions (empty = clean)

This is a validation utility, not a full rewrite. It checks the feature dict against the sample timestamp.

Add a `STRICT_PIT_MODE` flag (default `False` for now, `True` in tests). When `True`, feature extraction raises `TemporalLeakageError` if violations are found.

**Done-when:** `validate_point_in_time()` exists. A unit test with a deliberately leaking feature returns a violation. A clean feature returns none.

### Task 3.2 — Create sample builder `[NEW]`

Create `divical-api/app/ml/sample_builder.py`:

Define `SampleBuilder` class:

- `build_training_samples(tickers, start_date, end_date, provider) -> list[TrainingSample]`
  - For each ticker and ex-date in the window:
    - Fetch data available **up to** the sample date only
    - Build `MarketContext` and `TickerContext` from point-in-time data
    - Extract features
    - Run `validate_point_in_time()` in strict mode
    - Attach the label (see Slice 4 for label versioning — for now, use the existing label method)
- Returns a list of `TrainingSample` objects

**Done-when:** `SampleBuilder` produces samples for a mock provider. Unit test confirms no leakage violations on clean data.

### Task 3.3 — Add leakage detection test suite `[NEW]`

Create `tests/unit/ml/test_leakage.py`:

- Test that `validate_point_in_time()` catches a feature timestamped after the sample date
- Test that `validate_point_in_time()` passes a feature set built from historical data only
- Test that `SampleBuilder` in strict mode raises on a provider that returns future data
- Test that `SampleBuilder` in non-strict mode logs a warning but continues

**Done-when:** 4+ passing tests. All leakage scenarios are covered.

---

## Slice 4 — Label Versioning + Cleaner Labels ✅

**Goal:** Labels are versioned and configurable. Models can be tied to a specific label strategy. Cleaner alternatives to global-extremum labels are available.

### Task 4.1 — Create label module `[NEW]`

Create `divical-api/app/ml/labels.py`:

Define a `LabelStrategy` Protocol:

```python
class LabelStrategy(Protocol):
    name: str
    version: str
    def compute(self, prices: list[float], ex_date_index: int, **kwargs) -> dict: ...
```

Implement three concrete strategies:

1. `GlobalExtremumLabels` — wraps the current logic (extract from existing code)
2. `SmoothedOffsetLabels` — derive buy/sell targets from smoothed (SMA/EMA) price curves
3. `PercentileLabels` — buy near lower percentile of pre-ex window, sell near upper percentile of post-ex window

Each returns a dict with at least: `buy_offset`, `sell_offset`, `label_version`, `label_strategy_name`.

**Done-when:** All three strategies importable and produce valid label dicts for sample price arrays. Unit tests for each.

### Task 4.2 — Add label configuration to StrategyOptions `[EXISTING]`

Modify `divical-api/app/models/domain.py`:

- Add `label_strategy: str = "global_extremum"` field to `StrategyOptions`
- Add `label_version: str = "v1"` field to `StrategyOptions`

**Done-when:** `StrategyOptions` serializes/deserializes with the new fields. Defaults preserve backward compatibility.

### Task 4.3 — Wire label strategy into SampleBuilder `[EXISTING]`

Modify `divical-api/app/ml/sample_builder.py`:

- Accept a `label_strategy: str` parameter
- Look up the strategy by name from a registry dict
- Apply it during `build_training_samples()` to generate labels
- Store `label_version` and `label_strategy_name` on each sample

**Done-when:** `SampleBuilder` can produce samples with different label strategies. Test confirms a sample built with `"percentile"` has different labels than one built with `"global_extremum"` for the same data.

### Task 4.4 — Add label strategy unit tests `[NEW]`

Create `tests/unit/ml/test_labels.py`:

- Test `GlobalExtremumLabels` on a known price array produces expected offsets
- Test `SmoothedOffsetLabels` produces different (less extreme) offsets than global extremum
- Test `PercentileLabels` produces offsets within expected percentile bounds
- Test each strategy includes `label_version` and `label_strategy_name` in output
- Test edge case: flat price array doesn't crash

**Done-when:** 6+ passing tests covering all three strategies and edge cases.

---

## Slice 5 — Temporal CV + Baseline Evaluation ✅

**Goal:** Temporal cross-validation is the default experiment path. Every model is compared against deterministic baselines.

### Task 5.1 — Enhance temporal_cv module `[EXISTING]`

Modify `divical-api/app/ml/temporal_cv.py`:

- Add `calibration_by_window(predictions, actuals, window_labels) -> dict` — computes per-window accuracy/MAE
- Add `regime_performance_slices(predictions, actuals, regime_labels) -> dict` — groups metrics by regime
- Ensure `walk_forward_cv()` returns per-fold metrics, not just aggregated results

**Done-when:** Enhanced functions exist. Unit tests confirm per-window and per-regime metrics are produced.

### Task 5.2 — Create baselines module `[NEW]`

Create `divical-api/app/ml/evaluation/baselines.py`:

Implement deterministic baselines:

1. `FixedOffsetBaseline` — always predicts buy at -5, sell at +5 (or configurable constants)
2. `HistoricalMeanBaseline` — predicts the historical average buy/sell offset for the ticker
3. `NaiveLastBaseline` — predicts the last observed offset

Each baseline implements a `predict(sample) -> dict` method returning `buy_offset`, `sell_offset`.

**Done-when:** Three baselines importable. Unit tests confirm deterministic output.

### Task 5.3 — Create evaluation metrics module `[NEW]`

Create `divical-api/app/ml/evaluation/__init__.py` and `divical-api/app/ml/evaluation/metrics.py`:

Implement:

- `compute_prediction_metrics(predictions, actuals) -> dict` — MAE, RMSE, directional accuracy, hit rate
- `compare_against_baselines(model_preds, baseline_preds_dict, actuals) -> dict` — produces a comparison table
- `format_evaluation_report(comparison: dict) -> str` — human-readable summary

**Done-when:** Functions return correct metrics for known inputs. A comparison against baselines shows relative performance. Unit tests pass.

### Task 5.4 — Create calibration report module `[NEW]`

Create `divical-api/app/ml/evaluation/calibration_report.py`:

Implement:

- `CalibrationReport` dataclass with fields: `model_name`, `label_strategy`, `training_window`, `validation_window`, `metrics`, `baseline_comparison`, `regime_slices`, `confidence_calibration`
- `generate_calibration_report(model, samples, label_strategy, baselines) -> CalibrationReport` — runs temporal CV, computes all metrics, compares against baselines, slices by regime

**Done-when:** A `CalibrationReport` can be generated from mock data. It includes baseline comparison and regime slices. Unit test confirms structure.

### Task 5.5 — Wire temporal CV into model training path `[EXISTING]`

Modify `divical-api/app/ml/model_manager.py`:

- After training, run `walk_forward_cv()` on the trained model
- Generate a `CalibrationReport`
- Log the report via structlog
- Store the report dict on the model metadata (in-memory for now — DB storage in Slice 6)

**Done-when:** Training a model produces a calibration report logged to structured output. Existing tests still pass.

---

## Slice 6 — Experiment Manifest + Evidence Ledger ✅

**Goal:** Every ML experiment and strategy candidate has machine-readable lineage and evidence. The system can answer "why was this strategy approved?"

### Task 6.1 — Define experiment data models `[NEW]`

Create `divical-api/app/models/experiments.py`:

SQLAlchemy models:

```python
class ExperimentManifest(Base):
    __tablename__ = "experiment_manifests"
    id: str  # experiment_id from observability/ids.py
    strategy_candidate_id: str | None
    label_strategy: str
    label_version: str
    feature_version: str
    training_window_start: date
    training_window_end: date
    validation_window_start: date
    validation_window_end: date
    backtest_parameters: JSON  # dict serialized
    evaluator_vote_summary: JSON | None
    created_at: datetime

class EvidenceLedger(Base):
    __tablename__ = "evidence_ledger"
    id: int  # autoincrement
    experiment_id: str  # FK to ExperimentManifest
    entry_type: str  # "metric", "failure", "regime_slice", "calibration", "incubation", "source_ref"
    key: str
    value: JSON
    created_at: datetime

class StrategyStateTransition(Base):
    __tablename__ = "strategy_state_transitions"
    id: int
    strategy_candidate_id: str
    from_state: str
    to_state: str
    actor: str  # "evaluator_swarm", "backtester", "incubator", "user"
    rationale: str | None
    timestamp: datetime
```

**Done-when:** Models importable. Alembic migration generated and applies cleanly.

### Task 6.2 — Define strategy lifecycle states `[NEW]`

Create `divical-api/app/models/strategy_lifecycle.py`:

Define the lifecycle enum:

```python
class StrategyState(str, Enum):
    PROPOSED = "proposed"
    APPROVED_FOR_BACKTEST = "approved_for_backtest"
    BACKTESTING = "backtesting"
    BACKTEST_FAILED = "backtest_failed"
    BACKTEST_PASSED = "backtest_passed"
    INCUBATING = "incubating"
    INCUBATION_FAILED = "incubation_failed"
    INCUBATION_PASSED = "incubation_passed"
    PROMOTED = "promoted_to_simulation_dashboard"
    ARCHIVED = "archived"
```

Add a `transition(strategy_id, from_state, to_state, actor, rationale)` function that:

- Validates the transition is legal (define an allowed-transitions dict)
- Creates a `StrategyStateTransition` record
- Updates the strategy's current state
- Emits a metrics event

**Done-when:** Transition function works. Illegal transitions raise `ValueError`. Unit tests cover happy path + illegal transition.

### Task 6.3 — Add state field to DiscoveredStrategy `[EXISTING]`

Modify `divical-api/app/models/database.py`:

- Add `state: str` column to `DiscoveredStrategy` (default `"proposed"`)
- Add `experiment_id: str | None` column to `DiscoveredStrategy`
- Add `strategy_candidate_id: str | None` column to `DiscoveredStrategy`

Generate and apply an Alembic migration.

**Done-when:** Migration applies. Existing strategies get default state. New strategies can be queried by state.

### Task 6.4 — Create experiment service `[NEW]`

Create `divical-api/app/services/experiment_service.py`:

Implement:

- `create_experiment(config: dict) -> ExperimentManifest` — creates manifest, assigns experiment_id
- `record_evidence(experiment_id, entry_type, key, value)` — appends to evidence ledger
- `get_experiment_evidence(experiment_id) -> list[EvidenceLedger]` — retrieves all evidence
- `get_strategy_history(strategy_candidate_id) -> list[StrategyStateTransition]` — retrieves lifecycle

**Done-when:** Service creates/reads experiments and evidence through the DB. Integration test confirms round-trip.

### Task 6.5 — Wire experiment tracking into research orchestrator `[EXISTING]`

Modify `divical-api/app/services/research/orchestrator.py`:

- Create an `ExperimentManifest` at the start of each research run
- Attach `experiment_id` to proposals
- Record evidence entries for evaluator votes, backtest results
- Call `transition()` when strategy state changes

Modify `divical-api/app/services/research/proposal_backtester.py`:

- Record backtest metrics as evidence ledger entries
- Transition strategy state to `backtesting` → `backtest_passed` / `backtest_failed`

**Done-when:** Research run produces experiment manifest + evidence entries in DB. Strategy state transitions are recorded.

### Task 6.6 — Add API endpoints for experiments `[NEW]`

Add routes to `divical-api/app/api/routes/strategies.py` (or create `experiments.py` if cleaner):

- `GET /api/experiments` — list experiments with pagination
- `GET /api/experiments/{id}` — get manifest + evidence
- `GET /api/strategies/{id}/history` — get lifecycle transitions

**Done-when:** Endpoints return data. Tested with a simple integration test or manual curl.

---

## Slice 7 — Proposal Quality + Bounded Strategy Schema ✅

**Goal:** Research proposals pass quality gates before consuming backtest resources. Only strategies expressible in a bounded format are auto-backtested.

### Task 7.1 — Define bounded strategy specification format `[NEW]`

Create `divical-api/app/services/research/contracts/strategy_spec.py`:

Define a Pydantic model:

```python
class StrategySpec(BaseModel):
    name: str
    hypothesis: str
    entry_logic: EntryLogicType  # enum: fixed_offset, smoothed_signal, percentile_trigger
    exit_logic: ExitLogicType    # enum: fixed_offset, trailing_stop, percentile_trigger
    offset_policy: OffsetPolicy  # min/max buy offset, min/max sell offset
    ticker_filters: list[str]    # e.g. ["bdc_only", "min_yield_3pct"]
    factor_modifiers: list[str]  # e.g. ["rate_sensitivity", "regime_aware"]
    risk_gates: list[str]        # e.g. ["max_drawdown_10pct", "min_sharpe_0.5"]
    position_sizing: str         # "equal_weight" or "kelly" or "fixed"
    required_inputs: list[str]
    unsupported_requirements: list[str]
    confidence: float            # 0.0–1.0
    citations: list[str]
```

Define the enums (`EntryLogicType`, `ExitLogicType`, `OffsetPolicy`) in the same file.

**Done-when:** `StrategySpec` validates and rejects malformed specs. Unit tests confirm validation.

### Task 7.2 — Create proposal quality filter `[NEW]`

Create `divical-api/app/services/research/proposal_quality.py`:

Implement `ProposalQualityFilter`:

- `check(proposal: StrategySpec) -> tuple[bool, list[str]]`
  - Returns `(passed, list_of_rejection_reasons)`
- Rejection rules:
  1. Hypothesis is empty or under 20 characters
  2. No entry or exit logic specified
  3. Required inputs include unavailable data sources
  4. Unsupported requirements list is non-empty and critical
  5. Confidence is 0 or not set
  6. No evaluation plan / risk gates

**Done-when:** Filter rejects bad proposals and passes good ones. Unit tests for each rejection rule.

### Task 7.3 — Create proposal deduplication `[NEW]`

Create `divical-api/app/services/research/proposal_deduper.py`:

Implement `ProposalDeduper`:

- `is_duplicate(new_spec: StrategySpec, existing_specs: list[StrategySpec]) -> tuple[bool, str | None]`
  - Compare entry_logic + exit_logic + offset_policy + factor_modifiers
  - If the combination matches an existing spec, return `(True, existing_spec_name)`
- `novelty_score(new_spec: StrategySpec, existing_specs: list[StrategySpec]) -> float`
  - 0.0 = exact duplicate, 1.0 = completely novel
  - Score based on Jaccard similarity of feature sets

**Done-when:** Duplicate detection works. Novelty score differentiates similar vs. different specs. Unit tests pass.

### Task 7.4 — Wire quality gates into research pipeline `[EXISTING]`

Modify `divical-api/app/services/research/orchestrator.py`:

- After proposal generation, convert proposals to `StrategySpec` format
- Run `ProposalQualityFilter.check()` on each
- Run `ProposalDeduper.is_duplicate()` against existing strategies
- Emit metrics: `proposal_rejected` with reason, or `proposal_approved`
- Only pass approved, non-duplicate proposals to backtest

Modify `divical-api/app/services/research/strategy_evaluator.py`:

- Validate evaluator outputs conform to structured contracts (hypothesis, mechanism, expected_edge, etc.)
- Reject evaluations that lack required fields

**Done-when:** Research pipeline filters low-quality and duplicate proposals before backtesting. Existing tests updated.

### Task 7.5 — Add structured agent output contracts `[NEW]`

Create `divical-api/app/services/research/contracts/__init__.py` and `divical-api/app/services/research/contracts/agent_output.py`:

Define Pydantic models for structured agent outputs:

```python
class ResearchAgentOutput(BaseModel):
    hypothesis: str
    mechanism: str
    required_inputs: list[str]
    assumptions: list[str]
    expected_edge: str
    risk_factors: list[str]
    evaluation_plan: str
    unsupported_claims: list[str]
    confidence: float
    citations: list[str]
```

Create a `validate_agent_output(raw_output: dict) -> ResearchAgentOutput | None` function that returns `None` (with logged reason) if validation fails.

**Done-when:** Validation accepts well-formed outputs and rejects incomplete ones. Unit tests pass.

---

## Slice 8 — RunExecutor Decomposition ✅

**Goal:** `RunExecutor` (~1300 lines) becomes a thin orchestrator. Business logic moves to testable phase services.

### Task 8.1 — Extract Phase 1: Data Fetching `[NEW]`

Create `divical-api/app/services/run_phases/__init__.py` and `divical-api/app/services/run_phases/data_fetcher.py`:

Move data fetching logic out of `RunExecutor`:

- `DataFetcher` class with `async fetch(tickers, provider, trading_options) -> FetchResult`
- `FetchResult` dataclass containing: price data, dividend data, market context, ticker contexts
- Progress reporting via a callback

Identify the data-fetching section of `RunExecutor.execute()` (the phase that calls the provider for each ticker) and extract it.

**Done-when:** `DataFetcher` works standalone. A unit test with mock provider confirms data is fetched and structured. `RunExecutor` calls `DataFetcher` instead of inlining the logic.

### Task 8.2 — Extract Phase 2: ML Predictions `[NEW]`

Create `divical-api/app/services/run_phases/predictor.py`:

Move ML prediction logic:

- `Predictor` class with `predict(fetch_result, model_manager, strategy_options) -> PredictionResult`
- `PredictionResult` dataclass containing: per-ticker `ModelPrediction` list
- This wraps the model manager calls that happen in RunExecutor

**Done-when:** `Predictor` works standalone. RunExecutor delegates to it. Unit test with mocked model manager passes.

### Task 8.3 — Extract Phase 3: Historical Strategy Application `[NEW]`

Create `divical-api/app/services/run_phases/historical_strategist.py`:

Move historical strategy logic:

- `HistoricalStrategist` class with `apply(fetch_result, strategy_options) -> list[StrategyResult]`
- Wraps the historical backtesting/strategy application that RunExecutor currently inlines

**Done-when:** Standalone class works. RunExecutor delegates. Unit test with mock data passes.

### Task 8.4 — Extract Phase 4: Future Prediction `[NEW]`

Create `divical-api/app/services/run_phases/future_predictor.py`:

Move future prediction logic:

- `FuturePredictor` class with `predict(fetch_result, prediction_result, strategy_options) -> list[ModelPrediction]`
- Generates forward-looking predictions for upcoming ex-dates

**Done-when:** Standalone class works. RunExecutor delegates. Unit test passes.

### Task 8.5 — Extract Phase 5: Quantile Enrichment `[NEW]`

Create `divical-api/app/services/run_phases/quantile_enricher_phase.py`:

Move quantile enrichment logic:

- `QuantileEnrichmentPhase` class with `enrich(predictions, fetch_result) -> list[ModelPrediction]`
- Wraps the `QuantileEnricher` calls

**Done-when:** Standalone class works. RunExecutor delegates. Unit test passes.

### Task 8.6 — Extract persistence and progress reporting `[NEW]`

Create `divical-api/app/services/run_phases/persistence.py`:

- `RunPersistenceService` with `save_results(run_id, results, predictions)` — handles DB writes

Create `divical-api/app/services/run_phases/progress.py`:

- `RunProgressReporter` with `report(phase, progress_pct, message)` — wraps the WebSocket progress callback

**Done-when:** Both services work. RunExecutor uses them. Existing integration test still passes.

### Task 8.7 — Slim down RunExecutor `[EXISTING]`

Refactor `divical-api/app/services/run_executor.py`:

- `execute()` becomes ~50-80 lines of orchestration
- Each phase call is one line: `fetch_result = await self.data_fetcher.fetch(...)`
- Error handling and cancellation checks remain in the coordinator
- Remove all extracted logic (it now lives in `run_phases/`)

**Done-when:** `RunExecutor` is under 200 lines. All existing tests pass. Integration test from Slice 1 still passes.

---

## Slice 9 — Incubation / Forward Simulation ✅

**Goal:** Strategies that pass backtest gates enter forward simulation. Predicted vs. realized outcomes are tracked. Confidence drift is monitored.

### Task 9.1 — Define incubation observation model `[NEW]`

Add to `divical-api/app/models/experiments.py`:

```python
class IncubationObservation(Base):
    __tablename__ = "incubation_observations"
    id: int
    incubation_id: str
    strategy_candidate_id: str
    observation_date: date
    simulated_entry_date: date | None
    simulated_exit_date: date | None
    predicted_buy_offset: int | None
    predicted_sell_offset: int | None
    predicted_return: Decimal | None
    realized_return: Decimal | None
    confidence_at_prediction: float | None
    confidence_drift: float | None  # delta from initial confidence
    block_decision: str | None  # "none", "blocked_by_regime", "blocked_by_gate"
    created_at: datetime
```

Generate Alembic migration.

**Done-when:** Table exists. Migration applies cleanly.

### Task 9.2 — Create forward simulator `[NEW]`

Create `divical-api/app/services/research/incubation/forward_simulator.py`:

Implement `ForwardSimulator`:

- `simulate(strategy_spec: StrategySpec, market_data, start_date, end_date) -> list[IncubationObservation]`
  - For each ex-date in the incubation window:
    - Apply the strategy's entry/exit logic
    - Record predicted outcome (from model) vs. realized outcome (from actual data once available)
    - Compute confidence drift (initial confidence vs. current calibration)
- This runs on newly arriving data — called periodically for incubating strategies

**Done-when:** Forward simulator produces observations for a mock strategy + mock data. Unit test confirms observations have both predicted and realized fields populated.

### Task 9.3 — Create incubation evaluator `[NEW]`

Create `divical-api/app/services/research/incubation/incubation_evaluator.py`:

Implement `IncubationEvaluator`:

- `evaluate(observations: list[IncubationObservation], min_horizon: int = 30) -> IncubationVerdict`
  - `IncubationVerdict` dataclass: `passed: bool`, `reason: str`, `metrics: dict`
- Pass criteria:
  - Minimum N observations (e.g., 5+)
  - Predicted vs. realized correlation above threshold
  - Confidence drift within acceptable bounds
  - No catastrophic realized losses
- On pass: transition strategy to `incubation_passed`
- On fail: transition to `incubation_failed`, record rationale

**Done-when:** Evaluator passes/fails strategies based on observation quality. Unit tests for pass and fail paths.

### Task 9.4 — Wire incubation into research lifecycle `[EXISTING]`

Modify `divical-api/app/services/research/orchestrator.py` (or create a new `incubation_manager.py`):

- After a strategy reaches `backtest_passed`, transition to `incubating`
- Register it with the forward simulator
- Periodically (or on new data arrival), run `ForwardSimulator.simulate()`
- After the minimum horizon, run `IncubationEvaluator.evaluate()`
- Transition to `incubation_passed` or `incubation_failed`
- Record all evidence in the ledger

**Done-when:** A strategy can flow through the full lifecycle: proposed → approved → backtesting → backtest_passed → incubating → incubation_passed/failed. Integration test confirms the flow.

### Task 9.5 — Add incubation API endpoints `[EXISTING]`

Add to `divical-api/app/api/routes/strategies.py`:

- `GET /api/strategies/{id}/incubation` — get incubation observations
- `GET /api/strategies/incubating` — list all currently incubating strategies
- `POST /api/strategies/{id}/evaluate-incubation` — trigger incubation evaluation

**Done-when:** Endpoints return data. Manual test or integration test confirms.

---

## Deferred Slices (Not Detailed Here)

The following are recommended for phases 3–5 of the upgrade but do not need implementation plans until Slices 1–9 are complete:

- **PortfolioDetailPage decomposition** (Epic F3) — split 880-line page into composable components
- **Regime-conditioned evaluation** (Epic C) — formalize factor inputs, add learned regime models, dynamic weighting
- **RBI Dashboard upgrade** (Epic G) — proposal table, evidence panel, comparison views, incubation timeline
- **PostgreSQL migration** (Epic A3) — database switch for research-heavy flows
- **Config/default unification** (Epic F4) — eliminate backend/frontend config drift

These depend on the foundation laid by Slices 1–9 and should be planned once that foundation is stable.

---

## Cross-Cutting Rules (from spec §20)

Every task must respect these:

1. No live trading assumptions
2. No broker APIs
3. No autonomous code execution from LLM proposals
4. Prefer bounded schemas over free-form text
5. Every research decision must be auditable
6. Every ML experiment must be reproducible
7. New models must beat deterministic baselines or remain experimental

---

## Validation After Each Slice

After completing each slice, run:

```bash
# Backend
cd divical-api
ruff check app/
pyright app/
pytest

# Frontend (if modified)
cd divical-web
npm run lint
npm run build
npm test
```

CI must pass before merging the slice branch.
