# Content Accuracy Register

## Purpose
Keep public copy useful without presenting hypotheses, unshared materials, or image labels as established facts.

## Editorial Rules
- Frame active research as a question, test, exploration, or evaluation unless public results support a stronger claim.
- Do not add author lists, venues, dates, DOI links, citations, or conference artifacts without owner-provided primary records.
- Keep manuscript, poster, and technical-method readiness labels explicit.
- Prefer descriptive state language such as `senescence-associated endothelial states` over undefined placeholder regulators.
- Treat labels baked into image assets separately from editable HTML text.

## Resume-Based Update: 2026-10-19
- Primary source: owner-provided `public/assets/cv.pdf`, checked visually because its extracted Chinese text has a broken character mapping.
- Added education, BGI internship, clinical rotations, project roles, research periods, selected honors, community founding, and digital projects directly from that resume.
- Master's graduation in 2027 and research completion dates remain explicitly expected; both research projects remain ongoing.
- Replaced the unsupported 2025 Westlake poster claim with attendance. Removed unconfirmed conference months and the previous talk title.
- Conference record now says speaking and attendance at the 22nd Chinese Medical Association plastic surgery academic exchange meeting (Beijing, 2025), and attendance at Westlake x Nature's Stem Cells Across the Lifespan (2025).
- Replaced manuscript-preparation placeholders with Research & Activities at the existing `/publications` route. The resume supplies no publication citations or public conference files.
- Public email updated to `daijie@hust.edu.cn`. Jackson Dai remains the public name; About includes 代杰.
- Personal projects without owner-provided public URLs have descriptions only. No product readiness, adoption figures, or public demos are inferred.
- Experimental methods and basic R/Python skills follow the resume; no proficiency ratings or validated-tool claims are added.

## Completed in Phase 2A
- Removed editable public references to `NRX`; no `NRX` text remains in `src/` HTML.
- Replaced generic candidate-regulator wording in Research and Publications with state- and program-level language.
- Preserved hypothesis framing for active vascular-aging and follicle-repair research.
- Confirmed Publications labels work as explicit availability statements rather than bibliographic claims.

## Asset Review
The following public image assets still contain `NRX` inside the bitmap and should be revised only when the underlying scientific figure is ready to change:

- `public/assets/skin_aging/web_scanalysis.webp`
- `public/assets/skin_aging/web_clinical_transl.webp`
- `public/assets/skin_aging/websummary_scEC.webp`
- `public/assets/skin_aging/web_workflow_EC.webp`

The 2026-10-16 redesign keeps these images unchanged, removes them from the homepage hero, and labels working schematics and proposed outcomes in Research captions. The vHFO diagrams also depict repair outcomes that must remain framed as hypotheses, not demonstrated results.

The new homepage concept art is AI-generated and visibly labeled as illustration. It contains no measured results or regulator labels; provenance is recorded in HERO_ASSET_PROVENANCE.md.

Article body claims and code examples have not undergone scientific or runtime validation in this visual pass. Schedule a separate content audit before treating the notes as validated methods.

The matching PNG files are deployable legacy copies and should be updated in the same source-asset pass, not by editing the compressed WebP alone.

## Owner Input Needed
The resume now supports the education, experience, activities, honors, and project records above. Additional source material is still required for:

- publication title, full author list, venue, year, DOI or stable link
- conference title, event date, public abstract, poster, or slide link
- tool documentation for input formats, demo data, assumptions, and export behavior

Until those records are supplied, keep the current readiness labels and do not infer missing details.
