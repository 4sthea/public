---
name: distillator
description: Create a high-retention, LLM-optimized distillate from one or more source documents. Use when the user needs dense reusable context rather than a conventional summary.
argument-hint: "[source_documents] [downstream_consumer optional] [token_budget optional] [output_path optional] [--validate optional] [--anchors optional]"
---

# Distillator

## Purpose

Produce a high-retention, token-efficient distillate from one or more source documents.

A distillate is not a summary.

A summary optimizes for readability and brevity.
A distillate optimizes for downstream LLM usefulness while preserving the material content needed to reconstruct intent, decisions, constraints, relationships, and unresolved questions.

The distillate should be usable as a standalone context artifact for downstream workflows.

---

## Inputs

Required:
- `source_documents`: one or more file paths, directory paths, or glob patterns

Optional:
- `downstream_consumer`: target workflow, agent, or task
- `token_budget`: approximate maximum desired size for the final distillate
- `output_path`: output file or folder path
- `--validate`: run optional round-trip validation
- `--anchors`: include lightweight provenance anchors on bullets where useful

---

## Distillation Standard

A valid distillate must preserve:
- facts and data points
- named entities
- dates, versions, percentages, and numeric thresholds
- decisions and rationale
- rejected alternatives and why they were rejected
- requirements and constraints
- dependencies and relationships
- scope boundaries and exclusions
- success criteria and validation methods
- risks and opportunities
- open questions and unresolved conflicts
- user segments, stakeholders, and ownership signals

A valid distillate must remove:
- rhetorical framing
- repeated introductions and conclusions
- persuasive or decorative prose
- self-reference
- common-knowledge explanation
- unnecessary transitions
- repeated examples unless each adds unique signal

A valid distillate must transform:
- paragraphs into dense self-contained bullets
- repeated concepts into one retained canonical bullet
- vague relationships into explicit relationships
- conflicting claims into explicit conflict notes
- loose narrative into grouped thematic structure

---

## Core Principles

### 1. Extraction before compression
Do not start by rewriting the source into shorter prose.

First extract the content plan:
- salient facts
- salient decisions
- salient constraints
- salient entities
- salient rationale
- open questions
- cross-document relationships

Then compress the extracted material.

### 2. Structure-aware handling
Prefer document headings, section boundaries, and semantic topic boundaries over arbitrary chunk sizes.

If splitting is necessary, split semantically, not by raw size alone.

### 3. Coverage before elegance
A complete but dense distillate is better than a readable but lossy summary.

### 4. Optional provenance
If the source set is large, conflicting, or high-stakes, include lightweight provenance anchors.

Suggested anchor format:
- `[src: relative/path.md > Heading Name]`
- `[src: relative/path.md#Heading Name]`

Anchors are optional unless ambiguity, conflict, or compliance needs make them useful.

### 5. Bounded compression
If the requested token budget would force destructive loss of required categories, stop and report that instead of pretending the result is lossless.

---

## Process

### Step 1: Resolve and inspect sources
Accept file paths, directories, and globs.

Prefer recursive discovery for supported text-like source types:
- `.md`
- `.txt`
- `.rst`
- `.yaml`
- `.yml`
- `.json`

Ignore clearly irrelevant directories such as:
- `node_modules`
- `.git`
- `__pycache__`
- `.venv`
- `venv`
- `.idea`
- `.claude`
- `.cursor`
- `.vscode`
- `_bmad-output`
- `dist`
- `build`
- `coverage`

If no readable source files are found, stop and report that clearly.

### Step 2: Inspect structure and estimate scale
Determine:
- file count
- estimated total source tokens
- heading density
- likely semantic groupings
- likely need for split mode

Recommended heuristic defaults:
- use single-file mode when there are at most 3 files and about 15,000 estimated source tokens or fewer
- use split mode otherwise
- strongly prefer split mode if the estimated final distillate would exceed roughly 5,000 tokens

These are routing heuristics, not hard laws.

### Step 3: Build a coverage ledger
Before compression, create an internal coverage ledger for each source.

Track whether the distillate preserves:
- major headings or sections
- named entities
- decisions
- constraints
- open questions
- scope boundaries
- success criteria
- risks
- conflicts or contradictions

This ledger is mandatory even if it is not emitted to the user.

### Step 4: Extract a highlight/content plan
For each source, extract the highest-salience items first.

Prefer preserving:
- entities and terminology
- quantitative data
- concrete decisions
- rationale and trade-offs
- rejection reasons
- critical examples only when they encode unique meaning
- ownership or responsibility signals

This pass exists to reduce the risk of dropping the most valuable content during compression.

### Step 5: Extract all material content
Extract discrete items, not prose blocks.

Extraction categories:
- facts
- definitions
- decisions
- rationale
- rejected alternatives
- constraints
- dependencies
- interfaces
- entities
- open questions
- scope inclusions
- scope exclusions
- success criteria
- validation methods
- risks
- opportunities
- stakeholder concerns

### Step 6: Merge and deduplicate
Merge overlapping items.

Deduplication rules:
- keep the version with the strongest context
- keep the more specific version when one strictly subsumes another
- keep one canonical phrasing for repeated content
- preserve explicit contradiction when sources disagree
- preserve chronology if the disagreement may be time-based rather than truly contradictory

### Step 7: Apply downstream filtering conservatively
Only filter aggressively if a downstream consumer is specified.

Ask:
- would this item materially help the downstream task?

When uncertain, keep it.

Never remove by default:
- decisions
- rationale
- rejected alternatives
- constraints
- scope boundaries
- open questions
- risks
- conflicts

### Step 8: Group thematically
Organize by natural themes that emerge from the documents.

Common themes:
- problem / motivation
- stakeholders / users
- architecture / solution
- requirements / constraints
- decisions / trade-offs
- rejected alternatives
- implementation notes
- success criteria / validation
- open questions
- risks / opportunities

Avoid rigid templates if they distort the source structure.

### Step 9: Compress language
For each retained item:
- make it self-contained
- remove prose overhead
- preserve concrete detail
- make relationships explicit
- prefer dense bullets over narrative paragraphs

Compression rules:
- use direct nouns and verbs
- collapse repeated framing
- preserve important qualifiers
- keep causal words when they carry rationale
- preserve negations and exclusions
- preserve numbers verbatim where possible

### Step 10: Format output
Output format rules:
- use `##` headings
- use `- ` bullets only under headings
- no prose paragraphs
- no repeated information
- no decorative formatting
- no filler bullets
- every bullet must be understandable on its own

If `--anchors` is enabled or provenance is needed:
- append a lightweight anchor to ambiguous, contested, or high-value bullets

---

## Splitting Rules

When split mode is needed, create:
- one root distillate
- one or more semantic section distillates

### Root distillate must contain
- 3-5 orientation bullets
- source manifest
- section manifest
- cross-cutting facts and constraints
- global decisions and trade-offs
- cross-document conflicts
- top-level scope summary

### Each section distillate must contain
- 1-line context header
- thematic bullets for that section
- local decisions, constraints, and open questions
- cross-references when necessary

### Splitting guidance
Prefer boundaries such as:
- architecture vs implementation vs evaluation
- stakeholder groups
- major feature areas
- temporal phases
- top-level headings or document families

Avoid:
- arbitrary equal-sized splits
- splits that separate decision from rationale
- splits that separate constraint from the thing constrained

If a boundary is fuzzy, allow small overlap in the internal analysis phase, but avoid duplicated bullets in final output.

---

## Completeness Check

After producing the distillate:

1. compare the distillate against the coverage ledger
2. verify that major headings or section themes are represented
3. verify that named entities and numbers are preserved where material
4. verify that decisions, rationale, constraints, open questions, and scope boundaries remain present
5. verify that conflicts are surfaced rather than flattened
6. if important gaps exist, run a targeted fix pass
7. limit targeted fix passes to 2

Do not restart from scratch unless the distillate is fundamentally broken.

---

## Optional Round-Trip Validation

If `--validate` is requested:

1. attempt to reconstruct plausible source structure using only the distillate
2. do not consult the originals during reconstruction
3. note where reconstruction is weak, underspecified, or impossible
4. compare those gaps against the coverage ledger
5. report likely missing content explicitly

This is a stress test for completeness, not proof of perfect reversibility.

---

## Output

### Single Distillate
Save one markdown file with frontmatter:

- `type: distillate`
- `sources`
- `downstream_consumer`
- `created`
- `token_estimate`
- `parts: 1`
- `anchors: true|false`

### Split Distillate
Save a folder containing:
- `_index.md`
- one markdown file per semantic section

The index must contain:
- frontmatter
- orientation bullets
- source manifest
- section manifest
- cross-cutting decisions and constraints
- conflicts ledger
- top-level open questions

---

## Quality Standard

A good distillate:
- preserves decisions, rationale, and constraints
- preserves terminology, entities, and quantitative details where material
- is semantically grouped
- is dense without becoming cryptic
- can serve as standalone context for downstream LLM workflows
- makes uncertainty and disagreement explicit
- optionally preserves provenance when that materially helps trust or reuse

A bad distillate:
- reads like a generic summary
- drops rationale
- drops rejected alternatives
- drops numbers or named entities
- collapses conflicts into a false single answer
- removes open questions
- splits arbitrarily
- compresses so aggressively that downstream use becomes lossy

---

## Failure Conditions

Stop and report clearly if:
- no readable source files are found
- the source set is too ambiguous to distill safely
- the token budget would force destructive loss
- key decisions or constraints cannot be preserved
- the source set is mostly non-textual or structurally unreadable
- validation reveals major unrecoverable gaps

---

## Suggested Output Sequence

1. resolve sources
2. inspect scale and structure
3. choose single or split mode
4. build coverage ledger
5. extract highlight/content plan
6. extract all material items
7. deduplicate and merge
8. group semantically
9. compress language
10. emit output
11. run completeness check
12. optionally run round-trip validation
