# Content Accuracy Register

## Purpose
Keep public copy useful without presenting hypotheses, unshared materials, or image labels as established facts.

## Editorial Rules
- Frame active research as a question, test, exploration, or evaluation unless public results support a stronger claim.
- Do not add author lists, venues, dates, DOI links, citations, or conference artifacts without owner-provided primary records.
- Keep manuscript, poster, and technical-method readiness labels explicit.
- Prefer descriptive state language such as `senescence-associated endothelial states` over undefined placeholder regulators.
- Treat labels baked into image assets separately from editable HTML text.

## Completed in Phase 2A
- Removed editable public references to `NRX`; no `NRX` text remains in `src/` HTML.
- Replaced generic candidate-regulator wording in Research and Publications with state- and program-level language.
- Preserved hypothesis framing for active vascular-aging and follicle-repair research.
- Confirmed Publications labels work as explicit availability statements rather than bibliographic claims.

## Asset Review
The following public image assets still contain `NRX` inside the bitmap and should be revised only when the underlying scientific figure is ready to change:

- `public/assets/skin_aging/web_scanalysis.webp`
- `public/assets/skin_aging/web_clinical_transl.webp`

The matching PNG files are deployable legacy copies and should be updated in the same source-asset pass, not by editing the compressed WebP alone.

## Owner Input Needed
Phase 2B requires source material from Jackson Dai before it can add public records:

- publication title, full author list, venue, year, DOI or stable link
- conference title, event date, public abstract, poster, or slide link
- tool documentation for input formats, demo data, assumptions, and export behavior

Until those records are supplied, keep the current readiness labels and do not infer missing details.
