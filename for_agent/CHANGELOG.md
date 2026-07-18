# Project Changelog

All notable changes to the **bio-tools** personal research website are documented here.

## Unreleased

### Changed
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
