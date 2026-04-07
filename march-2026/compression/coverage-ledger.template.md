# Coverage Ledger

Use this ledger during or after distillation to track whether important source material is represented in the final artifact.

This ledger is especially useful when:
- more than 3 source files are involved
- split mode is used
- the source set is high-stakes
- completeness matters more than elegance

---

## Distillation Run Metadata

- **Run ID:**
- **Date:**
- **Source Set:**
- **Downstream Consumer:**
- **Mode:** single / split
- **Output Path:**
- **Anchors Enabled:** yes / no
- **Validation Requested:** yes / no

---

## Coverage Summary

- **Total source files:**
- **Total source headings/themes tracked:**
- **Total decisions tracked:**
- **Total constraints tracked:**
- **Total open questions tracked:**
- **Total conflicts tracked:**
- **Coverage status:** complete / partial / incomplete

---

## File-Level Coverage

| Source File | Section / Theme | Category | Material Item | Represented? | Distillate Location | Notes / Fix Needed |
|---|---|---|---|---|---|---|
| `example.md` | `Decision` | decision | Chose modular monolith over microservices | yes | `_index.md > Decisions` | |
| `example.md` | `Rejected Alternatives` | rejected_alternative | Rejected microservices due to operational overhead | yes | `architecture.md > Rejected Alternatives` | |
| `research.md` | `Open Questions` | open_question | Scaling bottleneck still unknown | no |  | add to `_index.md > Open Questions` |

---

## Category Definitions

Use one of these categories where possible:

- `fact`
- `definition`
- `entity`
- `decision`
- `rationale`
- `rejected_alternative`
- `constraint`
- `dependency`
- `relationship`
- `scope_inclusion`
- `scope_exclusion`
- `success_criterion`
- `validation_method`
- `risk`
- `opportunity`
- `open_question`
- `conflict`
- `stakeholder`
- `ownership`

---

## High-Priority Material Checklist

These should almost never be omitted.

| Item Type | Preserved? | Notes |
|---|---|---|
| global decisions |  |  |
| rationale for decisions |  |  |
| rejected alternatives |  |  |
| constraints / non-negotiables |  |  |
| scope boundaries |  |  |
| success criteria |  |  |
| major risks |  |  |
| open questions |  |  |
| source conflicts |  |  |
| key named entities |  |  |
| material numbers / thresholds |  |  |

---

## Conflict Ledger

Record any places where sources disagree or appear to disagree.

| Conflict ID | Source A | Source B | Topic | Resolved in Distillate? | Distillate Location | Notes |
|---|---|---|---|---|---|---|
| C-001 | `spec.md > Scope` | `research.md > Findings` | offline support | no | `_index.md > Open Questions` | scope unclear across documents |

---

## Missing or Weak Coverage

Record material items that are missing, underspecified, or too compressed.

| Issue ID | Source File | Material Item | Problem Type | Severity | Required Action | Fixed? |
|---|---|---|---|---|---|---|
| M-001 | `research.md` | unresolved scaling question | missing_open_question | high | add to root open questions | no |
| M-002 | `adr.md` | rejection rationale for option B | over_compressed | medium | restore rationale bullet | no |

Suggested problem types:

- `missing_fact`
- `missing_decision`
- `missing_rationale`
- `missing_constraint`
- `missing_scope_boundary`
- `missing_open_question`
- `missing_conflict`
- `over_compressed`
- `bad_grouping`
- `bad_split_boundary`
- `missing_anchor`

---

## Section-Level Split Coverage

Use this only in split mode.

| Section File | Semantic Theme | Self-Contained? | Cross-Cutting Items Included? | Missing Items | Notes |
|---|---|---|---|---|---|
| `_index.md` | root index | yes | yes | none | |
| `architecture.md` | architecture / decisions | yes | partial | one open question | add cross-reference to `_index.md` |

---

## Final Coverage Decision

- **Coverage complete?**
- **If not complete, why?**
- **Targeted fix pass required?**
- **Round-trip validation gap?**
- **Can the distillate be accepted as standalone downstream context?**

---

## Notes

Use this ledger as a repair tool, not bureaucracy.

The point is not to document everything forever.
The point is to prevent silent omission and make targeted correction easy.