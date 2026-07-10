# Project Roadmap

## North Star
Make `daiger.top` feel like Jackson Dai's personal research system: credible academic identity, clear research programs, useful browser tools, and a growing knowledge base.

## Phase 1: Live Visual QA
- Review `/` on desktop, tablet, and mobile.
- Confirm homepage hero is strong but not crowded.
- Check Research, Tools, Knowledge, and Publications pages for text overflow.
- Validate scroll reveal feels subtle and never blocks content.
- Confirm the `Jackson Dai Research` brand reads correctly across pages.

## Phase 1A: Homepage Hero Sharpening
Status: implemented and locally verified on 1440px desktop and 390px mobile screenshots.

- Treat the current homepage as visually correct in direction but too heavy in first-screen proportion.
- Reduce the hero from a poster-like layout to a sharper research interface.
- Keep the dark academic system language, real portrait, and vascular aging figure.
- Compress the desktop headline to roughly 2-3 lines instead of 4 lines.
- Make CTA copy feel like opening a research system rather than a generic landing page.
- Reduce collage crowding by lowering the visual weight of secondary panels.
- Keep image corners square or small-radius; avoid returning to soft SaaS cards.
- Acceptance checks:
  - headline does not dominate the first viewport on 1440px desktop
  - CTA row stays visible without scrolling
  - right-side collage has one clear focal point
  - mobile hero remains readable without overlapping panels

## Phase 2: Content Accuracy
Status: started. Public copy now reframes `NRX` as candidate endothelial regulators unless the term appears inside existing image assets.

- Replace or reframe placeholder scientific terms such as `NRX`.
- Add real publication metadata when available:
  - title
  - authors
  - venue
  - year
  - DOI or public link
- Add public conference materials when cleared.
- Add clearer project status labels for manuscripts and posters.

## Phase 3: BioTools Expansion
- Document current tools:
  - accepted input formats
  - demo data
  - export behavior
  - statistical assumptions
- Candidate next modules:
  - pathway enrichment
  - GO/KEGG bubble plot
  - gene set intersection and UpSet plot
  - reusable figure export presets

## Phase 4: Knowledge Base Growth
- Add per-article meta descriptions.
- Add tags to notes.
- Add related-note links between articles.
- Consider turning the hardcoded Knowledge index into a generated index if article count grows.

## Phase 5: Search and AI
- Decide whether to add site search beyond the Knowledge page.
- If RAG is still desired, use the stabilized Knowledge content as the source corpus.
- Candidate stack:
  - Cloudflare Vectorize
  - Workers AI
  - Cloudflare Pages Functions
- Keep RAG answers citation-first and avoid unsupported claims.

## Phase 6: Deployment Hygiene
- Keep `robots.txt` and `sitemap.xml` current.
- Consider automatic sitemap generation.
- Keep large original source images outside deployable `public/`.
- Remove unused large PNGs after confirming WebP replacements and archive strategy.
- Continue running:
```bash
./node_modules/.bin/vite build
git diff --check
xmllint --noout public/sitemap.xml
```
