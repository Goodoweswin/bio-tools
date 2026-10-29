# Project Changelog

All notable changes to the **bio-tools** personal research website are documented here.

## Unreleased

### 2026-10-29: M.D. Identity and Type Hierarchy
- Corrected master's labels to M.D. student in clinical medicine (plastic surgery), expected graduation 2027, in visible content and social/search metadata.
- Self-hosted Source Serif 4 for editorial headings and Source Sans 3 for reading/UI, with official licenses and explicit Chinese fallbacks.
- Rebalanced name, section, institution/project, body, and metadata typography; replaced slogan headings with descriptive labels and stacked mobile portrait/biography.
- Synchronized submitted scaffold work, co-first authorship, BGI spatial-omics duties, Pilotus team and modeling work, named talks/poster, and corrected football results from both current resumes.
- Preserved original routes, bilingual CV files, scientific images, tools, and backend behavior. Public work headings describe contributions without inventing bibliographic metadata or acceptance.
- Local verification: build and whitespace checks, 70 Firefox checks, 43 local links/assets, all four font faces loaded, desktop/mobile screenshots, and short-screen framing passed. Commit/push authorized by owner; Git history records transport state. Deployed verification remains open.

### 2026-10-27: Bilingual CV
- Replaced the Chinese CV with the new owner-provided PDF and added the English PDF.
- Added direct English/Chinese links in the homepage hero, experience section, and shared footer, including language metadata.
- Preserved `/assets/cv.pdf` for Chinese; added `/assets/cv-en.pdf` for English. Updated link revision to `20261027` and cache revalidation for both PDFs.
- This update replaces downloadable documents and their UI only; it does not revise biographical or research copy from the new resumes. Commit/push and deployed verification remain separate.
- Verified production build, exact source/output PDF hashes, valid PDF responses for both languages and the legacy link, and Firefox layouts at 320, 390, 768, and 1440 pixels. Mobile/desktop screenshots reviewed.

### 2026-10-19: Resume-Based Content
- Added the owner's HUST master's identity, education, BGI internship, clinical rotations, and selected research methods.
- Added Pilotus Studio, voice-based work management, Lab circle, and a responsive experience timeline to Home.
- Updated research with resume-supported dates, responsibilities, ongoing status, and earlier undergraduate training.
- Replaced manuscript placeholders with Research & Activities at the original `/publications` route, retaining existing section anchors.
- Corrected conference participation, added selected honors and football association founding, and updated public email to `daijie@hust.edu.cn`.
- Added a gated implementation plan and updated source-accuracy and handoff documentation.
- Local verification: production build, 66 Firefox checks, 40 local links/assets, desktop and mobile screenshots, and whitespace checks passed. Owner requested a local commit on 2026-10-19; push and live verification remain pending.

### 2026-10-16: Clearer Research Portfolio
- Replaced the dark Future Lab OS visual system with white surfaces, readable charcoal text, restrained green controls, and a full-bleed conceptual skin illustration.
- Made Jackson Dai the homepage identity, simplified copy across all five pages, and retained the portrait in its original color.
- Put tool launch links and note search directly in view. Preserved all 12 note routes and the two tool application URLs.
- Replaced publication-policy framing with concise availability statements; no citations or scientific findings were invented.
- Kept research diagrams uncropped, linked to original images, and distinguished working hypotheses from results in captions.
- Added accessible mobile navigation, current-page indication, note empty/reset states, and focus-aware assistant controls.
- Replaced assistant response HTML insertion with plain text rendering; kept the existing API contract and backend unchanged.
- Updated shared article reading styles and contained the batch-correction comparison table on mobile.
- Added image provenance and updated active design documentation. Owner authorized commit/push on 2026-10-16; deployed verification remains pending.
- Verified production build, 66 Firefox browser checks, 40 local links/assets, responsive screenshots, and sitemap XML. Live service and deployment checks remain separate.

The older OS entries below describe previous iterations, not the active design.

### Changed
- Phase 2A content-accuracy pass:
  - removed editable public `NRX` and generic candidate-regulator placeholder language
  - reframed Research and Publications around senescence-associated endothelial states and active hypotheses
  - added `CONTENT_ACCURACY.md` to track bitmap-label debt and owner-provided records required for Phase 2B
- Publications page Publications OS Ledger redesign:
  - replaced the generic scholarly-output list with an evidence-led public-record system
  - added a public-record protocol that prevents invented citations, metrics, and inaccessible claims
  - rebuilt manuscripts, conference materials, and technical notes as explicit readiness-aware records
  - added a release route for future citable records and retained the BioTools route for technical methods
  - added Publications reveal targets, hover motion, and mobile layout handling
- Knowledge page Knowledge Atlas redesign:
  - replaced the sidebar-plus-list index with an asset-led `Knowledge system` hero
  - added visible note count, English and Chinese search, and segmented track filters
  - grouped all 12 stable article routes into computation, biology, and translation-led tracks
  - added Knowledge Atlas reveal targets, hover motion, and mobile layout handling
- Tools page BioTools Control Room redesign:
  - replaced the browser workbench hero with a `BioTools control room` OS hero
  - added a runtime console for local-file, no-login, WASM-oriented analysis
  - rebuilt live tool entries as instrument stations for ElementPrism and DEG Analysis
  - added an analysis loop section for input, compute, and export flow
  - retained the pathway enrichment module as the next planned instrument
  - added Tools OS reveal targets, hover motion, and mobile layout handling
- Research page Future Lab OS module redesign:
  - replaced proposal-like project briefs with a research operating-system hero
  - added module rail navigation for skin axis, follicle repair, and validation layers
  - rebuilt project content as visual module boards with real research assets
  - added responsive Research OS layouts for desktop, tall desktop, tablet, and mobile
  - added Research OS reveal targets and restrained hover motion
  - tightened mobile navigation so all primary links are visible at 390px width
- Homepage Phase 1B Future Lab OS redesign:
  - replaced the split collage hero with a `Regeneration OS` atlas hero
  - added semantic route grid entries for Map, Niche, Tools, and Notes
  - replaced the old research focus block with a translational research loop
  - reframed BioTools as browser instruments with workflow steps
  - changed Latest News into a compact signal feed
  - added atlas scan, matrix pulse, hover depth, and scroll reveal targets
- Homepage Phase 1A hero sharpening pass after live screenshot review:
  - shortened the hero headline to reduce poster-like first-screen weight
  - changed primary CTA copy to `Open Research System`
  - quieted secondary collage layers while preserving the portrait and vascular aging figure
  - reduced mobile navigation spacing and hid the mobile scrollbar
  - adjusted first-frame hero animation so content remains readable during screenshot and load states
- Research and Publications copy now reframes `NRX` as candidate endothelial regulators in public text.

### Verified
- `./node_modules/.bin/vite build` passes.
- Local Firefox screenshots checked at 1440px desktop and 390px mobile.
- Homepage Phase 1B checked with local Firefox screenshots at 1440px desktop and 390px mobile.
- Research OS checked with local Chrome screenshots at 1440px desktop, 1440px tall desktop, and 390px mobile.
- Tools OS checked with local Chrome screenshots at 1440px desktop, 1440px tall desktop, and 390px mobile.
- Knowledge Atlas checked with local Firefox screenshots at 1440px desktop, 390px mobile, and 390px tall mobile.
- Publications OS Ledger checked with local Firefox screenshots at 1440px desktop, 390px mobile, and 390px tall mobile.

## [2026-07-01] - Research Website Redesign and Deployment Hygiene

### Added
- Homepage research identity around `Jackson Dai Research`.
- Research collage hero using portrait, research figure, single-cell dot matrix, and research axis labels.
- Editorial research page layout with two structured project briefs:
  - vascular-skin axis in dermal aging
  - angio-follicular crosstalk in alopecia
- BioTools workbench page for browser-based tools.
- Knowledge page as a searchable research-note index.
- Publications page as a conservative scholarly output ledger.
- Lightweight scroll reveal motion in `src/js/site.js`.
- Main-page SEO metadata:
  - descriptions
  - canonical URLs
  - Open Graph metadata
  - Twitter card metadata
- `public/robots.txt`.
- `public/sitemap.xml`.
- Long-term project docs:
  - `DESIGN_STRATEGY.md`
  - `DESIGN_SYSTEM.md`
  - `DEPLOYMENT.md`
  - `SEO_CHECKLIST.md`
  - `ASSET_POLICY.md`
  - `TEST_CHECKLIST.md`

### Changed
- Public identity now uses `Jackson Dai` as the pen name.
- Main pages now share visual structure through `src/css/style.css` instead of page-local style blocks.
- Global shape language tightened to small-radius, research-led UI.
- Large public research images now use WebP where available.
- Tools, Knowledge, and Publications pages now use denser, ledger-like layouts instead of generic rounded cards.
- Homepage hero composition was tuned after live screenshot review to reduce visual crowding.

### Verified
- `./node_modules/.bin/vite build` passes.
- `https://daiger.top/`, `/research`, `/robots.txt`, and `/sitemap.xml` returned HTTP 200 after deployment.
- Live HTML included latest hero text, meta tags, and built CSS.

### Notes
- `for_agent/CHANGELOG.md`, `for_agent/HANDOFF_TO_AGENT.md`, and `for_agent/ROADMAP.md` were refreshed after the redesign to remove stale January 2026-only status language.
- Existing commits pushed before this refresh include:
  - `d58e5ec Consolidate pages and add SEO metadata`
  - `de2971a Tune homepage hero composition`
  - `41541d3 Add subtle scroll reveal motion`

## Earlier Work

Earlier project history included:
- Vite setup and shared header/footer components.
- Cloudflare Pages deployment.
- ElementPrism statistical workbench.
- DEG volcano plot tool.
- Knowledge article scaffolding.
- Static page favicon and navigation improvements.
