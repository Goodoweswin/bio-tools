# Project Changelog

All notable changes to the **bio-tools** personal research website are documented here.

## Unreleased

### Changed
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
