# Asset Policy

## Goals
- Keep deployable assets small.
- Preserve image quality for research visuals.
- Avoid shipping source-only images when optimized versions are available.

## Directory Rules
- `src/assets/`: assets imported or referenced by source pages, including optimized portrait assets.
- `public/assets/`: files served directly by Cloudflare Pages.
- `public/tools/assets/`: tool runtime assets. Treat as sensitive; do not delete without testing tools.
- `dist/`: generated output. Do not edit directly.

## Image Format Policy
- Use WebP for large public-facing images.
- Keep PNG/JPG only when:
  - transparency or exact source fidelity is required
  - the file is small
  - it is an editable source asset intentionally kept outside the deploy path

## Current Optimized Assets
- `src/assets/profile-hero.webp`
- `public/assets/knowledge/封面scVI.webp`
- `public/assets/skin_aging/*.webp`
- `public/assets/vHFO_exos/*.webp`

## Cleanup Rule
Before deleting a large asset:
1. Search source and public HTML references with `rg`.
2. Confirm an optimized replacement exists.
3. Run `npm run build`.
4. Run generated HTML asset reference check.
5. Test live pages after deploy.

## Known Cleanup Candidate
The large PNG research images replaced by WebP can be removed after manual confirmation:
- `public/assets/knowledge/封面scVI.png`
- `public/assets/skin_aging/websummary_scEC.png`
- `public/assets/skin_aging/web_clinical_transl.png`
- `public/assets/skin_aging/web_scanalysis.png`
- `public/assets/skin_aging/web_workflow_EC.png`
- `public/assets/vHFO_exos/web_cellular_mechnism.png`
- `public/assets/vHFO_exos/web_exp_design.png`
- `public/assets/vHFO_exos/web_vHFO.png`

Estimated deploy size reduction: about 47 MB.

## Tool Asset Warning
Do not remove:
- `public/tools/assets/stlite/`
- `public/tools/assets/pypi/`

These are required by the browser-based Python tools.
