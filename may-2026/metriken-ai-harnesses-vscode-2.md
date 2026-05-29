# Aktuelle Metriken für AI Harnesses in VS Code und GitHub Copilot

## Kurzfazit

**Fakt:** Für dein Ziel ist die richtige Frage **nicht** „welches Modell ist besser?“, sondern „liefert mein *Harness* nach einer Änderung an Agent, Prompt, Instructions oder Skills unter denselben Bedingungen bessere Ergebnisse als vorher?“. Die aktuell belastbarsten 2026-Quellen sagen praktisch alle dasselbe: **Outcome-only-Metriken** wie ein einzelner Pass-Score oder ein einmaliger Demo-Run reichen dafür nicht aus. Du brauchst mindestens vier Ebenen gleichzeitig: **Aufgabenerfolg**, **Trajektorienqualität**, **Effizienz** und **menschliche Nacharbeit**. Das ist heute der Stand der Technik bei VS Code selbst, bei Anthropic-Agent-Evals und in mehreren 2026er Forschungsarbeiten. Quellenstand hier: 09.01.2026 bis 15.05.2026, Alter am 28.05.2026: ca. 13 Tage bis 4,5 Monate. citeturn3view0turn18view3turn22view0turn32view0turn33view0

**Fakt:** Der offizielle VS-Code-Engineering-Post vom **15.05.2026** (Alter: **13 Tage**) ist für dich besonders wichtig, weil er explizit vom **coding harness** spricht und erklärt, dass VS Code intern Änderungen am Harness nicht nur über öffentliche Benchmarks, sondern über **produktnahe Offline-Evals**, **A/B-Tests**, **Nutzungssignale** und **wöchentliche Reports** bewertet. VS Code misst in seinem VSC-Bench ausdrücklich **solution correctness, agent effort, token efficiency und latency** und startet für PRs mit potentiell verhaltensändernden Harness-Änderungen einen automatisierten Eval-Assessment-Flow, bevor gemergt wird. citeturn3view0turn18view0turn18view2

**Fakt:** Für dein konkretes Vorhaben sind die **besten Kernmetriken** daher:  
Erstens **Task Resolution Rate** mit deterministischen Verifiern. Zweitens **Instruction/Constraint Adherence**. Drittens **Trajectory Quality** mit Fokus auf Tool-Wahl, Recovery, Stop-Verhalten und unnötige Schleifen. Viertens **Human Burden** wie Review-Runden, Korrekturen, Ablehnungen und Survival-to-Commit. Fünftens **Effizienz** über Tokens, Latenz, Tool-Calls und Kosten. Sechstens **Safety/Policy-Compliance**, also z. B. verbotene Kommandos, fehlende Bestätigung bei sensiblen Aktionen, Policy-Verstöße. Genau diese Breite wird in 2026er Quellen immer wieder als notwendig beschrieben. Quellenstand: 09.01.2026 bis 26.05.2026, Alter: ca. 2 Tage bis 4,5 Monate. citeturn22view0turn21view0turn21view1turn27view0turn23view2

**Empfehlung:** Wenn du nur **eine** Scorecard bauen willst, nimm **keinen einzelnen Gesamtwert als Hauptsignal**. Nimm stattdessen ein **Scoreboard mit harten Gates**:  
1) deterministischer Aufgabenerfolg darf nicht sinken,  
2) Adherence darf nicht sinken,  
3) gefährliche Aktionen müssen null bleiben,  
4) Kosten/Latenz dürfen nur in definierten Grenzen steigen.  
Erst **danach** darfst du einen Komfort-Index für Trendbeobachtung bauen. Das ist robuster als ein einziger „AI score“. Diese Empfehlung ist eine Synthese aus den Quellen, nicht selbst ein standardisierter Benchmark. citeturn18view0turn22view0turn33view0

**Wichtige Einschränkung:** Den Inhalt deines ausgewählten GitHub-Repos **4sthea/Divical** konnte ich in dieser Sitzung **nicht verifizieren**. Deshalb nenne ich **keine repo-spezifischen Dateien, Klassen oder Build-Kommandos** aus Divical. Der Integrationsplan unten ist daher absichtlich **repo-neutral**, aber direkt auf **VS Code + GitHub Copilot + AI-Harness-Evaluation** zugeschnitten.

## Was du wirklich messen solltest

### Aufgabenerfolg als Primärsignal

**Fakt:** Der stabilste Primärwert bleibt **Aufgabenerfolg gegen eine reproduzierbare Aufgabe**. Anthropic beschreibt in seinem Engineering-Artikel vom **09.01.2026** (Alter: **ca. 4,5 Monate**) Agent-Evals genau so: Ein Task bekommt klare Inputs, eine Trial ist ein einzelner Versuch, ein Grader bewertet Output oder Outcome, und wegen Nichtdeterminismus werden **mehrere Trials pro Task** empfohlen. Für Coding Agents sind laut Anthropic **deterministische Verifier** wie Unit-Tests, state checks, static analysis und outcome verification der natürliche Kern. citeturn22view0

Für dich heißt das praktisch: Jede Änderung an Agent, Prompt, Instructions oder Skill muss gegen eine **feste Aufgaben-Suite** laufen. Gute Aufgaben sind nicht „schreibe mal etwas“, sondern Dinge wie:  
„behebe diesen Bug, sodass genau diese Tests grün werden“,  
„implementiere diese kleine Feature-Änderung mit diesen Akzeptanzkriterien“,  
„erzeuge diese Refactoring-Änderung ohne Typ- oder Lint-Fehler“,  
„migriere diese Konfiguration und verifiziere Ergebnis X“.  
Wenn möglich, sollten diese Aufgaben **deterministisch** verifizierbar sein, denn das billiger, reproduzierbarer und debugbarer ist als reine Judge-Evals. citeturn22view0turn18view2

**Empfehlung:** Nimm als Primärmetrik **Task Resolution Rate**:

```text
Task Resolution Rate = bestandene Trials / alle validen Trials
```

Berichte sie **pro Task-Familie** und **gesamt**. Also z. B. Bugfix, Refactoring, Testgen, Diagnose, Build/CI, Repo-Navigation. Ein globaler Wert ohne Segmentierung versteckt oft, dass ein Prompt einen Bereich verbessert und einen anderen verschlechtert. Genau das zeigt auch die 2026er Arbeit „When Better Prompts Hurt“: generisch „bessere“ Regeln verbesserten teils Instruction-Following, verschlechterten aber andere task-spezifische Ziele. Veröffentlicht am **29.01.2026** (Alter: **ca. 4 Monate**). citeturn21view4

### Instruction- und Constraint-Adherence

**Fakt:** Wenn dein eigentliches Veränderungsobjekt **Instructions, Skills, AGENTS.md oder Prompts** sind, dann musst du **Adherence** separat messen. Sonst verwechselst du „Task zufällig bestanden“ mit „Harness hat deine Regeln tatsächlich eingehalten“. AgentAtlas vom **27.05.2026** bzw. „1 day ago“ in der Fundstelle (Alter: **sehr frisch**, praktisch **1–2 Tage**) argumentiert deshalb, dass Outcome Success von **Control-Decision Quality** und **Trajectory Quality** getrennt werden muss. Das Paper schlägt explizit die sechs Kontrollzustände **Act / Ask / Refuse / Stop / Confirm / Recover** vor. citeturn32view0turn32view2

Für deinen Fall sind daraus sehr gute Harness-Metriken ableitbar:

- **Ask/Confirm-Compliance:** Hat der Agent bei irreversiblen oder sensiblen Schritten nachgefragt?
- **Stop-Correctness:** Hat er beendet, als das Ziel tatsächlich erreicht war, statt weiter zu editieren?
- **Recover-Rate:** Hat er nach Tool- oder Testfehlern sinnvoll umgesteuert?
- **Refuse-Policy-Rate:** Hat er verbotene oder riskante Schritte korrekt verweigert?
- **Constraint-Adherence:** Hat er Anweisungen wie TDD, keine neuen Dependencies, keine Prod-Konfig ändern, nur in Pfad X arbeiten, befolgt?

Diese Metriken sind **harness-nah**, nicht modellnah. Sie messen nicht abstrakte Modellintelligenz, sondern ob dein Setup das gewünschte Arbeitsverhalten reproduzierbar erzwingt. citeturn32view0turn33view3

**Empfehlung:** Baue für jede Eval-Aufgabe zusätzlich **2–5 explizite Adherence-Checks** ein. Beispiel:  
„nur Dateien unter `/src/features/calendar/**` ändern“,  
„vor Finalantwort `dotnet test` oder `npm test` ausführen“,  
„keine Dependency hinzufügen“,  
„bei fehlendem Kontext Rückfrage stellen“.  
Diese Checks können deterministisch sein oder durch einen kleinen Rubric-Judge ergänzt werden. Die Kombination aus **deterministischem Regelcheck + LLM-Judge + stichprobenartigem Human-Audit** wird 2026 von Anthropic und Phoenix praktisch genau so empfohlen. citeturn22view0turn23view2

### Trajektorienqualität statt nur Endergebnis

**Fakt:** Die 2026er Forschung ist hier extrem eindeutig: **Pass/Fail allein reicht nicht**. AgentAtlas, „Log analysis is necessary for credible evaluation of AI agents“ und mehrere weitere Arbeiten sagen, dass reine Outcome-Messung Abkürzungen, falsche Zwischenschritte, Sicherheitsverstöße und Scaffold-/Harness-Probleme maskiert. Das Paper zur Log-Analyse vom **08.05.2026** (Alter: **20 Tage**) sagt wörtlich, dass Outcome-only-Evals die Glaubwürdigkeit von Agent-Bewertung bedrohen, weil Scores durch Artefakte verzerrt sein können, Real-World-Utility schlecht vorhersagen und gefährliche Zwischenaktionen verbergen. citeturn33view0turn33view3

Das ist genau dein Anwendungsfall. Wenn du nur misst, ob am Ende Tests grün sind, entgeht dir zum Beispiel:

- dass dein neuer Prompt 3× mehr nutzlose Tool-Calls erzeugt,
- dass neue Instructions mehr Recovery-Schleifen auslösen,
- dass der Agent häufiger falsche Dateien bearbeitet,
- dass er mehr Tokens verbraucht,
- dass er häufiger „fertig“ sagt, obwohl Testfehler noch offen sind.

**Empfehlung:** Miss für jede Session zusätzlich mindestens diese Trajektorienmetriken:

- **Bad Tool Call Rate**  
  Anteil fehlerhafter, redundanter oder schema-inkompatibler Tool-Aufrufe.
- **Recovery Rate**  
  Anteil der Sessions mit Tool-/Testfehler, die danach noch erfolgreich wurden.
- **Loop Rate**  
  Anteil Sessions mit erkennbarer Schleife oder unnötigen Wiederholungen.
- **Tool Efficiency**  
  Verhältnis aus nützlichen Tool-Calls zu allen Tool-Calls.
- **Plan-to-Execution Drift**  
  Wie stark weicht das tatsächliche Verhalten vom geplanten Vorgehen ab?
- **Stop Correctness**  
  Hat der Agent sinnvoll aufgehört oder zu früh/zu spät gestoppt?

Diese Metriken sind im Alltag häufig wertvoller als ein nackter Pass-Score, weil sie dir sagen, **warum** eine Änderung besser oder schlechter wurde. citeturn32view1turn33view0turn21view3

### Effizienz, Kosten und Latenz

**Fakt:** VS Code misst intern laut Engineering-Post vom **15.05.2026** (Alter: **13 Tage**) explizit **agent effort, token efficiency und latency**. Anthropic nennt **latency, token usage, cost per task und error rates** als Standard-Nebensignale, sobald ein Eval-Suite existiert. Phoenix und VS Code OTel unterstützen genau diese Art von Erfassung in Produktiv- oder Experimentumgebungen. citeturn18view2turn22view0turn23view2turn36view0

Diese Metriken sind für dich nicht „nice to have“, sondern nötig, weil ein Harness sehr leicht scheinbar bessere Qualität erkaufen kann, indem es einfach **mehr Kontext**, **mehr Schleifen** und **mehr Tokens** verbrennt. Gerade bei Agenten mit mehreren Tool-Runden ist das ein häufiger versteckter Zielkonflikt. citeturn18view2turn21view6

**Empfehlung:** Miss mindestens:

- **Median Total Tokens pro Task**
- **Median Time-to-Last-Useful-Action**
- **Time-to-First-Useful-Action**
- **Tool Calls pro erfolgreicher Session**
- **Kosten pro erfolgreich gelöstem Task**
- **Cache Hit / Prompt Cache Efficiency**, wenn verfügbar

VS Code bietet dafür inzwischen eine sehr gute Grundlage: Die **Chat Debug View** zeigt Roh-Prompts, Kontext und Tool-Payloads; die **Agent Debug Logs** zeigen Ereignisse, Tool-Aufrufe und mehr; der **Cache Explorer** zeigt Cache-Hit-Prozente und die Abweichungspunkte innerhalb des Prompt-Präfixes; und Copilot Chat kann **OTel-Traces, Metrics und Events** inklusive Token-Nutzung exportieren. Quellenstand: 15.05.2026, 09.02.2026, 28.05.2026-Dokumentation; Alter: **13 Tage bis ca. 3,5 Monate**. citeturn19view3turn36view1turn36view0

### Menschliche Nacharbeit und echte Nutzbarkeit

**Fakt:** Die stärksten 2026er „wild data“-Signale kommen nicht aus Modellbenchmarks, sondern aus **realen Agent-Trails**. SWE-chat vom **22.04.2026** (Alter: **ca. 5 Wochen**) berichtet über 6.000 reale Coding-Agent-Sessions aus der Praxis; dort überleben nur **44 %** des agent-generierten Codes bis in User-Commits, und in **44 %** aller Turns greifen Nutzer korrigierend oder abbrechend ein. Parallel zeigt „Human-AI Synergy in Agentic Code Review“ vom **16.03.2026** (Alter: **ca. 2,5 Monate**), dass AI-Agent-Kommentare deutlich geringere Adoptierungsraten als menschliche Reviewer haben und angenommene AI-Vorschläge die Codegröße und Komplexität stärker erhöhen. citeturn31view4turn31view3

Das sind für dich extrem brauchbare **Harness-Qualitätsmetriken**, weil sie messen, wie viel **realer Reibungsverlust** nach dem eigentlichen Modell-Output übrig bleibt.

**Empfehlung:** Ergänze dein Scoreboard um:

- **Survival-to-Commit Rate**  
  Wie viel von AI-generierten Änderungen ist nach Review/Iteration tatsächlich im Commit?
- **Correction Rate**  
  Wie oft muss der Mensch AI-Änderungen umschreiben?
- **Review Rejection Rate**
- **Interruption Rate**  
  Wie oft wird eine Agent-Session abgebrochen oder umgelenkt?
- **Review Round Count**  
  Wie viele Rückfragen / Review-Schleifen braucht es?
- **Seven-day Survival**  
  Optional: Wie viel der AI-Änderung lebt nach 7 oder 14 Tagen noch?

Wenn du diese eine Ebene nicht misst, kannst du ein Harness leicht „optimieren“, das gut benchmarkt, aber im Teamworkflow nervt, ausufert oder technische Schuld produziert. Genau vor dieser Lücke warnen mehrere 2026er Arbeiten. citeturn31view3turn31view4turn31view1turn31view0

### Langfristige Wartbarkeit und Erosion

**Fakt:** SlopCodeBench vom **25.03.2026** (Alter: **ca. 2 Monate**) ist für diesen Punkt wichtig. Die Arbeit zeigt, dass bei längeren iterativen Coding-Aufgaben **Qualität schleichend degradiert**, mit wachsender Verbosität und Erosion, und dass reine Pass-Rate-Metriken diese Langfristprobleme systematisch unterschätzen. citeturn31view0

**Empfehlung:** Wenn dein Agent häufig auf derselben Codebasis iteriert, miss zusätzlich:

- **Diff Size Growth pro Iteration**
- **Cyclomatic Complexity Delta**
- **Duplication Delta**
- **Verbosity Delta**
- **Unnecessary File Touches**
- **Failed-to-Green Retry Count**

Gerade bei Skills und „helpful/debug/explain more“-Prompts kippt Qualität oft nicht sofort, sondern durch **zu viel Aktion**, **zu viel Kontextexpansion** und **zu viel Text**. Das ist ein klassisches Harness-Problem, kein reines Modellproblem. citeturn21view4turn31view0

## Welche Metriken du nicht überschätzen solltest

**Fakt:** Die offiziellen GitHub-Copilot-Usage-Metriken von 2026 sind nützlich, aber für dein eigentliches Ziel **nur sekundär**. GitHub misst u. a. **Adoption, Engagement, Acceptance Rate, Lines of Code und PR-Lifecycle-Metriken**; die REST-Reports liefern auch Aufschlüsselungen über **chat**, **agent modes**, Modelle und IDEs. Diese Daten sind gut für Rollout- und Nutzungsbeobachtung, aber sie sagen nicht zuverlässig, ob ein neuer Skill oder Instruction-Satz **objektiv bessere Agent-Outputs** erzeugt. Quellenstand: GitHub Docs, 2026; Alter: **0–5 Monate**, je nach Seite. citeturn24view0turn24view1turn24view2turn24view3

**Empfehlung:** Nutze diese GitHub-Metriken nur als **Begleitindikatoren**:

- steigende Agent-Adoption kann bedeuten, dass der Harness nützlicher wurde,
- fallende Acceptance Rate kann auf schlechtere Relevanz hindeuten,
- mehr Requests pro Agent-Mode können für Nützlichkeit sprechen,

aber **niemals** als alleinige Qualitätsmetrik für Harness-Änderungen. Eine höhere Nutzung kann auch bedeuten, dass der Agent häufiger festhängt und Nutzer öfter nachsteuern müssen. citeturn24view0turn24view1turn31view4

**Fakt:** Ein weiterer häufiger Fehler ist **Single-Shot-Vergleich**. Reddit-Diskussionen aus 2026 zeigen ziemlich klaren Praktiker-Konsens: Ein einzelner Run oder ein Screenshotvergleich ist bei Agenten wertlos. In einer Diskussion vom **22.05.2026** bzw. wenige Tage alt (Alter: **< 1 Woche**) sagen mehrere Nutzer sinngemäß, man müsse **mindestens 10 Durchläufe** machen, sonst urteile man nur über Varianz. Dieselbe Diskussion weist außerdem auf Tokens und Tool-Effizienz als wichtige Vergleichsdimension hin. Das ist anekdotisch, aber mit der Literatur konsistent. citeturn12view1

**Fakt:** Außerdem sind **PR-Review-Surfaces auf GitHub Web** derzeit kein idealer Ort, um Instruction-Änderungen zu evaluieren. Mehrere GitHub-Community-Threads aus **Oktober 2025 bis Januar 2026** berichten, dass `.github/copilot-instructions.md` in PR-Reviews nur **best effort** greift, teils inkonsistent ist und sich zwischen Runs unterschiedlich auswirkt. In derselben Zeit wird VS Code Chat von Community-Antworten als konsistenter in der Anwendung von Instructions beschrieben. Das bleibt Community-Material, also nicht dieselbe Evidenzklasse wie Produktdoku; als Praxissignal ist es aber stark genug, um die Surface-Wahl zu beeinflussen. citeturn29view0turn29view1turn29view2turn29view3

## So implementierst du das in VS Code und GitHub Copilot

### Instrumentierung ohne eigene Plattform

**Fakt:** VS Code bietet dir 2026 bereits fast alles, was du für einen guten lokalen Harness-Messaufbau brauchst. Die wichtigsten Bausteine sind:

- **Chat Debug View** für Roh-Prompts, User Prompt, Kontext und Tool-Payloads,  
- **Agent Debug Logs** für chronologische Tool- und LLM-Ereignisse,  
- **Export von Debug-Sessions als OTLP JSON**,  
- **Export von Chat-Sessions als JSON**,  
- **OTel-Export** von Traces, Metrics und Events inklusive Tool-Ausführung und Token-Nutzung,  
- **lokale SQLite-Span-Datenbank** bei aktiviertem DB Span Exporter.  
Quellenstand: VS Code Docs, 2026; Alter: **13 Tage bis ca. 4 Monate**. citeturn19view3turn36view1turn36view2turn36view0

**Empfehlung:** Starte mit genau diesem Minimal-Setup in deinem Eval-Workspace:

```json
{
  "github.copilot.chat.agentDebugLog.enabled": true,
  "github.copilot.chat.fileLogging.enabled": true,
  "github.copilot.chat.otel.enabled": true,
  "github.copilot.chat.otel.captureContent": true,
  "github.copilot.chat.otel.exporterType": "file",
  "github.copilot.chat.otel.outfile": ".ai-evals/copilot-otel.jsonl",
  "github.copilot.chat.otel.dbSpanExporter.enabled": true
}
```

Damit bekommst du ohne Drittplattform schon genug Daten, um **Trials, Tool-Nutzung, Tokens, Latenz, Context Composition und Fehlermuster** auswerten zu können. VS Code dokumentiert die relevanten Settings und den DB-Export explizit. citeturn36view0turn36view1

### Nutze Hooks für einen echten Debug- oder Eval-Modus

**Fakt:** Die wahrscheinlich wichtigste 2026er VS-Code-Funktion für dich sind **Agent Hooks**. Die Doku vom **09.02.2026** (Alter: **ca. 3,5 Monate**) sagt explizit, dass Hooks an Lifecycle-Punkten wie `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PreCompact`, `SubagentStart`, `SubagentStop` und `Stop` Shell-Kommandos ausführen können, JSON via stdin bekommen und JSON via stdout zurückgeben können, um Verhalten zu beeinflussen. Sie sind genau für **Validation, Automation, Audit Trails und Integration mit externen Tools** gedacht. citeturn20view0turn20view3

Das ist die saubere Antwort auf deine Idee eines „Debug Mode“:  
**nicht** den Agenten bitten, sich selber ehrlich zu bewerten, sondern **deterministische Hooks** nutzen, die die Session beobachten, Tests ausführen und Metriken wegschreiben.

Ein sehr brauchbares Muster ist:

- `UserPromptSubmit`: starte eine neue Eval-Session-ID und markiere Variante `baseline` oder `candidate`
- `PreToolUse`: logge Tool-Name, Input, Policy-Entscheidung, evtl. gefährliche Kommandos
- `PostToolUse`: nach `edit`/`apply_patch`/`replace_string_in_file` automatisch Lint/Typecheck/Test anwerfen
- `Stop`: finalen Metrics-Snapshot erzeugen

Beispiel-Konfiguration:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "type": "command",
        "command": "node .github/evals/start-run.mjs"
      }
    ],
    "PreToolUse": [
      {
        "type": "command",
        "command": "node .github/evals/pre-tool.mjs"
      }
    ],
    "PostToolUse": [
      {
        "type": "command",
        "command": "node .github/evals/post-tool.mjs"
      }
    ],
    "Stop": [
      {
        "type": "command",
        "command": "node .github/evals/finalize-run.mjs"
      }
    ]
  }
}
```

Das ist technisch direkt mit der Hook-Doku vereinbar; der Input enthält u. a. `hookEventName`, `sessionId`, `transcript_path` sowie bei Tool-Hooks `tool_name`, `tool_input` und `tool_response`. citeturn20view0turn20view3

### Trenne sauber zwischen Instructions, Prompts, Skills und Agents

**Fakt:** GitHub und VS Code haben 2026 eine recht klare Rollenverteilung dieser Artefakte:

- `.github/copilot-instructions.md` für repository-weite Regeln,  
- `.github/instructions/**/*.instructions.md` für pfadspezifische Regeln,  
- `AGENTS.md` für agent-spezifische Anweisungen, wobei die nächste Datei im Verzeichnisbaum priorisiert,  
- `.github/prompts/*.prompt.md` für manuell aufrufbare, wiederverwendbare Aufgabenprompts,  
- **Agent Skills** als portable Bündel aus Instructions, Scripts und Ressourcen,  
- **Custom Agents** als Markdown-Profile mit Prompt, Tools und optional MCP-Servern.  
Quellenstand: GitHub Docs und VS Code Docs, 2026; Alter: **10 Tage bis 5 Monate**. citeturn19view4turn19view5turn19view2turn19view1

**Empfehlung:** Für Messbarkeit solltest du jede Änderung **isoliert** testen:

- Änderung nur in `.github/copilot-instructions.md`
- Änderung nur in `AGENTS.md`
- Änderung nur im Skill
- Änderung nur im `.prompt.md`
- Änderung nur im Custom Agent

Wenn du zwei Dinge gleichzeitig änderst, weißt du hinterher nicht, was den Effekt verursacht hat. Das klingt banal, wird aber laut 2026er Papers und Praxisberichten ständig missachtet. citeturn21view4turn22view0

### Verwende OTel oder ein Evals-Backend, aber nur als Transport

**Fakt:** VS Code kann Agent-Nutzung via OpenTelemetry exportieren; LangSmith kann OTel-Traces an Evaluations-Experimente knüpfen; Phoenix unterstützt deterministische Evaluatoren und LLM-as-a-Judge auf Traces, Datasets oder Experimenten. Das Entscheidende ist: **OTel wird hier zum Transportstandard**, nicht zur Metrik selbst. Quellenstand: 2026-Dokumentation, Alter: **0–4 Monate**. citeturn36view0turn23view1turn23view2

**Empfehlung:** Wenn du schnell starten willst, nimm zuerst **lokale JSONL/SQLite/OTLP-Exporte** aus VS Code. Wenn du später Dashboards, Online-Evals oder Regression-Gates willst, leite dieselben Traces an Phoenix, LangSmith oder ein eigenes OTel-Backend weiter. Dein Messsystem sollte **backend-unabhängig** sein: Tasks, Grader, Scores und Session-IDs gehören dir; OTel ist nur die Leitung.

### Achte streng auf Experimentdesign

**Fakt:** Der offizielle VS-Code-Post vom **15.05.2026** sagt ausdrücklich, dass unterschiedliche Modelle unterschiedliche Harness-Logik, andere Tooling-Präferenzen und sogar andere System-Prompts brauchen. GitHub listet 2026 mehrere aktuelle Modelle; OpenAI führt in den offiziellen 2026-Seiten **GPT-5.4/GPT-5.5** auf, Anthropic-Dokumentation und Preisseite führen **Claude Opus 4.6/4.7**. Gleichzeitig hat GitHub am **18.03.2026** **GPT-5.3-Codex** als LTS-Modell ausgewiesen. citeturn18view3turn25view0turn25view1turn25view3turn41search15

**Konsequenz:** Für Harness-Evals musst du das Modell **pinnen**. Wenn du Prompt/Instructions/Skill änderst, darf sich **nicht gleichzeitig** das Modell, die Reasoning-Stufe, die Tool-Liste oder der Runner ändern. Sonst misst du mehrere Variablen auf einmal. Das ist keine Geschmacksfrage, sondern zwingend, weil VS Code selbst dokumentiert, dass dieselbe Harness-Änderung je nach Modell anders wirkt. citeturn18view3

**Empfehlung:** Für belastbare Vorher/Nachher-Vergleiche:

- gleiches Repo-Snapshot
- gleicher Modellname
- gleicher Reasoning-/Effort-Modus
- gleiche Tool-Liste
- gleiche Timeout-Grenzen
- gleiche Setup-Schritte
- gleiche Task-Suite
- mindestens **5–10 Trials pro Task** bei nichtdeterminischen Aufgaben
- Ergebnisse als **Verteilung**, nicht als Einzellauf

Bei binären Metriken wie „Task bestanden / nicht bestanden“ solltest du mindestens ein **Konfidenzintervall** über die Rate berichten; die NIST-Handbook-Seite empfiehlt für Proportionen u. a. die **Wilson-Methode**. Für gepaarte Vorher/Nachher-Binärvergleiche ist ein **paired proportion test** wie McNemar fachlich passend. Diese Statistikempfehlung ist Standardstatistik; die konkrete Auswahl ist meine Empfehlung für dein Setup. citeturn34search1turn34search0

## So würde ich es in Divical einbauen

### Ein robuster Minimalaufbau

**Empfehlung:** Ich würde in Divical einen Ordner wie `.github/evals/` oder `tools/ai-evals/` anlegen und dort vier Dinge definieren:

1. **Task-Katalog**  
   Kleine, realistische Tasks mit deterministischen Verifiern.
2. **Variant-Definitionen**  
   `baseline` und `candidate`, also z. B. zwei Instruction-Dateien oder zwei Skill-Versionen.
3. **Hook-Skripte**  
   Start, Tool-Logging, Post-Validation, Finalizer.
4. **Scorer-Pipeline**  
   Ein Skript, das aus OTel/JSON/Logs die Metriken aggregiert.

Für den Task-Katalog würde ich drei Schichten bauen:

- **Smoke Suite**  
  15–30 sehr billige Tasks, die immer in CI laufen
- **Capability Suite**  
  30–100 echte Repo-Tasks für Vorher/Nachher-Vergleiche
- **Regression Suite**  
  dauerhaft grüne, historisch bereits gelöste Problemfälle

Anthropic unterscheidet explizit zwischen **capability evals** und **regression evals**; genau diese Trennung solltest du übernehmen. citeturn22view0

### Der Debug-Mode, den du angesprochen hast

**Empfehlung:** Ja, ein **gezielter Debug- oder Eval-Mode** ist sinnvoll — aber als **instrumentierter Modus**, nicht als bloße zusätzliche Modellanweisung.

Ich würde ihn so aufziehen:

- Ein `.prompt.md` wie `/evalTask`, das eine Task-ID übernimmt.
- Ein Custom Agent oder Skill namens **Evaluator** oder **Strict Solver**.
- Hooks aktivieren nur in diesem Modus.
- Jede Session bekommt `experimentId`, `variant`, `taskId`, `trial`, `model`, `timestamp`.
- `Stop`-Hook erzeugt eine JSON-Zeile mit den Scores.

Ein mögliches Ergebnis-JSON pro Trial:

```json
{
  "experimentId": "2026-05-28-instructions-v3",
  "variant": "candidate",
  "taskId": "calendar-bug-014",
  "trial": 7,
  "model": "gpt-5.5",
  "resolved": true,
  "adherenceScore": 0.92,
  "recoveryRate": 1.0,
  "badToolCallCount": 2,
  "toolCallCount": 11,
  "totalTokens": 18422,
  "latencyMs": 148220,
  "dangerousActionAttempted": false,
  "humanInterventionCount": 0,
  "notes": ["used tests before final answer", "one redundant file read"]
}
```

Wichtig ist: **kein Selbstbericht des Agents als Ground Truth**. Wenn der Agent selber sagt „ich habe mich an alle Regeln gehalten“, ist das höchstens Zusatzsignal. Der eigentliche Score muss aus **Hooks, Tests, Logs und Review-Artefakten** kommen. Genau in diese Richtung argumentieren die 2026er Log-Analyse- und Agent-Eval-Arbeiten. citeturn33view0turn22view0

### Ein konkreter Score, der in der Praxis funktioniert

**Empfehlung:** Wenn du in Divical einen einzigen Vergleichsreport sehen willst, würde ich so gewichten:

**Harte Gates**
- `resolved_rate_delta >= 0`
- `dangerous_action_attempts == 0`
- `adherence_delta >= 0`
- `regression_failures == 0`

**Danach ein sekundärer Composite Score**
- 45 % Resolution Rate
- 20 % Adherence
- 15 % Trajectory Quality
- 10 % Human Burden inverse
- 10 % Efficiency inverse

Diese Gewichtung ist **meine Engineering-Empfehlung**, nicht ein offiziell standardisierter 2026-Benchmark. Sie passt aber gut zu dem, was VS Code, Anthropic, SWE-chat, Log-Analysis und AgentAtlas gemeinsam nahelegen. citeturn18view2turn22view0turn31view4turn33view0turn32view1

### Wenn du auch Copilot Cloud Agent nutzen willst

**Fakt:** Für den Cloud-Agent gibt es 2026 mehrere relevante Bausteine:  
GitHub dokumentiert `copilot-setup-steps.yml` zur Konfiguration des Environments; Session-Logs zeigen inzwischen Setup-Schritte, Custom Setup Output und Subagent-Aktivität besser an; Commits verlinken auf Session Logs; und GitHub beschreibt explizit Session Tracking und Environment Customization. Quellenstand: März bis Mai 2026, Alter: **2 Tage bis 2 Monate**. citeturn27view1turn41search0turn41search5turn41search11

**Empfehlung:** Wenn Divical später Cloud-Agent-Evals bekommt, dann sollte dein `copilot-setup-steps.yml` nicht nur Build-Dependencies installieren, sondern auch deine **Verifikationstools** garantieren: Testframework, Linter, Typechecker, Security-Scanner, ggf. repo-spezifische Guardrails. Sonst verwechselst du Harness-Qualität mit zufälligen Environment-Unterschieden. GitHub weist selbst darauf hin, dass trial-and-error Dependency Discovery langsam und unzuverlässig sein kann. citeturn41search3turn41search0

## Nutzerstimmung und Praxissignale aus 2026

**Anekdotisches, aber konsistentes Signal:** In Reddit- und HN-Diskussionen von 2026 ist der Konsens erstaunlich klar: Entwickler halten den **Harness** oft für den größeren Hebel als das Modell allein. Mehrere Diskussionen berichten, dass derselbe Modellkern je nach Harness deutlich anders performt, und dass große Systemprompts, zu viele Tools und schwache Edit-Mechaniken reale Qualität und Geschwindigkeit sichtbar verschlechtern können. Ein Reddit-Post vom Mai 2026 beschreibt beispielsweise, dass derselbe Modellkern in GitHub Copilot deutlich mehr File-Edit-Versuche brauchte als in anderen Harnesses; die Kommentare verlangen dort explizit wiederholte Runs statt Einzelscreenshots. HN-Diskussionen im Februar 2026 sprechen ähnlich von „2026 is the year of the harness“. Diese Quellen sind **anektodisch**, aber als Stimmungsbild relevant. citeturn12view1turn40search2turn40search6

**Anekdotisches Signal:** Eine wiederkehrende positive Wahrnehmung 2026 ist, dass **leichtere Harnesses** oder gut gemachte **Skills** lokaler und stabiler wirken als dicke, kontextschwere Setups. In Reddit-Kommentaren zu Pi/OpenCode vom Mai 2026 wird mehrmals gelobt, dass ein kleinerer Prompt-Overhead und gezielte Skills bei lokalen oder kleineren Modellen deutlich bessere Reaktionszeiten und teils bessere Steuerbarkeit bringen. Das ist kein wissenschaftlicher Beweis, aber es unterstützt eine klare Designentscheidung: **kleine, austauschbare Skills und deterministische Hooks** schlagen oft einen monolithischen Mega-Prompt. citeturn12view2

**Anekdotisches Signal:** Gegen GitHub Copilot PR Review und Web-Surfaces gibt es 2025/2026 spürbar Frust wegen inkonsistenter Anwendung von Instructions. Mehrere GitHub-Community-Threads berichten, dass Review-Kommentare zwischen Re-Requests variieren, Instructions nicht vollständig respektiert werden und Restarts manchmal helfen. Für dein Messproblem ist das eine sehr wichtige Konsequenz: **evaluiere Instruction-Änderungen nicht primär auf GitHub-Web-Review**, sondern in **VS Code lokal mit Debug/OTel/Hooks** oder im **Cloud-Agent mit Session Logs**. citeturn29view0turn29view1turn29view2turn29view3

**Wichtig:** Ich habe in dieser Sitzung zwar YouTube-Videos zu **Custom Instructions**, **Chat Debug View** und **Agent Debug Logs** identifiziert, aber die **Kommentarbereiche** waren über die öffentliche Abrufstrecke nicht zuverlässig extrahierbar. Das belastbare User-Sentiment in diesem Report stammt deshalb primär aus **Reddit, HN und GitHub Community**, nicht aus vollständig ausgelesenen YouTube-Kommentaren. Die Video-Inhalte selbst bestätigen allerdings den starken 2026er Fokus auf **Debugbarkeit, Session-Logs und Kontexthygiene**. citeturn10search1turn10search6turn13search0turn13search16

## Was ich dir konkret empfehlen würde

**Meine Empfehlung, wenn du nächste Woche anfangen willst:**

Baue zuerst **eine kleine, ehrliche Evalsuite mit 20–40 Divical-nahen Tasks**. Halte Modell, Effort-Level, Tool-Set und Repo-Snapshot konstant. Miss pro Trial **Resolution**, **Adherence**, **Recovery**, **Bad Tool Calls**, **Tokens**, **Latency** und **Human Burden**. Instrumentiere **VS Code Hooks + OTel + Chat Debug Export**. Nutze **Instructions/AGENTS/Skills/Prompt Files** als separate Varianten und vergleiche sie immer **gepaart** gegen dieselbe Task-Suite. Verwende GitHub-Nutzungsmetriken nur als Ergänzung, nicht als Kernsignal. Und wenn ein Change die Pass-Rate minimal verbessert, aber Tool-Fehler, Tokens, Schleifen oder Nacharbeit stark verschlechtert, ist das **kein Gewinn**, sondern meist nur anders versteckte Kosten. Diese Schlussfolgerung ist meine Synthese, aber sie ist sehr gut durch die 2026er Primärquellen gedeckt. citeturn18view2turn22view0turn33view0turn36view0turn31view4

## Offene Fragen und Grenzen

**Unvollständig verifiziert:** Ich konnte den ausgewählten GitHub-Quellbestand **4sthea/Divical** in dieser Sitzung nicht direkt lesen. Daher ist der Integrationsplan **repo-neutral** und nennt bewusst keine verifizierten Divical-Dateien, Skripte oder Build-Befehle.

**Wichtige methodische Grenze:** Viele 2026er Publikationen und Produktdokumente beschreiben **Prinzipien, interne Frameworks oder Plattformfähigkeiten**, aber veröffentlichen **nicht immer den vollständigen Produktionscode** ihrer Harnesses. Besonders bei VS Code VSC-Bench und der internen Eval-Pipeline ist die **Architektur öffentlich beschrieben**, aber nicht als vollständig auditierbares öffentliches Repo in meinem hier genutzten Material verfügbar. citeturn18view0turn18view2

**Praktische Grenze:** User-Sentiment aus Reddit, HN und GitHub Community ist wertvoll, aber anekdotisch und selektiv. Ich habe es deshalb im Report klar als Praxissignal behandelt, nicht als harte Primärevidenz. citeturn12view1turn12view2turn29view0turn40search0