# Spezifikation und Implementierungsplan: Python Context Graph für DiviCal + CLASP

**Status:** Entwurf / MVP-Spezifikation  
**Zielsystem:** DiviCal Repository + CLASP AI-Ökosystem in VS Code + GitHub Copilot  
**Primäre Sprache für das Tooling:** Python 3.11+  
**MVP-Abhängigkeiten:** Nur Python-Standardbibliothek, keine Third-Party-Packages  
**Primäres Ziel:** Weniger Kontext, weniger Tokens, bessere Datei-/Regelauswahl für Agenten

---

## 1. Executive Summary

Ziel ist ein lokales Python-Tool, das aus dem DiviCal-Repository einen kompakten, deterministischen Repository-Graph erzeugt und daraus für konkrete Copilot-/Agent-Aufgaben kleine `context-pack` Dateien ableitet.

Der Graph ersetzt nicht VS Codes semantische Indexierung. Er ergänzt sie um strukturelle Repository-Intelligenz:

- Welche Dateien importieren welche anderen Dateien?
- Welche Komponenten, Funktionen, Routen und Tests gehören zusammen?
- Welche CLASP Agents, Skills, Instructions und Prompts hängen zusammen?
- Welche Regeln gelten für welche Pfade?
- Welche Dateien sollte ein Agent zuerst lesen?

Das Tool soll nicht den ganzen Graph in den LLM-Kontext geben. Der Graph ist ein **Context Filter**, kein Context Dump.

**Zielbild:**

```text
User Task
  ↓
Python Context Graph Resolver
  ↓
.ai/tmp/context-pack.current.json
  ↓
Copilot Agent liest nur relevante Dateien/Regeln
  ↓
Agent arbeitet mit kleinem, evidenzbasiertem Kontext
```

---

## 2. Verifizierte und nicht verifizierte Annahmen

### Verifiziert aus der Anforderung

Der gewünschte Ansatz soll:

- in Python oder einer ähnlich leichtgewichtigen Sprache umgesetzt werden,
- ohne Third-Party-Packages starten,
- für TypeScript/React und Python besser passen als ein C#-Tool,
- DiviCal und das CLASP AI-Ökosystem unterstützen,
- Kontext für VS Code + GitHub Copilot minimieren,
- später optional über MCP bereitgestellt werden können,
- aber nicht zwingend sofort einen MCP-Server benötigen.

### Nicht verifiziert

Die tatsächliche aktuelle DiviCal-Repository-Struktur wurde in dieser Spezifikation nicht live analysiert. Daher sind konkrete Pfade wie `src/`, `.github/skills/`, `.github/agents/`, `.ai/tmp/` als empfohlene Zielstruktur zu verstehen, nicht als Behauptung, dass sie bereits existieren.

---

## 3. Problemstellung

GitHub Copilot und ähnliche Agenten können große Repositories durchsuchen. Trotzdem entstehen in größeren Codebasen typische Probleme:

1. Der Agent liest zu viele Dateien.
2. Der Agent liest plausible, aber irrelevante Dateien.
3. Der Agent lädt zu viele globale Instructions, Skills oder Kontextdateien.
4. Sub-Agenten bekommen zu breite oder unscharfe Aufgaben.
5. Tokenverbrauch steigt durch Explorationslogs, Dateidumps und unnötige Kontextwiederholung.
6. Die Auswahl relevanter Tests und Regeln ist inkonsistent.

Das Ziel ist ein lokaler Context Resolver, der vor der Agent-Ausführung eine kleine, strukturierte Antwort liefert:

```json
{
  "query": "implement dividend recovery confidence in prediction UI",
  "read": [
    "frontend/src/features/dividends/DividendPredictionCard.tsx",
    "frontend/src/api/dividendPredictionClient.ts",
    "frontend/src/features/dividends/DividendPredictionCard.test.tsx",
    ".github/copilot-instructions.md"
  ],
  "limits": {
    "max_files": 8,
    "policy": "read listed files first; expand once only if blocked"
  }
}
```

---

## 4. Ziele

### 4.1 Primäre Ziele

- Kontextgröße pro Agent-Aufgabe reduzieren.
- Relevante Dateien schneller und deterministischer finden.
- CLASP Agents, Skills, Instructions und Prompts explizit modellieren.
- Copilot-Agenten eine kleine Liste relevanter Dateien und Regeln geben.
- Tokenverbrauch durch Context Packs statt Repository-Dumps senken.
- Ohne Third-Party-Packages mit einem wartbaren MVP starten.

### 4.2 Sekundäre Ziele

- Später optional als lokaler MCP-Server nutzbar machen.
- Später optional mit echter TypeScript-Analyse, Embeddings oder Vector Search erweitern.
- Messbare Qualitäts- und Effizienzmetriken einführen.
- Context Packs für Sub-Agenten nutzbar machen.

---

## 5. Nicht-Ziele

Für den MVP explizit **nicht** bauen:

- vollständiger TypeScript-AST,
- vollständiger C#-/Roslyn-Graph,
- vollständiger Call Graph,
- eigene Vector Database,
- LLM-generierter Knowledge Graph als Quelle der Wahrheit,
- LangChain/LlamaIndex/NetworkX/Tree-sitter-basierte Lösung,
- MCP-Server als erste Implementierung,
- automatische Bearbeitung des Repositories ohne Review,
- vollständige Ersetzung von VS Codes semantischer Indexierung.

---

## 6. Architekturentscheidung

### 6.1 Empfohlener Ansatz

```text
Python CLI zuerst
  ↓
JSON Repo Graph
  ↓
Context Resolver
  ↓
.ai/tmp/context-pack.current.json
  ↓
Copilot Orchestrator liest Context Pack
  ↓
optional später: MCP Wrapper
```

### 6.2 Warum Python?

| Kriterium | Bewertung |
|---|---|
| Schnelles File-/Text-Scanning | Sehr gut |
| JSON, Markdown, Regex | Sehr gut |
| Python-AST | Eingebaut über `ast` |
| Lokales CLI-Tooling | Sehr gut |
| CLASP-Regeln und Markdown scannen | Sehr gut |
| Keine Third-Party-Packages nötig | Ja |
| Späterer MCP-Wrapper | Gut möglich |
| TypeScript/React-Heuristiken | Gut genug für MVP |

### 6.3 Warum kein MCP zuerst?

MCP spart keine Tokens von selbst. MCP ist nur die Schnittstelle. Tokens werden nur gespart, wenn das Tool kleine, strukturierte Antworten liefert.

Deshalb zuerst:

```text
CLI + JSON + Context Pack
```

Erst wenn das messbar nützlich ist:

```text
MCP Wrapper über denselben Core
```

---

## 7. Zielstruktur im Repository

Empfohlene Struktur:

```text
tools/
  context_graph/
    context_graph.py

.ai/
  index/
    repo-graph.json
  tmp/
    context-pack.current.json

.github/
  context/
    repo-map.md              # optional, stabile manuelle Übersicht
    clasp-map.md             # optional, stabile CLASP-Übersicht
```

Empfohlene `.gitignore` Ergänzung:

```gitignore
.ai/tmp/
.ai/index/repo-graph.json
.ai/index/context-pack.current.json
```

Alternative: `repo-graph.json` kann committed werden, wenn er klein, stabil und nützlich für Team-Workflows ist. Für große Repos ist ein lokal generierter Graph wahrscheinlich besser.

---

## 8. Kernprinzipien

### 8.1 Graph = Context Filter

Der Graph darf nicht dazu führen, dass mehr Kontext in den Agent geladen wird.

Falsch:

```text
Agent liest kompletten repo-graph.json.
```

Richtig:

```text
Agent liest context-pack.current.json mit 5–12 Dateien plus kurze Gründe.
```

### 8.2 Evidenz statt Meinung

Jede Kante im Graph soll eine überprüfbare Evidenz haben:

```json
{
  "source": "file:frontend/src/api/dividendClient.ts",
  "target": "route:POST /api/dividends/predict",
  "kind": "route_consumes",
  "evidence": "axios.post('/api/dividends/predict'",
  "line": 42,
  "confidence": 0.8
}
```

Nicht:

```json
{
  "claim": "This file is probably important."
}
```

### 8.3 Determinismus vor LLM-Extraktion

Der Graph wird aus Dateien, Pfaden, Imports, Tests, Routen, Markdown-Referenzen und Konventionen erzeugt. LLMs können später Zusammenfassungen erzeugen, aber nicht die kanonische Quelle des Graphen sein.

### 8.4 Klein anfangen

Der MVP muss nicht perfekt sein. Er muss besser sein als blindes Suchen.

---

## 9. Datenmodell

### 9.1 Node

```json
{
  "id": "file:frontend/src/features/dividends/DividendPredictionCard.tsx",
  "kind": "file",
  "name": "DividendPredictionCard.tsx",
  "path": "frontend/src/features/dividends/DividendPredictionCard.tsx",
  "line": null,
  "meta": {
    "ext": ".tsx",
    "dir": "frontend/src/features/dividends"
  }
}
```

### 9.2 Edge

```json
{
  "source": "file:frontend/src/features/dividends/DividendPredictionCard.tsx",
  "target": "file:frontend/src/api/dividendPredictionClient.ts",
  "kind": "imports",
  "evidence": "import { getDividendPrediction } from '../../api/dividendPredictionClient'",
  "line": 3,
  "confidence": 1.0
}
```

### 9.3 Unterstützte Node-Arten im MVP

```text
file
package
symbol
react_component
class
function
api_route
api_client_call
test
agent
skill
instruction
prompt
script
config
```

### 9.4 Unterstützte Edge-Arten im MVP

```text
imports
exports
defines
references
tests
route_defines
route_consumes
same_module
uses_skill
uses_instruction
uses_prompt
applies_to
```

---

## 10. Scanner-Spezifikation

### 10.1 File Scanner

Der File Scanner erzeugt:

- File Nodes,
- Directory-Metadaten,
- Extension-Metadaten,
- Ignored-Path-Filterung.

Ignorierte Verzeichnisse:

```text
.git
node_modules
dist
build
coverage
.next
.vite
.pytest_cache
__pycache__
.venv
bin
obj
```

Ignorierte Dateitypen/Suffixe:

```text
*.lock
*.map
*.min.js
```

---

### 10.2 TypeScript/React Scanner

Der MVP-Scanner ist heuristisch. Er verwendet Regex, keinen echten TypeScript-AST.

Erkennt:

- `import ... from "..."`,
- `export ... from "..."`,
- `function Name(...)`,
- `const Name = (...) => ...`,
- `class`, `interface`, `type`, `enum`,
- React-Komponenten über PascalCase in `.tsx`,
- einfache `fetch(...)` und `axios.get/post/put/patch/delete(...)` Aufrufe,
- JSX-Komponentenreferenzen.

Nicht zuverlässig erkannt:

- dynamische Imports,
- Alias-Resolver aus `tsconfig.paths`,
- Axios-Instanzen mit `baseURL`,
- Routen aus Variablen,
- vollständiger Call Graph,
- TypeScript-Typauflösung.

MVP-Ziel ist nicht perfekte TypeScript-Semantik, sondern brauchbare Kandidatenauswahl.

---

### 10.3 Python Scanner

Der Python Scanner nutzt die Standardbibliothek `ast`.

Erkennt:

- Imports,
- Klassen,
- Funktionen,
- Async-Funktionen,
- einfache FastAPI-Decorator-Routen:
  - `@router.get("/...")`
  - `@router.post("/...")`
  - `@app.get("/...")`
  - `@app.post("/...")`

Nicht zuverlässig erkannt:

- dynamisch gebaute Routen,
- Router-Prefix-Zusammensetzung,
- Dependency Injection Details,
- vollständige Call-Beziehungen.

---

### 10.4 CLASP Markdown Scanner

Der CLASP Scanner ist für dein Use Case besonders wichtig.

Erkennt Dateien nach Pfadkonvention:

```text
.github/agents/*.agent.md
.github/skills/**
.github/instructions/*.instructions.md
.github/prompts/*.prompt.md
.github/copilot-instructions.md
AGENTS.md
```

Erzeugt Nodes:

```text
agent
skill
instruction
prompt
instruction
```

Erzeugt Kanten:

```text
agent -> skill
agent -> instruction
prompt -> skill
instruction -> applies_to glob
prompt -> context file
```

MVP-Erkennung:

- Markdown-Titel über `# Heading`,
- `applyTo:` Zeilen,
- Pfadreferenzen auf `.github/skills/...`, `.github/instructions/...`, `.github/prompts/...`.

---

### 10.5 Config Scanner

Erkennt im MVP:

- `package.json` Scripts,
- `tsconfig.json` als Konfigurationsdatei,
- optional später `pyproject.toml`, `.env.example`, Dockerfiles, GitHub Actions Workflows.

Da TOML in Python erst ab neueren Versionen über `tomllib` lesbar ist und nicht immer relevant ist, wird `pyproject.toml` im MVP optional behandelt.

---

## 11. Resolver-Spezifikation

Der Resolver erzeugt aus einer Query ein kleines Context Pack.

Input:

```bash
python tools/context_graph/context_graph.py resolve \
  --root . \
  --query "implement dividend recovery confidence in prediction UI" \
  --max-files 8
```

Output:

```text
.ai/tmp/context-pack.current.json
```

### 11.1 Scoring im MVP

Ohne Embeddings wird lexikalisch und graphbasiert gerankt:

```text
score =
  path/name match
+ symbol match
+ route match
+ graph-neighborhood bonus
+ test relation bonus
+ CLASP rule relation bonus
- noisy file penalty
```

### 11.2 Graph Expansion

Nach initialer Kandidatensuche erweitert der Resolver über relevante Kanten:

```text
imports
exports
tests
route_consumes
route_defines
same_module
```

### 11.3 Output-Struktur

```json
{
  "query": "implement dividend recovery confidence in prediction UI",
  "top": [
    {
      "path": "frontend/src/features/dividends/DividendPredictionCard.tsx",
      "score": 8.4,
      "why": [
        "path/name:dividend",
        "path/name:prediction",
        "symbol:DividendPredictionCard"
      ]
    }
  ],
  "tests": [
    {
      "path": "frontend/src/features/dividends/DividendPredictionCard.test.tsx",
      "why": "test filename matches source filename"
    }
  ],
  "rules": [
    ".github/copilot-instructions.md"
  ],
  "read": [
    "frontend/src/features/dividends/DividendPredictionCard.tsx",
    "frontend/src/features/dividends/DividendPredictionCard.test.tsx",
    ".github/copilot-instructions.md"
  ],
  "limits": {
    "max_files": 8,
    "policy": "read listed files first; expand once only if blocked"
  }
}
```

---

## 12. CLI-Spezifikation

### 12.1 Build Command

```bash
python tools/context_graph/context_graph.py build --root .
```

Erzeugt:

```text
.ai/index/repo-graph.json
```

Konsolenausgabe:

```text
Wrote: .ai/index/repo-graph.json
Nodes: <number>
Edges: <number>
```

### 12.2 Resolve Command

```bash
python tools/context_graph/context_graph.py resolve \
  --root . \
  --query "<task>" \
  --max-files 8
```

Erzeugt:

```text
.ai/tmp/context-pack.current.json
```

Gibt zusätzlich das Context Pack auf stdout aus.

---

## 13. Copilot-Orchestrator-Regel

Diese Regel sollte in den Orchestrator-Agent oder die zentrale CLASP Instruction aufgenommen werden.

```md
## Context minimization policy

Before broad repository exploration:

1. Prefer the generated context pack:
   `.ai/tmp/context-pack.current.json`

2. If the context pack is missing or stale, ask the user to run:

   `python tools/context_graph/context_graph.py resolve --root . --query "<task>" --max-files 8`

3. Read only files listed under `read` first.

4. Do not inspect the whole repository unless:
   - the context pack is clearly wrong,
   - the task is blocked,
   - or the user explicitly requests broader exploration.

5. Expand context once only:
   - use exact search for one missing symbol, or
   - regenerate the context pack with a more precise query.

6. Return compact structured output:
   - changed files,
   - tests run,
   - unresolved risks,
   - no exploration log unless requested.
```

---

## 14. Sub-Agent Context Contract

Wenn ein Orchestrator Sub-Agenten verwendet, sollte er nicht die ganze Aufgabe und nicht den ganzen Graph weitergeben, sondern ein kleines Slice.

### 14.1 Input an Sub-Agent

```yaml
slice: frontend-prediction-ui
objective: Implement dividend recovery confidence display in prediction UI.
allowed_files:
  - frontend/src/features/dividends/DividendPredictionCard.tsx
  - frontend/src/api/dividendPredictionClient.ts
  - frontend/src/features/dividends/DividendPredictionCard.test.tsx
rules:
  - .github/copilot-instructions.md
constraints:
  - Do not inspect unrelated directories.
  - Do not change backend contract unless explicitly required.
  - Return compact structured result.
output_schema: implementation_result_v1
```

### 14.2 Output vom Sub-Agent

```yaml
slice: frontend-prediction-ui
status: done|blocked|risky
changed:
  - path: frontend/src/features/dividends/DividendPredictionCard.tsx
    reason: Added confidence display.
tests:
  run:
    - npm test -- DividendPredictionCard
  result: pass|fail|not-run
issues:
  - none
next:
  - none
```

---

## 15. Token-Effizienz-Regeln

### 15.1 Input-Kontext reduzieren

- Nur Context Pack lesen, nicht Graph dumpen.
- Maximal 5–12 Dateien initial lesen.
- Tests gezielt über Graph vorschlagen.
- CLASP-Regeln gezielt auswählen.
- Bei Blockade einmal gezielt expandieren.

### 15.2 Output reduzieren

Output-Kompression bedeutet im MVP nicht magische Token-Kompression. Sie entsteht durch:

1. klare Output-Schemas,
2. keine Explorationslogs,
3. kurze Evidenzfelder,
4. Dateiliste statt Prosa,
5. Statuswerte statt Fließtext,
6. harte Obergrenzen für Listen.

Beispiel:

```yaml
status: done
changed:
  - path: src/foo.ts
    reason: added validation
risk: none
```

statt:

```text
I inspected the repository and then I looked through several files and noticed that...
```

### 15.3 Harte Token-Limits allein reichen nicht

Eine Instruktion wie:

```text
Do not output more than 5000 tokens.
```

reduziert zwar Maximaloutput, verbessert aber nicht automatisch die Informationsdichte. Effektiver sind strukturierte, kleine Schemas und klare Stop Conditions.

---

## 16. Compression-Mechanismen im Kontext dieses Systems

### 16.1 Empfohlene Mechanismen

| Mechanismus | Empfehlung | Grund |
|---|---:|---|
| Context Pack | Sehr hoch | Direkter Token-Hebel |
| Strukturierte YAML/JSON Outputs | Sehr hoch | Reduziert Prosa und Log-Ausgaben |
| CLASP-Regel-Routing | Sehr hoch | Verhindert globales Instruction-Bloating |
| Diff-only Context | Hoch | Gut bei bestehenden Änderungen |
| Repository Map | Hoch | Gute Orientierung ohne Dateidumps |
| AST-lite Graph | Hoch | Gutes Kosten/Nutzen-Verhältnis |
| Embeddings | Später | Nützlich, aber zusätzliche Komplexität |
| Full Knowledge Graph | Später/selektiv | Nur bei messbarem Bedarf |
| LLM-Kompression | Vorsichtig | Risiko von Informationsverlust |

### 16.2 Caveman-artige Kompression

Ohne konkrete Verifikation der Caveman-Implementierung in dieser Spezifikation gilt allgemein:

Output-Kompression kann über mehrere Wege passieren:

1. **Instruktionsbasierte Begrenzung**  
   Beispiel: „Antworte maximal 300 Zeilen.“  
   Einfach, aber grob.

2. **Strukturelle Kodierung**  
   Beispiel: YAML/JSON mit fixen Feldern.  
   Besser, weil weniger natürliche Sprache entsteht.

3. **Abkürzungs-/Symbolschema**  
   Beispiel: `S=done`, `F[]=changed files`, `T=tests`.  
   Sehr kompakt, aber schlechter lesbar.

4. **Post-Processing**  
   Agent erzeugt normal, ein weiteres Tool komprimiert.  
   Kann Tokens im gespeicherten Ergebnis sparen, aber nicht unbedingt beim initialen Output.

5. **Context Summarization**  
   Lange Zwischenergebnisse werden zusammengefasst.  
   Nützlich, aber kann Details verlieren.

Für DiviCal + CLASP ist der beste Start nicht extreme Symbolkompression, sondern:

```text
Context Packs + strukturierte Agent-I/O + harte Scoping-Regeln
```

---

## 17. MVP-Implementierungsplan

## Phase 0: Vorbereitung

### Aufgaben

- Zielpfade anlegen:
  - `tools/context_graph/`
  - `.ai/index/`
  - `.ai/tmp/`
- `.gitignore` ergänzen.
- Python-Version festlegen: 3.11+.

### Ergebnis

```text
tools/context_graph/context_graph.py existiert
.ai/tmp/ ist ignoriert
.ai/index/ ist vorbereitet
```

---

## Phase 1: Graph Builder MVP

### Aufgaben

- `Node`, `Edge`, `RepoGraph` Dataclasses erstellen.
- File Scanner bauen.
- Ignore-Regeln implementieren.
- JSON-Serializer implementieren.
- CLI Command `build` implementieren.

### Akzeptanzkriterien

- `python tools/context_graph/context_graph.py build --root .` läuft ohne Third-Party-Packages.
- `.ai/index/repo-graph.json` wird erzeugt.
- Nodes und Edges werden auf stdout gezählt.
- Ignorierte Ordner wie `node_modules` und `.git` werden nicht indexiert.

---

## Phase 2: TypeScript/React Scanner

### Aufgaben

- Regex für Imports.
- Regex für Exports.
- Regex für Funktionen, Const-Arrow-Funktionen, Klassen, Interfaces, Types.
- React-Komponenten-Heuristik für `.tsx` + PascalCase.
- API Call-Erkennung für einfache `fetch` und `axios` Calls.
- Relative Import-Auflösung implementieren.

### Akzeptanzkriterien

- TS/TSX-Dateien erzeugen `defines` Edges.
- Relative Imports werden, soweit einfach möglich, auf File Nodes aufgelöst.
- Einfache API Calls erzeugen `route_consumes` Edges.

---

## Phase 3: Python Scanner

### Aufgaben

- Python `ast` Parser verwenden.
- Imports extrahieren.
- Klassen und Funktionen extrahieren.
- FastAPI-Decorator-Routen extrahieren.

### Akzeptanzkriterien

- Python-Dateien erzeugen Symbolnodes.
- Einfache FastAPI-Routen erzeugen `route_defines` Edges.
- Syntaxfehler in einzelnen Dateien brechen den Build nicht ab.

---

## Phase 4: Test- und Module-Kanten

### Aufgaben

- Test-Dateien über Namenskonventionen erkennen:
  - `.test.tsx`
  - `.spec.tsx`
  - `test_*.py`
  - `*_test.py`
  - `tests/`
- Testdateien mit Source-Dateien über Dateinamen verbinden.
- Same-module Kanten für kleine Verzeichnisse erzeugen.

### Akzeptanzkriterien

- Tests werden im Context Pack vorgeschlagen.
- Verzeichnisse mit zu vielen Dateien erzeugen keine zu dichten Same-module Kanten.

---

## Phase 5: CLASP Scanner

### Aufgaben

- CLASP-Dateien per Pfadkonvention erkennen.
- Agent-, Skill-, Instruction- und Prompt-Nodes erzeugen.
- `applyTo:` erkennen.
- Pfadreferenzen auf Skills, Instructions und Prompts erkennen.
- Glob-Matching später vorbereiten.

### Akzeptanzkriterien

- `.github/agents/*.agent.md` erzeugt Agent Nodes.
- `.github/skills/**` erzeugt Skill Nodes.
- `.github/instructions/*.instructions.md` erzeugt Instruction Nodes.
- `applyTo:` wird als `applies_to` Edge gespeichert.

---

## Phase 6: Context Resolver MVP

### Aufgaben

- CLI Command `resolve` implementieren.
- Query tokenisieren.
- Dateien lexikalisch nach Pfad, Name und Symbolen scoren.
- Graph-neighbor Expansion hinzufügen.
- Tests und Regeln ergänzen.
- `context-pack.current.json` erzeugen.

### Akzeptanzkriterien

- `resolve` erzeugt `.ai/tmp/context-pack.current.json`.
- Das Context Pack enthält:
  - `query`,
  - `top`,
  - `tests`,
  - `rules`,
  - `read`,
  - `limits`.
- Die `read` Liste bleibt klein.

---

## Phase 7: Copilot/CLASP Integration

### Aufgaben

- Orchestrator-Agent-Regel hinzufügen.
- Agent soll zuerst `context-pack.current.json` lesen.
- Agent soll nicht breit durchs Repo suchen, bevor das Context Pack geprüft wurde.
- Sub-Agent Output-Schema definieren.

### Akzeptanzkriterien

- Agent liest initial nur die Dateien aus `read`.
- Agent erweitert Kontext nur bei Blockade.
- Output ist strukturiert und kurz.

---

## Phase 8: Messung

### Aufgaben

Eine kleine Benchmark-Suite mit echten DiviCal-/CLASP-Aufgaben erstellen:

```text
5 Frontend Tasks
5 Backend/API Tasks
5 Test Tasks
5 CLASP/Agent Tasks
```

Für jede Aufgabe messen:

| Metrik | Beschreibung |
|---|---|
| gelesene Dateien | Anzahl der durch Agent geöffnete Dateien |
| irrelevante Dateien | manuell bewertete irrelevante Dateien |
| Input Tokens | soweit verfügbar |
| Output Tokens | soweit verfügbar |
| Tool Calls | Anzahl Such-/Read-/Edit-Aufrufe |
| Task Success | bestanden/nicht bestanden |
| Testauswahl korrekt | ja/nein |
| Review-Fixes nötig | Anzahl |

### Akzeptanzkriterien

- Context Pack reduziert gelesene Dateien im Vergleich zu blindem Copilot-Suchen.
- Task Success darf nicht schlechter werden.
- Falsch-positive Dateien sinken.
- CLASP-Regeln werden gezielter ausgewählt.

---

## Phase 9: Optionaler MCP Wrapper

Erst nach erfolgreichem CLI-MVP.

### MCP Tools

```text
resolve_context
impact
tests_for
clasp_rules_for
explain_path
```

### Prinzipien

- MCP gibt keine vollen Dateien zurück.
- MCP gibt kleine strukturierte Context Packs zurück.
- Core bleibt CLI/JSON-fähig.
- MCP ist nur Adapter, nicht Kernlogik.

---

## 18. Erweiterungen nach dem MVP

### 18.1 Besseres Glob Matching

Python Standardbibliothek:

```python
from fnmatch import fnmatch
```

Nutzen:

- `applyTo` Regeln korrekt auf Pfade anwenden.
- CLASP Instructions gezielter auswählen.

### 18.2 Repo Map Generator

Zusätzlich zu JSON:

```text
.github/context/repo-map.md
```

Inhalt:

- Module,
- wichtige Entry Points,
- Frontend/Backend-Grenzen,
- Testkonventionen,
- CLASP-Struktur.

### 18.3 Diff-only Context

Für geänderte Dateien:

```bash
git diff --name-only
```

Resolver kann geänderte Dateien priorisieren.

### 18.4 TypeScript-Alias-Auflösung

Später `tsconfig.json` `paths` lesen und einfache Aliasauflösung implementieren.

### 18.5 Optionaler Node-Sidecar

Falls echte TypeScript-AST-Daten nötig werden:

```text
scripts/context_graph_ts.mjs
```

Das kann im TypeScript-Stack leben. Für den MVP aber nicht nötig.

### 18.6 Embeddings / Semantic Retrieval

Später möglich, aber nicht zuerst:

- lokale Embeddings,
- SQLite + Vektorähnlichkeit,
- externe Vector DB.

Vorher messen, ob der graphbasierte MVP nicht bereits ausreichend ist.

---

## 19. Risiken und Gegenmaßnahmen

| Risiko | Auswirkung | Gegenmaßnahme |
|---|---|---|
| Regex-Scanner erkennt nicht alles | fehlende Kandidaten | graph expansion + exact search fallback |
| Zu viele Same-module Kanten | noisy Context Packs | Verzeichnisse mit >25 Dateien überspringen |
| CLASP-Regeln werden zu breit geladen | Token-Bloat | applyTo-Glob-Matching einbauen |
| Graph wird groß | Agent darf ihn nicht lesen | nur Context Pack lesen |
| Stale Graph | falsche Vorschläge | bei Resolve automatisch rebuilden oder Hash prüfen |
| Dynamische Routen fehlen | API-Kanten unvollständig | später Routen-Summary ergänzen |
| Agent ignoriert Context Pack | kein Nutzen | Orchestrator-Instructions verschärfen |
| Token sinken, Qualität sinkt auch | falsche Optimierung | Benchmark mit Task Success messen |

---

## 20. Definition of Done für den MVP

Der MVP gilt als fertig, wenn:

1. `build` einen Graph erzeugt.
2. `resolve` ein kleines Context Pack erzeugt.
3. TypeScript/React-Dateien grob erkannt werden.
4. Python-Dateien über `ast` erkannt werden.
5. CLASP Agents/Skills/Instructions/Prompts erkannt werden.
6. Tests über einfache Namenskonventionen vorgeschlagen werden.
7. Copilot-Agenten angewiesen sind, zuerst das Context Pack zu verwenden.
8. Mindestens 10 reale Aufgaben mit und ohne Context Pack verglichen wurden.
9. Das Context Pack im Durchschnitt weniger initiale Dateien erzeugt als manuelles/breites Repo-Suchen.
10. Die Lösungsqualität nicht schlechter wird.

---

## 21. Erste konkrete Umsetzungsschritte

### Schritt 1

Datei anlegen:

```text
tools/context_graph/context_graph.py
```

### Schritt 2

Minimalen Graph Builder implementieren:

```bash
python tools/context_graph/context_graph.py build --root .
```

### Schritt 3

Context Resolver implementieren:

```bash
python tools/context_graph/context_graph.py resolve \
  --root . \
  --query "implement dividend recovery confidence in prediction UI" \
  --max-files 8
```

### Schritt 4

Agent-Regel einfügen:

```md
Before broad repository exploration, read `.ai/tmp/context-pack.current.json` and inspect only files listed in `read` first.
```

### Schritt 5

Mit 5 echten Tasks testen:

```text
1 Frontend UI Änderung
1 Backend/API Änderung
1 Test-Erweiterung
1 CLASP Skill/Instruction Änderung
1 Bugfix mit unbekannter Ursache
```

### Schritt 6

Metriken dokumentieren:

```text
Task
Context Pack read files
Copilot actual read files
irrelevant files
success
tests selected
notes
```

---

## 22. Empfohlene Priorität

| Priorität | Aufgabe |
|---:|---|
| P0 | Python CLI + File Scanner |
| P0 | JSON Graph Output |
| P0 | Resolve Command + Context Pack |
| P1 | TypeScript/React Scanner |
| P1 | Python AST Scanner |
| P1 | CLASP Markdown Scanner |
| P1 | Test Edge Detection |
| P2 | applyTo Glob Matching |
| P2 | Diff-aware Ranking |
| P2 | Repo Map Markdown Generator |
| P3 | MCP Wrapper |
| P3 | Embeddings / Semantic Hybrid Search |
| P4 | echter TypeScript-AST oder Node-Sidecar |

---

## 23. Kurzfazit

Die empfohlene Lösung ist kein großer Knowledge-Graph und kein MCP-first System.

Die empfohlene Lösung ist:

```text
kleines Python CLI
+ deterministischer Repo Graph
+ CLASP Governance Graph
+ kompakte Context Packs
+ strikte Agent-Regeln
+ spätere MCP-Hülle nur bei nachgewiesenem Nutzen
```

Der Graph muss nicht perfekt sein. Er muss nur gut genug sein, damit Copilot und Sub-Agenten schneller zu den richtigen Dateien, Tests und Regeln kommen.

Der wichtigste Leitsatz:

```text
Graph = Context Filter, nicht Context Dump.
```
