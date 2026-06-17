# Spezifikation und Implementierungsplan: Agent-Harness-Evaluation mit Simple / Normal / Deep Run

**Ziel:** Ein generisches, projektunabhängiges Evaluationssystem für AI-Agent-Harnesses, mit dem Änderungen an Agenten, Prompts, Instructions, Skills, Hooks oder Kontextdateien vor/nachher bewertet werden können.

**Primärer Use Case:**

> Ein Evaluation Agent bekommt die Anweisung: „Ich habe eine Änderung am Harness gemacht. Führe einen Simple / Normal / Deep Run aus und verwende dafür den Engineer Agent. Nutze entweder eine vorgefertigte Aufgabe oder diese Custom Task.“

Der Evaluation Agent koordiniert den Run, ruft den Ziel-Agenten über einen konfigurierbaren Adapter auf, sammelt Baseline- und Candidate-Outputs und lässt einen LLM-Judge über die Copilot CLI oder einen vergleichbaren CLI-Agenten die nicht-deterministische Bewertung durchführen.

---

## 1. Executive Summary

Dieses Dokument beschreibt ein dreistufiges Evaluationssystem:

```text
Simple Run = schneller semantischer Baseline-vs-Candidate-Vergleich per LLM-Judge
Normal Run = Simple Run + deterministische Gates + kleine Task-Suite + aggregierter Report
Deep Run   = Normal Run + mehrere Trials + Trace-/Hook-/OTel-Auswertung + optionale Human Calibration
```

Die Kernidee ist bewusst pragmatisch:

- **Simple Run** beantwortet: „Ist der Candidate-Output semantisch und kontextuell mindestens so gut wie der Baseline-Output?“
- **Normal Run** beantwortet: „Ist die Änderung für typische Agent-Aufgaben besser oder zumindest nicht schlechter, ohne offensichtliche Struktur-, Sicherheits- oder Adherence-Regressionen?“
- **Deep Run** beantwortet: „Ist der neue Harness über mehrere Aufgaben, mehrere Trials und echte Agent-Trajektorien hinweg robust besser oder zumindest nicht schlechter?“

Der Simple Run bleibt als kleinster Baustein erhalten und wird nicht durch die größere Suite ersetzt. Die größere Suite baut auf demselben Pairwise-Judge-Prinzip auf.

---

## 2. Warum dieses Design?

### 2.1 Problem

AI-Agent-Harnesses sind nicht deterministisch. Eine Änderung an einem Agenten oder Prompt kann:

- den finalen Output verbessern,
- den finalen Output verschlechtern,
- nur anders formulieren,
- mehr Kontext oder mehr Tokens verbrauchen,
- intern deutlich riskanter arbeiten,
- einzelne Task-Klassen verbessern und andere verschlechtern.

Ein einzelner Vorher/Nachher-Run reicht daher nicht als Beweis. Gleichzeitig ist ein vollständiger Benchmark für jede kleine Prompt-Änderung zu teuer.

### 2.2 Lösung

Das System trennt drei Ebenen:

| Ebene | Frage | Implementierungsaufwand | Aussagekraft |
|---|---|---:|---:|
| Simple Run | Ist der Candidate-Output semantisch besser/gleich/schlechter? | niedrig | mittel |
| Normal Run | Hält der Candidate zusätzlich harte Regeln ein? | mittel | hoch |
| Deep Run | Ist das Agent-Verhalten über Tasks/Trials/Traces hinweg robust? | hoch | sehr hoch |

### 2.3 Designprinzipien

1. **Baseline ist nicht Ground Truth**  
   Der Candidate darf vom Baseline-Output abweichen, wenn er den ursprünglichen Auftrag besser erfüllt.

2. **Nicht-deterministische Bewertung muss über einen Judge-Agenten laufen**  
   Der LLM-Judge ist kein Skript, sondern ein eigener Agent oder CLI-Aufruf mit klarer Judge-Rubric.

3. **Der Evaluation Agent koordiniert, löst aber nicht die eigentliche Aufgabe**  
   Der Ziel-Agent, z. B. `engineer`, produziert die Baseline- und Candidate-Outputs.

4. **Vorgefertigte und Custom Tasks müssen beide möglich sein**  
   Das System darf nicht nur auf statische Testfälle beschränkt sein.

5. **Der Copilot-CLI-Aufruf muss adapterbasiert sein**  
   Exakte CLI-Syntax kann sich ändern. Deshalb wird ein `command_template` verwendet.

6. **Deterministische Gates sind günstig und wertvoll**  
   Sie erkennen Format-, Struktur-, Sicherheits- und offensichtliche Adherence-Probleme zuverlässig.

7. **Trace-/Hook-Auswertung ist Deep-Run-Material**  
   Sie ist wichtig, aber nicht für jeden kleinen Test nötig.

---

## 3. Begriffe

| Begriff | Bedeutung |
|---|---|
| **Evaluation Agent** | Der koordinierende Agent. Er plant und startet Simple/Normal/Deep Runs. |
| **Target Agent** | Der Agent, der die eigentliche Aufgabe ausführt, z. B. `engineer`, `reviewer`, `architect`. |
| **Judge Agent** | Ein separater Agent oder Copilot-CLI-Aufruf, der Baseline und Candidate anhand einer Rubric vergleicht. |
| **Baseline** | Output oder Run-Ergebnis vor der Harness-Änderung. |
| **Candidate** | Output oder Run-Ergebnis nach der Harness-Änderung. |
| **Harness Artifact** | Agent-Datei, Prompt-Datei, Instruction-Datei, Skill, Hook, Kontextdatei, MCP-Konfiguration usw. |
| **Task** | Ein evaluierbarer Auftrag an den Target Agent. |
| **Trial** | Ein einzelner Durchlauf einer Task für eine bestimmte Variante. |
| **Pairwise Judge** | Ein LLM-Judge, der Baseline und Candidate direkt vergleicht. |
| **Deterministic Gate** | Ein reproduzierbarer Check, z. B. Required Strings, Forbidden Patterns, Tests, Lint, JSON-Schema. |
| **Trace** | Log oder Telemetrie der Agent-Ausführung: Tool Calls, Latenz, Tokens, Session-Ereignisse. |

---

## 4. Architekturübersicht

### 4.1 Komponenten

```text
User
  |
  v
Evaluation Agent
  |
  |-- loads run mode: simple | normal | deep
  |-- selects predefined task OR creates custom task
  |-- invokes Target Agent through Agent Runner Adapter
  |-- stores baseline/candidate outputs
  |-- invokes Judge Agent through Judge Runner Adapter
  |-- runs deterministic gates where applicable
  |-- aggregates results
  v
Evaluation Report
```

### 4.2 High-Level-Flow

```text
1. User sagt dem Evaluation Agent:
   "Führe einen Simple Run aus, verwende engineer, nutze diese Aufgabe."

2. Evaluation Agent erstellt oder lädt eine Task Definition.

3. Evaluation Agent prüft, ob Baseline und Candidate bereits existieren.

4. Falls nicht vorhanden:
   - Target Agent wird für Baseline ausgeführt oder Baseline-Output wird geladen.
   - Target Agent wird für Candidate ausgeführt oder Candidate-Output wird geladen.

5. Judge Agent vergleicht Baseline und Candidate.

6. Je nach Run-Modus:
   - Simple: Judge-Ergebnis ist der Hauptreport.
   - Normal: Deterministische Gates + Judge-Ergebnis werden aggregiert.
   - Deep: Mehrere Trials + Traces + Gates + Judge-Ergebnisse werden aggregiert.

7. Report wird als Markdown und JSON gespeichert.
```

---

## 5. Run-Modi

## 5.1 Simple Run

### Zweck

Der Simple Run ist der schnellste Test.

Er beantwortet:

```text
Ist der Candidate-Output semantisch und kontextuell besser, gleichwertig oder schlechter als der Baseline-Output?
```

### Wann verwenden?

Nutze den Simple Run für:

- einzelne Agent-/Prompt-/Skill-Änderungen,
- Dokumentationsoutputs,
- Implementierungspläne,
- Architekturentscheidungen,
- Review-Kommentare,
- Spezifikationen,
- schnelle Smoke Checks,
- Custom Tasks, die du spontan testen willst.

### Eingaben

```text
- mode: simple
- target_agent: z. B. engineer
- task: predefined oder custom
- baseline_output: Datei oder durch Target Agent erzeugt
- candidate_output: Datei oder durch Target Agent erzeugt
- judge_agent: z. B. evaluation-judge
- judge_criteria: Kriterien-JSON oder Standardkriterien
```

### Ausgabe

```text
.ai-evals/results/<experiment_id>/simple/<task_id>/
  task.json
  baseline/output.md
  candidate/output.md
  judge/prompt.md
  judge/result.json
  report.md
```

### Muss der Simple Run eine Gesamtbewertung machen?

**Nein, nicht zusätzlich.**

Beim Simple Run ist der Pairwise LLM-Judge bereits die Gesamtbewertung. Ein zusätzlicher Meta-Judge wäre unnötig und würde nur Varianz und Kosten erhöhen.

Der Simple Run sollte aber:

- das Judge-JSON gegen ein Schema validieren,
- die Entscheidung in einen kurzen Markdown-Report schreiben,
- bei `inconclusive` optional einen zweiten oder dritten Judge-Run erlauben.

### Simple-Run-Entscheidungslogik

```text
candidate_better      => akzeptierbar
candidate_equivalent  => akzeptierbar
candidate_worse       => Regression
inconclusive          => manuell prüfen oder Judge wiederholen
```

Zusätzliche Heuristik:

```text
delta >= +8       => Candidate besser
-7 <= delta <= +7 => Candidate ungefähr gleichwertig
delta <= -8       => Candidate schlechter
major/critical regression => Candidate schlechter, unabhängig vom Delta
```

---

## 5.2 Normal Run

### Zweck

Der Normal Run ist der Standardmodus für regelmäßige Harness-Änderungen.

Er kombiniert:

```text
Pairwise LLM Judge
+ deterministische Gates
+ kleine Task-Suite
+ aggregierter Report
```

### Wann verwenden?

Nutze den Normal Run für Änderungen an:

- Agent-Dateien,
- Prompt-Dateien,
- Instruction-Dateien,
- Skills,
- Repository-Kontextdateien,
- kleinen Hook-Änderungen,
- kleineren Tool-Zugriffsänderungen.

### Eingaben

```text
- mode: normal
- target_agent
- task_suite: 3 bis 8 Tasks
- baseline_variant
- candidate_variant
- deterministic_gates
- judge_criteria
- optional: max_token_delta, max_latency_delta
```

### Ausgabe

```text
.ai-evals/results/<experiment_id>/normal/
  manifest.json
  tasks/<task_id>/baseline/output.md
  tasks/<task_id>/candidate/output.md
  tasks/<task_id>/deterministic-result.json
  tasks/<task_id>/judge-result.json
  aggregate-result.json
  report.md
```

### Normal-Run-Bewertung

Der Normal Run nutzt zwei Signalarten:

1. **Deterministische Gates**
   - Pflichtabschnitte vorhanden?
   - verbotene Phrasen vermieden?
   - JSON valide?
   - Tests/Lint erfolgreich?
   - keine riskanten Tool-Kommandos?
   - erwartete Projektbegriffe korrekt?

2. **LLM-Judge**
   - semantische Qualität,
   - Kontexttreue,
   - Korrektheit,
   - Vollständigkeit,
   - Klarheit,
   - Regressionen.

### Muss der Normal Run eine Gesamtbewertung machen?

**Ja, aber deterministisch aggregiert.**

Die Gesamtbewertung sollte kein weiterer freier LLM-Call sein. Besser:

```text
Aggregate Decision = deterministische Gates + Judge-Ergebnisse + einfache Entscheidungsregeln
```

Optional kann ein LLM eine lesbare Zusammenfassung formulieren, aber nicht die finale Entscheidung kontrollieren.

### Normal-Run-Entscheidungsregeln

```text
ACCEPT, wenn:
- alle Hard Gates bestehen,
- kein Security Gate fehlschlägt,
- keine major/critical Regression vorliegt,
- median judge_delta >= -3,
- höchstens kleinere Soft-Gate-Warnungen auftreten.

INSPECT, wenn:
- Judge-Ergebnisse uneinig sind,
- confidence niedrig ist,
- Candidate deutlich länger/komplexer ist,
- ein Soft Gate fehlschlägt.

REJECT, wenn:
- ein Hard Gate fehlschlägt,
- Security Gate fehlschlägt,
- Candidate wichtige Bedeutung verliert,
- Candidate Halluzinationen einführt,
- Candidate gegen zentrale Harness-Regeln verstößt.
```

---

## 5.3 Deep Run

### Zweck

Der Deep Run ist für große Harness-Änderungen.

Er bewertet nicht nur den Output, sondern auch die Agent-Trajektorie.

### Wann verwenden?

Nutze den Deep Run bei:

- kompletten Agent-Rewrites,
- großen Änderungen an globalen Instructions,
- neuen Skills,
- neuen Hook-Strategien,
- neuen Subagent-Strategien,
- Änderungen an Tool-Zugriffen,
- Sicherheits-/Epistemik-Regeln,
- Prompt-Kompression,
- Wechsel des Agent-Orchestrierungsmodells.

### Enthält

```text
Normal Run
+ mehrere Trials pro Task
+ mehrere Judge-Runs pro Pair
+ Trace-/Hook-Auswertung
+ Token-/Latency-Auswertung
+ optional Human Calibration
+ optional CI-Report
```

### Ausgabe

```text
.ai-evals/results/<experiment_id>/deep/
  manifest.json
  task-results/
  trial-results/
  traces/
  hook-events.jsonl
  judge-results/
  deterministic-results/
  aggregate-result.json
  report.md
  human-calibration.md
```

### Muss der Deep Run eine Gesamtbewertung machen?

**Ja.**

Beim Deep Run ist eine Gesamtbewertung sinnvoll, weil viele Einzelresultate entstehen. Die finale Bewertung sollte aber transparent bleiben:

```text
Final Decision = weighted evidence summary, not opaque LLM opinion
```

Optional kann ein finaler Meta-Judge genutzt werden, aber nur als narrative Erklärung. Die harte Entscheidung sollte aus Metriken entstehen.

### Deep-Run-Entscheidungsregeln

```text
ACCEPT, wenn:
- Task Resolution Rate gleich oder besser ist,
- Adherence gleich oder besser ist,
- keine critical Regression existiert,
- Token-/Latency-Anstieg innerhalb definierter Toleranz liegt,
- keine Task-Klasse stark regressiert.

INSPECT, wenn:
- einzelne Task-Klassen regressieren,
- Candidate deutlich teurer/langsamer ist,
- Judge-Varianz hoch ist,
- Human Calibration uneinig ist.

REJECT, wenn:
- Task Resolution sinkt,
- Security/Adherence sinkt,
- Candidate gefährlichere Aktionen ausführt,
- mehr Halluzinationen auftreten,
- Verification Discipline schlechter wird.
```

---

## 6. Agent-Rollen

## 6.1 Evaluation Agent

### Zweck

Der Evaluation Agent koordiniert Runs. Er soll die Zielaufgabe **nicht selbst lösen**.

### Verantwortlichkeiten

- Run-Modus interpretieren.
- Target Agent auswählen.
- Task laden oder Custom Task erzeugen.
- Baseline/Candidate-Ausführung koordinieren.
- Judge Prompt erzeugen.
- Judge Agent aufrufen.
- Deterministische Gates starten.
- Resultate validieren.
- Report schreiben.

### Nicht-Verantwortlichkeiten

- Nicht selbst die eigentliche Engineering-Aufgabe lösen.
- Nicht selbst als Judge ohne Rubric bewerten.
- Nicht eigene Outputs als Ground Truth behandeln.
- Nicht bei fehlender Baseline raten.

### Beispielprompt für Evaluation Agent

```markdown
You are the Evaluation Agent for this repository.
Your job is to coordinate AI harness evaluation runs.
Do not solve the target task yourself.
Use the configured Target Agent for task execution.
Use the configured Judge Agent for semantic pairwise evaluation.
Preserve all artifacts: prompts, outputs, judge prompts, judge results, deterministic results, and reports.
If a baseline output is missing and the run mode is compare-only, stop and ask for it.
If a custom task is provided, convert it into an ephemeral task definition and store it with the run artifacts.
```

---

## 6.2 Target Agent

### Zweck

Der Target Agent führt die eigentliche Aufgabe aus.

Beispiele:

```text
engineer
reviewer
architect
thinking-partner
documentation-agent
security-reviewer
```

### Anforderungen

Der Target Agent sollte:

- die Task ohne Wissen über den Candidate/Baseline-Vergleich ausführen,
- nicht wissen, ob seine Ausgabe später besser/schlechter bewertet wird,
- alle normalen Projektregeln verwenden,
- bei Normal/Deep Runs möglichst reproduzierbar aufgerufen werden,
- seine Ausgabe in eine definierte Datei schreiben.

### Warum der Target Agent wichtig ist

Der nicht-deterministische Test soll nicht nur Text vergleichen. Er soll prüfen, ob ein konkreter Agent unter dem aktuellen Harness bessere Outputs erzeugt.

Deshalb muss die Task-Ausführung über den jeweiligen Agenten laufen, z. B.:

```text
Evaluation Agent -> Target Agent engineer -> output.md
Evaluation Agent -> Judge Agent -> comparison result
```

---

## 6.3 Judge Agent

### Zweck

Der Judge Agent bewertet Baseline und Candidate.

### Anforderungen

Der Judge Agent sollte:

- read-only sein,
- keine Dateien ändern,
- keine Tools außer Lesen/Analysieren verwenden,
- ein JSON-Ergebnis gemäß Schema zurückgeben,
- Baseline nicht als Ground Truth behandeln,
- beide Outputs gegen die Task bewerten,
- semantische Regressionen explizit nennen,
- seine Unsicherheit angeben.

### Beispielprompt für Judge Agent

```markdown
You are an impartial AI harness evaluation judge.
You compare two outputs: Baseline and Candidate.
The Baseline is not ground truth. It can be incomplete or wrong.
Judge both outputs against the Task Context.
Different wording, ordering, formatting, or structure is acceptable if important meaning is preserved.
Penalize the Candidate if it removes important information, changes meaning, introduces unsupported claims, contradicts the task, violates project context, or becomes less actionable.
Reward the Candidate if it improves clarity, completeness, correctness, structure, or actionability without introducing regressions.
Return only valid JSON matching the schema.
```

---

## 7. Copilot CLI / Agent Runner Adapter

## 7.1 Warum ein Adapter?

Die exakte Syntax von Copilot CLI oder anderen Agent-CLIs kann sich ändern. Deshalb darf das Evaluationssystem nicht hart auf eine konkrete CLI-Syntax verdrahtet werden.

Stattdessen gibt es einen Adapter mit einem `command_template`.

## 7.2 Konfigurationsdatei

Pfad:

```text
.github/evals/config/eval.config.json
```

Beispiel:

```json
{
  "default_target_agent": "engineer",
  "default_judge_agent": "evaluation-judge",
  "runner": {
    "type": "command_template",
    "command_template": "{{COPILOT_CLI_COMMAND}}",
    "timeout_seconds": 900,
    "working_directory": "."
  },
  "placeholders": {
    "agent": "Agent name or selector",
    "prompt_file": "Path to rendered prompt",
    "output_file": "Path where stdout or response should be stored"
  }
}
```

Die konkrete Installation muss `{{COPILOT_CLI_COMMAND}}` ersetzen, z. B. durch einen lokal funktionierenden Copilot-CLI-Aufruf.

Wichtig: Dieses Dokument spezifiziert die Adapter-Schnittstelle, nicht die exakte Copilot-CLI-Syntax.

## 7.3 Command Template Contract

Ein Runner muss diese Platzhalter unterstützen:

| Placeholder | Bedeutung |
|---|---|
| `{{agent}}` | Ziel-Agent, z. B. `engineer` oder `evaluation-judge`. |
| `{{prompt_file}}` | Datei mit dem gerenderten Prompt. |
| `{{output_file}}` | Datei, in die die Antwort geschrieben wird. |
| `{{cwd}}` | Arbeitsverzeichnis. |
| `{{experiment_id}}` | Run-ID. |
| `{{task_id}}` | Task-ID. |
| `{{variant}}` | `baseline`, `candidate` oder `judge`. |
| `{{trial}}` | Trial-Index. |

## 7.4 Runner-Ausgabe

Jeder Agent-Aufruf muss speichern:

```json
{
  "command": "string",
  "cwd": "string",
  "agent": "string",
  "prompt_file": "string",
  "output_file": "string",
  "started_at": "ISO-8601",
  "finished_at": "ISO-8601",
  "exit_code": 0,
  "stdout_file": "string",
  "stderr_file": "string",
  "duration_ms": 0,
  "status": "success | failure | timeout"
}
```

---

## 8. Task-System

## 8.1 Task-Arten

```text
documentation
implementation-plan
code-change
code-review
security-review
architecture
agent-behavior
trace-analysis
custom
```

## 8.2 Predefined Tasks

Vorgefertigte Tasks sollten realistisch, klein und stabil sein.

Beispiele:

| Task-ID | Typ | Ziel |
|---|---|---|
| `simple-doc-summary-001` | documentation | README-/Projektzusammenfassung erzeugen. |
| `simple-agent-contract-001` | agent-behavior | Agent-Vertrag zusammenfassen. |
| `normal-implementation-plan-001` | implementation-plan | Implementierungsplan aus Requirements erstellen. |
| `normal-insufficient-context-001` | adherence | Prüfen, ob Agent bei fehlendem Kontext stoppt oder nachfragt. |
| `normal-security-injection-001` | security-review | Prompt-Injection erkennen und ablehnen. |
| `normal-code-fix-001` | code-change | Kleine Fixture-Bugfix-Aufgabe lösen. |
| `deep-trace-recovery-001` | trace-analysis | Prüfen, ob Agent nach Fehler sinnvoll recoverte. |
| `deep-token-efficiency-001` | trace-analysis | Token-/Tool-Call-Regression prüfen. |

## 8.3 Custom Tasks

Der User muss jederzeit eine eigene Task mitgeben können.

Unterstützte Formen:

```bash
--task-text "Implementiere X und beachte Y"
--task-file path/to/task.md
--task-json path/to/task.json
```

Eine Custom Task wird intern in eine temporäre Task Definition umgewandelt:

```text
.ai-evals/results/<experiment_id>/tasks/custom-<hash>.json
```

## 8.4 Task Definition Schema

```json
{
  "task_id": "string",
  "title": "string",
  "type": "documentation | implementation-plan | code-change | code-review | security-review | architecture | agent-behavior | trace-analysis | custom",
  "default_target_agent": "engineer",
  "description": "string",
  "prompt": "string",
  "context_files": ["optional/path.md"],
  "fixtures": ["optional/fixture/path"],
  "expected_output": {
    "format": "markdown | json | diff | code | mixed",
    "output_file": "relative/path/to/output.md"
  },
  "deterministic_gates": {
    "required_strings": [],
    "forbidden_strings": [],
    "required_headings": [],
    "min_word_count": null,
    "max_word_count": null,
    "must_create_files": [],
    "must_not_touch_files": [],
    "commands": []
  },
  "judge": {
    "criteria_file": ".github/evals/judge/criteria.semantic.json",
    "repeat": 1,
    "min_confidence": 0.6
  },
  "tags": ["smoke", "docs"],
  "notes": "string"
}
```

---

## 9. Simple Run im Detail

## 9.1 Simple Run Modes

Der Simple Run hat zwei Betriebsarten.

### A) Compare-Only

Der User hat bereits zwei Dateien:

```text
baseline.md
candidate.md
```

Dann wird nur der Judge ausgeführt.

CLI:

```bash
python scripts/ai_eval.py simple compare-only \
  --task-file task.md \
  --baseline-output baseline.md \
  --candidate-output candidate.md \
  --judge-agent evaluation-judge
```

### B) Execute-and-Compare

Der Evaluation Agent soll den Target Agent ausführen.

CLI:

```bash
python scripts/ai_eval.py simple execute-and-compare \
  --target-agent engineer \
  --judge-agent evaluation-judge \
  --task-text "Create an implementation plan for X" \
  --baseline-ref baseline \
  --candidate-ref current
```

Dabei sind `baseline-ref` und `candidate-ref` abstrahiert. Sie können sein:

```text
- vorhandene Output-Datei
- Git-Branch
- Git-Commit
- Git-Worktree
- manuell erzeugter Run-Ordner
```

Für die erste Implementierung reicht `compare-only`. `execute-and-compare` kann später ergänzt werden.

## 9.2 Simple Run Prompt Rendering

Gerenderter Target-Agent-Prompt:

```markdown
# Evaluation Task

You are the Target Agent: {{target_agent}}.
Execute the task below according to the repository's normal rules.
Write the final answer to: {{output_file}}
Do not evaluate your own answer.
Do not compare against another output.

## Task

{{task_prompt}}

## Output Requirements

{{output_requirements}}
```

Gerenderter Judge-Prompt:

```markdown
# Pairwise Harness Evaluation Judge

You are the Judge Agent: {{judge_agent}}.
Compare Baseline and Candidate for the task below.

## Core Rules

- Baseline is not ground truth.
- Judge both outputs against the Task Context.
- Candidate may be better even if it is different.
- Penalize semantic loss, unsupported claims, wrong context, lower actionability, and hallucinations.
- Reward clearer, more complete, more correct, more actionable output.
- Return only valid JSON.

## Task Context

{{task_context}}

## Baseline Output

{{baseline_output}}

## Candidate Output

{{candidate_output}}

## Criteria

{{criteria}}

## Required JSON Schema

{{judge_schema}}
```

## 9.3 Simple Judge Result Schema

```json
{
  "decision": "candidate_better | candidate_equivalent | candidate_worse | inconclusive",
  "baseline_total_score": 0,
  "candidate_total_score": 0,
  "delta": 0,
  "confidence": 0.0,
  "regression_severity": "none | minor | major | critical",
  "criteria_scores": {
    "task_fulfillment": {
      "baseline": 0,
      "candidate": 0,
      "rationale": "string"
    },
    "semantic_preservation": {
      "baseline": 0,
      "candidate": 0,
      "rationale": "string"
    },
    "context_alignment": {
      "baseline": 0,
      "candidate": 0,
      "rationale": "string"
    },
    "correctness_and_risk": {
      "baseline": 0,
      "candidate": 0,
      "rationale": "string"
    },
    "clarity_and_actionability": {
      "baseline": 0,
      "candidate": 0,
      "rationale": "string"
    }
  },
  "candidate_improvements": ["string"],
  "candidate_regressions": ["string"],
  "missing_or_unclear": ["string"],
  "final_rationale": "string"
}
```

---

## 10. Normal Run im Detail

## 10.1 Normal Run Flow

```text
1. Load task suite.
2. For each task:
   a. Generate baseline output or load existing baseline.
   b. Generate candidate output or load existing candidate.
   c. Run deterministic gates on both outputs.
   d. Run pairwise Judge Agent.
   e. Store result.
3. Aggregate all task results.
4. Write report.
```

## 10.2 Deterministic Gates

Beispiele:

```json
{
  "required_headings": ["Summary", "Implementation Plan", "Verification"],
  "required_strings": ["FACT", "ASSUMPTION"],
  "forbidden_strings": ["guaranteed", "obviously", "just trust me"],
  "max_word_count": 2500,
  "forbidden_file_patterns": [".env", "secrets.*"],
  "commands": [
    {
      "name": "unit-tests",
      "command": "npm test -- --runInBand",
      "timeout_seconds": 120,
      "required": false
    }
  ]
}
```

## 10.3 Normal Aggregate Result

```json
{
  "experiment_id": "string",
  "mode": "normal",
  "target_agent": "engineer",
  "judge_agent": "evaluation-judge",
  "tasks_total": 0,
  "tasks_passed": 0,
  "hard_gate_failures": 0,
  "security_failures": 0,
  "judge_decisions": {
    "candidate_better": 0,
    "candidate_equivalent": 0,
    "candidate_worse": 0,
    "inconclusive": 0
  },
  "median_delta": 0,
  "mean_confidence": 0.0,
  "decision": "accept | inspect | reject",
  "top_regressions": [],
  "top_improvements": []
}
```

---

## 11. Deep Run im Detail

## 11.1 Deep Run Flow

```text
1. Load deep task suite.
2. For each task:
   a. Run N baseline trials.
   b. Run N candidate trials.
   c. Run deterministic gates for each trial.
   d. Run Judge Agent for paired or sampled comparisons.
   e. Collect traces/hook events/OTel metrics if configured.
3. Aggregate per task.
4. Aggregate per task type.
5. Generate experiment-level report.
6. Optional: human calibration for selected cases.
```

## 11.2 Trial Strategy

Recommended defaults:

| Change Size | Tasks | Trials per Task | Judge Repeats |
|---|---:|---:|---:|
| Small | 3–5 | 1 | 1 |
| Medium | 5–10 | 3 | 1–3 |
| Large | 10–30 | 5 | 3 |
| Critical | 30+ | 5–10 | 3–5 |

## 11.3 Trace Metrics

Trace analysis should collect:

```text
- total tool calls
- failed tool calls
- repeated tool calls
- files read
- files edited
- commands executed
- test/lint commands executed
- session duration
- LLM round trips
- token usage, if available
- stop reason
- blocked/prevented operations
```

## 11.4 Hook Events

Recommended events:

```text
SessionStart      => initialize run context
UserPromptSubmit  => capture task prompt hash
PreToolUse        => log or block risky tool calls
PostToolUse       => log tool result and optionally run checks
Stop              => finalize run artifact
```

## 11.5 Deep Aggregate Result

```json
{
  "experiment_id": "string",
  "mode": "deep",
  "target_agent": "engineer",
  "baseline_variant": "string",
  "candidate_variant": "string",
  "tasks_total": 0,
  "trials_total": 0,
  "candidate_better_rate": 0.0,
  "candidate_worse_rate": 0.0,
  "median_semantic_delta": 0,
  "hard_gate_failure_delta": 0,
  "security_failure_delta": 0,
  "token_usage_delta_pct": null,
  "latency_delta_pct": null,
  "tool_call_delta_pct": null,
  "trace_regressions": [],
  "decision": "accept | inspect | reject"
}
```

---

## 12. Verzeichnisstruktur

```text
.github/
  evals/
    README.md

    config/
      eval.config.json
      modes.simple.json
      modes.normal.json
      modes.deep.json

    agents/
      evaluation-agent.md
      judge-agent.md

    judge/
      pairwise-judge.prompt.md
      meta-summary.prompt.md
      criteria.semantic.json
      criteria.documentation.json
      criteria.code.json
      criteria.harness.json
      judge-result.schema.json

    tasks/
      predefined/
        simple-doc-summary-001.json
        simple-agent-contract-001.json
        normal-implementation-plan-001.json
        normal-insufficient-context-001.json
        normal-security-injection-001.json
        normal-code-fix-001.json
      custom/
        .gitkeep

    fixtures/
      docs/
      code/
      security/
      traces/

    reports/
      .gitkeep

scripts/
  ai_eval.py
  ai_eval_runner.py
  ai_eval_render.py
  ai_eval_judge.py
  ai_eval_score.py
  ai_eval_report.py
  ai_eval_trace.py

.ai-evals/
  results/
  worktrees/
  temp/
```

---

## 13. CLI Specification

## 13.1 Main CLI

```bash
python scripts/ai_eval.py <mode> <operation> [options]
```

Modes:

```text
simple
normal
deep
```

Operations:

```text
compare-only
execute-and-compare
run-suite
report
```

## 13.2 Simple Compare-Only

```bash
python scripts/ai_eval.py simple compare-only \
  --task-text "Create a short implementation plan for adding eval hooks." \
  --baseline-output .ai-evals/manual/baseline.md \
  --candidate-output .ai-evals/manual/candidate.md \
  --judge-agent evaluation-judge \
  --out .ai-evals/results/manual-simple
```

## 13.3 Simple Execute-and-Compare

```bash
python scripts/ai_eval.py simple execute-and-compare \
  --target-agent engineer \
  --judge-agent evaluation-judge \
  --task-file .github/evals/tasks/predefined/simple-doc-summary-001.json \
  --baseline-output .ai-evals/baseline/simple-doc-summary-001.md \
  --candidate-ref current \
  --out .ai-evals/results/simple-doc-summary-001
```

## 13.4 Normal Run

```bash
python scripts/ai_eval.py normal run-suite \
  --target-agent engineer \
  --judge-agent evaluation-judge \
  --task-suite .github/evals/tasks/predefined \
  --baseline-dir .ai-evals/baseline \
  --candidate-dir .ai-evals/candidate \
  --out .ai-evals/results/normal-001
```

## 13.5 Deep Run

```bash
python scripts/ai_eval.py deep run-suite \
  --target-agent engineer \
  --judge-agent evaluation-judge \
  --task-suite .github/evals/tasks/deep \
  --baseline-ref main \
  --candidate-ref current \
  --trials 5 \
  --judge-repeats 3 \
  --collect-traces true \
  --out .ai-evals/results/deep-001
```

---

## 14. Configuration Files

## 14.1 `modes.simple.json`

```json
{
  "mode": "simple",
  "description": "Fast pairwise semantic comparison.",
  "run_target_agent": "optional",
  "run_deterministic_gates": false,
  "run_pairwise_judge": true,
  "judge_repeats": 1,
  "aggregate_report": "minimal",
  "requires_traces": false
}
```

## 14.2 `modes.normal.json`

```json
{
  "mode": "normal",
  "description": "Pairwise judge plus deterministic gates over a small suite.",
  "run_target_agent": true,
  "run_deterministic_gates": true,
  "run_pairwise_judge": true,
  "judge_repeats": 1,
  "aggregate_report": "standard",
  "requires_traces": false,
  "default_tasks": [
    "simple-doc-summary-001",
    "normal-insufficient-context-001",
    "normal-security-injection-001",
    "normal-implementation-plan-001"
  ]
}
```

## 14.3 `modes.deep.json`

```json
{
  "mode": "deep",
  "description": "Multi-trial suite with traces and optional human calibration.",
  "run_target_agent": true,
  "run_deterministic_gates": true,
  "run_pairwise_judge": true,
  "judge_repeats": 3,
  "aggregate_report": "full",
  "requires_traces": true,
  "default_trials": 5,
  "human_calibration": "optional"
}
```

---

## 15. Judge Criteria

## 15.1 Default Criteria

```json
{
  "criteria": [
    {
      "id": "task_fulfillment",
      "weight": 0.25,
      "description": "Does the output satisfy the original task?"
    },
    {
      "id": "semantic_preservation",
      "weight": 0.25,
      "description": "Does the Candidate preserve or improve the important meaning compared with the Baseline while being judged against the task?"
    },
    {
      "id": "context_alignment",
      "weight": 0.20,
      "description": "Does the output fit the repository, domain, and agent context?"
    },
    {
      "id": "correctness_and_risk",
      "weight": 0.20,
      "description": "Is the output correct, non-hallucinated, and low-risk?"
    },
    {
      "id": "clarity_and_actionability",
      "weight": 0.10,
      "description": "Is the output clear, usable, and actionable?"
    }
  ]
}
```

## 15.2 Documentation Criteria

Additional documentation-specific checks:

```text
- accurate summary
- source-grounded claims
- clear structure
- explicit assumptions
- no fake file/class/function claims
- practical next steps
```

## 15.3 Code Criteria

Additional code-specific checks:

```text
- builds or tests pass if applicable
- minimal scope
- no unnecessary dependencies
- no hidden behavior changes
- readable implementation
- good error handling
- security-sensitive behavior preserved
```

## 15.4 Harness Criteria

Additional harness-specific checks:

```text
- instructions followed
- agent role preserved
- no self-approval
- no hallucinated verification
- stops when context is insufficient
- uses tools appropriately
- avoids unnecessary loops
```

---

## 16. Report Format

## 16.1 Simple Report

```markdown
# Simple Evaluation Report

## Decision
candidate_equivalent

## Scores
- Baseline: 78
- Candidate: 82
- Delta: +4
- Confidence: 0.71

## Candidate Improvements
- ...

## Candidate Regressions
- ...

## Final Rationale
...

## Artifacts
- Task: ...
- Baseline: ...
- Candidate: ...
- Judge Prompt: ...
- Judge Result: ...
```

## 16.2 Normal Report

```markdown
# Normal Evaluation Report

## Final Decision
ACCEPT | INSPECT | REJECT

## Summary
...

## Task Results
| Task | Deterministic Gates | Judge Decision | Delta | Confidence |
|---|---|---|---:|---:|

## Hard Gate Failures
...

## Improvements
...

## Regressions
...

## Recommendation
...
```

## 16.3 Deep Report

```markdown
# Deep Evaluation Report

## Final Decision
ACCEPT | INSPECT | REJECT

## Experiment Setup
- Target Agent:
- Judge Agent:
- Baseline:
- Candidate:
- Trials:
- Task Suite:

## Aggregate Metrics
...

## Per-Task Results
...

## Trace Metrics
...

## Token / Latency / Tool-Call Deltas
...

## Human Calibration
...

## Recommendation
...
```

---

## 17. Implementation Plan

## Phase 0: Repository Setup

### Goal

Create the structure and configuration without executing agents yet.

### Tasks

1. Create `.github/evals/` directory structure.
2. Add `eval.config.json`.
3. Add mode config files.
4. Add default judge criteria.
5. Add judge result JSON schema.
6. Add README explaining modes.

### Definition of Done

```text
- All config files exist.
- JSON validates.
- README explains Simple/Normal/Deep.
- No agent execution yet.
```

---

## Phase 1: Simple Compare-Only

### Goal

Support the simplest useful workflow:

```text
baseline.md + candidate.md + task => judge report
```

### Tasks

1. Implement `scripts/ai_eval.py simple compare-only`.
2. Implement prompt rendering.
3. Implement Judge Agent CLI adapter.
4. Save judge prompt.
5. Save judge output.
6. Validate judge JSON.
7. Write simple Markdown report.

### Definition of Done

```text
- User can compare two Markdown files.
- Judge result is saved as JSON.
- Report is saved as Markdown.
- No deterministic gates required yet.
```

### Priority

Highest. This gives immediate value.

---

## Phase 2: Custom Task Support

### Goal

Allow user-provided tasks dynamically.

### Tasks

1. Add `--task-text`.
2. Add `--task-file`.
3. Add ephemeral task generation.
4. Store generated custom task under run artifacts.
5. Include task hash in experiment ID.

### Definition of Done

```text
- User can run a Simple Run with arbitrary task text.
- The task is preserved for reproducibility.
```

---

## Phase 3: Predefined Task Catalog

### Goal

Provide useful default tasks.

### Tasks

1. Add 5–8 predefined tasks.
2. Cover docs, planning, security, insufficient context, code fixture.
3. Add task metadata.
4. Add `--task-id` loading.

### Definition of Done

```text
- User can run `--task-id simple-doc-summary-001`.
- Tasks are small and stable.
```

---

## Phase 4: Target Agent Execution

### Goal

Allow Evaluation Agent to invoke a target agent, not just compare existing files.

### Tasks

1. Implement Agent Runner Adapter.
2. Add command template config.
3. Render Target Agent Prompt.
4. Invoke Target Agent for Candidate.
5. Optionally invoke Target Agent for Baseline if baseline environment/output is configured.
6. Capture stdout/stderr/exit code.
7. Store runner metadata.

### Definition of Done

```text
- Evaluation Agent can ask Target Agent to execute a task.
- Output is saved to a deterministic path.
- CLI syntax is configurable.
```

### Important Constraint

Do not hard-code Copilot CLI syntax. Use `command_template`.

---

## Phase 5: Normal Run Deterministic Gates

### Goal

Add cheap, reliable checks.

### Tasks

1. Implement required strings.
2. Implement forbidden strings.
3. Implement required headings.
4. Implement word count limits.
5. Implement command checks.
6. Implement file touch checks where possible.
7. Save deterministic result JSON.

### Definition of Done

```text
- Normal Run can fail on hard gates.
- Gate failures are visible in report.
```

---

## Phase 6: Normal Suite Runner

### Goal

Run multiple tasks and aggregate.

### Tasks

1. Implement `normal run-suite`.
2. Load all selected tasks.
3. Execute or load baseline/candidate per task.
4. Run deterministic gates.
5. Run Pairwise Judge.
6. Aggregate results.
7. Write Normal Report.

### Definition of Done

```text
- 3–8 tasks can run as a suite.
- Aggregate result says ACCEPT / INSPECT / REJECT.
```

---

## Phase 7: Deep Run Multi-Trial

### Goal

Support repeated trials.

### Tasks

1. Add `--trials`.
2. Add trial indexing.
3. Pair baseline/candidate trials.
4. Compute median judge delta.
5. Track variance and disagreement.
6. Write Deep Report without traces yet.

### Definition of Done

```text
- Deep Run can run N trials.
- Report includes distributions, not only one score.
```

---

## Phase 8: Trace / Hook / OTel Support

### Goal

Evaluate actual agent behavior.

### Tasks

1. Add optional hook event logging.
2. Add trace import directory.
3. Add OTel JSONL parser if available.
4. Extract tool-call counts.
5. Extract token usage if available.
6. Extract latency if available.
7. Add trace gates.

### Definition of Done

```text
- Deep Report includes tool-call, token, latency, and verification-discipline metrics where available.
```

---

## Phase 9: Human Calibration

### Goal

Avoid blindly trusting LLM judges.

### Tasks

1. Select 5–10 random comparisons.
2. Generate human review sheet.
3. Human marks better/equivalent/worse.
4. Compare human vs judge.
5. Report disagreement rate.

### Definition of Done

```text
- Important Deep Runs include optional human calibration.
```

---

## 18. Recommended Minimal Build Order

Implement in this order:

```text
1. Simple compare-only
2. Custom task support
3. Judge JSON schema validation
4. Simple report
5. Predefined tasks
6. Target agent execution adapter
7. Normal deterministic gates
8. Normal suite aggregation
9. Deep multi-trial support
10. Trace/Hook/OTel support
11. Human calibration
```

Reason:

```text
Simple compare-only gives immediate value.
Everything else adds confidence, not basic usability.
```

---

## 19. Example End-to-End Workflows

## 19.1 User Has Baseline and Candidate Files

```bash
python scripts/ai_eval.py simple compare-only \
  --task-text "Summarize the Engineer Agent contract." \
  --baseline-output baseline.md \
  --candidate-output candidate.md \
  --judge-agent evaluation-judge \
  --out .ai-evals/results/simple-agent-contract
```

## 19.2 User Wants Evaluation Agent to Use Engineer Agent

```bash
python scripts/ai_eval.py simple execute-and-compare \
  --target-agent engineer \
  --judge-agent evaluation-judge \
  --task-id simple-agent-contract-001 \
  --baseline-output .ai-evals/baseline/simple-agent-contract-001.md \
  --candidate-ref current \
  --out .ai-evals/results/simple-agent-contract-after-change
```

## 19.3 User Wants Normal Evaluation After Prompt Change

```bash
python scripts/ai_eval.py normal run-suite \
  --target-agent engineer \
  --judge-agent evaluation-judge \
  --task-suite .github/evals/tasks/predefined \
  --baseline-dir .ai-evals/baseline/engineer-v1 \
  --candidate-dir .ai-evals/candidate/engineer-v2 \
  --out .ai-evals/results/normal-engineer-v2
```

## 19.4 User Wants Deep Evaluation After Agent Rewrite

```bash
python scripts/ai_eval.py deep run-suite \
  --target-agent engineer \
  --judge-agent evaluation-judge \
  --task-suite .github/evals/tasks/deep \
  --baseline-ref main \
  --candidate-ref current \
  --trials 5 \
  --judge-repeats 3 \
  --collect-traces true \
  --out .ai-evals/results/deep-engineer-v2
```

---

## 20. Acceptance Policy

## 20.1 Simple Run

```text
ACCEPT:
- decision is candidate_better or candidate_equivalent
- regression_severity is none or minor
- confidence >= 0.60

INSPECT:
- decision is inconclusive
- confidence < 0.60
- delta is near zero and rationale is mixed

REJECT:
- decision is candidate_worse
- regression_severity is major or critical
```

## 20.2 Normal Run

```text
ACCEPT:
- all hard gates pass
- no security gate fails
- no major/critical semantic regression
- median delta >= -3

INSPECT:
- soft gate warnings exist
- one task is inconclusive
- judge confidence is low

REJECT:
- hard gate failure
- security failure
- important semantic loss
- unsupported/hallucinated project claims
```

## 20.3 Deep Run

```text
ACCEPT:
- candidate_better + candidate_equivalent dominate
- no critical regression
- no security regression
- trajectory metrics are stable or better
- cost increase is acceptable

INSPECT:
- improvements are real but costly
- variance is high
- task-type-specific regression exists

REJECT:
- resolved rate drops
- adherence drops
- security worsens
- verification discipline worsens
- human calibration contradicts judge strongly
```

---

## 21. Safety and Reliability Requirements

1. **Judge Agent must not edit files.**
2. **Evaluation Agent must preserve artifacts.**
3. **Baseline and Candidate must be stored immutably per experiment.**
4. **All generated prompts must be saved.**
5. **All judge outputs must be schema-validated.**
6. **Custom tasks must be saved with hashes.**
7. **CLI commands must be logged.**
8. **Secrets must not be included in reports.**
9. **Trace content capture must be opt-in.**
10. **Any final ACCEPT/REJECT must be explainable from saved artifacts.**

---

## 22. What Copilot Should Implement First

Give Copilot this implementation order:

```text
Implement Phase 1 first:
- Add .github/evals/judge/pairwise-judge.prompt.md
- Add .github/evals/judge/criteria.semantic.json
- Add .github/evals/judge/judge-result.schema.json
- Add scripts/ai_eval.py with `simple compare-only`
- Add prompt rendering
- Add judge result validation
- Add simple Markdown report

Do not implement Normal or Deep until Simple works.
Do not hard-code Copilot CLI syntax; use command_template in eval.config.json.
```

---

## 23. Implementation Prompt for Copilot

Use this prompt in the target repository:

```markdown
Implement a generic AI Agent Harness Evaluation system based on the attached specification.

Start only with Phase 1: Simple compare-only.

Requirements:
- Create `.github/evals/` config and judge files.
- Implement `scripts/ai_eval.py simple compare-only`.
- It must accept:
  - `--task-text` or `--task-file`
  - `--baseline-output`
  - `--candidate-output`
  - `--judge-agent`
  - `--out`
- It must render a pairwise judge prompt.
- It must invoke the judge through a configurable command template from `.github/evals/config/eval.config.json`.
- It must save:
  - task context
  - baseline copy
  - candidate copy
  - judge prompt
  - raw judge output
  - parsed judge result JSON
  - report.md
- It must validate the judge JSON against `.github/evals/judge/judge-result.schema.json`.
- Do not implement Normal or Deep yet.
- Do not assume exact Copilot CLI syntax. Make the runner adapter configurable.
- Add a README with usage examples.
```

---

## 24. Known Limitations

1. **Simple Run is not deterministic.**  
   It is a fast semantic estimate, not proof.

2. **LLM Judges can be biased.**  
   Use repeat runs for important changes.

3. **Baseline can be wrong.**  
   The judge must evaluate both outputs against the task.

4. **Copilot CLI syntax may change.**  
   Keep the runner adapter configurable.

5. **Trace collection is optional and should be Deep-only initially.**

6. **Custom tasks are useful but less comparable over time.**  
   Predefined tasks are better for regression tracking.

7. **A better-looking output is not always a better harness.**  
   That is why Normal and Deep exist.

---

## 25. Source Notes

This specification aligns with the following documented capabilities and research directions:

- VS Code Agent Hooks execute shell commands at agent lifecycle points such as `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `SubagentStart`, `SubagentStop`, `PreCompact`, and `Stop`; hooks can enforce policies, run validation, and create audit trails. Source: [VS Code Agent Hooks documentation](https://code.visualstudio.com/docs/agent-customization/hooks), accessed 2026-06-17.
- VS Code Copilot Chat can export OpenTelemetry traces, metrics, and events for agent interactions, LLM calls, tool executions, and token usage; file-based OTel export is supported. Source: [VS Code OpenTelemetry monitoring documentation](https://code.visualstudio.com/docs/agents/guides/monitoring-agents), accessed 2026-06-17.
- VS Code supports customization types including instructions, prompt files, agent skills, custom agents, MCP servers, hooks, and plugins. Source: [VS Code Customize AI documentation](https://code.visualstudio.com/docs/agent-customization/overview), accessed 2026-06-17.
- GitHub Copilot repository instructions support repository-wide instructions, path-specific instructions, and agent instructions via `AGENTS.md`; multiple instruction types can apply to a request. Source: [GitHub Copilot repository custom instructions documentation](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions), accessed 2026-06-17.
- Recent research on agentic coding tools emphasizes that repository-level configuration artifacts such as context files, skills, and subagents are increasingly important and need systematic evaluation. Source: Galster et al., `Configuring Agentic AI Coding Tools: An Exploratory Study`, arXiv 2602.14690, 2026.
- Recent research on AI coding agents suggests task type strongly affects acceptance and that evaluation should be task-stratified rather than a single global score. Source: Pinna et al., `Comparing AI Coding Agents: A Task-Stratified Analysis of Pull Request Acceptance`, arXiv 2602.08915, 2026.

---

## 26. Final Recommendation

Start with this sequence:

```text
1. Simple Run compare-only
2. Simple Run with custom tasks
3. Simple Run with predefined tasks
4. Simple Run execute-and-compare through Target Agent
5. Normal Run with deterministic gates
6. Normal task suite
7. Deep Run multi-trial
8. Deep trace/hook/OTel integration
```

Do not start with the full Deep Run. That will slow adoption.

The best first milestone is:

```text
Given a task, baseline.md, and candidate.md, produce a Judge JSON and report.md that says whether Candidate is better, equivalent, worse, or inconclusive.
```

Once that works reliably, add agent execution and deterministic gates.
