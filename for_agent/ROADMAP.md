# Project Roadmap

## North Star
Make `daiger.top` feel like Jackson Dai's personal research system: credible academic identity, clear research programs, useful browser tools, and a growing knowledge base.

## Phase 1: Live Visual QA
Status: in progress. Homepage, Research, Tools, and Knowledge have local desktop and mobile visual checks; Publications and deployed-site confirmation remain.

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

## Phase 1B: Future Lab OS Homepage
Status: implemented and locally verified on 1440px desktop and 390px mobile screenshots.

- Rebuild homepage into a stronger future-facing research operating system.
- Use `Regeneration OS` as the first-screen identity.
- Replace generic split-hero rhythm with:
  - atlas core
  - semantic route grid
  - translational research loop
  - BioTools instrument dock
  - compact signal feed
- Keep existing routes, navigation, assets, and deployment behavior.
- Next acceptance check:
  - verify the deployed `https://daiger.top/` homepage after push
  - decide whether Knowledge should receive the same OS treatment

## Phase 1C: Research OS Modules
Status: implemented and locally verified on 1440px desktop, 1440px tall desktop, and 390px mobile screenshots.

- Rebuild `/research` into a Future Lab OS module page.
- Keep existing research programs, Chinese summaries, and public route stable.
- Replace the older editorial brief rhythm with:
  - research module hero
  - skin axis, follicle repair, and validation module rail
  - real research-asset orbit
  - Question, Model, Computation, and Translation boards
  - validation route panels
- Acceptance checks passed:
  - mobile navigation shows all primary links at 390px width
  - hero avoids oversized empty space on tall desktop viewports
  - module boards do not overlap or collapse in screenshot QA
  - `npm run build`, `git diff --check`, and `xmllint --noout public/sitemap.xml` pass

## Phase 1D: BioTools Control Room
Status: implemented and locally verified on 1440px desktop, 1440px tall desktop, and 390px mobile screenshots.

- Rebuild `/tools` into a BioTools OS control room.
- Keep current tool URLs stable:
  - `/tools/stat_analysis/index.html`
  - `/tools/deg/index.html`
- Replace the older workbench list rhythm with:
  - control-room hero
  - runtime console
  - live instrument stations
  - input, compute, and export analysis loop
  - pathway enrichment as the next planned instrument
- Acceptance checks:
  - mobile navigation remains visible at 390px width
  - hero avoids oversized empty space on tall desktop viewports
  - tool station cards do not overlap or trap CTA buttons
  - `npm run build`, `git diff --check`, and `xmllint --noout public/sitemap.xml` pass

## Phase 1E: Knowledge Atlas
Status: implemented, committed, and pushed. Deployed-site verification remains pending because the agent environment could not reach the public route.

- Rebuild `/knowledge` as a searchable Future Lab OS knowledge module.
- Keep all 12 note URLs and their original Chinese article titles stable.
- Replace the former sidebar-plus-list rhythm with:
  - knowledge-atlas hero using the existing single-cell integration image
  - search command strip with visible-result status
  - segmented research-track filters
  - computation, biology, and translation routes
  - grouped public-note ledger
- Keep search responsive to English, Chinese, and method-specific terms.
- Acceptance checks passed locally:
  - 1440px desktop hero fits with the next module visible at the viewport edge
  - 390px mobile hero, image, navigation, search, and filters remain legible without horizontal overflow
  - article links remain unchanged
  - `npm run build`, `git diff --check`, and `xmllint --noout public/sitemap.xml` pass
- Remaining verification:
  - verify deployed `/knowledge` on `https://daiger.top/` when public access is available

Exception: on 2026-07-18, the user explicitly approved starting Phase 1F before the deferred deployed-site check could be completed.

## Phase 1F: Publications OS Ledger
Status: implemented and locally verified. Checkpoint remains open until the changes are committed and pushed.

- Rebuild `/publications` as the final Future Lab OS module page.
- Preserve the conservative public-claims policy and existing status language.
- Establish clear locations for future citation records, conference materials, and technical notes.
- Replace the generic output list with:
  - evidence-led output hero using an existing experimental-design asset
  - public record protocol
  - grouped manuscript, conference, and technical-method ledgers
  - explicit readiness state for each output
  - release route for future citable records
- Acceptance checks passed locally:
  - 1440px desktop hero keeps the module rail visible at the viewport edge
  - 390px mobile hero, protocol, and output records remain legible without horizontal overflow
  - `/tools` route remains available from the technical-method record
  - `npm run build`, `git diff --check`, and `xmllint --noout public/sitemap.xml` pass
- Checkpoint close criteria:
  - commit the Publications OS Ledger changes
  - push to `origin/main`
  - verify deployed `/publications` on `https://daiger.top/`

Do not begin Phase 2 before this checkpoint is closed.

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
