# Tiefenanalyse zu Agent Harnesses, Tokeneffizienz und einer skills-zentrierten Copilot-Architektur

## Kurzurteil

Deine Grundidee ist **im Kern gut**, aber **nur in einer streng abgespeckten Variante**. Der Teil „wenige stabile Agenten, möglichst viel wiederverwendbares Verhalten in Skills“ passt erstaunlich gut zu dem, was GitHub/VS Code, OpenAI und Anthropic inzwischen selbst dokumentieren: einfache, komponierbare Muster schlagen oft komplexe Agentennetze; Skills sind für on-demand geladene, spezialisierte Workflows gedacht; und die eigentliche Qualität eines Coding-Agents kommt weniger aus „mehr Agenten“ als aus **Kontextaufbau, Tool-/Interface-Design, Guardrails, Feedbackschleifen und Evaluierung**. citeturn24view0turn6view1turn27view0turn27view5

Der problematische Teil deiner Idee ist etwas anderes: **alles Relevante zu Beginn laden**, **zu früh zu viele Tools in den Kontext kippen** und **standardmäßig an Subagents delegieren**. Genau das ist oft **nicht** token-effizient. Offizielle Quellen beschreiben inzwischen sehr klar das Gegenteil als Best Practice: **progressive disclosure**, also kleine stabile Einstiegskontexte, dann gezielte Suche, dann nur die wirklich nötigen Details; Skills und Tooldefinitionen sollten **on demand** geladen werden; und Multi-Agent-Setups lohnen sich vor allem dort, wo Aufgaben wirklich parallelisierbar oder kontext-isolierbar sind. Für viele Coding-Aufgaben ist das nur eingeschränkt der Fall. citeturn28view0turn31view0turn20view1turn7view2

Die robuste Schlussfolgerung lautet deshalb: **Ja zu 2–3 Agenten plus vielen Skills. Nein zu einem „immer alles vorladen“-Orchestrator und nein zu „immer Subagent“ als Default.** Wenn du das sauber trennst, ist dein Ansatz zugleich **token-effizienter, wartbarer und näher an modernen Plattformmustern** als ein Zoo aus zehn Agenten mit überlappenden Rollen. citeturn29view1turn6view1turn35view0turn24view0

## Was die Forschung und Praxis tatsächlich zeigt

Die zuverlässigsten Quellen zeigen ein konsistentes Muster: **Harness- und Interface-Design schlagen Agenten-Mythologie**. SWE-agent hat früh gezeigt, dass ein speziell für LLMs entworfenes Agent-Computer-Interface die Leistung deutlich verbessert, weil Suche, Editieren und Feedback agententauglich gemacht werden. Fast in die Gegenrichtung argumentiert Agentless: Eine einfachere, interpretierbare Drei-Phasen-Pipeline aus Lokalisierung, Reparatur und Validierung kann auf SWE-bench Lite sehr konkurrenzfähig oder sogar stärker sein als komplexere Open-Source-Agenten – bei deutlich geringeren Kosten. Diese beiden Ergebnisse widersprechen sich nicht; zusammen sagen sie: **Nicht die Menge der Agenten ist der Hebel, sondern die Qualität der Schleife, des Kontexts und der Werkzeuge.** citeturn9view1turn19view3turn8search0turn19view2

Dass **Repository-Verständnis** ein Engpass ist, wird ebenfalls breit gestützt. VS Code beschreibt, dass Copilot-Agenten große Codebasen über semantische Suche, Grep, Usages, File Search und iteratives Nachfassen erschließen, statt „einfach alles“ in den Prompt zu laden. Aider nutzt dafür eine kompakte Repository Map; RepoGraph zeigt in der Forschung, dass strukturierte Repräsentationen auf Repository-Ebene sowohl agentische als auch prozedurale Software-Engineering-Ansätze verbessern können. Das heißt für dein Vorhaben: Die Idee einer „Repository Map“ ist **gut**, aber nur dann, wenn sie **kompakt, budgetiert und selektiv** ist, nicht als monolithischer Dump. citeturn6view4turn22view0turn22view1turn9view3turn10view4

Auch zur Frage „viel statischer Repository-Kontext oder nicht?“ ist die Lage inzwischen differenzierter als viele Tutorials suggerieren. Die ETH-Zürich-Arbeit zu `AGENTS.md` findet über mehrere Agenten und Modelle hinweg, dass Kontextdateien die Erfolgsrate im Schnitt eher leicht senken, die Zahl der Schritte erhöhen und die Inferenzkosten im Schnitt um etwa 20–23 % steigern können; zugleich folgen Agenten den Anweisungen darin durchaus. Dass die Wirkung trotzdem manchmal subjektiv positiv erlebt wird, erklärt dieselbe Arbeit teilweise: In Repositories mit **schwacher sonstiger Dokumentation** können generierte Kontextdateien helfen; wenn bestehende Doku entfernt wurde, verbesserten sie die Performance in diesem Setting im Schnitt um 2,7 %. Eine zweite Studie aus dem PR-Alltag kommt sogar zu dem Ergebnis, dass `AGENTS.md` in realen Pull-Request-Workflows mit niedrigerer Median-Laufzeit und geringerem Output-Token-Verbrauch assoziiert war, bei vergleichbarem Abschlussverhalten. Die einzig ehrliche Schlussfolgerung ist also: **Kontextdateien sind kein pauschaler Gewinn; sie helfen nur, wenn sie knapp, konkret und nicht redundant sind.** citeturn37view0turn12view1

Das deckt sich bemerkenswert gut mit Community-Signalen. In Reddit-Diskussionen berichten Entwickler immer wieder, dass **hyper-spezifische** Hinweise – exakte Build-/Test-Kommandos, reale Produktions-Gotchas, konkrete Fehlerbilder – nützlich sind, während lange Prinzipienlisten und vage Architekturprosa eher „Kontextverschmutzung“ erzeugen. Bei Multi-Agent-Setups ist das Stimmungsbild ähnlich: Sinnvoll nur dann, wenn unabhängige Such- oder Prüfpfade existieren; ansonsten steigen Debugging- und Koordinationskosten schnell, weshalb Tracing und Observability als entscheidend beschrieben werden. Das sind keine belastbaren Benchmarks, aber als Praxis-Signal passen sie gut zur formalen Evidenz. citeturn14view2turn14view1

## Wo deine Tokens wirklich verloren gehen

Wenn du **wirklich** auf Token-Effizienz optimieren willst, musst du zuerst die richtige Stelle ins Visier nehmen: **nicht** die Oberfläche der Antwort, sondern **den Kontext**. Eine aktuelle Diplomarbeit zu Software-Engineering-Agents zeigt, dass in diesem Setting **mehr als 90 %** der verarbeiteten Tokens auf Codekontext entfallen; der eigentliche Reparatur-Codeanteil lag in der Analyse bei **91,8 %** der Tokens. Der größte Kostenhebel ist also fast nie „weniger höfliche Antworten“, sondern **weniger irrelevanter oder redundanter Code- und Toolkontext**. citeturn25view0turn25view5

Das ist der Grund, warum „Caveman“-artige Stile zwar nützlich sein können, aber nur ein Nebenschauplatz sind. Das Caveman-Repository selbst sagt ausdrücklich, dass es vor allem **Output-Tokens** komprimiert; „thinking/reasoning tokens“ bleiben unberührt. Seine größere Idee – auch Memory-Dateien zu komprimieren – ist interessanter, weil sie Startkontext dauerhaft verkleinert. Aber selbst dann gilt: Wenn dein Agent unnötig viele Dateien liest, zu viele Tooldefinitionen lädt oder große Zwischenergebnisse durch den Prompt schleift, frisst das die Einsparung durch komprimierten Ausgabestil sehr schnell wieder auf. citeturn20view0turn25view0

Genau hier ist das Prinzip **progressive disclosure** zentral. Anthropic beschreibt Skills explizit so: Beim Start werden nur Name und Beschreibung jeder installierten Skill in den Prompt geladen; der eigentliche `SKILL.md`-Inhalt und tieferliegende Referenzen werden erst gelesen, wenn der Skill für die Aufgabe relevant ist. OpenAI beschreibt dasselbe Muster für Repository-Wissen: Ein großes `AGENTS.md` als Enzyklopädie sei gescheitert; stattdessen funktioniere ein **kurzes `AGENTS.md` als Inhaltsverzeichnis**, das auf versionierte tiefe Doku verweist. Das ist der richtige mentale Frame für deine Architektur. citeturn31view0turn28view0

Dasselbe gilt für Tools. Anthropic zeigt sehr konkret, warum große MCP-/Toolsets teuer werden: Die Tooldefinitionen selbst belegen Kontext, und Zwischenergebnisse laufen oft mehrfach durch das Modell. Im demonstrierten Beispiel reduziert ein Code-Execution-Ansatz mit MCP den Tokenbedarf von **150 000 auf 2 000 Tokens**, also um **98,7 %**, weil nur relevante Werkzeuge on demand geladen werden und große Daten im Ausführungskontext statt im Modellkontext bleiben. Für dein Design heißt das brutal einfach: **Der Orchestrator darf nicht „alle Toolsets“ vorladen.** Er darf höchstens einen kleinen globalen Werkzeugindex oder Skill-Metadaten haben und dann selektiv nachladen. citeturn20view1

Auch Copilot/VS Code selbst sind inzwischen auf dieses Muster ausgelegt. Die Plattform sucht bei größeren Workspaces iterativ und automatisch über semantische Suche, Grep, File Search und Usages, statt die gesamte Codebasis direkt einzublenden. In den Harness-Blogs beschreibt VS Code außerdem Gesprächskompression bei wachsender History, und Copilot CLI bietet explizite Kontext-Metriken und Compaction; nahe am Limit wird die History automatisch komprimiert. Das spricht erneut gegen dein anfängliches „erst alles Fundamentale laden“ – modernere Harnesses versuchen genau das **nicht** zu tun. citeturn6view4turn27view0turn35view0

## Was für wenige Agenten und viele Skills spricht

Die sauberste Trennung, die sich aus den Dokumentationen ergibt, ist diese: **Custom Agents** sind für **Rolle, Tool-Berechtigungen, Modellwahl und Handoffs** da; **Skills** sind für **wiederverwendbare Fähigkeiten, Prozeduren, Skripte, Beispiele und tiefere Referenzen** da; **Instructions** sind für **immer geltende Fakten und Regeln**; **Prompt Files** sind für **wiederkehrende Entrypoints und Varianten** eines Workflows. Sowohl GitHub/VS Code als auch Anthropic sagen im Kern dasselbe: Prozeduren und Spezialwissen gehören **nicht** in den immer geladenen globalen Kontext, sondern in **on-demand ladbare Skills**. citeturn29view1turn6view1turn18view1turn18view0

Für deine Idee ist das ein starkes Ja. VS Code dokumentiert Agent Skills ausdrücklich als task-spezifisch und **on-demand geladen**; sie funktionieren über VS Code, Copilot CLI und Cloud-Agent hinweg. Anthropic formuliert es noch schärfer: Statt für jeden Use Case fragmentierte Spezialagenten zu bauen, kann man allgemeine Agenten mit kompositorischen Skills spezialisieren. Genau das ist im Grunde dein Vorschlag – und genau dafür ist die Mechanik gebaut worden. citeturn6view1turn31view0

Dass wenige Agenten genügen, sieht man auch daran, wie GitHub selbst sein System strukturiert. Copilot CLI kommt nicht mit zwanzig Kernrollen, sondern mit einem **kleinen Standard-Portfolio** wie Explore, Task, General purpose, Code review, Research und einer automatisch genutzten Rubber-duck-Rolle. Das ist kein mathematischer Beweis, aber es ist ein praktisches Produkt-Signal: **wenige stabile Modi**, viel Verhalten durch Kontext, Tools und Spezialisierung. citeturn35view0

Subagents sind dabei ein Spezialwerkzeug, kein Grundprinzip. VS Code beschreibt sie als **kontextisolierte Agenten**, die unabhängige Teilaufgaben erledigen und nur eine Zusammenfassung zurückgeben; für konsistentes Verhalten soll man die Bedingungen für Subagent-Nutzung in die Agent-Instruktionen aufnehmen, nicht jedes Mal manuell ad hoc triggern. Gleichzeitig sagt Anthropic sehr ausdrücklich, dass Multi-Agent-Setups zwar bei breit verzweigten Research-Aufgaben stark sind, in der Praxis aber **viel mehr Tokens verbrennen** und für viele Coding-Aufgaben **weniger gut passen**, weil diese oft nicht stark parallelisierbar sind und die Echtzeit-Koordination zwischen Agenten schwierig bleibt. Eine neuere Vergleichsarbeit kommt ebenfalls dazu, dass der Vorteil von Multi-Agent gegenüber Single-Agent mit stärkeren Modellen kleiner wird; vorgeschlagen wird ein Hybrid, der nur bei Bedarf eskaliert. citeturn6view3turn7view2turn33view0

Dein bestes Zielbild ist deshalb **nicht** „Orchestrator plus standardmäßiger Worker-Subagent“, sondern **„Single-Agent-first, skill-heavy, subagent-optional“**. Anders gesagt: Ein Agent sollte die Aufgabe **zuerst selbst** mit gezielter Suche und passenden Skills lösen; nur wenn eine Teilaufgabe klar isolierbar ist – etwa unabhängige Recherche, parallele Alternativanalyse, unabhängige Review-Perspektive oder ein anderer Permission-/Tool-Scope – sollte er einen Subagenten starten. citeturn24view1turn6view3turn7view2

## Bewertung deines konkreten Entwurfs

**Der Schritt „erst alles Fundamentale laden“ ist der schwächste Teil deines Designs.** Fundamentaler, immer geladener Kontext sollte minimal bleiben: Build-/Test-Kommandos, wenige harte repo-spezifische Konventionen, Routing-Hinweise und Links auf tieferes Wissen. Große Toolsets, lange Dokus, vollständige Skill-Inhalte oder breite Codebasis-Summaries zu Beginn sind genau das Muster, vor dem OpenAI, Anthropic, Aider und die AGENTS.md-Evaluationen faktisch warnen. citeturn16view0turn28view0turn20view1turn22view2turn37view0

**Der Schritt „gezielt Fragen stellen“ ist gut**, aber nur in einer gebundenen Form. VS Code zeigt im Context-Engineering-Guide ausdrücklich einen `/plan-qna`-Stil mit **kurzer Analyse, dann 3 Klärungsfragen, dann Planung**. Das ist sinnvoller als entweder sofort loszulegen oder sich in einem endlosen Interview festzufahren. Die richtige Reihenfolge ist: kurze Repo-/Issue-Sichtung, dann maximal wenige offene Fragen, dann Plan. citeturn30view0

**Der Schritt „Repository Map / relevante Bereiche bestimmen“ ist sehr gut**, solange diese Map **kompakt und budgetiert** ist. Die offizielle VS-Code-Suche, Aiders RepoMap und Forschung wie RepoGraph zeigen alle, dass selektive Strukturrepräsentationen wertvoll sind. Schlechte Variante: „Projektüberblick“ als langer Markdown-Fließtext. Gute Variante: graphisch/strukturell verdichtete Symbol- und Dateisicht plus gezieltes Nachlesen. citeturn6view4turn22view0turn22view1turn9view3

**Der Schritt „passende Skills wählen“ ist einer der stärksten Teile deiner Idee.** Genau dafür sind Skills gedacht: wiederkehrende, procedural knowledge, Beispiele, kleine Skripte, testbare Abläufe. Sie erhöhen Portabilität und sparen Tokens, weil sie nicht immer vollständig mitgeschleppt werden. citeturn6view1turn18view1turn31view0

**Der Schritt „immer an einen Subagenten delegieren“ ist meistens zu viel.** VS Code und Anthropic beschreiben Subagents als wertvoll bei Kontextisolation und Parallelisierung, aber nicht als pauschalen Default für jeden Implementierungsauftrag. Wenn der Main Agent die Aufgabe bereits mit denselben Tools, derselben Berechtigung und überschaubarem lokalen Kontext ausführen kann, erzeugt Delegation nur Koordinations- und Token-Overhead. citeturn6view3turn7view2turn33view0

**Der Wunsch nach einem festen Rückgabeformat ist richtig**, aber die Form sollte leichtgewichtig sein. Anthropic warnt explizit davor, unnötigen Format-Overhead zu erzeugen; Code oder längere Inhalte in JSON zu verpacken ist für Modelle oft schwerer als natürliches Markdown/YAML. Wenn der Orchestrator selbst wieder ein LLM ist, ist ein kleines Markdown- oder YAML-Schema meistens der bessere Default. Große Ergebnisse sollten nicht durch den Chat „telefoniert“ werden, sondern als Artefakte im Dateisystem landen, auf die der Orchestrator nur referenziert. citeturn24view1turn36view0

## Empfohlene Zielarchitektur für dein Repo

Meine klare Empfehlung ist eine **schmale Drei-Rollen-Architektur**, die aber im Alltag oft wie **zwei** Rollen benutzt wird.

Der **Planner/Clarifier** ist read-only. Er bekommt Suchwerkzeuge, Repo-Navigation, eventuell Web/Issue-Kontext und maximal begrenzte Klärungsfragen. Seine Aufgabe ist nicht, Code zu schreiben, sondern **den Scope sauber zu bestimmen**, offene Fragen zu identifizieren und einen **kleinen Plan als Artefakt** zu erzeugen. Das passt direkt zu den VS-Code-Handoffs und dem Plan-Agent-Muster. citeturn29view1turn29view2turn30view0

Der **Implementer** ist der Default-Agent für echte Arbeit. Er bekommt Edit-/Build-/Test-Tools, Skill-Zugriff und nur so viel Kontext wie nötig: das Issue, den Plan, relevante Dateien, relevante Skills. Er darf selbst arbeiten und **nur dann** Subagents starten, wenn eine Teilaufgabe isoliert werden sollte – beispielsweise unabhängige Recherche, alternative Lösungsanalyse, Security-/Performance-Review oder ein klar anderer Permissions-Scope. citeturn6view4turn6view3turn24view1

Der **Reviewer/Verifier** ist optional, aber nützlich. Er sollte möglichst unabhängig prüfen: Diff gegen Plan, Tests, Sicherheits-/Performance-/Regression-Checks, Architekturregeln. In vielen Teams reicht es, diese Rolle **nicht als ständig sichtbaren Agenten**, sondern als subagentfähige Review-Persona oder Prompt-File bereitzuhalten. Genau dafür sind Custom Agents mit Toolrestriktionen und Handoffs sinnvoll. citeturn29view1turn23view0

Wenn du radikal vereinfachen willst, ist die beste Alternative sogar noch schlanker: **ein General/Implement-Agent plus ein Reviewer-Agent**, und der Planner bleibt als Prompt/Handoff oder built-in Plan Agent erhalten. Diese Architektur ist in der Regel effizienter als ein dauernd dazwischengeschalteter Orchestrator, weil der Main Agent nicht jedes Mal Metasummaries und Delegationsprompts erzeugen muss. Die Literatur zu Agentless und zu Single-vs-Multi-Agent spricht eher **für** diesen reduzierten Default und **für Eskalation bei Bedarf**, nicht für permanente Orchestration. citeturn8search0turn33view0turn24view1

Ein praxistauglicher Repo-Aufbau dafür wäre:

```text
.github/
  copilot-instructions.md          # immer geladene, knappe Fakten
  agents/
    plan.agent.md                  # read-only, Klärung + Plan
    implement.agent.md             # edit/build/test
    review.agent.md                # review/verifier
  prompts/
    plan-qna.prompt.md             # kurze Analyse -> max. 3 Fragen -> Plan
    implement-from-plan.prompt.md  # implementiere referenzierten Plan
    review-against-plan.prompt.md  # prüfe Diff gegen Plan
  skills/
    tdd/
      SKILL.md
    migration/
      SKILL.md
    api-design/
      SKILL.md
    perf-check/
      SKILL.md
docs/
  PRODUCT.md
  ARCHITECTURE.md
  CONTRIBUTING.md
plans/
  active/
  completed/
reports/
  review/
```

Diese Kombination entspricht ziemlich genau den dokumentierten Plattformrollen: **immer-gültige Fakten** in Instructions/AGENTS, **tieferes Wissen** in versionierter Doku, **Abläufe und Skripte** in Skills, **Rollen/Berechtigungen/Handoffs** in Agents, **Varianten** in Prompt Files. OpenAI empfiehlt ausdrücklich ein kleines Repository-Entry-Point-Dokument plus verlinkte Wissensbasis; VS Code empfiehlt kurze projektweite Doku-Dateien wie `PRODUCT.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`; und Anthropic empfiehlt Skills für Prozeduren statt aufgeblähter globaler Erinnerungsdateien. citeturn28view0turn30view0turn18view0turn31view0

Für das Rückgabeformat der Worker/Subagents würde ich **kein schweres JSON-Objekt als Default** verwenden, sondern etwas in dieser Art:

```yaml
status: done | blocked
artifact: plans/active/feature-x.md
changed:
  - src/foo.ts
  - tests/foo.spec.ts
verified:
  - pnpm test --filter foo
  - pnpm lint --filter foo
risks:
  - edge case around null handling not covered
next:
  - ask user to confirm API field naming
```

Das ist kurz, stabil und für LLMs natürlich genug. Für größere Ergebnisse – Research, Review, Migrationspläne – sollte der Subagent die eigentliche Ausgabe **als Datei speichern** und nur `artifact:` zurückgeben. Anthropic empfiehlt genau das, um das „game of telephone“ zu vermeiden, also das verlustreiche Durchreichen großer Resultate durch den Coordinator. citeturn36view0turn24view1

## Konkrete Designregeln, wenn du das wirklich sauber bauen willst

Erstens: **Halte den always-on Kontext brutal klein.** In `copilot-instructions.md` oder `AGENTS.md` gehören nur Dinge, die in fast jeder Session gelten und nicht leicht aus dem Repo inferierbar sind: Build-/Test-Kommandos, wenige harte Konventionen, Routing-Hinweise, Sicherheitshinweise. OpenAI sagt inzwischen wörtlich: `AGENTS.md` klein halten; in ihrem internen Codex-Repo wurde ein großes monolithisches `AGENTS.md` verworfen und durch ein kurzes Inhaltsverzeichnis plus tiefe Doku ersetzt. citeturn16view0turn28view0

Zweitens: **Alles, was prozedural ist, wandert in Skills.** Wenn du denselben Ablauf, dieselbe Checkliste, dieselben Skripte oder dieselben Referenzdateien wiederholt brauchst, ist das ein Skill, kein globaler Regeltext. Anthropic und VS Code beschreiben Skills explizit als on-demand, portabel und geeignet für Skripte, Beispiele und Ressourcen. citeturn6view1turn18view1turn31view0

Drittens: **Skills müssen selbst tokenbewusst gebaut sein.** Halte Referenzen nur **eine Ebene tief** ab `SKILL.md`, gib längeren Referenzdateien ein Inhaltsverzeichnis, und trenne selten benötigte Details in separate Dateien. Genau so vermeiden die offiziellen Skill-Guides unvollständige Reads und unnötigen Kontext. citeturn18view2

Viertens: **Nicht verhandelbare Regeln gehören in Code, nicht in Prosa.** Architekturgrenzen, Logging-Standards, Dateigrößen, Layering, Security-Regeln, Formatierung, Testpflichten: Wenn es weh tut, wenn der Agent es vergisst, dann gehört es in Lints, Tests, Hooks oder CI. OpenAI beschreibt genau diesen Shift: menschlicher Geschmack und Review-Kommentare werden schrittweise in Goldprinzipien, Linter und strukturelle Tests überführt. citeturn28view0turn6view6turn6view7

Fünftens: **Subagents nur mit klaren Einsatzschwellen.** Gute Trigger sind: unabhängige Recherchepfade, anderer Tool-/Permission-Scope, anderes Modell, unabhängige Review-Perspektive oder harte Kontextisolation. Schlechte Trigger sind: „eigentlich jede mittlere Aufgabe“, „weil Orchestrator-Pattern modern klingt“ oder „damit es modular aussieht“. VS Code empfiehlt, die Bedingungen für Subagent-Nutzung direkt in Agent-Instruktionen zu definieren; Anthropic weist darauf hin, dass Coding-Aufgaben oft nicht genug echte Parallelisierbarkeit bieten, um Multi-Agent-Kosten zu rechtfertigen. citeturn6view3turn7view2

Sechstens: **Nutze Repo-Maps, Suche und Artefakte statt Vollkontext.** Eine gute Harness-Strategie ist: kleiner Einstiegskontext → selektive Suche (semantic, grep, usages, file search) → kompakte Map → gezieltes Nachladen → Plan-/Review-Artefakt schreiben. Das ist sowohl in VS Code als auch bei Aider/OpenAI/Anthropic praktisch das dominante Muster. citeturn6view4turn22view0turn28view0

Siebtens: **Miss dein Harness wie ein Produkt.** VS Code misst Korrektheit, Agent-Effort, Token-Effizienz und Latenz im VSC-Bench; Anthropic empfiehlt, sofort mit kleinen Eval-Sets zu starten, selbst wenn es zunächst nur etwa 20 repräsentative Aufgaben sind. Für dein Repo würde ich mindestens erfassen: Erfolgsrate, Token pro Task, Tool-Calls pro Task, Anzahl der gelesenen Dateien, Zeit bis zur ersten relevanten Datei, Test-Pass-Rate, manuelle Korrekturen nach Agent-Lauf und Reopen-Rate nach PR/Review. Ohne diese Zahlen optimierst du ins Blaue. citeturn27view2turn36view0

## Offene Fragen und Grenzen

Die Evidenz zu `AGENTS.md`-artigen Kontextdateien ist **noch nicht vollständig stabil**. Eine starke Benchmark-Arbeit findet im Mittel eher mehr Kosten und nicht mehr Erfolg; eine andere Arbeit im Pull-Request-Alltag findet bessere Effizienzmetriken bei vergleichbarem Abschlussverhalten. Das ist kein Widerspruch, sondern ein Hinweis darauf, dass **Kontextqualität, Redundanz, Repo-Dokumentation, Agent-Harness und Tasktyp** entscheidend sind. Pauschale Aussagen wie „AGENTS.md ist immer gut“ oder „immer schlecht“ sind aktuell nicht haltbar. citeturn37view0turn12view1

Außerdem ist der Bereich extrem schnelllebig. Einige der besten Daten stammen aus Vendor-Blogs und Produktdokumentationen, also aus Quellen, die sehr nah an realen Harnesses sind, aber nicht immer alle Rohdaten öffentlich machen. Gleichzeitig sind bestimmte neuere Forschungsarbeiten – etwa zu Architekturverständnis von Code-Agents – noch vorläufig und nicht so belastbar wie etablierte Benchmarks. Die robusteste Strategie ist deshalb nicht, auf eine perfekte allgemeine Wahrheit zu warten, sondern **dein eigenes kleines Eval-Set in deinem eigenen Repo** aufzubauen und Architekturänderungen daran zu messen. citeturn27view0turn36view0turn34view0

Unterm Strich ist die beste Antwort auf deine Ausgangsfrage deshalb sehr klar: **Ja, reduziere auf wenige Agenten. Ja, verlagere den Großteil wiederverwendbarer Intelligenz in Skills. Aber baue das System als progressive-disclosure Harness, nicht als „Lade alles und delegiere immer“-Orchestrator.** Wenn du maximale Tokeneffizienz und Wartbarkeit willst, dann ist die Prioritätenliste: **kleiner Dauerkontext, selektive Repo-Navigation, on-demand Skills, Artefakte statt langer Zwischenzusammenfassungen, harte Regeln als Lints/Tests/Hooks, und Evals/Tracing als Pflichtbestandteil.** citeturn24view0turn28view0turn31view0turn27view2