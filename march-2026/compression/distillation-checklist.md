# Distillation Checklist

Use this checklist after producing a distillate and before marking it complete.

## 1. Source Resolution

- [ ] All intended source files were discovered and read
- [ ] Irrelevant/generated/vendor directories were excluded
- [ ] Unsupported or unreadable files were reported explicitly
- [ ] The chosen source set matches the requested scope

## 2. Routing

- [ ] Single-file vs split mode was chosen deliberately
- [ ] Split mode was used if the source set was too large for one coherent artifact
- [ ] Splits were semantic, not arbitrary
- [ ] The root distillate contains cross-cutting items if split mode was used

## 3. Preservation of Material Content

- [ ] Facts and concrete data points were preserved
- [ ] Named entities were preserved
- [ ] Dates, versions, thresholds, and quantitative details were preserved where material
- [ ] Decisions were preserved
- [ ] Rationale for decisions was preserved
- [ ] Rejected alternatives were preserved
- [ ] Reasons for rejection were preserved
- [ ] Constraints and non-negotiables were preserved
- [ ] Dependencies and relationships were preserved
- [ ] Scope boundaries and exclusions were preserved
- [ ] Success criteria were preserved
- [ ] Validation methods were preserved if present
- [ ] Risks were preserved
- [ ] Open questions were preserved
- [ ] Stakeholders / user segments / ownership signals were preserved if present

## 4. Compression Quality

- [ ] The output is not just a summary
- [ ] Decorative prose was removed
- [ ] Repeated introductions and conclusions were removed
- [ ] Repeated concepts were deduplicated
- [ ] Bullets are dense but still self-contained
- [ ] Important qualifiers were preserved
- [ ] Negations and exclusions were preserved
- [ ] Conflicting source claims were surfaced explicitly instead of flattened

## 5. Grouping and Structure

- [ ] Content is grouped by natural semantic themes
- [ ] Decision and rationale were kept together
- [ ] Constraint and constrained item were kept together where relevant
- [ ] Related open questions remain near the relevant topic
- [ ] Cross-document relationships are explicit
- [ ] The structure would still make sense to a downstream LLM without the source docs

## 6. Formatting

- [ ] `##` headings are used consistently
- [ ] Content appears as bullets under headings
- [ ] No unnecessary prose paragraphs remain
- [ ] No decorative formatting adds noise
- [ ] Bullets do not repeat each other
- [ ] The output is easy to scan and reuse

## 7. Completeness Check

- [ ] Major source headings or section themes are represented
- [ ] Major entities are represented
- [ ] Major decisions are represented
- [ ] Major constraints are represented
- [ ] Major open questions are represented
- [ ] Major scope boundaries are represented
- [ ] Any missing material items were corrected in a targeted fix pass
- [ ] No more than 2 targeted fix passes were needed

## 8. Optional Provenance

- [ ] Provenance anchors were added where ambiguity, conflict, or compliance needs justify them
- [ ] Anchors are lightweight and do not overwhelm the output
- [ ] Anchors point to useful source locations

## 9. Optional Validation

- [ ] Round-trip validation was run if requested
- [ ] Validation gaps were reported explicitly
- [ ] Validation did not falsely claim reversibility or proof of completeness

## 10. Final Quality Gate

- [ ] The distillate can serve as standalone context for the downstream task
- [ ] The distillate preserves all material decisions and constraints
- [ ] The distillate is dense without becoming cryptic
- [ ] The distillate does not silently omit critical content
- [ ] The output should be accepted

## If Not Accepted

If the distillate fails this checklist, classify the issue as one or more of:

- missing material content
- poor semantic grouping
- over-compression
- under-compression
- unresolved conflict flattening
- bad split boundaries
- formatting drift
- insufficient provenance
- failed completeness check

Then run a targeted fix pass instead of rewriting from scratch.