# Spezifikation und Implementierungsplan: KI-unterstützte WCAG-2.2-AA-Barrierefreiheitstests für Backstage/React

**Zielsystem:** Backstage + React + TypeScript, Entwicklung in Visual Studio Code mit GitHub Copilot/Copilot Chat  
**Zielstandard:** WCAG 2.2, primär Level A und AA  
**Datum:** 2026-07-01  
**Ausgabe:** Implementierungsfähiger Plan für Copilot-Agenten, CI-Workflow und Reporting

---

## 1. Ergebnis in einem Satz

Baue **keinen reinen KI-Prüfer**, sondern eine **deterministische Accessibility-Test-Pipeline** aus ESLint, axe-core, Playwright, jest-axe, optional Storybook/Lighthouse/Pa11y und einem eigenen Report-Generator; Copilot/KI wird als **Orchestrator, Implementierungshelfer, Triage-Helfer und Remediation-Assistent** eingesetzt, aber nicht als alleinige Quelle für WCAG-Konformität.

---

## 2. Brutal ehrliche Einordnung

### FACT

- WCAG 2.2 besteht aus testbaren Erfolgskriterien, aber nicht alle Erfolgskriterien sind vollständig automatisierbar.
- Automatisierte Tools wie axe-core, Playwright-Axe, jest-axe, Lighthouse oder Pa11y finden viele typische technische Fehler, aber sie können **keine vollständige WCAG-Konformität garantieren**.
- KI kann Code, DOM-Snippets, Screenshots und Findings analysieren und Fix-Vorschläge machen. Sie darf aber nicht als alleiniger Prüfer für semantische, kontextuelle, sprachliche, kognitive oder assistive-technology-nahe Kriterien verwendet werden.

### ASSUMPTION

Ich nehme für diesen Plan an:

- Du nutzt ein Backstage-Monorepo oder eine Backstage-App mit mehreren Plugins.
- Du nutzt TypeScript, React und wahrscheinlich Yarn/NPM sowie GitHub Actions oder eine vergleichbare CI.
- Du willst mindestens WCAG 2.2 AA als internes Qualitätsziel.
- Die Anwendung ist eine Web-App, vermutlich mit authentifizierten Routen und dynamischen Zuständen.

Wenn eine dieser Annahmen falsch ist, muss Copilot die betroffenen Stellen im Plan anpassen, aber die Architektur bleibt im Kern gleich.

### OPINION / Empfehlung

Für deinen Stack ist der beste Ansatz:

1. **Static Layer:** ESLint + `eslint-plugin-jsx-a11y` für JSX/TSX-Probleme.
2. **Component Layer:** `jest-axe` mit Backstage-Test-Utilities für isolierte Komponenten und Plugin-Extensions.
3. **E2E Layer:** Playwright + `@axe-core/playwright` für gerenderte Seiten, Routen und UI-Zustände.
4. **Scenario Layer:** explizite Tastatur-, Fokus-, Formular-, Dialog-, Navigation- und Fehlerzustandstests.
5. **Report Layer:** eigener Generator, der alle Findings in ein WCAG-2.2-AA-Checklist-Format normalisiert.
6. **AI Layer:** Copilot-Agenten, die Findings triagieren, Fixes vorschlagen, Tests ergänzen und Reports erklären.
7. **Manual Review Queue:** Kriterien, die nicht automatisch sicher prüfbar sind, werden nicht als bestanden markiert, sondern als `needs_manual_review` geführt.

---

## 3. Was KI hier leisten kann und was nicht

| Aufgabe | KI geeignet? | Verlässlichkeit | Empfehlung |
|---|---:|---:|---|
| Test-Infrastruktur implementieren | Ja | Hoch, wenn Tests laufen | Copilot mit klaren Prompts nutzen |
| WCAG-Kriterien auf Tool-Ausgaben mappen | Ja | Mittel bis hoch | Mapping deterministisch speichern, nicht jedes Mal neu generieren lassen |
| Findings gruppieren und priorisieren | Ja | Mittel | KI darf helfen, aber Report muss Rohdaten enthalten |
| Fix-Vorschläge für React-Komponenten | Ja | Mittel bis hoch | Nur akzeptieren, wenn Tests danach grün sind |
| Semantische Bewertung von Alt-Texten | Teilweise | Niedrig bis mittel | KI als Review-Hilfe, Mensch entscheidet |
| Keyboard-Fokus-Logik prüfen | Teilweise | Mittel | Playwright-Szenarien + manuelle Stichproben |
| Screenreader-Kompatibilität garantieren | Nein | Niedrig | Manuelle Tests mit NVDA/VoiceOver/JAWS o. ä. nötig |
| Vollständige WCAG-2.2-AA-Konformität zertifizieren | Nein | Nicht ausreichend | Externe/manuelle Evaluation nötig, falls rechtlich relevant |

**Wichtige Regel:**  
Der Report darf am Ende nicht sagen: “WCAG 2.2 AA erfüllt”, nur weil axe keine Fehler findet. Korrekte Formulierung:

> “Automatisierte Prüfungen haben für die geprüften Routen/Zustände keine blockierenden automatisiert erkennbaren Findings gefunden. Manuelle Prüfpunkte bleiben offen oder wurden separat dokumentiert.”

---

## 4. Zielarchitektur

```text
Backstage / React App
│
├─ Static Checks
│  ├─ TypeScript
│  ├─ ESLint
│  └─ eslint-plugin-jsx-a11y
│
├─ Component Accessibility Tests
│  ├─ React Testing Library
│  ├─ Backstage renderInTestApp / createExtensionTester
│  └─ jest-axe
│
├─ E2E Accessibility Tests
│  ├─ Playwright
│  ├─ @axe-core/playwright
│  ├─ Route inventory
│  ├─ UI-state scenarios
│  └─ Keyboard/focus tests
│
├─ Optional Scanners
│  ├─ Storybook addon-a11y
│  ├─ Lighthouse CI
│  ├─ Pa11y CI
│  └─ optional MCP scanner for local ad-hoc scans
│
├─ Report Generator
│  ├─ axe JSON results
│  ├─ ESLint JSON results
│  ├─ Jest results
│  ├─ Playwright metadata
│  ├─ manual-review checklist
│  ├─ waiver/baseline handling
│  └─ Markdown/JSON/HTML/SARIF output
│
└─ Copilot / AI Workflow
   ├─ a11y-architect agent
   ├─ a11y-implementer agent
   ├─ a11y-reviewer agent
   ├─ repository instructions
   └─ repeatable prompts
```

---

## 5. Tooling-Entscheidung

### 5.1 Empfohlene Kern-Tools

| Tool | Zweck | Warum für Backstage/React sinnvoll? | Einschränkung |
|---|---|---|---|
| `eslint-plugin-jsx-a11y` | Statische TSX/JSX-Regeln | Findet viele frühe Fehler ohne Browser | Sieht nicht den final gerenderten DOM |
| `jest-axe` | Komponenten-/Unit-Accessibility | Gut für React-Komponenten, Plugin-Pages, Backstage-Test-Harness | JSDOM bildet Browser/Contrast/Fokus nicht vollständig ab |
| `@axe-core/playwright` | Browserbasierte E2E-Scans | Beste Basis für real gerendertes Backstage UI | Findet nur automatisch erkennbare Issues |
| Playwright Keyboard Tests | Fokus, Tab-Reihenfolge, Dialoge, Tastaturbedienung | Kritisch für Backstage-Plugins mit komplexen UIs | Muss pro UI-Zustand explizit geschrieben werden |
| eigener Report-Generator | Konsolidierter WCAG-Report | Du willst eine Checkliste pro WCAG-Kategorie | Muss gepflegt werden |
| GitHub Actions / CI | Regressionsschutz | Automatisierbar auf PRs | Initiale Legacy-Fehler können noisy sein |

### 5.2 Optional sinnvolle Tools

| Tool | Empfehlung | Kommentar |
|---|---|---|
| Storybook `@storybook/addon-a11y` | Nutzen, falls Storybook vorhanden ist | Gut für Komponentenbibliothek und visuelle Reviews |
| Lighthouse CI | Optional ergänzen | Backstage selbst schlägt Lighthouse-CI-Checks für Plugins vor; aber Lighthouse ist kein vollständiger WCAG-Prüfer |
| Pa11y / Pa11y CI | Optional für URL-Listen | Gut für einfache Route-Scans, schwächer bei komplexen SPA-Zuständen |
| Accessibility Insights for Web | Manuelle Reviews | Gut für geführte manuelle Checks |
| axe DevTools / axe Linter | Optional lokal | Gut für Entwickler-Feedback in VS Code/Browser |
| MCP Accessibility Scanner | Optional experimentell | Nur als lokales Hilfstool, nicht als CI-Quelle der Wahrheit |
| `ally.js` | Nur als Utility | Nicht als Testframework; kann bei Fokus-/Focusable-Utilities helfen, macht die App aber nicht automatisch accessible |
| React Aria | Für eigene interaktive Komponenten | Besonders nützlich bei komplexen Widgets statt selbst ARIA/Fokuslogik zu bauen |

### 5.3 Nicht empfohlen als alleinige Lösung

| Ansatz | Warum nicht ausreichend? |
|---|---|
| “Copilot, prüfe meine App auf WCAG” | Codeanalyse allein sieht nicht alle DOM-, Fokus-, Theme-, Viewport- und Runtime-Zustände |
| Nur Lighthouse Score | Score ist grob und deckt WCAG nicht vollständig ab |
| Nur axe auf Homepage | Backstage ist plugin- und routebasiert; relevante Zustände bleiben ungeprüft |
| Nur Snapshot/Screenshot durch KI | KI kann visuelle Hinweise geben, aber keine verlässliche Konformitätsprüfung liefern |
| Alles mit ARIA fixen | Falsch gesetztes ARIA verschlechtert Accessibility oft; native HTML-Elemente sind meist besser |

---

## 6. Zielstruktur im Repository

Copilot soll folgende Struktur anlegen oder an vorhandene Konventionen anpassen:

```text
.github/
├─ copilot-instructions.md
├─ agents/
│  ├─ a11y-architect.agent.md
│  ├─ a11y-implementer.agent.md
│  └─ a11y-reviewer.agent.md
└─ workflows/
   └─ a11y.yml

a11y/
├─ README.md
├─ routes.json
├─ scenarios.json
├─ wcag22-aa-checklist.json
├─ manual-review.md
├─ waivers.yml
├─ baseline.json
└─ report-template.md

scripts/
└─ a11y/
   ├─ generate-a11y-report.ts
   ├─ normalize-axe-results.ts
   ├─ normalize-eslint-results.ts
   ├─ wcag-tag-parser.ts
   ├─ baseline.ts
   └─ markdown-report.ts

tests/
└─ a11y/
   ├─ axePlaywright.ts
   ├─ formatAxeViolations.ts
   ├─ keyboardAssertions.ts
   └─ routeScenarios.ts

a11y-results/
├─ axe/
├─ eslint/
├─ jest/
├─ playwright/
├─ screenshots/
├─ a11y-report.json
├─ a11y-report.md
└─ a11y-report.html
```

Falls dein Backstage-Repo bereits eine andere Struktur verwendet, soll Copilot die Dateien in die vorhandenen Test- und CI-Konventionen integrieren statt blind neue Ordner zu erzwingen.

---

## 7. Zielzustand des Reports

Der Report soll am Ende mindestens enthalten:

1. **Metadaten**
   - App/Repo
   - Commit SHA
   - Branch
   - CI-Run-ID
   - Testdatum
   - Zielstandard: WCAG 2.2 A/AA
   - getestete Browser
   - getestete Viewports
   - getestete Themes
   - getestete Routen und UI-Zustände

2. **Executive Summary**
   - Anzahl Findings nach Severity
   - Anzahl Findings nach WCAG-Prinzip
   - Anzahl Findings nach Quelle
   - Anzahl blockierende Findings
   - Anzahl manuelle Review-Punkte
   - Regression gegenüber Baseline

3. **WCAG-2.2-AA-Checkliste**
   - Prinzip
   - Guideline
   - Success Criterion
   - Level
   - Status
   - Automatisierungsgrad
   - Evidence
   - Findings
   - Owner
   - Bemerkungen

4. **Findings-Liste**
   - ID
   - Quelle
   - Regel
   - WCAG-SC
   - Impact/Severity
   - Route
   - UI-Zustand
   - Selector
   - DOM-Snippet
   - Beschreibung
   - Hilfe-Link
   - Fix-Vorschlag
   - Status
   - Owner

5. **Manual Review Queue**
   - Kriterien, die nicht zuverlässig automatisch geprüft wurden
   - genaue manuelle Prüfanweisung
   - erwartete Evidence
   - Status

6. **Waivers/Baseline**
   - akzeptierte temporäre Abweichungen
   - Begründung
   - Ablaufdatum
   - Verantwortlicher

---

## 8. Report-Datenmodell

### 8.1 TypeScript Interfaces

```ts
export type A11ySource =
  | 'axe-playwright'
  | 'jest-axe'
  | 'eslint-jsx-a11y'
  | 'storybook-a11y'
  | 'lighthouse'
  | 'pa11y'
  | 'manual'
  | 'ai-review';

export type A11yStatus =
  | 'pass'
  | 'fail'
  | 'needs_manual_review'
  | 'not_applicable'
  | 'not_covered'
  | 'waived';

export type AutomationCoverage =
  | 'automated'
  | 'semi_automated'
  | 'manual'
  | 'not_applicable'
  | 'unknown';

export type A11ySeverity =
  | 'critical'
  | 'serious'
  | 'moderate'
  | 'minor'
  | 'needs_review';

export interface A11yTestContext {
  route?: string;
  path: string;
  routeId?: string;
  routeName?: string;
  scenarioId: string;
  scenarioName: string;
  viewport: 'desktop' | 'tablet' | 'mobile' | string;
  theme?: 'light' | 'dark' | string;
  browser?: string;
  authState?: string;
}

export interface A11yFinding {
  id: string;
  source: A11ySource;
  ruleId: string;
  wcag: string[];
  wcagLevel?: 'A' | 'AA' | 'AAA' | 'best-practice' | 'unknown';
  principle?: 'perceivable' | 'operable' | 'understandable' | 'robust';
  guideline?: string;
  severity: A11ySeverity;
  status: A11yStatus;
  confidence: 'high' | 'medium' | 'low';
  context: A11yTestContext;
  selector?: string;
  htmlSnippet?: string;
  description: string;
  help?: string;
  helpUrl?: string;
  impactForUsers?: string;
  remediation?: string;
  evidenceFiles: string[];
  screenshotFiles?: string[];
  owner?: string;
  createdAt: string;
  updatedAt?: string;
}

export interface WcagChecklistItem {
  sc: string;
  title: string;
  level: 'A' | 'AA' | 'AAA';
  principle: 'perceivable' | 'operable' | 'understandable' | 'robust';
  guideline: string;
  status: A11yStatus;
  automationCoverage: AutomationCoverage;
  evidence: string[];
  findings: string[];
  manualReviewRequired: boolean;
  notes?: string;
}

export interface A11yReport {
  metadata: {
    generatedAt: string;
    repository?: string;
    branch?: string;
    commitSha?: string;
    ciRunUrl?: string;
    targetStandard: 'WCAG 2.2';
    targetLevel: 'AA';
    browsers: string[];
    viewports: string[];
    themes: string[];
  };
  summary: {
    totalFindings: number;
    blockingFindings: number;
    bySeverity: Record<A11ySeverity, number>;
    bySource: Record<A11ySource, number>;
    byPrinciple: Record<string, number>;
    manualReviewItems: number;
    newFindingsAgainstBaseline: number;
  };
  checklist: WcagChecklistItem[];
  findings: A11yFinding[];
  waivers: A11yWaiver[];
}

export interface A11yWaiver {
  id: string;
  findingFingerprint: string;
  ruleId: string;
  route?: string;
  selector?: string;
  reason: string;
  owner: string;
  approvedBy: string;
  expiresAt: string;
}
```

---

## 9. WCAG-2.2-AA-Checkliste für den Report

Statuswerte:

- `pass`: geprüft und keine Findings.
- `fail`: Finding vorhanden.
- `needs_manual_review`: kann nicht zuverlässig automatisch entschieden werden.
- `not_applicable`: nachweislich nicht relevant, z. B. keine Videos.
- `not_covered`: im aktuellen Testumfang nicht geprüft.
- `waived`: temporär akzeptiert mit dokumentierter Begründung und Ablaufdatum.

### 9.1 Perceivable

| SC | Level | Kriterium | Automatisierung | Empfehlung |
|---|---:|---|---|---|
| 1.1.1 | A | Non-text Content | semi_automated | axe findet fehlende Alt-Attribute; Sinnhaftigkeit von Alt-Text manuell/KI-gestützt prüfen |
| 1.2.1 | A | Audio-only and Video-only | manual | Nur relevant bei Audio/Video |
| 1.2.2 | A | Captions (Prerecorded) | manual | Video-Inhalte erfassen, Captions manuell prüfen |
| 1.2.3 | A | Audio Description or Media Alternative | manual | Meist manuell |
| 1.2.4 | AA | Captions (Live) | manual/not_applicable | Falls Live-Medien vorhanden |
| 1.2.5 | AA | Audio Description (Prerecorded) | manual | Falls Video vorhanden |
| 1.3.1 | A | Info and Relationships | semi_automated | Headings, Labels, Tabellen, Landmarkmarks automatisiert + manuell prüfen |
| 1.3.2 | A | Meaningful Sequence | manual | DOM-/Lesereihenfolge manuell und mit Screenreader prüfen |
| 1.3.3 | A | Sensory Characteristics | manual | Texte dürfen nicht nur auf Farbe/Form/Position verweisen |
| 1.3.4 | AA | Orientation | semi_automated | Playwright-Viewports/Orientation ergänzen |
| 1.3.5 | AA | Identify Input Purpose | semi_automated | `autocomplete` und Formularzwecke prüfen |
| 1.4.1 | A | Use of Color | manual/semi_automated | Nicht nur farbige Statusindikatoren verwenden |
| 1.4.2 | A | Audio Control | manual/not_applicable | Nur relevant bei automatisch startendem Audio |
| 1.4.3 | AA | Contrast Minimum | automated/semi_automated | axe/Playwright im echten Browser; Theme-Varianten testen |
| 1.4.4 | AA | Resize Text | semi_automated | Zoom/Textgröße mit Playwright testen; Layout manuell bewerten |
| 1.4.5 | AA | Images of Text | manual | Meist visuelle/manuelle Prüfung |
| 1.4.10 | AA | Reflow | semi_automated | Mobile/320px/Zoom-Szenarien; horizontales Scrollen prüfen |
| 1.4.11 | AA | Non-text Contrast | semi_automated/manual | Fokus, Icons, Controls, Graphen; automatisierte Tools sind begrenzt |
| 1.4.12 | AA | Text Spacing | semi_automated | CSS-Override-Test + manuelle Sichtprüfung |
| 1.4.13 | AA | Content on Hover or Focus | manual/semi_automated | Tooltips, Popovers, Menüs mit Playwright-Szenarien testen |

### 9.2 Operable

| SC | Level | Kriterium | Automatisierung | Empfehlung |
|---|---:|---|---|---|
| 2.1.1 | A | Keyboard | semi_automated/manual | Kritische Flows mit Playwright Keyboard testen |
| 2.1.2 | A | No Keyboard Trap | semi_automated/manual | Dialoge, Menüs, Popovers, Tabellenfilter prüfen |
| 2.1.4 | A | Character Key Shortcuts | manual | Nur falls eigene Shortcuts vorhanden |
| 2.2.1 | A | Timing Adjustable | manual | Session Timeout, Auto-Refresh, Token-Expiry prüfen |
| 2.2.2 | A | Pause, Stop, Hide | manual/semi_automated | Animationen, Auto-Updates, Loader, Marquees |
| 2.3.1 | A | Three Flashes or Below Threshold | manual | Visuelle Prüfung bei Animationen |
| 2.4.1 | A | Bypass Blocks | semi_automated | Skip-Link/Landmarks prüfen |
| 2.4.2 | A | Page Titled | automated | Browser title pro Route prüfen |
| 2.4.3 | A | Focus Order | manual/semi_automated | Tab-Reihenfolge in kritischen Flows prüfen |
| 2.4.4 | A | Link Purpose in Context | semi_automated/manual | Linktexte prüfen; KI kann unklare Texte flaggen |
| 2.4.5 | AA | Multiple Ways | manual | Navigation, Suche, Breadcrumbs, Catalog-Zugänge prüfen |
| 2.4.6 | AA | Headings and Labels | semi_automated | axe/ESLint + semantische Review |
| 2.4.7 | AA | Focus Visible | semi_automated/manual | Screenshots/Playwright + manuelle Bewertung |
| 2.4.11 | AA | Focus Not Obscured Minimum | semi_automated/manual | Neu in WCAG 2.2; Sticky Header, Drawers, Cookie-Banner, Modals prüfen |
| 2.5.1 | A | Pointer Gestures | manual | Drag, Swipe, komplexe Gesten brauchen Alternativen |
| 2.5.2 | A | Pointer Cancellation | manual | Pointer-Down darf nicht destruktiv auslösen |
| 2.5.3 | A | Label in Name | semi_automated/manual | Sichtbarer Labeltext muss im Accessible Name enthalten sein |
| 2.5.4 | A | Motion Actuation | manual/not_applicable | Nur bei Bewegungssensorik relevant |
| 2.5.7 | AA | Dragging Movements | manual/semi_automated | Neu in WCAG 2.2; Drag&Drop braucht Alternative |
| 2.5.8 | AA | Target Size Minimum | semi_automated/manual | Neu in WCAG 2.2; `target-size`-Regel prüfen, Ausnahmen manuell bewerten |

### 9.3 Understandable

| SC | Level | Kriterium | Automatisierung | Empfehlung |
|---|---:|---|---|---|
| 3.1.1 | A | Language of Page | automated | `html lang` prüfen |
| 3.1.2 | AA | Language of Parts | semi_automated/manual | Gemischte Sprache in Inhalten prüfen |
| 3.2.1 | A | On Focus | manual/semi_automated | Fokus darf keine unerwartete Kontextänderung auslösen |
| 3.2.2 | A | On Input | manual/semi_automated | Formulare/Selects dürfen nicht unerwartet navigieren |
| 3.2.3 | AA | Consistent Navigation | manual | Navigation über Routen hinweg konsistent halten |
| 3.2.4 | AA | Consistent Identification | manual/ai-review | Gleiche Icons/Actions gleich benennen |
| 3.2.6 | A | Consistent Help | manual/ai-review | Neu in WCAG 2.2; Help/Support-Mechanismen konsistent platzieren |
| 3.3.1 | A | Error Identification | semi_automated/manual | Validierungsfehler sichtbar und programmatisch erfassbar machen |
| 3.3.2 | A | Labels or Instructions | semi_automated/manual | Formulare mit Labels, Instructions, Required-State |
| 3.3.3 | AA | Error Suggestion | manual/ai-review | Fehler müssen hilfreiche Korrekturhinweise geben |
| 3.3.4 | AA | Error Prevention Legal/Financial/Data | manual/not_applicable | Relevanz prüfen; bei destruktiven Aktionen Confirm/Review/Undo |
| 3.3.7 | A | Redundant Entry | manual/ai-review | Neu in WCAG 2.2; bereits eingegebene Daten nicht unnötig erneut verlangen |
| 3.3.8 | AA | Accessible Authentication Minimum | manual/ai-review | Neu in WCAG 2.2; Login/SSO/MFA auf kognitive Tests prüfen |

### 9.4 Robust

| SC | Level | Kriterium | Automatisierung | Empfehlung |
|---|---:|---|---|---|
| 4.1.2 | A | Name, Role, Value | automated/semi_automated | axe findet viele ARIA-/Role-Probleme; Custom Widgets manuell prüfen |
| 4.1.3 | AA | Status Messages | semi_automated/manual | Toasts, Alerts, Loading, Save-State, Errors mit `role=status/alert` oder `aria-live` prüfen |

### 9.5 Obsolete Kriterium

| SC | Status | Empfehlung |
|---|---|---|
| 4.1.1 Parsing | obsolete in WCAG 2.2 | Nicht als neues WCAG-2.2-Gate verwenden. Falls dein Unternehmen noch WCAG 2.1/EN-301-549-Mappings fordert, gesondert behandeln. |

---

## 10. Route- und Szenario-Inventar

### 10.1 `a11y/routes.json`

Copilot soll eine Datei mit kritischen Routen erzeugen. Beispiel:

```json
{
  "baseUrlEnv": "PLAYWRIGHT_URL",
  "defaultBaseUrl": "http://localhost:3000",
  "routes": [
    {
      "id": "home",
      "name": "Home",
      "path": "/",
      "requiresAuth": false,
      "criticality": "high",
      "owner": "platform"
    },
    {
      "id": "catalog-list",
      "name": "Software Catalog List",
      "path": "/catalog",
      "requiresAuth": true,
      "criticality": "high",
      "owner": "catalog"
    },
    {
      "id": "catalog-entity",
      "name": "Catalog Entity Page",
      "path": "/catalog/default/component/example-service",
      "requiresAuth": true,
      "criticality": "high",
      "owner": "catalog"
    },
    {
      "id": "search",
      "name": "Search",
      "path": "/search",
      "requiresAuth": true,
      "criticality": "medium",
      "owner": "platform"
    },
    {
      "id": "create-template",
      "name": "Scaffolder Template Form",
      "path": "/create/templates/default/template/example-template",
      "requiresAuth": true,
      "criticality": "high",
      "owner": "scaffolder"
    },
    {
      "id": "techdocs",
      "name": "TechDocs Page",
      "path": "/docs/default/component/example-service",
      "requiresAuth": true,
      "criticality": "medium",
      "owner": "techdocs"
    }
  ]
}
```

### 10.2 `a11y/scenarios.json`

```json
{
  "viewports": [
    { "id": "desktop", "width": 1440, "height": 900 },
    { "id": "tablet", "width": 768, "height": 1024 },
    { "id": "mobile", "width": 390, "height": 844 }
  ],
  "themes": ["light", "dark"],
  "scenarios": [
    {
      "id": "default",
      "name": "Default loaded state",
      "type": "axe-scan",
      "appliesTo": ["*"]
    },
    {
      "id": "keyboard-navigation",
      "name": "Keyboard tab order smoke test",
      "type": "keyboard",
      "appliesTo": ["home", "catalog-list", "create-template"]
    },
    {
      "id": "form-validation-errors",
      "name": "Form validation error state",
      "type": "interaction-plus-axe",
      "appliesTo": ["create-template"]
    },
    {
      "id": "dialog-open",
      "name": "Dialog/modal open state",
      "type": "interaction-plus-axe",
      "appliesTo": ["*"]
    },
    {
      "id": "search-open",
      "name": "Search interaction state",
      "type": "interaction-plus-axe",
      "appliesTo": ["search"]
    }
  ]
}
```

---

## 11. Dependencies

Copilot soll zuerst den vorhandenen Package Manager erkennen und dann entsprechend installieren.

### 11.1 Yarn

```bash
yarn add -D @axe-core/playwright axe-core jest-axe @types/jest-axe eslint-plugin-jsx-a11y tsx
```

Optional:

```bash
yarn add -D pa11y pa11y-ci axe-html-reporter
```

Falls Storybook vorhanden ist:

```bash
npx storybook add @storybook/addon-a11y
```

### 11.2 NPM

```bash
npm install --save-dev @axe-core/playwright axe-core jest-axe @types/jest-axe eslint-plugin-jsx-a11y tsx
```

Optional:

```bash
npm install --save-dev pa11y pa11y-ci axe-html-reporter
```

---

## 12. Package Scripts

Copilot soll die Skripte an vorhandene Backstage-Konventionen anpassen.

```json
{
  "scripts": {
    "lint:a11y": "eslint \"packages/**/*.{ts,tsx}\" \"plugins/**/*.{ts,tsx}\" --format json --output-file a11y-results/eslint/eslint-a11y.json",
    "test:a11y:unit": "backstage-cli repo test -- --runInBand --testMatch='**/*.a11y.test.tsx'",
    "test:a11y:e2e": "playwright test --grep @a11y",
    "a11y:report": "tsx scripts/a11y/generate-a11y-report.ts",
    "a11y": "yarn lint:a11y && yarn test:a11y:unit && yarn test:a11y:e2e && yarn a11y:report"
  }
}
```

Falls dein Repo keine `packages/` oder `plugins/`-Struktur hat, soll Copilot die Globs anpassen.

---

## 13. ESLint-Konfiguration

### 13.1 Legacy `.eslintrc`

```json
{
  "extends": [
    "plugin:jsx-a11y/recommended"
  ],
  "plugins": [
    "jsx-a11y"
  ],
  "settings": {
    "jsx-a11y": {
      "components": {
        "Button": "button",
        "Link": "a",
        "IconButton": "button"
      }
    }
  },
  "rules": {
    "jsx-a11y/alt-text": "error",
    "jsx-a11y/anchor-is-valid": "error",
    "jsx-a11y/aria-props": "error",
    "jsx-a11y/aria-proptypes": "error",
    "jsx-a11y/aria-role": "error",
    "jsx-a11y/aria-unsupported-elements": "error",
    "jsx-a11y/click-events-have-key-events": "warn",
    "jsx-a11y/heading-has-content": "error",
    "jsx-a11y/html-has-lang": "error",
    "jsx-a11y/iframe-has-title": "error",
    "jsx-a11y/interactive-supports-focus": "error",
    "jsx-a11y/label-has-associated-control": "error",
    "jsx-a11y/media-has-caption": "warn",
    "jsx-a11y/no-autofocus": "warn",
    "jsx-a11y/no-noninteractive-element-interactions": "warn",
    "jsx-a11y/no-static-element-interactions": "warn",
    "jsx-a11y/role-has-required-aria-props": "error",
    "jsx-a11y/role-supports-aria-props": "error"
  }
}
```

### 13.2 Flat Config Beispiel

```ts
import jsxA11y from 'eslint-plugin-jsx-a11y';

export default [
  {
    files: ['**/*.{js,jsx,ts,tsx}'],
    plugins: {
      'jsx-a11y': jsxA11y,
    },
    languageOptions: {
      parserOptions: {
        ecmaFeatures: { jsx: true },
      },
    },
    rules: {
      ...jsxA11y.configs.recommended.rules,
      'jsx-a11y/alt-text': 'error',
      'jsx-a11y/anchor-is-valid': 'error',
      'jsx-a11y/click-events-have-key-events': 'warn',
      'jsx-a11y/interactive-supports-focus': 'error',
      'jsx-a11y/label-has-associated-control': 'error',
    },
  },
];
```

---

## 14. Component Tests mit `jest-axe`

### 14.1 Setup-Datei

`tests/a11y/jestAxeSetup.ts`:

```ts
import { toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);
```

In deiner Jest-Konfiguration:

```ts
setupFilesAfterEnv: [
  '<rootDir>/tests/a11y/jestAxeSetup.ts'
]
```

### 14.2 Beispiel für eine Backstage-Komponente

```tsx
import React from 'react';
import { axe } from 'jest-axe';
import { screen } from '@testing-library/react';
import { renderInTestApp } from '@backstage/test-utils';
import { MyPluginPage } from './MyPluginPage';

it('has no automatically detectable accessibility violations', async () => {
  const { container } = await renderInTestApp(<MyPluginPage />);

  await expect(screen.findByRole('heading', { name: /my plugin/i }))
    .resolves.toBeInTheDocument();

  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### 14.3 Beispiel für Frontend Extensions

```tsx
import React from 'react';
import { axe } from 'jest-axe';
import { screen } from '@testing-library/react';
import {
  createExtensionTester,
  renderInTestApp,
} from '@backstage/frontend-test-utils';
import { indexPageExtension } from './plugin';

it('renders the extension without automatically detectable accessibility violations', async () => {
  const { container } = await renderInTestApp(
    createExtensionTester(indexPageExtension).reactElement(),
  );

  await expect(screen.findByText(/index page/i)).resolves.toBeInTheDocument();

  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### 14.4 Regeln für Component Tests

- Jede neue Page-Komponente bekommt mindestens einen `*.a11y.test.tsx`.
- Jede eigene komplexe Komponente bekommt einen A11y-Test, wenn sie interaktiv ist.
- Component Tests ersetzen keine Playwright-Tests.
- Color Contrast nicht primär mit JSDOM testen; dafür echte Browser-Scans nutzen.

---

## 15. Playwright + axe-core

### 15.1 Gemeinsamer Scanner

`tests/a11y/axePlaywright.ts`:

```ts
import AxeBuilder from '@axe-core/playwright';
import type { Page, TestInfo } from '@playwright/test';
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';

export interface ScanContext {
  routeId: string;
  routeName: string;
  path: string;
  scenarioId: string;
  scenarioName: string;
  viewport: string;
  theme?: string;
}

const axeTags = [
  'wcag2a',
  'wcag2aa',
  'wcag21a',
  'wcag21aa',
  'wcag22aa',
];

function safeFileName(input: string): string {
  return input.replace(/[^a-z0-9._-]+/gi, '-').toLowerCase();
}

function fingerprint(context: ScanContext): string {
  return crypto
    .createHash('sha256')
    .update(JSON.stringify(context))
    .digest('hex')
    .slice(0, 12);
}

export async function scanA11y(
  page: Page,
  testInfo: TestInfo,
  context: ScanContext,
) {
  await fs.mkdir('a11y-results/axe', { recursive: true });

  const builder = new AxeBuilder({ page }).withTags(axeTags);

  // WCAG 2.2 nuance:
  // Some axe-core WCAG 2.2 rules may be disabled by default depending on axe version.
  // Keep this configuration only if verified against the installed axe-core version.
  // Do not cargo-cult enable/disable rules without a test.
  builder.configure({
    rules: [
      { id: 'target-size', enabled: true },
    ],
  });

  const results = await builder.analyze();

  const resultFile = path.join(
    'a11y-results/axe',
    `${safeFileName(context.routeId)}-${safeFileName(context.scenarioId)}-${fingerprint(context)}.json`,
  );

  await fs.writeFile(
    resultFile,
    JSON.stringify(
      {
        context,
        testTitle: testInfo.title,
        projectName: testInfo.project.name,
        results,
      },
      null,
      2,
    ),
    'utf8',
  );

  return { results, resultFile };
}

export function getBlockingViolations(results: { violations: Array<{ impact?: string }> }) {
  return results.violations.filter(v =>
    v.impact === 'critical' || v.impact === 'serious',
  );
}
```

### 15.2 Formatierte Fehlermeldung

`tests/a11y/formatAxeViolations.ts`:

```ts
export function formatAxeViolations(violations: any[]): string {
  return violations
    .map(v => {
      const nodes = v.nodes
        ?.slice(0, 5)
        .map((n: any) => {
          return [
            `    selector: ${n.target?.join(', ')}`,
            `    html: ${n.html}`,
            `    failureSummary: ${n.failureSummary}`,
          ].join('\n');
        })
        .join('\n');

      return [
        `rule: ${v.id}`,
        `impact: ${v.impact}`,
        `description: ${v.description}`,
        `help: ${v.help}`,
        `helpUrl: ${v.helpUrl}`,
        `nodes:\n${nodes}`,
      ].join('\n');
    })
    .join('\n\n---\n\n');
}
```

### 15.3 Route-basierter E2E-Test

`tests/a11y/backstage-routes.a11y.spec.ts`:

```ts
import { test, expect } from '@playwright/test';
import fs from 'node:fs';
import { scanA11y, getBlockingViolations } from './axePlaywright';
import { formatAxeViolations } from './formatAxeViolations';

interface RouteConfig {
  id: string;
  name: string;
  path: string;
  requiresAuth?: boolean;
  criticality: 'high' | 'medium' | 'low';
  owner: string;
}

const routesConfig = JSON.parse(
  fs.readFileSync('a11y/routes.json', 'utf8'),
) as { routes: RouteConfig[] };

test.describe('@a11y Backstage route scans', () => {
  for (const route of routesConfig.routes) {
    test(`${route.id}: default state has no blocking automated a11y violations`, async ({ page }, testInfo) => {
      await page.goto(route.path);

      // Replace this with route-specific readiness checks where possible.
      await page.waitForLoadState('networkidle');

      const { results } = await scanA11y(page, testInfo, {
        routeId: route.id,
        routeName: route.name,
        path: route.path,
        scenarioId: 'default',
        scenarioName: 'Default loaded state',
        viewport: testInfo.project.name,
      });

      const blocking = getBlockingViolations(results);

      expect(
        blocking,
        formatAxeViolations(blocking),
      ).toEqual([]);
    });
  }
});
```

### 15.4 Bessere Readiness Checks statt `networkidle`

Copilot soll `networkidle` später durch konkrete Checks ersetzen:

```ts
await expect(page.getByRole('heading', { name: /software catalog/i }))
  .toBeVisible();

await expect(page.getByTestId('loading-progress'))
  .toHaveCount(0);
```

`networkidle` ist bequem, aber bei SPAs nicht immer semantisch genug.

---

## 16. Keyboard- und Fokus-Tests

### 16.1 Utility

`tests/a11y/keyboardAssertions.ts`:

```ts
import { expect, type Page, type Locator } from '@playwright/test';

export async function expectTabFocusSequence(
  page: Page,
  expected: Locator[],
) {
  for (const locator of expected) {
    await page.keyboard.press('Tab');
    await expect(locator).toBeFocused();
  }
}

export async function expectNoKeyboardTrap(page: Page, maxTabs = 50) {
  const seen = new Set<string>();

  for (let i = 0; i < maxTabs; i += 1) {
    await page.keyboard.press('Tab');
    const activeElementSignature = await page.evaluate(() => {
      const element = document.activeElement;
      if (!element) return 'none';
      return [
        element.tagName,
        element.id,
        element.getAttribute('role'),
        element.getAttribute('aria-label'),
        element.textContent?.slice(0, 40),
      ].join('|');
    });

    if (seen.has(activeElementSignature)) {
      return;
    }

    seen.add(activeElementSignature);
  }

  throw new Error(`Possible keyboard trap: focus did not cycle within ${maxTabs} Tab presses`);
}
```

### 16.2 Beispiel: Dialog

```ts
test('@a11y modal traps focus and exposes accessible name', async ({ page }) => {
  await page.goto('/my-plugin');

  await page.getByRole('button', { name: /create/i }).click();

  const dialog = page.getByRole('dialog', { name: /create/i });
  await expect(dialog).toBeVisible();

  await expect(page.getByRole('button', { name: /cancel/i })).toBeFocused();

  await page.keyboard.press('Escape');
  await expect(dialog).toBeHidden();

  await expect(page.getByRole('button', { name: /create/i })).toBeFocused();
});
```

### 16.3 Beispiel: Formularfehler

```ts
test('@a11y form validation errors are accessible', async ({ page }, testInfo) => {
  await page.goto('/create/templates/default/template/example-template');

  await page.getByRole('button', { name: /review/i }).click();

  const error = page.getByText(/required/i).first();
  await expect(error).toBeVisible();

  const firstInvalidField = page.locator('[aria-invalid="true"]').first();
  await expect(firstInvalidField).toBeVisible();

  const { results } = await scanA11y(page, testInfo, {
    routeId: 'create-template',
    routeName: 'Scaffolder Template Form',
    path: '/create/templates/default/template/example-template',
    scenarioId: 'form-validation-errors',
    scenarioName: 'Form validation error state',
    viewport: testInfo.project.name,
  });

  const blocking = getBlockingViolations(results);
  expect(blocking, formatAxeViolations(blocking)).toEqual([]);
});
```

---

## 17. Playwright-Konfiguration

Wenn bereits eine Backstage-Playwright-Konfiguration existiert, soll Copilot diese erweitern.

```ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 30_000,
  expect: {
    timeout: 5_000,
  },
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  reporter: [
    ['list'],
    ['html', { outputFolder: 'a11y-results/playwright-html', open: 'never' }],
    ['json', { outputFile: 'a11y-results/playwright/playwright-results.json' }],
  ],
  use: {
    baseURL: process.env.PLAYWRIGHT_URL ?? 'http://localhost:3000',
    screenshot: 'only-on-failure',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium-desktop',
      use: { ...devices['Desktop Chrome'], viewport: { width: 1440, height: 900 } },
    },
    {
      name: 'chromium-mobile',
      use: { ...devices['Pixel 5'] },
    },
  ],
});
```

Backstage-spezifisch kann stattdessen `generateProjects()` aus `@backstage/e2e-test-utils/playwright` genutzt werden, wenn dein Repo das bereits tut.

---

## 18. Report-Generator

### 18.1 WCAG-Tag-Parser

axe-Regeln liefern Tags wie `wcag111`, `wcag143`, `wcag2411`, `wcag258`.

`scripts/a11y/wcag-tag-parser.ts`:

```ts
export function axeWcagTagToSuccessCriterion(tag: string): string | undefined {
  if (!tag.startsWith('wcag')) return undefined;

  const digits = tag.slice('wcag'.length);
  if (!/^\d{3,4}$/.test(digits)) return undefined;

  if (digits.length === 3) {
    return `${digits[0]}.${digits[1]}.${digits[2]}`;
  }

  return `${digits[0]}.${digits[1]}.${digits.slice(2)}`;
}

export function extractSuccessCriteria(tags: string[]): string[] {
  return Array.from(
    new Set(
      tags
        .map(axeWcagTagToSuccessCriterion)
        .filter((value): value is string => Boolean(value)),
    ),
  ).sort();
}
```

### 18.2 Axe Normalizer

`scripts/a11y/normalize-axe-results.ts`:

```ts
import crypto from 'node:crypto';
import { extractSuccessCriteria } from './wcag-tag-parser';
import type { A11yFinding } from './types';

function hash(input: unknown): string {
  return crypto
    .createHash('sha256')
    .update(JSON.stringify(input))
    .digest('hex')
    .slice(0, 16);
}

export function normalizeAxeResultFile(filePath: string, fileContent: any): A11yFinding[] {
  const context = fileContent.context;
  const violations = fileContent.results?.violations ?? [];
  const incomplete = fileContent.results?.incomplete ?? [];

  const violationFindings: A11yFinding[] = violations.flatMap((violation: any) => {
    const wcag = extractSuccessCriteria(violation.tags ?? []);

    return (violation.nodes ?? []).map((node: any) => {
      const fingerprintPayload = {
        source: 'axe-playwright',
        ruleId: violation.id,
        route: context.path,
        scenarioId: context.scenarioId,
        selector: node.target,
        html: node.html,
      };

      return {
        id: `axe-${hash(fingerprintPayload)}`,
        source: 'axe-playwright',
        ruleId: violation.id,
        wcag,
        wcagLevel: inferWcagLevelFromTags(violation.tags ?? []),
        severity: violation.impact ?? 'needs_review',
        status: 'fail',
        confidence: 'high',
        context,
        selector: Array.isArray(node.target) ? node.target.join(', ') : String(node.target ?? ''),
        htmlSnippet: node.html,
        description: violation.description,
        help: violation.help,
        helpUrl: violation.helpUrl,
        impactForUsers: node.failureSummary,
        remediation: undefined,
        evidenceFiles: [filePath],
        createdAt: new Date().toISOString(),
      } satisfies A11yFinding;
    });
  });

  const incompleteFindings: A11yFinding[] = incomplete.flatMap((item: any) => {
    const wcag = extractSuccessCriteria(item.tags ?? []);

    return (item.nodes ?? []).map((node: any) => ({
      id: `axe-incomplete-${hash({ ruleId: item.id, context, selector: node.target, html: node.html })}`,
      source: 'axe-playwright',
      ruleId: item.id,
      wcag,
      wcagLevel: inferWcagLevelFromTags(item.tags ?? []),
      severity: 'needs_review',
      status: 'needs_manual_review',
      confidence: 'medium',
      context,
      selector: Array.isArray(node.target) ? node.target.join(', ') : String(node.target ?? ''),
      htmlSnippet: node.html,
      description: item.description,
      help: item.help,
      helpUrl: item.helpUrl,
      impactForUsers: node.failureSummary,
      remediation: undefined,
      evidenceFiles: [filePath],
      createdAt: new Date().toISOString(),
    }));
  });

  return [...violationFindings, ...incompleteFindings];
}

function inferWcagLevelFromTags(tags: string[]): 'A' | 'AA' | 'AAA' | 'best-practice' | 'unknown' {
  if (tags.includes('wcag2aaa') || tags.includes('wcag21aaa') || tags.includes('wcag22aaa')) return 'AAA';
  if (tags.includes('wcag2aa') || tags.includes('wcag21aa') || tags.includes('wcag22aa')) return 'AA';
  if (tags.includes('wcag2a') || tags.includes('wcag21a') || tags.includes('wcag22a')) return 'A';
  if (tags.includes('best-practice')) return 'best-practice';
  return 'unknown';
}
```

### 18.3 Report-Generator Hauptdatei

`scripts/a11y/generate-a11y-report.ts`:

```ts
import fs from 'node:fs/promises';
import path from 'node:path';
import { normalizeAxeResultFile } from './normalize-axe-results';
import { renderMarkdownReport } from './markdown-report';
import type { A11yFinding, A11yReport, WcagChecklistItem } from './types';

async function readJsonFile<T>(filePath: string): Promise<T> {
  const content = await fs.readFile(filePath, 'utf8');
  return JSON.parse(content) as T;
}

async function listJsonFiles(dir: string): Promise<string[]> {
  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    return entries
      .filter(e => e.isFile() && e.name.endsWith('.json'))
      .map(e => path.join(dir, e.name));
  } catch {
    return [];
  }
}

async function main() {
  await fs.mkdir('a11y-results', { recursive: true });

  const checklist = await readJsonFile<WcagChecklistItem[]>('a11y/wcag22-aa-checklist.json');

  const axeFiles = await listJsonFiles('a11y-results/axe');
  const axeFindingsNested = await Promise.all(
    axeFiles.map(async file => normalizeAxeResultFile(file, await readJsonFile(file))),
  );

  const findings: A11yFinding[] = axeFindingsNested.flat();

  const checklistWithStatus = applyFindingsToChecklist(checklist, findings);

  const report: A11yReport = {
    metadata: {
      generatedAt: new Date().toISOString(),
      repository: process.env.GITHUB_REPOSITORY,
      branch: process.env.GITHUB_REF_NAME,
      commitSha: process.env.GITHUB_SHA,
      ciRunUrl: process.env.GITHUB_SERVER_URL && process.env.GITHUB_REPOSITORY && process.env.GITHUB_RUN_ID
        ? `${process.env.GITHUB_SERVER_URL}/${process.env.GITHUB_REPOSITORY}/actions/runs/${process.env.GITHUB_RUN_ID}`
        : undefined,
      targetStandard: 'WCAG 2.2',
      targetLevel: 'AA',
      browsers: ['chromium'],
      viewports: ['desktop', 'mobile'],
      themes: ['light', 'dark'],
    },
    summary: summarize(findings, checklistWithStatus),
    checklist: checklistWithStatus,
    findings,
    waivers: [],
  };

  await fs.writeFile('a11y-results/a11y-report.json', JSON.stringify(report, null, 2), 'utf8');
  await fs.writeFile('a11y-results/a11y-report.md', renderMarkdownReport(report), 'utf8');
}

function applyFindingsToChecklist(
  checklist: WcagChecklistItem[],
  findings: A11yFinding[],
): WcagChecklistItem[] {
  return checklist.map(item => {
    const relatedFindings = findings.filter(f => f.wcag.includes(item.sc));

    if (relatedFindings.length > 0) {
      return {
        ...item,
        status: relatedFindings.some(f => f.status === 'fail') ? 'fail' : 'needs_manual_review',
        findings: relatedFindings.map(f => f.id),
        evidence: Array.from(new Set(relatedFindings.flatMap(f => f.evidenceFiles))),
      };
    }

    if (item.automationCoverage === 'manual' || item.automationCoverage === 'semi_automated') {
      return {
        ...item,
        status: item.status === 'not_applicable' ? 'not_applicable' : 'needs_manual_review',
      };
    }

    return {
      ...item,
      status: item.status === 'not_applicable' ? 'not_applicable' : 'pass',
    };
  });
}

function summarize(findings: A11yFinding[], checklist: WcagChecklistItem[]) {
  const bySeverity = countBy(findings, f => f.severity);
  const bySource = countBy(findings, f => f.source);
  const byPrinciple = countBy(findings, f => f.principle ?? 'unknown');

  return {
    totalFindings: findings.length,
    blockingFindings: findings.filter(f => f.severity === 'critical' || f.severity === 'serious').length,
    bySeverity,
    bySource,
    byPrinciple,
    manualReviewItems: checklist.filter(i => i.status === 'needs_manual_review').length,
    newFindingsAgainstBaseline: 0,
  };
}

function countBy<T extends string>(items: A11yFinding[], selector: (item: A11yFinding) => T): Record<T, number> {
  return items.reduce((acc, item) => {
    const key = selector(item);
    acc[key] = (acc[key] ?? 0) + 1;
    return acc;
  }, {} as Record<T, number>);
}

main().catch(error => {
  console.error(error);
  process.exit(1);
});
```

### 18.4 Markdown Rendering

`scripts/a11y/markdown-report.ts`:

```ts
import type { A11yReport } from './types';

export function renderMarkdownReport(report: A11yReport): string {
  const lines: string[] = [];

  lines.push('# Accessibility Report');
  lines.push('');
  lines.push(`Generated: ${report.metadata.generatedAt}`);
  lines.push(`Target: ${report.metadata.targetStandard} ${report.metadata.targetLevel}`);
  lines.push(`Commit: ${report.metadata.commitSha ?? 'n/a'}`);
  lines.push('');

  lines.push('## Summary');
  lines.push('');
  lines.push(`- Total findings: ${report.summary.totalFindings}`);
  lines.push(`- Blocking findings: ${report.summary.blockingFindings}`);
  lines.push(`- Manual review items: ${report.summary.manualReviewItems}`);
  lines.push('');

  lines.push('## WCAG 2.2 AA Checklist');
  lines.push('');
  lines.push('| SC | Level | Title | Status | Automation | Findings | Evidence |');
  lines.push('|---|---:|---|---|---|---:|---|');

  for (const item of report.checklist) {
    lines.push(
      `| ${item.sc} | ${item.level} | ${escapeMd(item.title)} | ${item.status} | ${item.automationCoverage} | ${item.findings.length} | ${item.evidence.join('<br>')} |`,
    );
  }

  lines.push('');
  lines.push('## Findings');
  lines.push('');

  if (report.findings.length === 0) {
    lines.push('No findings in the automated result files. Manual review may still be required.');
  } else {
    for (const finding of report.findings) {
      lines.push(`### ${finding.id}`);
      lines.push('');
      lines.push(`- Source: ${finding.source}`);
      lines.push(`- Rule: ${finding.ruleId}`);
      lines.push(`- WCAG: ${finding.wcag.join(', ') || 'n/a'}`);
      lines.push(`- Severity: ${finding.severity}`);
      lines.push(`- Status: ${finding.status}`);
      lines.push(`- Route: ${finding.context.route ?? finding.context.path}`);
      lines.push(`- Scenario: ${finding.context.scenarioName}`);
      lines.push(`- Selector: \`${finding.selector ?? 'n/a'}\``);
      lines.push(`- Help: ${finding.helpUrl ?? finding.help ?? 'n/a'}`);
      lines.push('');
      lines.push('```html');
      lines.push(finding.htmlSnippet ?? '');
      lines.push('```');
      lines.push('');
    }
  }

  lines.push('## Manual Review Queue');
  lines.push('');

  const manualItems = report.checklist.filter(i => i.status === 'needs_manual_review');
  if (manualItems.length === 0) {
    lines.push('No manual-review items generated by the current checklist logic. Verify scope before treating this as complete.');
  } else {
    for (const item of manualItems) {
      lines.push(`- ${item.sc} ${item.title} (${item.level}): ${item.notes ?? 'Manual validation required.'}`);
    }
  }

  lines.push('');
  lines.push('## Disclaimer');
  lines.push('');
  lines.push('This report summarizes automated and semi-automated accessibility checks for the configured routes and states. It is not a legal certification of WCAG conformance.');

  return lines.join('\n');
}

function escapeMd(input: string): string {
  return input.replace(/\|/g, '\\|');
}
```

---

## 19. `wcag22-aa-checklist.json` Skeleton

Copilot soll die vollständige Liste aus Abschnitt 9 als JSON anlegen. Beispiel-Auszug:

```json
[
  {
    "sc": "1.1.1",
    "title": "Non-text Content",
    "level": "A",
    "principle": "perceivable",
    "guideline": "1.1 Text Alternatives",
    "status": "not_covered",
    "automationCoverage": "semi_automated",
    "evidence": [],
    "findings": [],
    "manualReviewRequired": true,
    "notes": "Automated tools can detect missing alt attributes, but meaningful alternative text requires human review."
  },
  {
    "sc": "1.4.3",
    "title": "Contrast (Minimum)",
    "level": "AA",
    "principle": "perceivable",
    "guideline": "1.4 Distinguishable",
    "status": "not_covered",
    "automationCoverage": "automated",
    "evidence": [],
    "findings": [],
    "manualReviewRequired": false,
    "notes": "Run in real browser with all supported themes."
  },
  {
    "sc": "2.4.11",
    "title": "Focus Not Obscured (Minimum)",
    "level": "AA",
    "principle": "operable",
    "guideline": "2.4 Navigable",
    "status": "not_covered",
    "automationCoverage": "semi_automated",
    "evidence": [],
    "findings": [],
    "manualReviewRequired": true,
    "notes": "Check sticky headers, drawers, modals and overlays."
  }
]
```

---

## 20. Waivers und Baseline

### 20.1 Warum Baseline?

Wenn du Accessibility in einer bestehenden Backstage-App nachrüstest, wird der erste Lauf wahrscheinlich Findings erzeugen. Wenn du sofort alle Findings blockierst, wird die Pipeline politisch und praktisch scheitern.

Besser:

1. Initialen Zustand als `a11y/baseline.json` speichern.
2. CI blockiert neue `critical`/`serious` Findings.
3. Bestehende Findings werden als Backlog sichtbar.
4. Jede temporäre Ausnahme braucht Owner und Ablaufdatum.

### 20.2 `a11y/waivers.yml`

```yaml
waivers:
  - id: waiver-2026-001
    findingFingerprint: axe-1234567890abcdef
    ruleId: color-contrast
    route: /catalog
    selector: '.legacy-owner-chip'
    wcag:
      - '1.4.3'
    reason: 'Legacy MUI chip color from old theme. Fixed in BUI migration epic.'
    owner: '@team-platform'
    approvedBy: '@accessibility-owner'
    createdAt: '2026-07-01'
    expiresAt: '2026-10-01'
```

### 20.3 Gate-Policy

Empfohlenes CI-Verhalten:

| Bedingung | CI-Verhalten |
|---|---|
| Neues `critical` Finding | Fail |
| Neues `serious` Finding | Fail |
| Neues `moderate` Finding | Warn oder Fail nach Rollout-Phase |
| Neues `minor` Finding | Warn |
| Abgelaufener Waiver | Fail |
| Report kann nicht erzeugt werden | Fail |
| WCAG-Checkliste fehlt | Fail |
| Neue interaktive Komponente ohne A11y-Test | Warn oder Fail nach Rollout-Phase |

---

## 21. GitHub Actions Workflow

`.github/workflows/a11y.yml`:

```yaml
name: Accessibility

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pull-requests: write

jobs:
  a11y:
    name: Accessibility checks
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version-file: .nvmrc
          cache: yarn

      - name: Install dependencies
        run: yarn install --immutable

      - name: Install Playwright browsers
        run: yarn playwright install --with-deps chromium

      - name: Prepare result folders
        run: mkdir -p a11y-results/axe a11y-results/eslint a11y-results/jest a11y-results/playwright

      - name: Run static accessibility lint
        run: yarn lint:a11y
        continue-on-error: true

      - name: Run component accessibility tests
        run: yarn test:a11y:unit
        continue-on-error: true

      - name: Start Backstage app
        run: |
          yarn start &
          npx wait-on http://localhost:3000
        env:
          CI: true

      - name: Run Playwright accessibility tests
        run: yarn test:a11y:e2e
        env:
          PLAYWRIGHT_URL: http://localhost:3000

      - name: Generate accessibility report
        if: always()
        run: yarn a11y:report

      - name: Upload accessibility artifacts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: accessibility-report
          path: |
            a11y-results/**
            playwright-report/**

      - name: Add report summary
        if: always()
        run: |
          echo "## Accessibility report" >> $GITHUB_STEP_SUMMARY
          if [ -f a11y-results/a11y-report.md ]; then
            cat a11y-results/a11y-report.md >> $GITHUB_STEP_SUMMARY
          else
            echo "No report generated." >> $GITHUB_STEP_SUMMARY
          fi
```

**Hinweis:** `continue-on-error: true` bei Lint/Unit ist nur in der Einführungsphase sinnvoll, damit der Report trotzdem erzeugt wird. Sobald die Baseline steht, sollte Copilot daraus harte Gates ableiten.

---

## 22. Copilot Custom Instructions

`.github/copilot-instructions.md` Ergänzung:

```md
# Accessibility Engineering Rules

Target accessibility standard: WCAG 2.2 Level AA unless a task explicitly states otherwise.

Rules:

1. Do not claim WCAG compliance from automated tests alone.
2. Prefer native semantic HTML over custom ARIA.
3. For Backstage UI, prefer existing Backstage UI/BUI or MUI components before creating custom interactive controls.
4. For custom complex interactive controls, prefer React Aria or another proven headless accessibility foundation.
5. Every new page-level React component must have at least one accessibility test.
6. Every new custom interactive component must have keyboard and focus behavior covered by tests.
7. Do not disable axe or jsx-a11y rules unless there is a documented waiver with owner, reason, and expiry date.
8. For every accessibility finding, record route, scenario, selector, WCAG success criterion, evidence file, severity, and remediation suggestion.
9. Treat `needs_manual_review` as a valid and honest status. Do not convert it to `pass` without evidence.
10. When fixing accessibility issues, add or update tests that would fail without the fix.
11. Do not replace visible labels with aria-label unless there is a strong reason. Keep visible label and accessible name aligned.
12. Do not use `div` or `span` as buttons/links when native `button` or `a` works.
13. For forms, always provide labels, validation messages, `aria-invalid` when invalid, and programmatic association with error/help text.
14. For dialogs, test accessible name, focus trap, Escape behavior, and focus return.
15. For loading, save, error, and success states, ensure status messages are programmatically announced where needed.
```

---

## 23. Copilot Agenten

### 23.1 `a11y-architect.agent.md`

`.github/agents/a11y-architect.agent.md`:

```md
---
name: a11y-architect
description: Plan WCAG 2.2 AA accessibility automation for this Backstage/React repository.
tools: ['search', 'codebase']
agents: []
handoffs:
  - label: Implement accessibility pipeline
    agent: a11y-implementer
    prompt: Implement the accessibility automation plan. Start with the smallest safe vertical slice and do not skip tests.
    send: false
---

You are an accessibility automation architect for a Backstage + React + TypeScript repository.

Your job:

1. Inspect the repository structure before proposing changes.
2. Identify package manager, test framework, Playwright config, Backstage plugin layout, CI provider, Storybook presence, and current ESLint config.
3. Define the minimal viable accessibility pipeline for WCAG 2.2 AA.
4. Separate automated, semi-automated, and manual review checks.
5. Produce an implementation plan with exact files to create or modify.
6. Do not claim that automated tools prove WCAG conformance.
7. Prefer deterministic tests and report generation over AI-only judgement.

Output format:

- Verified facts from the repository
- Assumptions
- Proposed file changes
- Risks
- Step-by-step implementation sequence
- Acceptance criteria

Stop condition:

If required repository facts are missing, inspect the repository. Do not invent paths.
```

### 23.2 `a11y-implementer.agent.md`

`.github/agents/a11y-implementer.agent.md`:

```md
---
name: a11y-implementer
description: Implement WCAG 2.2 AA accessibility automation, reports, and CI for Backstage/React.
tools: ['search', 'codebase', 'terminal', 'problems', 'changes']
agents: []
handoffs:
  - label: Review accessibility implementation
    agent: a11y-reviewer
    prompt: Review the accessibility implementation for correctness, maintainability, false claims, and missing coverage.
    send: false
---

You implement accessibility automation for a Backstage + React + TypeScript repository.

Implementation rules:

1. Work in small commits/patches.
2. Prefer existing project conventions over introducing new ones.
3. Add dependencies only when needed.
4. Add or update tests for every new helper.
5. Generate deterministic reports from raw tool outputs.
6. Do not hide failures by disabling rules.
7. If a rule must be suppressed, create or update `a11y/waivers.yml` with reason, owner, approver, and expiry.
8. Every report status must be evidence-based.
9. Preserve raw tool outputs as artifacts.
10. Ensure `yarn a11y` or equivalent command runs locally.

Required deliverables:

- a11y route inventory
- WCAG 2.2 AA checklist JSON
- Playwright axe scans
- at least one route scan
- at least one keyboard/focus scenario
- jest-axe setup
- report generator
- CI workflow or documented integration point
- README explaining local usage

After each phase, run the relevant command and report exact failures.
```

### 23.3 `a11y-reviewer.agent.md`

`.github/agents/a11y-reviewer.agent.md`:

```md
---
name: a11y-reviewer
description: Review WCAG 2.2 AA accessibility automation changes for reliability and false confidence.
tools: ['search', 'codebase', 'problems', 'changes']
agents: []
---

You review accessibility automation changes in a Backstage + React + TypeScript repository.

Review checklist:

1. Does the implementation avoid claiming full WCAG conformance from automated tests alone?
2. Are automated, semi-automated, manual, not-applicable, and not-covered statuses separated?
3. Are raw results preserved?
4. Are axe, eslint, jest, and Playwright results normalized consistently?
5. Does every finding include route, scenario, selector, WCAG SC, severity, evidence, and remediation field?
6. Are WCAG 2.2 AA additions covered explicitly?
7. Are keyboard/focus tests included for interactive states?
8. Are there unjustified disabled rules?
9. Are waivers time-bounded and owned?
10. Does CI fail on new critical/serious findings after baseline?
11. Does the implementation fit Backstage conventions?
12. Are tests deterministic and not dependent on flaky network state?

Output:

- Blockers
- Non-blocking issues
- Missing coverage
- Suggested patch list
- Verdict: approve / request changes
```

**Hinweis:** Tool-Namen in VS Code können je nach Copilot-Version/Extensions variieren. Wenn VS Code einen Tool-Namen in der Agent-Datei nicht akzeptiert, soll Copilot ihn entfernen oder durch den verfügbaren äquivalenten Tool-Namen ersetzen. Wichtig ist Least Privilege: Der Reviewer braucht z. B. normalerweise keinen Terminal-Zugriff.

---

## 24. Prompts für Copilot

### Prompt 1: Repository-Audit

```text
Use the a11y-architect agent.

I want to implement WCAG 2.2 AA accessibility automation for this Backstage + React + TypeScript repository.

First inspect the repository. Do not edit files yet.

Find and report:
1. package manager and lockfile
2. Backstage app/package/plugin structure
3. existing test commands
4. existing Playwright config
5. existing Jest config
6. existing ESLint config
7. existing Storybook setup, if any
8. existing CI workflows
9. important app routes and plugin routes
10. authentication/test-data constraints for E2E tests

Then produce a concrete implementation plan with exact files to create or modify.

Do not claim that automated testing guarantees WCAG compliance.
Separate automated, semi-automated, and manual review scope.
```

### Prompt 2: Minimal Vertical Slice

```text
Use the a11y-implementer agent.

Implement the first minimal vertical slice of the accessibility pipeline.

Scope:
1. Add required dev dependencies for @axe-core/playwright, axe-core, jest-axe, @types/jest-axe, eslint-plugin-jsx-a11y and tsx using the repository's package manager.
2. Add a11y/routes.json with one or two existing critical routes from the repository.
3. Add a11y/wcag22-aa-checklist.json with the complete WCAG 2.2 A/AA checklist and correct automationCoverage values.
4. Add tests/a11y/axePlaywright.ts and tests/a11y/formatAxeViolations.ts.
5. Add one Playwright @a11y route scan.
6. Add a basic report generator that reads axe JSON results and writes a11y-results/a11y-report.md and a11y-results/a11y-report.json.
7. Add package scripts for lint:a11y, test:a11y:e2e, a11y:report and a11y.

Do not add broad rule disables.
Do not mark manual criteria as pass.
Run the new commands and fix implementation errors.
```

### Prompt 3: Component Test Layer

```text
Use the a11y-implementer agent.

Add component-level accessibility testing.

Scope:
1. Detect existing Jest/React Testing Library/Backstage test utilities.
2. Add jest-axe setup in the existing Jest setupFilesAfterEnv mechanism.
3. Add one *.a11y.test.tsx for a real page-level Backstage plugin component.
4. Use renderInTestApp or createExtensionTester when appropriate.
5. Ensure the test waits for meaningful rendered content before running axe.
6. Update the report generator to include jest-axe result evidence if feasible, or document that jest failures are handled by Jest output in CI.

Run the unit accessibility test command and fix failures caused by the setup.
```

### Prompt 4: Keyboard and Dynamic States

```text
Use the a11y-implementer agent.

Add accessibility scenarios for dynamic UI states.

Scope:
1. Add tests/a11y/keyboardAssertions.ts.
2. Add at least one keyboard navigation test for a critical route.
3. Add at least one dialog/menu/popover/form-validation accessibility scenario, using a real component in this repo.
4. After creating the dynamic state, run scanA11y again so the report captures the state.
5. Update a11y/scenarios.json to describe the implemented scenarios.
6. Ensure tests are stable and use role-based locators where possible.

Do not rely only on screenshots.
Do not use implementation-private selectors unless there is no accessible locator available; if you must, explain why.
```

### Prompt 5: CI und Baseline

```text
Use the a11y-implementer agent.

Add CI integration for the accessibility pipeline.

Scope:
1. Add or update .github/workflows/a11y.yml.
2. Ensure raw outputs are uploaded as artifacts.
3. Ensure a markdown summary is added to the CI step summary.
4. Add baseline support so existing findings can be tracked without hiding new regressions.
5. Fail the workflow for new critical or serious findings not present in baseline.
6. Fail the workflow for expired waivers.
7. Keep moderate/minor findings as warnings initially unless the repository already enforces stricter gates.

Run or statically validate the workflow where possible.
```

### Prompt 6: Review

```text
Use the a11y-reviewer agent.

Review the accessibility automation implementation.

Check for:
1. false claims of WCAG compliance
2. missing WCAG 2.2 A/AA criteria
3. criteria incorrectly marked as automated
4. missing manual review queue
5. unjustified disabled axe/jsx-a11y rules
6. missing route/state coverage
7. flaky Playwright waits
8. missing raw artifacts
9. missing owner/expiry on waivers
10. Backstage convention violations

Return blockers first, then non-blocking improvements, then a concrete patch list.
```

---

## 25. Rollout-Plan

### Phase 0: Scope festlegen

**Ziel:** Nicht “die ganze App irgendwie prüfen”, sondern klare erste Coverage.

Tasks:

- Zielstandard bestätigen: WCAG 2.2 AA.
- Kritische Routen definieren.
- Kritische User Flows definieren.
- Unterstützte Browser/Viewports/Themes definieren.
- Auth/Testdaten-Konzept klären.

Deliverables:

- `a11y/routes.json`
- `a11y/scenarios.json`
- `a11y/README.md`

### Phase 1: Minimaler automatischer Scan

Tasks:

- Dependencies installieren.
- Playwright-Axe-Helper bauen.
- Eine bis drei Routen scannen.
- JSON-Rohdaten speichern.
- Report als Markdown erzeugen.

Definition of Done:

- `yarn test:a11y:e2e` läuft lokal.
- `a11y-results/axe/*.json` wird erzeugt.
- `a11y-results/a11y-report.md` wird erzeugt.

### Phase 2: WCAG-Checkliste

Tasks:

- Vollständige WCAG-2.2-A/AA-Liste als JSON anlegen.
- axe Tags auf SCs mappen.
- Unprüfbare SCs als `needs_manual_review` führen.
- Report nach Prinzipien gruppieren.

Definition of Done:

- Jede relevante SC erscheint im Report.
- Kein manuelles Kriterium wird ohne Evidence als `pass` markiert.

### Phase 3: Component Tests

Tasks:

- `jest-axe` integrieren.
- Page-Komponenten testen.
- Backstage-Test-Utilities verwenden.
- Neue Komponentenregeln dokumentieren.

Definition of Done:

- Mindestens ein realer Backstage-Plugin-Component-Test läuft.
- Neue Komponenten können das Muster kopieren.

### Phase 4: Dynamische Zustände

Tasks:

- Tastatur-Tests ergänzen.
- Dialoge, Menüs, Formulare, Fehlerzustände prüfen.
- Nach Interaktion erneut axe scannen.

Definition of Done:

- Mindestens ein Dialog/Menu/Form-State wird getestet.
- Fokusverhalten ist testbar dokumentiert.

### Phase 5: CI und Baseline

Tasks:

- GitHub Actions Workflow hinzufügen.
- Artifacts hochladen.
- Report in Step Summary schreiben.
- Baseline und Waiver-Mechanismus einführen.

Definition of Done:

- PRs bekommen einen Report.
- Neue critical/serious Findings schlagen fehl.
- Legacy Findings bleiben sichtbar.

### Phase 6: Erweiterung

Tasks:

- Alle kritischen Backstage-Routen abdecken.
- Mobile/Tablet erweitern.
- Dark Theme prüfen.
- Storybook addon-a11y ergänzen, falls vorhanden.
- Lighthouse/Pa11y optional ergänzen.
- Manuelle Screenreader-Reviews in Release-Prozess aufnehmen.

---

## 26. Backstage-spezifische Prüfpunkte

### 26.1 Typische Backstage-Routen

Priorisiere:

1. Startseite / App Shell
2. Catalog List
3. Catalog Entity Page
4. Search
5. Scaffolder/Create Template Form
6. TechDocs
7. User Settings
8. Custom Plugin Pages
9. Permission/Error/Empty States
10. Admin-/Config-Seiten, falls vorhanden

### 26.2 Typische Backstage-Probleme

| Bereich | Risiko | Test |
|---|---|---|
| Catalog Tables | Tabellenstruktur, Sortierung, Filter, Fokus | axe + Keyboard + role assertions |
| Scaffolder Forms | Labels, Errors, Required, Instructions | jest-axe + Playwright validation state |
| TechDocs | Heading-Hierarchie, Linktexte, Codeblocks | route scan + semantic review |
| Search | Combobox, Results, Live Updates | keyboard + status messages |
| Sidebar/Nav | Skip-Link, Landmarks, Focus Order | keyboard + axe |
| Entity Cards | Clickable Cards, Name/Role/Value | role-based locators + axe |
| Modals/Drawers | Focus Trap, Escape, Focus Return | Playwright keyboard test |
| Theme Customization | Contrast Regression | axe in light/dark theme |
| Plugin-owned Components | Mixed MUI/BUI/custom UI | component a11y tests |

### 26.3 Komponentenregeln

- Verwende `button` für Aktionen.
- Verwende `a`/Backstage Link-Komponenten für Navigation.
- Verwende sichtbare Labels für Formularfelder.
- Vermeide Click-Handler auf `div`/`span`.
- Nutze ARIA nur, wenn native Semantik nicht reicht.
- Bei eigenen komplexen Widgets: React Aria oder bewährte Headless-Komponente bevorzugen.
- Fokuszustände dürfen nicht durch Theme/CSS entfernt werden.
- Toasts und asynchrone Statusänderungen brauchen passende Live-Regionen, wenn Nutzer informiert werden müssen.

---

## 27. AI-gestützte Triage

Copilot/KI darf nach der Report-Erzeugung folgende Aufgaben übernehmen:

### 27.1 Finding Clustering

Prompt:

```text
Analyze a11y-results/a11y-report.json.
Group findings by root cause.
Do not hide individual findings.
For each group, provide:
- affected WCAG criteria
- affected routes
- likely component/source file
- remediation strategy
- risk if ignored
- suggested test to prevent regression
Mark confidence as high/medium/low.
```

### 27.2 Fix-Vorschläge

Prompt:

```text
For finding <ID>, inspect the affected component and propose a minimal fix.
Rules:
1. Prefer semantic HTML over ARIA.
2. Keep visible label and accessible name aligned.
3. Add or update a test that fails before the fix.
4. Do not change unrelated styling.
5. After patching, run the smallest relevant a11y test.
```

### 27.3 Manual Review Vorbereitung

Prompt:

```text
Read the Manual Review Queue in a11y-results/a11y-report.md.
For each item, create a concise manual test procedure.
Include:
- route
- UI state
- keyboard steps
- expected result
- evidence to capture
- whether screenreader testing is recommended
Do not mark any item as pass without human evidence.
```

---

## 28. Manuelle Review-Vorlage

`a11y/manual-review.md`:

```md
# Manual Accessibility Review

Target: WCAG 2.2 AA  
Date:  
Reviewer:  
Build/Commit:  
Browser:  
Assistive Technology:  

## Scope

- Routes:
- Viewports:
- Themes:
- Exclusions:

## Keyboard Review

| Route | Scenario | Pass/Fail | Notes | Evidence |
|---|---|---|---|---|

## Screenreader Smoke Review

| Route | Screenreader | Scenario | Pass/Fail | Notes | Evidence |
|---|---|---|---|---|---|

## WCAG Manual Criteria

| SC | Title | Result | Notes | Evidence |
|---|---|---|---|---|
| 1.1.1 | Non-text Content |  |  |  |
| 1.3.2 | Meaningful Sequence |  |  |  |
| 1.3.3 | Sensory Characteristics |  |  |  |
| 1.4.1 | Use of Color |  |  |  |
| 2.1.1 | Keyboard |  |  |  |
| 2.4.3 | Focus Order |  |  |  |
| 2.4.7 | Focus Visible |  |  |  |
| 2.4.11 | Focus Not Obscured |  |  |  |
| 3.2.3 | Consistent Navigation |  |  |  |
| 3.3.3 | Error Suggestion |  |  |  |
| 4.1.3 | Status Messages |  |  |  |

## Findings

| ID | SC | Severity | Description | Owner | Fix Target |
|---|---|---|---|---|---|
```

---

## 29. Optional: Storybook Integration

Nur falls Storybook vorhanden ist:

```bash
npx storybook add @storybook/addon-a11y
```

Empfohlene Regeln:

- Jede gemeinsame UI-Komponente bekommt eine Story.
- Storybook-A11y-Panel wird lokal genutzt.
- Für kritische Komponenten kann Storybook-Test-Runner später in CI ergänzt werden.
- Storybook Findings werden optional in den Report normalisiert.

Nicht als Ersatz für App-/Route-Tests verwenden, weil Backstage-Plugins stark vom App-Kontext abhängen.

---

## 30. Optional: Lighthouse CI

Backstage empfiehlt selbst Lighthouse-CI-artige Checks für Plugin-Routen. Sinnvoll als zusätzlicher Smoke-Test:

```bash
yarn add -D @lhci/cli
```

`.lighthouserc.js` Beispiel:

```js
module.exports = {
  ci: {
    collect: {
      url: [
        'http://localhost:3000/',
        'http://localhost:3000/catalog',
        'http://localhost:3000/search',
      ],
      numberOfRuns: 1,
    },
    assert: {
      assertions: {
        'categories:accessibility': ['warn', { minScore: 0.95 }],
      },
    },
    upload: {
      target: 'filesystem',
      outputDir: 'a11y-results/lighthouse',
    },
  },
};
```

Wichtig: Lighthouse-Score ist kein WCAG-2.2-AA-Report. Er ist ein zusätzlicher Signalgeber.

---

## 31. Optional: Pa11y CI

Für einfache URL-Listen:

```json
{
  "defaults": {
    "standard": "WCAG2AA",
    "timeout": 30000,
    "chromeLaunchConfig": {
      "args": ["--no-sandbox"]
    }
  },
  "urls": [
    "http://localhost:3000/",
    "http://localhost:3000/catalog",
    "http://localhost:3000/search"
  ]
}
```

Empfehlung: Pa11y höchstens ergänzend verwenden. Für komplexe Backstage-SPA-Zustände ist Playwright präziser.

---

## 32. Optional: MCP Accessibility Scanner in VS Code

Es gibt Community-Projekte, die Accessibility-Scans als MCP-Tool für Copilot/VS Code anbieten. Das kann nützlich sein für lokale Ad-hoc-Prüfungen, z. B. “scanne aktuelle URL und fasse Findings zusammen”.

Empfehlung:

- Nur optional einsetzen.
- Nicht als CI-Gate verwenden.
- Nicht als alleinige Quelle für den Report verwenden.
- Wenn verwendet, Rohdaten in das gleiche `A11yFinding`-Schema normalisieren.

---

## 33. Definition of Done

Die Implementierung gilt als fertig, wenn:

- `yarn a11y` oder äquivalenter Befehl lokal läuft.
- Playwright-Axe mindestens die wichtigsten Routen scannt.
- Mindestens ein dynamischer UI-Zustand nach Interaktion gescannt wird.
- Mindestens ein Keyboard-/Fokus-Test existiert.
- Mindestens ein `jest-axe` Component Test existiert.
- `a11y-results/a11y-report.md` und `a11y-results/a11y-report.json` erzeugt werden.
- Jede WCAG-2.2-A/AA-SC im Report erscheint.
- Unautomatisierbare Kriterien als `needs_manual_review` statt `pass` markiert werden.
- CI lädt Rohdaten und Report als Artefakte hoch.
- Neue critical/serious Findings blockieren PRs nach Baseline.
- Waivers haben Owner, Begründung und Ablaufdatum.
- Copilot-Agenten und Custom Instructions sind im Repo vorhanden.

---

## 34. Akzeptanzkriterien für Copilot-Implementierung

Copilot darf die Aufgabe erst als abgeschlossen betrachten, wenn folgende Checks erfüllt sind:

```text
[ ] Repository-Struktur wurde verifiziert, nicht geraten.
[ ] Package Manager wurde verifiziert.
[ ] Testframeworks wurden verifiziert.
[ ] WCAG 2.2 A/AA Checklist existiert vollständig.
[ ] Playwright-Axe läuft gegen mindestens eine echte Backstage-Route.
[ ] Axe-Rohdaten werden gespeichert.
[ ] Markdown-Report wird erzeugt.
[ ] JSON-Report wird erzeugt.
[ ] Manual Review Queue ist vorhanden.
[ ] Keine unbefristeten Waivers existieren.
[ ] Keine Accessibility-Regel wurde ohne Begründung deaktiviert.
[ ] CI-Workflow erzeugt Artifacts.
[ ] README dokumentiert lokale Nutzung.
[ ] Report behauptet keine vollständige Konformität ohne manuelle Evidence.
```

---

## 35. Häufige Fehler, die Copilot vermeiden soll

| Fehler | Warum problematisch? | Besser |
|---|---|---|
| `aria-label` auf alles setzen | Kann sichtbare Labels und Screenreader-Namen entkoppeln | Sichtbare Labels korrekt verbinden |
| `div onClick` als Button | Tastatur/Fokus/Role fehlen | `<button>` nutzen |
| Axe-Regeln global deaktivieren | Versteckt echte Probleme | Waiver mit Owner und Ablaufdatum |
| Nur `/` scannen | Backstage-Routen bleiben ungeprüft | Route inventory |
| Nur Default State scannen | Menüs/Dialoge/Formularfehler fehlen | Szenario-Scans |
| `needs_manual_review` als `pass` behandeln | Falsches Sicherheitsgefühl | Ehrlicher Status |
| Nur JSDOM testen | Kein echter Browser, kein verlässlicher Contrast | Playwright ergänzen |
| Lighthouse Score als WCAG-Report verkaufen | Falsch | Lighthouse nur ergänzend |
| Report ohne Rohdaten | Nicht auditierbar | Rohdaten als Artifact speichern |
| Kein Baseline-Konzept | CI wird bei Legacy-App unbrauchbar | Baseline + Regression Gate |

---

## 36. Empfohlener erster PR-Schnitt

### PR 1: Infrastructure Vertical Slice

- Dependencies
- `a11y/routes.json`
- `a11y/wcag22-aa-checklist.json`
- Playwright-Axe helper
- 1 route scan
- Report generator
- README

### PR 2: Component Layer

- jest-axe setup
- 2–3 real component tests
- test docs

### PR 3: Dynamic States

- keyboard helpers
- dialog/menu/form validation scenarios
- route/scenario inventory expanded

### PR 4: CI + Baseline

- GitHub Actions workflow
- artifact upload
- baseline
- waivers
- PR summary

### PR 5+: Coverage Expansion

- alle kritischen Plugins
- mobile/dark theme
- manual review queue
- remediation backlog

---

## 37. README für `a11y/README.md`

````md
# Accessibility Testing

Target: WCAG 2.2 Level AA.

This repository uses automated and semi-automated accessibility checks.
Automated checks do not prove full WCAG conformance. Manual review is still required for criteria that cannot be reliably automated.

## Commands

```bash
yarn lint:a11y
yarn test:a11y:unit
yarn test:a11y:e2e
yarn a11y:report
yarn a11y
```

## Artifacts

- `a11y-results/axe/*.json`: raw axe results
- `a11y-results/a11y-report.json`: normalized machine-readable report
- `a11y-results/a11y-report.md`: human-readable report

## Adding a new route

1. Add the route to `a11y/routes.json`.
2. Add any relevant dynamic states to `a11y/scenarios.json`.
3. Add Playwright readiness checks.
4. Add keyboard/focus tests for interactive flows.

## Waivers

Waivers are temporary. Every waiver requires:

- finding fingerprint
- WCAG criterion
- reason
- owner
- approver
- expiry date

No permanent waivers.
````

---

## 38. Quellen und Recherchebasis

### Offizielle Standards und Methodik

- W3C WCAG 2.2 Recommendation: https://www.w3.org/TR/WCAG22/
- W3C WCAG Overview: https://www.w3.org/WAI/standards-guidelines/wcag/
- W3C WCAG-EM Overview: https://www.w3.org/WAI/test-evaluate/conformance/wcag-em/
- W3C ACT Overview: https://www.w3.org/WAI/standards-guidelines/act/
- WAI-ARIA Authoring Practices Guide: https://www.w3.org/WAI/ARIA/apg/

### Tool-Dokumentation

- Playwright Accessibility Testing: https://playwright.dev/docs/accessibility-testing
- axe-core GitHub: https://github.com/dequelabs/axe-core
- axe-core rules documentation: https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md
- `@axe-core/playwright`: https://www.npmjs.com/package/@axe-core/playwright
- `eslint-plugin-jsx-a11y`: https://github.com/jsx-eslint/eslint-plugin-jsx-a11y
- `jest-axe`: https://github.com/NickColley/jest-axe
- Pa11y: https://github.com/pa11y/pa11y
- Storybook addon-a11y: https://storybook.js.org/docs/writing-tests/accessibility-testing

### Backstage / React

- Backstage Accessibility: https://backstage.io/docs/accessibility/
- Backstage Frontend Testing: https://backstage.io/docs/frontend-system/building-plugins/testing/
- Backstage Playwright config example: https://github.com/backstage/backstage/blob/master/playwright.config.ts
- Backstage UI: https://ui.backstage.io/
- React Accessibility docs: https://legacy.reactjs.org/docs/accessibility.html
- React Aria: https://react-spectrum.adobe.com/react-aria/

### Copilot / VS Code

- VS Code Custom Agents: https://code.visualstudio.com/docs/agent-customization/custom-agents
- VS Code Custom Instructions: https://code.visualstudio.com/docs/agent-customization/custom-instructions
- GitHub Copilot custom instructions: https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions
- Awesome Copilot: https://github.com/github/awesome-copilot

### Rechtlicher / europäischer Kontext

- European Accessibility Act overview: https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/disability/union-equality-strategy-rights-persons-disabilities-2021-2030/european-accessibility-act_en
- Web Accessibility Directive / EN 301 549 context: https://digital-strategy.ec.europa.eu/en/policies/web-accessibility

### Community-/Praxis-Signale

Gesichtete Community-Diskussionen aus Reddit/Foren zeigen konsistent: Teams nutzen häufig Playwright + axe-core als sinnvolle Automatisierungsbasis, betrachten das aber nicht als Ersatz für manuelle Tastatur-/Screenreader-Tests und kritisieren reine Lighthouse-/Homepage-Checks als zu oberflächlich. Diese Community-Signale sind keine Normquelle, passen aber zu den Aussagen der offiziellen Tool- und W3C-Dokumentation.

---

## 39. Kurzempfehlung

Für deine Backstage/React-App solltest du die Lösung so aufbauen:

```text
eslint-plugin-jsx-a11y
+ jest-axe for component tests
+ @axe-core/playwright for real browser route/state scans
+ explicit keyboard/focus Playwright tests
+ custom WCAG 2.2 AA report generator
+ baseline/waiver mechanism
+ GitHub Actions artifact/report workflow
+ Copilot agents for implementation, triage and review
```

Das ist der realistischste Weg, um Accessibility systematisch und CI-fähig zu machen, ohne dir eine falsche 100%-Automatisierungsillusion einzubauen.
