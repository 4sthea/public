# SampleProject AI-Harness Evaluation  
## Spezifikations- und Implementierungsplan

**Stand:** 2026-06-03  
**Ziel:** Vorher/Nachher-Bewertung von Änderungen an SampleProject-Agenten, Prompts, Instructions, Skills und ähnlichen Harness-Artefakten.  
**Priorität:** Minimaler Implementierungsaufwand, hoher praktischer Signalwert, zuerst lokale Auswertung, später CI/Telemetry.

---

## 0. Kurzfazit

Der beste Startpunkt für SampleProject ist **kein großes Benchmark-System**, sondern eine kleine, harte, gepaarte Eval-Suite:

1. **Gleicher Task, gleicher Repo-Snapshot, gleiches Modell, gleiche Tools.**
2. Agent-Artefakt-Version A erzeugt Output A.
3. Agent-Artefakt-Version B erzeugt Output B.
4. Ein lokaler Scorer bewertet:
   - deterministische Gates,
   - Scope-/Security-Verstöße,
   - Instruction-Adherence,
   - semantische Nicht-Regression,
   - Code-/Dokumentationsqualität,
   - optional Trace-/Token-/Tool-Metriken.
5. Ergebnis ist **PASS / FAIL / INCONCLUSIVE**, plus Delta-Report.

Wichtig: **Der alte Output ist nicht automatisch Gold-Truth.**  
Er ist nur ein Vergleichsanker. Die eigentliche Ground Truth sind:

- der ursprüngliche Task,
- die Akzeptanzkriterien,
- SampleProject-Kontext,
- harte Verifier,
- Rubrics.

Ein neuer Output darf anders formuliert, anders strukturiert oder sogar deutlich besser sein. Er darf aber keine korrekten Anforderungen verlieren, keine falschen Repo-Behauptungen einführen und keine schlechtere Validierung liefern.

---

## 1. Verifizierter SampleProject-Kontext

Die folgenden Punkte sind aus dem Repository verifiziert und werden als Planbasis genutzt.

### 1.1 Repository-Struktur

SampleProject ist laut Root-Agent-Vertrag ein **Dividend-Capture Decision System für US-Dividendenaktien, primär BDCs**. Die wichtigsten Schichten sind:

| Bereich | Pfad |
|---|---|
| Backend | `sampleproject-api/` |
| Frontend | `sampleproject-web/` |
| Copilot-/Agent-Harness-Schicht | `.github/` |
| OpenCode-Schicht | `.opencode/` |
| Codex-Adapter | `.codex/` |
| Shared Rules | `clasp/rules/` |
| Kanonische Repo-Maps | `.github/context/project-paths.md`, `.github/context/repo-map.md` |

### 1.2 Bestehende Verifikationsbefehle

SampleProject hat bereits verifizierte Validierungspfade:

```text
Python lint:  ruff check sampleproject-api/app/
Python types: cd sampleproject-api && pyright app/
Python tests: cd sampleproject-api && python -m pytest tests/ -x -q

TypeScript lint:  cd sampleproject-web && eslint src/
TypeScript types: cd sampleproject-web && tsc --noEmit
TypeScript tests: cd sampleproject-web && npm test -- --run
```

Für Agent-Harness-/`.github/`-Änderungen existieren bereits:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\verify-clasp-freshness.ps1 -Lint
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\verify-context-freshness.ps1
```

### 1.3 Bestehende Hook-Fläche

SampleProject hat bereits Hook-Konfigurationen unter `.github/hooks/hooks.json`:

- `SessionStart`
- `PreToolUse`
- `PostToolUse`
- `Stop`

Das ist ein großer Vorteil. Für die erste Eval-Version muss keine komplett neue Instrumentierungsschicht erfunden werden. Es reicht, die vorhandenen Hooks im Eval-Modus zusätzlich Metriken schreiben zu lassen.

### 1.4 Engineer-Agent als Hauptziel

Der Engineer-Agent ist ein guter erster Eval-Kandidat, weil er:

- editieren darf,
- terminal commands ausführen darf,
- Code, Tests und Dokumentation bearbeiten darf,
- den Ralph Loop nutzt: `Implement → build → test → read output → fix → loop`,
- vor Abschluss Build/Test-Evidenz liefern soll,
- bei Unsicherheit nicht raten soll.

Damit eignet er sich ideal für Vorher/Nachher-Tests von Agent-Artefaktänderungen.

---

## 2. Zielbild

### 2.1 Was gemessen wird

Gemessen wird die Qualität des **SampleProject AI Harness** nach Änderungen an:

| Artefakt-Typ | Beispiele |
|---|---|
| Agents | `.github/agents/*.agent.md` |
| Instructions | `.github/instructions/*.instructions.md` |
| Prompts | `.github/prompts/*.prompt.md` |
| Skills | `.github/skills/*/SKILL.md` |
| Root-/Subtree-Verträge | `AGENTS.md`, `*/AGENTS.md` |
| Shared Rules | `clasp/rules/*.md` |
| Adapter | `.codex/**`, `.opencode/**` |

### 2.2 Was ausdrücklich nicht gemessen wird

Nicht Ziel:

- Modellbenchmarking.
- Vergleich GPT vs Claude vs Gemini.
- Maximale akademische Messgenauigkeit.
- Vollautomatisches Repository-Repair-Benchmarking wie SWE-Bench.
- Vollständiges VS-Code-Produktbenchmarking wie VSC-Bench.

Das Modell wird für eine Messreihe **fixiert**, damit eine Änderung am Agent-Artefakt nicht mit einer Modelländerung vermischt wird.

---

## 3. Priorisierte Methodiken

Sortiert nach Verhältnis aus **Signalwert / Implementierungsaufwand**.

| Rang | Methodik | Aufwand | Signalwert | Sofort umsetzen? | Begründung |
|---:|---|---:|---:|---|---|
| 1 | Deterministische Gates | Niedrig | Sehr hoch | Ja | Nutzt vorhandene SampleProject-Lint/Test/Freshness-Befehle. Billig, objektiv, reproduzierbar. |
| 2 | Scope-/Security-Guardrails | Niedrig | Sehr hoch | Ja | Erkennt gefährliche oder irrelevante Änderungen sofort. Besonders wichtig bei Agenten mit Edit-/Execute-Rechten. |
| 3 | Task-Katalog mit Akzeptanzkriterien | Niedrig–Mittel | Sehr hoch | Ja | Ohne klare Tasks ist jede Messung Rauschen. 20–40 Tasks reichen für MVP. |
| 4 | Pairwise Semantic Regression Judge | Mittel | Hoch | Ja | Bewertet „neuer Output gleichwertig oder besser?“ besser als String-Diffs. |
| 5 | Dokumentations- und Code-Rubrics | Mittel | Hoch | Ja | Liefert strukturierte Qualitätskategorien statt Bauchgefühl. |
| 6 | Hook-basierter Eval-Modus | Mittel | Hoch | Ja, nach MVP | SampleProject hat bereits Hooks. Damit lassen sich Tool-Calls, Stop-Verhalten und Verifikationsnachweise erfassen. |
| 7 | OTel/Debug-Export-Auswertung | Mittel | Hoch | Ja, aber nach lokalen JSON-Reports | Sehr wertvoll für Token, Tool-Calls, Latenz, aber nicht für Tag 1 nötig. |
| 8 | CI-Smoke-Gate | Mittel | Mittel–hoch | Ja, nach stabiler lokaler Suite | Verhindert Regressionen bei `.github/**`, `clasp/**`, `.opencode/**`, `.codex/**`. |
| 9 | Mehrfach-Trials + statistische Auswertung | Mittel | Mittel–hoch | Später | Wichtig wegen Nichtdeterminismus, aber erst sinnvoll, wenn Tasks stabil sind. |
| 10 | Trace-Graph-/Dominator-Analyse | Hoch | Hoch bei UI/Computer-Use | Nicht MVP | Für SampleProject aktuell zu schwergewichtig. Optional für spätere Agent-Trace-Analyse. |
| 11 | AgentEval-/DAG-Failure-Attribution | Hoch | Hoch | Nicht MVP | Gut für große Trace-Korpora, aber nicht für den Start. |
| 12 | Vollständige VS-Code-Runner-Automation | Hoch | Sehr hoch | Nicht MVP | Realistisch, aber unnötig teuer für die erste SampleProject-Version. |

---

## 4. Implementierungsreihenfolge

### Phase 1 — Eval-MVP ohne neue externe Plattform

**Ziel:** Innerhalb kurzer Zeit Vorher/Nachher-Vergleiche erzeugen können.

#### 1.1 Neue Ordnerstruktur

Empfohlen:

```text
.github/evals/
  README.md
  tasks/
    smoke/
    capability/
    regression/
  prompts/
  rubrics/
    semantic-equivalence.rubric.md
    documentation-quality.rubric.md
    code-quality.rubric.md
    harness-adherence.rubric.md
  schemas/
    task.schema.json
    trial-result.schema.json
    comparison-report.schema.json

scripts/
  ai-eval-run.py
  ai-eval-score.py
  ai-eval-compare.py
  ai-eval-report.py

docs/tmp/ai-evals/
  .gitkeep
```

Zusätzlich in `.gitignore`:

```gitignore
docs/tmp/ai-evals/**
!docs/tmp/ai-evals/.gitkeep
```

**Warum `.github/evals/`?**  
SampleProject hält Copilot-bezogene Agenten, Prompts, Instructions, Skills, Hooks und Schemas bereits unter `.github/`. Der Eval-Katalog gehört als Copilot/Agent-Harness-nahe Harness-Fläche ebenfalls dort hin.

#### 1.2 Minimaler Task-Katalog

Starte mit **10 Smoke Tasks**, danach 20–40 Capability Tasks.

Task-Kategorien:

| Kategorie | Anteil im MVP | Beispiel |
|---|---:|---|
| Dokumentation | 30% | „Erzeuge eine kurze Spezifikation aus gegebenem Kontext.“ |
| Harness-Artefakt | 25% | „Verbessere eine Agent-Instruction ohne Duplikation und ohne Scope-Verlust.“ |
| Code klein | 25% | „Ändere eine kleine Funktion und führe passende Tests aus.“ |
| Test/QA | 10% | „Erzeuge oder aktualisiere Tests für eine kleine Komponente.“ |
| Kontext-Freshness | 10% | „Aktualisiere passende Kontextdateien nach einer Verhaltensänderung.“ |

Minimaler Task als JSON:

```json
{
  "id": "smoke-doc-001",
  "title": "Engineer erzeugt eine kurze Implementierungsspezifikation",
  "category": "documentation",
  "agent": ".github/agents/engineer.agent.md",
  "artifact_under_test": ".github/agents/engineer.agent.md",
  "prompt_file": ".github/evals/prompts/smoke-doc-001.md",
  "expected_outputs": {
    "output_kind": "markdown",
    "required_sections": [
      "Ziel",
      "Nicht-Ziele",
      "Implementierungsschritte",
      "Validierung",
      "Risiken"
    ],
    "required_terms": [
      "SampleProject",
      "Validierung",
      "Scope"
    ],
    "forbidden_terms": [
      "wahrscheinlich existiert",
      "müsste irgendwo sein"
    ]
  },
  "allowed_write_globs": [
    "docs/tmp/ai-evals/**"
  ],
  "forbidden_write_globs": [
    ".env*",
    "secrets/**",
    "credentials/**"
  ],
  "deterministic_verifiers": [
    "markdown_required_sections",
    "forbidden_terms",
    "scope_check"
  ],
  "rubrics": [
    "semantic-equivalence",
    "documentation-quality",
    "harness-adherence"
  ]
}
```

#### 1.3 Trial-Ergebnisformat

Jeder Agent-Run schreibt ein Ergebnis:

```json
{
  "schema_version": 1,
  "experiment_id": "2026-06-03-engineer-agent-v2",
  "task_id": "smoke-doc-001",
  "trial": 1,
  "variant": "candidate",
  "agent": ".github/agents/engineer.agent.md",
  "artifact_under_test": ".github/agents/engineer.agent.md",
  "git_sha": "unknown",
  "model": "pinned-by-runner",
  "runner": "vscode-copilot-local",
  "started_at": "2026-06-03T12:00:00Z",
  "output_path": "docs/tmp/ai-evals/runs/2026-06-03-engineer-agent-v2/candidate/smoke-doc-001/t01/output.md",
  "changed_files": [],
  "deterministic": {
    "scope_check": "PASS",
    "protected_file_check": "PASS",
    "required_sections": "PASS",
    "forbidden_terms": "PASS",
    "validation_commands": "SKIPPED"
  },
  "judge": {
    "semantic_equivalence": "candidate_equivalent",
    "documentation_quality_score": 0.84,
    "harness_adherence_score": 0.91,
    "requires_manual_review": false
  },
  "telemetry": {
    "total_tokens": null,
    "tool_call_count": null,
    "latency_ms": null,
    "terminal_error_count": null
  },
  "verdict": "PASS",
  "notes": []
}
```

#### 1.4 MVP-Report

Der erste Report muss nicht schön sein. Eine Markdown-Tabelle reicht:

| Task | Baseline | Candidate | Delta | Hard Gates | Judge | Verdict |
|---|---|---|---:|---|---|---|
| smoke-doc-001 | PASS | PASS | +0.05 | PASS | equivalent/better | PASS |
| smoke-code-002 | PASS | FAIL | -1.00 | FAIL | worse | FAIL |
| smoke-harness-003 | PASS | PASS | 0.00 | PASS | equivalent | PASS |

---

### Phase 2 — Deterministische Scorer

**Ziel:** Möglichst viel ohne LLM-Judge bewerten.

Implementiere `scripts/ai-eval-score.py` mit Python-Stdlib.

#### 2.1 Basis-Checks

| Check | Regel |
|---|---|
| Output existiert | erwarteter Output-Pfad wurde erzeugt |
| Output nicht leer | Mindestlänge je Output-Typ |
| Required sections | Markdown enthält geforderte Überschriften |
| Required terms | Geforderte Begriffe/Claims vorhanden |
| Forbidden terms | Unsichere Formulierungen/Fake-Claims nicht vorhanden |
| Scope check | Nur erlaubte Dateien geändert |
| Protected files | Keine `.env*`, `secrets/**`, `credentials/**` |
| No hallucinated paths | Behauptete Pfade optional gegen Repo-Dateiliste prüfen |
| Validation evidence | Bei Code-Tasks muss Test-/Lint-Nachweis im Output oder Trace vorhanden sein |

#### 2.2 Code-Checks

Nur ausführen, wenn relevante Dateien geändert wurden.

| Geänderter Bereich | Mindestcheck |
|---|---|
| `sampleproject-api/app/**` | `ruff check sampleproject-api/app/` |
| `sampleproject-api/app/**` | `cd sampleproject-api && pyright app/` |
| `sampleproject-api/tests/**` | `cd sampleproject-api && python -m pytest tests/ -x -q` |
| `sampleproject-web/src/**` | `cd sampleproject-web && eslint src/` |
| `sampleproject-web/src/**` | `cd sampleproject-web && tsc --noEmit` |
| `sampleproject-web/src/**` | `cd sampleproject-web && npm test -- --run` |
| `.github/**` | `scripts\verify-clasp-freshness.ps1 -Lint` |
| `.github/context/**` | `scripts\verify-context-freshness.ps1` |

#### 2.3 Minimaler Python-Pseudocode

```python
def score_trial(task, output_path, changed_files):
    result = {
        "scope_check": check_scope(task, changed_files),
        "protected_file_check": check_protected_files(changed_files),
        "required_sections": check_required_sections(task, output_path),
        "required_terms": check_required_terms(task, output_path),
        "forbidden_terms": check_forbidden_terms(task, output_path),
    }

    if touches_backend(changed_files):
        result["ruff"] = run("ruff check sampleproject-api/app/")
        result["pyright"] = run("cd sampleproject-api && pyright app/")

    if touches_frontend(changed_files):
        result["eslint"] = run("cd sampleproject-web && eslint src/")
        result["tsc"] = run("cd sampleproject-web && tsc --noEmit")

    if touches_github_layer(changed_files):
        result["clasp_freshness"] = run_powershell("scripts\\verify-clasp-freshness.ps1 -Lint")
        result["context_freshness"] = run_powershell("scripts\\verify-context-freshness.ps1")

    return result
```

---

### Phase 3 — Pairwise Semantic Regression Judge

**Ziel:** Dein konkreter Fall:  
„Alter Output vs neuer Output, gleicher Task. Ist der neue Output semantisch gleichwertig oder besser?“

#### 3.1 Warum Pairwise statt absoluter Score?

Ein absoluter Score wie `0.82` ist schwer zu interpretieren.  
Ein gepaarter Vergleich ist praktischer:

```text
Given:
- Original task
- Baseline output
- Candidate output
- SampleProject context/rubric

Classify candidate as:
- candidate_better
- candidate_equivalent
- candidate_worse
- inconclusive
```

Das ist näher an deiner Frage:  
**„Hat meine Agent-Änderung die Qualität verschlechtert?“**

#### 3.2 Judge-Regeln

Der Judge darf den Baseline-Output nicht blind als Wahrheit behandeln.

Bewertungslogik:

1. Task und Akzeptanzkriterien sind Primärquelle.
2. SampleProject-Kontext ist Primärquelle für Repo-spezifische Behauptungen.
3. Baseline ist Vergleichsanker, nicht Goldstandard.
4. Candidate ist schlechter, wenn:
   - eine korrekte Baseline-Anforderung verloren geht,
   - der Output falsche Repo-Fakten einführt,
   - der Output weniger validierbar ist,
   - der Output mehr Scope-Verstöße enthält,
   - der Output gefährlichere oder unklarere Handlungsempfehlungen gibt.
5. Candidate ist gleichwertig, wenn:
   - Inhalt und Kontext erhalten bleiben,
   - Struktur/Formulierung anders sein darf,
   - keine relevante Anforderung verloren geht.
6. Candidate ist besser, wenn:
   - mehr richtige Abdeckung,
   - klarere Validierung,
   - bessere Struktur,
   - weniger Risiko,
   - weniger Token-/Text-Bloat bei gleicher Qualität.

#### 3.3 Judge-Outputschema

```json
{
  "verdict": "candidate_better | candidate_equivalent | candidate_worse | inconclusive",
  "confidence": 0.0,
  "scores": {
    "requirement_coverage": 0.0,
    "semantic_equivalence": 0.0,
    "context_grounding": 0.0,
    "instruction_adherence": 0.0,
    "specificity": 0.0,
    "maintainability": 0.0,
    "validation_quality": 0.0,
    "conciseness": 0.0
  },
  "regressions": [
    {
      "category": "missing_requirement | fabricated_repo_fact | weaker_validation | unsafe_action | lower_specificity | bloat | contradiction",
      "severity": "low | medium | high",
      "evidence": "short quote or summary"
    }
  ],
  "improvements": [
    {
      "category": "better_coverage | better_structure | better_validation | less_bloat | clearer_risks",
      "evidence": "short quote or summary"
    }
  ],
  "manual_review_required": false
}
```

#### 3.4 Bias-Reduktion

Für wichtige Vergleiche:

- Outputs randomisiert als `Output A` und `Output B` geben.
- Judge muss erst `A/B/Tie` wählen.
- Danach Mapping zurück auf `baseline/candidate`.
- Bei hohem Risiko zwei unabhängige Judge-Runs.
- Bei Widerspruch: `INCONCLUSIVE`, manuelle Prüfung.

---

### Phase 4 — Rubric-Kategorien und Klassifikatoren

#### 4.1 Dokumentationsqualität

| Kategorie | 0 | 1 | 2 |
|---|---|---|---|
| Requirement Coverage | wichtige Anforderungen fehlen | teilweise abgedeckt | vollständig abgedeckt |
| Context Grounding | ungestützte/falsche Repo-Claims | teils belegt | sauber auf Kontext bezogen |
| Structure | unklar | brauchbar | logisch und scanbar |
| Specificity | generisch | teilweise konkret | konkrete Pfade/Kommandos/Schritte |
| Validation Quality | keine Validierung | grobe Validierung | prüfbare Gates/Commands |
| Risk Handling | Risiken fehlen | Risiken erwähnt | Risiken + Gegenmaßnahmen |
| Concision | viel Bloat | akzeptabel | präzise ohne Verlust |
| Non-Regression | schlechter als Baseline | gleichwertig | besser |

#### 4.2 Code-Qualität

| Kategorie | Harte Checks | Judge-/Review-Kriterien |
|---|---|---|
| Correctness | Tests grün | löst eigentlichen Task |
| Type/Lint | pyright/tsc/ruff/eslint | keine ignorierten Fehler |
| Scope | geänderte Dateien erlaubt | keine unnötigen Flächen |
| Maintainability | Komplexität/Dateigröße grob | klare Abstraktionen |
| Minimality | Diff-Größe | keine spekulativen Refactors |
| Test Adequacy | Tests hinzugefügt/geändert | Tests decken Fehlerfall ab |
| Security | keine Secret-/Env-Leaks | keine riskanten Patterns |
| Regression Risk | Regression-Tests grün | keine fragile Kopplung |

#### 4.3 Harness-Artefaktqualität

| Kategorie | Frage |
|---|---|
| Scope Precision | Wird klar, wann Agent/Skill/Instruction gilt? |
| Precedence Safety | Widerspricht es Root- oder Subtree-Regeln? |
| Token Efficiency | Fügt es viel Always-on-Text hinzu? |
| Actionability | Sagt es konkret, was der Agent tun soll? |
| Non-Duplication | Dupliziert es vorhandene Policy? |
| Failure Handling | Sagt es, was bei Unsicherheit/Fehlern passiert? |
| Verification Path | Erzwingt es prüfbare Evidenz? |
| Tool Safety | Passt Tool-Zugriff zum Zweck? |

---

### Phase 5 — Hook-basierter Eval-Modus

**Ziel:** Bestehende SampleProject-Hooks nutzen, aber nur im Eval-Modus aktiv zusätzliche Logs schreiben.

#### 5.1 Environment Flags

```powershell
$env:SAMPLEPROJECT_AI_EVAL="1"
$env:SAMPLEPROJECT_AI_EVAL_EXPERIMENT="2026-06-03-engineer-agent-v2"
$env:SAMPLEPROJECT_AI_EVAL_VARIANT="candidate"
$env:SAMPLEPROJECT_AI_EVAL_TASK="smoke-doc-001"
$env:SAMPLEPROJECT_AI_EVAL_TRIAL="1"
```

#### 5.2 Hook-Verhalten

| Hook | Eval-Aufgabe |
|---|---|
| `SessionStart` | Session-ID, Git-SHA, Variant, Task-ID initialisieren |
| `PreToolUse` | Toolname, Zielpfad, Command, Risiko-Klasse loggen |
| `PostToolUse` | Erfolg/Fehler, geänderte Dateien, Terminal-Ausgaben-Metadaten loggen |
| `Stop` | Finalen Run-Snapshot und Trial-Result schreiben |

#### 5.3 Keine Secrets in Logs

Default:

```text
captureContent = false
```

Nur lokal und bewusst aktivieren:

```json
{
  "github.copilot.chat.otel.enabled": true,
  "github.copilot.chat.otel.exporterType": "file",
  "github.copilot.chat.otel.outfile": "docs/tmp/ai-evals/otel/copilot-otel.jsonl",
  "github.copilot.chat.otel.captureContent": false,
  "github.copilot.chat.otel.dbSpanExporter.enabled": true
}
```

Für einzelne private Debug-Runs kann `captureContent` auf `true` gesetzt werden. Dann muss aber gelten:

- keine `.env*`,
- keine Credentials,
- keine Kundendaten,
- keine API Keys,
- keine Secrets in Prompts oder Toolausgaben.

---

### Phase 6 — Lokaler A/B-Workflow

#### 6.1 Ablauf

```text
1. git checkout baseline-branch
2. run task with engineer agent
3. save output to docs/tmp/ai-evals/.../baseline/...
4. git checkout candidate-branch
5. run same task with same model/settings
6. save output to docs/tmp/ai-evals/.../candidate/...
7. run deterministic scorer
8. run pairwise judge
9. generate Markdown report
```

#### 6.2 Mindestregeln

- Gleicher Task.
- Gleicher Repo-Snapshot oder klar dokumentierter Snapshot-Unterschied.
- Gleiches Modell.
- Gleicher Reasoning-/Effort-Modus.
- Gleiche Tools.
- Gleicher Agent-Runner.
- Gleiche Zeitlimits.
- Keine gleichzeitigen Änderungen an mehreren Harness-Artefakten, wenn Ursache isoliert werden soll.

#### 6.3 Trial-Anzahl

Für MVP:

| Change-Typ | Runs pro Task |
|---|---:|
| Kleine Instruction-Änderung | 1–3 |
| Engineer-Agent-Änderung | 3 |
| Skill mit großem Verhaltenseffekt | 3–5 |
| Große Orchestrator-Änderung | 5 |
| CI-Smoke | 1 |

Interpretation:

- `1 Run` ist nur ein Rauchtest.
- `3 Runs` zeigt grobe Varianz.
- `5+ Runs` lohnt sich erst, wenn Tasks stabil sind.

---

### Phase 7 — Composite Score nur als Sekundärsignal

Der Score darf nicht das Hauptgate sein.

#### 7.1 Harte Gates

Candidate darf nicht akzeptiert werden, wenn:

```text
protected_file_violation_count > 0
dangerous_command_count > 0
scope_violation_count > 0
required_deterministic_verifier == FAIL
semantic_verdict == candidate_worse
manual_review_required == true for high-risk task
```

#### 7.2 Sekundärer Quality Index

Nur für Trends:

```text
QualityIndex =
  0.35 * deterministic_success
+ 0.25 * instruction_adherence
+ 0.20 * semantic_non_regression
+ 0.10 * maintainability
+ 0.05 * validation_quality
+ 0.05 * efficiency_score
```

Effizienzscore:

```text
efficiency_score = clamp(1 - max(0, candidate_tokens - baseline_tokens) / baseline_tokens, 0, 1)
```

Wenn keine Token-Daten vorhanden sind:

```text
efficiency_score = null
```

Nicht künstlich schätzen.

#### 7.3 Verdict-Regeln

| Ergebnis | Bedeutung |
|---|---|
| `PASS` | Harte Gates grün und Candidate gleichwertig/besser |
| `FAIL` | Harte Gates fail oder Candidate schlechter |
| `INCONCLUSIVE` | Judge unsicher, Daten fehlen, widersprüchliche Signale |
| `PASS_WITH_WARNINGS` | Kein Blocker, aber Effizienz/Struktur schlechter |

---

## 5. Konkrete PR-/Umsetzungsreihenfolge

### PR 1 — Eval-Gerüst und Rubrics

**Ziel:** Keine Logik, nur Struktur.

Dateien:

```text
.github/evals/README.md
.github/evals/schemas/task.schema.json
.github/evals/schemas/trial-result.schema.json
.github/evals/rubrics/semantic-equivalence.rubric.md
.github/evals/rubrics/documentation-quality.rubric.md
.github/evals/rubrics/code-quality.rubric.md
.github/evals/rubrics/harness-adherence.rubric.md
docs/tmp/ai-evals/.gitkeep
```

Akzeptanz:

- Agent-Harness-Freshness bleibt grün.
- Kontext-Freshness bleibt grün.
- Keine bestehenden Agenten ändern.

---

### PR 2 — Deterministischer Scorer

**Ziel:** Lokale Outputs gegen Task-JSON bewerten.

Dateien:

```text
scripts/ai-eval-score.py
.github/evals/tasks/smoke/smoke-doc-001.json
.github/evals/prompts/smoke-doc-001.md
```

Funktionen:

- Task JSON laden.
- Output laden.
- Required sections prüfen.
- Required/forbidden terms prüfen.
- Scope prüfen.
- Protected paths prüfen.
- Result JSON schreiben.

Akzeptanz:

```powershell
python scripts/ai-eval-score.py --task .github/evals/tasks/smoke/smoke-doc-001.json --output docs/tmp/ai-evals/sample-output.md
```

---

### PR 3 — Pairwise Comparator

**Ziel:** Baseline vs Candidate Report erzeugen.

Dateien:

```text
scripts/ai-eval-compare.py
.github/evals/rubrics/semantic-equivalence.rubric.md
```

Funktionen:

- Baseline-Output und Candidate-Output lesen.
- Deterministische Ergebnisse zusammenführen.
- Optional LLM-Judge-Payload erzeugen.
- Vergleichsreport schreiben.

Akzeptanz:

```powershell
python scripts/ai-eval-compare.py `
  --task .github/evals/tasks/smoke/smoke-doc-001.json `
  --baseline docs/tmp/ai-evals/baseline/output.md `
  --candidate docs/tmp/ai-evals/candidate/output.md `
  --out docs/tmp/ai-evals/reports/smoke-doc-001-comparison.md
```

---

### PR 4 — 10 Smoke Tasks

**Ziel:** Erste echte Evaluationsbasis.

Task-Liste:

| ID | Kategorie | Zweck |
|---|---|---|
| `smoke-doc-001` | docs | Spezifikation aus Kontext |
| `smoke-doc-002` | docs | README-Abschnitt verbessern |
| `smoke-harness-001` | harness | Agent-Instruction minimal verbessern |
| `smoke-harness-002` | harness | Skill-Regel prüfen und kürzen |
| `smoke-context-001` | context | Kontext-Freshness bewerten |
| `smoke-code-py-001` | code | kleine Python-Änderung + ruff/pyright |
| `smoke-code-py-002` | test | Python-Test ergänzen |
| `smoke-code-ts-001` | code | kleine TS/React-Änderung + tsc/eslint |
| `smoke-review-001` | review | Diff-Review nach Schema |
| `smoke-qa-001` | qa | QA-Report nach Gates |

Akzeptanz:

- Alle Tasks haben eindeutige Akzeptanzkriterien.
- Jeder Task kann manuell durch den Engineer-Agent ausgeführt werden.
- Jeder Task hat mindestens 3 deterministische Checks.

---

### PR 5 — Eval-Modus in Hooks

**Ziel:** Bestehende Hooks nicht ersetzen, sondern erweitern.

Änderungen:

```text
.github/hooks/session-start.ps1
.github/hooks/pre-tool-use.ps1
.github/hooks/post-format.ps1
.github/hooks/stop-context-check.ps1
```

Nur wenn:

```text
SAMPLEPROJECT_AI_EVAL=1
```

Dann:

- JSONL-Event schreiben nach `docs/tmp/ai-evals/events/`.
- Keine Toolinhalte speichern, außer ausdrücklich erlaubt.
- Toolname, Eventname, Timestamp, Task-ID, Variant, Exit-Code erfassen.

Akzeptanz:

- Ohne `SAMPLEPROJECT_AI_EVAL=1` bleibt Verhalten unverändert.
- Mit `SAMPLEPROJECT_AI_EVAL=1` entsteht ein Event-Log.
- Secret-Pattern werden nicht geloggt.

---

### PR 6 — Report Generator

**Ziel:** Ein Markdown-Report pro Experiment.

Datei:

```text
scripts/ai-eval-report.py
```

Output:

```text
docs/tmp/ai-evals/reports/<experiment-id>.md
```

Report enthält:

- Experiment-Metadaten.
- Artefakt unter Test.
- Baseline/Candidate-Version.
- Task-Tabelle.
- Hard-Gate-Fails.
- Candidate wins/ties/losses.
- Token/Tool/Latency, falls vorhanden.
- Top 5 Regressionen.
- Top 5 Verbesserungen.
- Empfehlung: merge / do not merge / manual review.

---

### PR 7 — Optional: Promptfoo Adapter

**Ziel:** Nur wenn du schneller Matrix-Views und model-graded assertions willst.

Empfehlung:

- Nicht als Pflichtdependency.
- Nur als optionaler Adapter.
- SampleProject-eigene JSON-Ergebnisse bleiben Source of Truth.

Möglicher Nutzen:

- `llm-rubric`
- `agent-rubric`
- `select-best`
- `trajectory:goal-success`
- CI-/CLI-Matrix-Auswertung

---

### PR 8 — CI-Smoke-Gate

**Ziel:** Bei Harness-Artefaktänderungen automatisch minimal prüfen.

Trigger-Pfade:

```yaml
.github/agents/**
.github/instructions/**
.github/prompts/**
.github/skills/**
.github/hooks/**
.github/context/**
.github/schemas/**
AGENTS.md
*/AGENTS.md
clasp/rules/**
.codex/**
.opencode/**
```

CI-Ebene 1:

- JSON-Schema validieren.
- Rubric-Dateien vorhanden.
- Agent-Harness-Freshness.
- Context-Freshness.
- Deterministische Smoke-Scorer mit Fixture-Outputs.

CI-Ebene 2, optional:

- LLM-Judge nur lokal oder in geschütztem Workflow mit Secrets.

---

## 6. Beispiel: Vergleich zweier Engineer-Agent-Outputs

### 6.1 Task

```text
Bitte erstelle eine kurze Implementierungsspezifikation für eine Änderung am Backtesting-V2-Service.
Der Output muss Ziel, Nicht-Ziele, Schritte, Validierung und Risiken enthalten.
Erfinde keine Dateien. Nutze nur bereitgestellten oder verifizierten Kontext.
```

### 6.2 Baseline Output

```text
docs/tmp/ai-evals/runs/exp-001/baseline/smoke-doc-001/t01/output.md
```

### 6.3 Candidate Output

```text
docs/tmp/ai-evals/runs/exp-001/candidate/smoke-doc-001/t01/output.md
```

### 6.4 Bewertungslogik

Candidate ist **FAIL**, wenn:

- eine Pflichtsektion fehlt,
- falsche SampleProject-Dateien behauptet werden,
- keine Validierung genannt wird,
- Schutzpfade berührt werden,
- Candidate weniger konkrete Schritte enthält als Baseline,
- Candidate eine alte korrekte Anforderung verliert.

Candidate ist **PASS**, wenn:

- alle Pflichtsektionen vorhanden sind,
- keine falschen Pfade erfunden werden,
- Validierung konkreter oder gleichwertig ist,
- Candidate inhaltlich äquivalent oder besser ist,
- keine Scope-/Security-Verstöße auftreten.

---

## 7. Empfohlene Metriken für SampleProject

### 7.1 MVP-Metriken

| Metrik | Typ | Muss in MVP? |
|---|---|---|
| `deterministic_pass_rate` | objektiv | Ja |
| `scope_violation_count` | objektiv | Ja |
| `protected_file_violation_count` | objektiv | Ja |
| `required_section_pass_rate` | objektiv | Ja |
| `required_term_coverage` | objektiv | Ja |
| `forbidden_term_violation_count` | objektiv | Ja |
| `semantic_regression_verdict` | Judge | Ja |
| `documentation_quality_score` | Judge | Ja für Docs |
| `code_quality_score` | Judge + Tests | Ja für Code |
| `harness_adherence_score` | Judge | Ja |
| `manual_review_required` | Judge | Ja |

### 7.2 Nach MVP

| Metrik | Typ | Wann einführen? |
|---|---|---|
| `tool_call_count` | Trace | wenn Hook/OTel aktiv |
| `terminal_error_count` | Trace | wenn Hook/OTel aktiv |
| `total_tokens` | OTel | wenn OTel aktiv |
| `latency_ms` | OTel | wenn OTel aktiv |
| `turn_count` | OTel/Debug | wenn OTel aktiv |
| `recovery_success_rate` | Trace | wenn mehrere Fehlertraces vorhanden |
| `candidate_win_rate` | Vergleich | ab 20+ Tasks |
| `pass_at_1` | Statistik | ab Mehrfach-Trials |
| `pass_hat_k` | Statistik | ab Mehrfach-Trials |
| `diff_size_delta` | Git | für Code-Tasks |
| `complexity_delta` | statisch | später |
| `survival_to_commit` | Git-Historie | viel später |

---

## 8. Warum diese Reihenfolge?

### 8.1 Deterministische Gates zuerst

Sie sind:

- billig,
- schnell,
- objektiv,
- leicht in CI integrierbar,
- leicht zu debuggen.

Sie beantworten aber nicht alles. Ein Dokument kann alle Pflichtüberschriften enthalten und trotzdem inhaltlich schlecht sein. Deshalb kommt danach der Pairwise Judge.

### 8.2 Pairwise Judge statt allgemeinem „Quality Score“

Deine konkrete Frage lautet nicht:

```text
Wie gut ist dieser Output absolut?
```

Sondern:

```text
Ist Candidate mindestens so gut wie Baseline?
```

Dafür ist pairwise comparison besser geeignet.

### 8.3 Hooks vor OTel-Plattform

SampleProject hat Hooks bereits. Deshalb ist ein einfacher JSONL-Eval-Modus günstiger als sofort Phoenix/LangSmith/OTel-Backend einzuführen.

OTel ist trotzdem später sehr sinnvoll, weil VS Code damit Token, Tool Calls, Latenz und Trace-Struktur liefern kann.

### 8.4 Promptfoo nur optional

Promptfoo ist praktisch, wenn du schnell:

- Matrix-Vergleiche,
- `llm-rubric`,
- `agent-rubric`,
- `select-best`,
- `trajectory:goal-success`,
- CI-Anbindung

willst.

Aber: Eine zusätzliche Dependency und ein zweites Konfigurationsmodell erhöhen Komplexität. Darum erst SampleProject-eigene JSON-Ergebnisse als Source of Truth, Promptfoo später als Adapter.

---

## 9. Nicht empfohlene Starts

### 9.1 Kein einzelner „AI Quality Score“

Ein Einzelscore versteckt zu viel.

Beispiel:

```text
Candidate +5% QualityIndex
aber:
- 3x mehr Tokens
- Scope-Verstoß
- weniger Validierung
```

Das ist kein echter Gewinn.

### 9.2 Kein reiner String-/Diff-Vergleich

Für Dokumentation und Agent-Outputs ist ein Text-Diff zu spröde.  
Gute Outputs dürfen anders formuliert sein.

Nutze Diff nur für:

- Dateiumfang,
- geänderte Pfade,
- gelöschte Sektionen,
- offensichtliche Regressionen.

### 9.3 Kein Agent-Selbstbericht als Ground Truth

Wenn der Agent schreibt:

```text
Ich habe alle Tests ausgeführt.
```

ist das kein Beweis.

Beweis ist:

- Terminal-Output,
- Hook-Event,
- OTel-Trace,
- gespeicherter Testreport,
- Scorer-Ergebnis.

### 9.4 Kein großes Benchmark-System am Anfang

Ein reproduzierbarer VS-Code-Runner wäre langfristig gut, ist aber für den Start zu teuer.  
Erst Tasks, Scorer, Pairwise Judge, Hooks.

---

## 10. Source-Age-Katalog

Alle Altersangaben relativ zu **2026-06-03**.

| Quelle | Typ | Datum | Alter | Relevanz |
|---|---|---:|---:|---|
| VS Code Blog: “The Coding Harness Behind GitHub Copilot in VS Code” | Offizieller Blog | 2026-05-15 | 19 Tage | Harness als Produkt, VSC-Bench, Solution Correctness, Agent Effort, Token Efficiency, Latency, PR-Eval-Assessment |
| VS Code Docs: OpenTelemetry Monitoring | Offizielle Docs | online verifiziert 2026-06-03 | 0 Tage seit Verifikation | Traces, Metrics, Events, Tokens, Tool Calls, Latenz, SQLite/JSONL Export |
| VS Code Docs: Chat Debug View | Offizielle Docs | online verifiziert 2026-06-03 | 0 Tage seit Verifikation | Agent Debug Logs, Chat Debug View, Export als OTLP JSON |
| VS Code Docs: Agent Hooks | Offizielle Docs | online verifiziert 2026-06-03 | 0 Tage seit Verifikation | SessionStart, PreToolUse, PostToolUse, Stop, deterministic automation |
| Anthropic Engineering: “Demystifying evals for AI agents” | Engineering Blog | 2026-01-09 | ca. 4 Monate 25 Tage | Tasks, Trials, Grader, Traces, deterministic/model/human graders, 20–50 Tasks |
| GitHub Blog: “Validating agentic behavior when correct isn’t deterministic” | Offizieller Blog | 2026-05-06, aktualisiert 2026-05-26 | 8 Tage seit Update | Nichtdeterminismus, Trace-Graphen, essentielle Zustände, semantische Gleichwertigkeit |
| Promptfoo Docs | Tool-Dokumentation | 2026-06-03 | 0 Tage | Open-source CLI, model-graded assertions, agent-rubric, trajectory:goal-success |
| SlopCodeBench | arXiv Paper | 2026-03-25 | ca. 2 Monate 9 Tage | Pass-Rate reicht nicht; Verbosity/Structural Erosion bei iterativen Coding Agents |
| AgentAtlas | arXiv Paper | 2026-05-26 | 8 Tage | Outcome Success von Control-Decision und Trajectory Quality trennen |
| Log Analysis for AI Agents | arXiv Paper | 2026-05 | ca. <1 Monat | Outcome-only-Evals verdecken interne/sicherheitsrelevante Fehler |
| AgentAssay | arXiv Paper | 2026-03-03 | ca. 3 Monate | PASS/FAIL/INCONCLUSIVE, Regressionstests für nichtdeterministische Agent Workflows |
| Automated Structural Testing of LLM Agents | arXiv Paper | 2026-01-25 | ca. 4 Monate 9 Tage | OTel-Traces, Mocking, Assertions, Regression Testing |
| Agentic Harness Engineering | arXiv Paper | 2026-04-28 | ca. 1 Monat 6 Tage | Harness-Komponenten als editierbare, revertierbare Artefakte; Observability-basierte Evolution |

---

## 11. Quellen-URLs

- https://code.visualstudio.com/blogs/2026/05/15/agent-harnesses-github-copilot-vscode
- https://code.visualstudio.com/docs/agents/guides/monitoring-agents
- https://code.visualstudio.com/docs/agents/agent-troubleshooting/chat-debug-view
- https://code.visualstudio.com/docs/agent-customization/hooks
- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- https://github.blog/ai-and-ml/generative-ai/validating-agentic-behavior-when-correct-isnt-deterministic/
- https://www.promptfoo.dev/docs/intro/
- https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/
- https://arxiv.org/abs/2603.24755
- https://arxiv.org/html/2605.20530v2
- https://arxiv.org/html/2605.08545v1
- https://arxiv.org/abs/2603.02601
- https://arxiv.org/abs/2601.18827
- https://arxiv.org/html/2604.25850v1

---

## 12. Erste konkrete nächste Aktion

Starte mit **PR 1** und **PR 2**.

Minimaler erster Commit:

```text
.github/evals/README.md
.github/evals/schemas/task.schema.json
.github/evals/schemas/trial-result.schema.json
.github/evals/rubrics/semantic-equivalence.rubric.md
.github/evals/rubrics/documentation-quality.rubric.md
.github/evals/tasks/smoke/smoke-doc-001.json
.github/evals/prompts/smoke-doc-001.md
scripts/ai-eval-score.py
docs/tmp/ai-evals/.gitkeep
```

Danach kannst du den Engineer-Agent zweimal laufen lassen:

```text
baseline:  alter engineer.agent.md
candidate: neuer engineer.agent.md
task:      smoke-doc-001
```

Und dann:

```powershell
python scripts/ai-eval-score.py --task .github/evals/tasks/smoke/smoke-doc-001.json --output docs/tmp/ai-evals/runs/.../baseline/output.md
python scripts/ai-eval-score.py --task .github/evals/tasks/smoke/smoke-doc-001.json --output docs/tmp/ai-evals/runs/.../candidate/output.md
python scripts/ai-eval-compare.py --task .github/evals/tasks/smoke/smoke-doc-001.json --baseline ... --candidate ... --out docs/tmp/ai-evals/reports/exp-001.md
```

Wenn dieser manuelle Loop funktioniert, erst dann lohnt sich Hook- und OTel-Automatisierung.

---

## 13. Entscheidung

**Empfohlener MVP:**  
`Deterministische Gates + Task-Katalog + Pairwise Semantic Judge + optional Hook-Logging`.

**Nicht empfohlen als MVP:**  
Vollständige VS-Code-Runner-Automation, Trace-Graphen, automatische Harness-Evolution, großer Benchmark-Klon.

**Warum:**  
SampleProject hat bereits gute Bausteine: Validierungskommandos, Agent-Harness-Freshness-Skripte, Agent-/Skill-/Prompt-Struktur und Hooks. Der schnellste Weg zu verwertbaren Ergebnissen ist, diese vorhandenen Flächen zu nutzen, statt eine neue Plattform daneben zu bauen.
