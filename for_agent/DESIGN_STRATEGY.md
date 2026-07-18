# Design Strategy

## Current Design Read
- **Site type**: Personal academic portfolio plus browser-based bioinformatics toolkit.
- **Audience**: Research collaborators, mentors, clinicians, wet-lab users, and visitors evaluating credibility.
- **Vibe**: Academic cyber-future, restrained, research-driven, not generic dark SaaS.
- **Current issue**: All primary pages now share the Future Lab OS direction. The next design work should be content accuracy and the details that make each public record more useful.

## Target Dials
- **Design variance**: Move from 6 to 8.
- **Motion intensity**: Move from 2-3 to 5.
- **Visual density**: Keep around 4.

## Signature Upgrade Plan

### Phase 1: Hero Recomposition
Status: implemented on `src/index.html`; now entering a sharpening pass after live screenshot review.

- Rebuild the home hero around a memorable research identity, not only a standard left-text/right-image split.
- Candidate headline direction: `Regeneration, decoded at single-cell resolution`.
- Compress the subtext to one clear sentence about vascular skin aging, single-cell omics, AI methods, and regenerative medicine.
- Turn the visual area into a research collage:
  - portrait
  - vascular or skin-aging image
  - small single-cell dot matrix panel
  - structural labels for AI4Med, Skin Aging, and Regeneration
- Add a compact research axis under the hero:
  - `single-cell omics`
  - `endothelial senescence`
  - `regenerative medicine`
  - `browser tools`

### Phase 1A: Hero Sharpening Pass
Status: implemented on `src/index.html` and `src/css/style.css` after local desktop and mobile screenshot review.

- Keep the current identity, but make the first screen more precise and less heavy.
- Shorten or rebalance the headline so the desktop hero reads in roughly 2-3 lines.
- Shift CTA language from generic portfolio copy to system-entry copy.
- Tune the collage so the portrait and vascular aging image stay primary while the dot matrix, labels, and axis become quieter supporting structure.
- Preserve small-radius visual rules and avoid soft rounded rectangles for research image assets.
- Keep the section below the hero slightly discoverable on common desktop viewports.

### Phase 1B: Future Lab OS Homepage
Status: implemented on `src/index.html`, `src/css/style.css`, and `src/js/site.js`.

- Rebuilt the homepage around a `Regeneration OS` hero instead of the earlier split collage hero.
- Replaced the old research focus block with a translational research loop.
- Reframed BioTools as browser instruments with input, analysis, and export flow.
- Reworked news into a compact signal feed.
- Added atlas scan motion, cell-matrix pulse, hover depth, and reveal targets while keeping reduced-motion support.
- Kept page URLs, navigation, real research assets, and the existing dark academic theme stable.

### Phase 1C: Research OS Modules
Status: implemented on `src/research.html`, `src/css/style.css`, and `src/js/site.js`.

- Rebuilt Research as an OS-style module page rather than a proposal-like brief page.
- Added a first-screen research module hero using real vascular aging and vHFO assets.
- Added a module rail for:
  - `Skin Axis`
  - `Follicle Repair`
  - `Validation`
- Converted each project into a visual module board with Question, Model, Computation, and Translation panels.
- Kept Chinese summaries in compact disclosure panels.
- Added responsive handling for desktop, tall desktop, tablet, and mobile.
- Added scroll reveal targets and restrained hover motion while preserving reduced-motion support.

### Phase 1D: BioTools Control Room
Status: implemented on `src/tools.html`, `src/css/style.css`, and `src/js/site.js`.

- Rebuilt Tools as a BioTools control room rather than a standard tool directory.
- Added a first-screen runtime console for local-file, no-login, WASM-oriented workflows.
- Reframed ElementPrism and DEG Analysis as live instrument stations.
- Added an analysis loop section for Input, Compute, and Output.
- Kept pathway enrichment as the next planned instrument.
- Added responsive handling and reveal targets while preserving reduced-motion support.

### Phase 1E: Knowledge Atlas
Status: implemented and locally verified on 1440px desktop, 390px mobile, and 390px tall mobile screenshots. Commit and deployed-site verification remain before the checkpoint closes.

- Rebuilt `/knowledge` as a Knowledge System rather than a sidebar index.
- Added an asset-led atlas hero, three research-track routes, a search command strip, and a grouped note ledger.
- Preserved every existing note route and Chinese note title.
- Added segmented filters for all notes, AI x Single-cell, Skin aging, and AI4Med.
- Extended the lightweight motion system with Knowledge route and ledger reveals, while retaining reduced-motion support.

### Phase 1F: Publications OS Ledger
Status: implemented and locally verified on 1440px desktop, 390px mobile, and 390px tall mobile screenshots. Commit and deployed-site verification remain before the checkpoint closes.

- Rebuilt `/publications` as a public-record system rather than a generic output list.
- Added an evidence-led hero using the existing vHFO experimental-design asset.
- Added a public-record protocol so citations, authorship, links, and public materials are never invented.
- Rebuilt manuscripts, conference materials, and technical notes as separate readiness-aware output records.
- Added a release route for future citable records and preserved the direct `/tools` route for technical methods.
- Extended lightweight motion with Publications reveal targets and restrained hover states.

### Phase 2: Research Page Editorial Rewrite
Status: superseded by Phase 1C while preserving the same project content and bilingual summaries.

- Reframe each major project as an editorial research brief instead of proposal-style long-form copy.
- For every project, use the same four-part structure:
  - `Core Question`
  - `Model System`
  - `Computational Layer`
  - `Translational Angle`
- Keep bilingual support, but make English the primary scanning layer.
- Move long Chinese explanatory text into secondary notes or compact panels.

### Phase 3: Layout Rhythm Upgrade
Status: implemented on `src/tools.html`, `src/knowledge.html`, and `src/publications.html`.

- Reduce repeated card grids.
- Use mixed layouts:
  - one large visual panel
  - narrow structured notes
  - research plates
  - timeline or sparse list for news
  - tool cards only where they behave like product entries
- Avoid making every section a rounded card.
- Ensure each major homepage section has a distinct layout family.

### Phase 4: Light Motion Layer
Status: implemented with lightweight scroll reveal in `src/js/site.js`.

- Add restrained motion only where it clarifies hierarchy.
- Recommended effects:
  - hero text and visual layer entrance
  - section reveal on first viewport entry
  - image clip or opacity reveal
  - more tactile button and card hover states
- All motion must honor `prefers-reduced-motion`.
- Avoid scroll hijacking or heavy animation libraries unless the page is intentionally rebuilt for scroll storytelling.

### Phase 5: Performance and Deployment Hygiene
Status: partially implemented with main-page meta tags, `robots.txt`, and `sitemap.xml`.

- Keep WebP versions for public-facing research images.
- Remove unreferenced large PNG files after confirming WebP replacements are live.
- Preserve original source images outside the deployable `public/` tree if they are needed for editing.
- Run before deployment:
  - `npm run build`
  - local HTML asset reference check
  - live checks for `/`, `/research`, `/tools`, `/knowledge`

## Taste-Skill Guardrails
- No AI-purple gradients or generic neon glow.
- No repeated three-card feature rows as the default structure.
- No fake social proof, fake metrics, or invented precision.
- No decorative scroll cues, section-number eyebrows, or version labels.
- No em dash or en dash in visible page copy.
- Hero must fit the initial viewport.
- Navigation must stay one line on desktop.
- Real images are required for major portfolio/landing sections.

## Success Criteria
- A first-screen screenshot should feel recognizably like Jackson Dai's academic research brand.
- Research should be scannable in 30 seconds.
- The site should feel more like a personal research system than a generic SaaS landing page.
- Main pages should preserve current URLs and Cloudflare Pages deployment behavior.
- The homepage hero should feel sharp, controlled, and interface-like rather than simply large.

## Implementation Notes
- Homepage hero now uses a portrait, research image, single-cell dot matrix, and compact research axis.
- Homepage research section now uses a translational loop layout instead of repeated cards.
- Research page now presents each project as a four-part editorial brief with Chinese summaries in compact disclosure panels.
- Tools page now presents BioTools as a control room with a runtime console, live instrument stations, an analysis loop, and a next-instrument panel.
- Knowledge page now presents a searchable research atlas with track filters, visible-result status, and a grouped public-note ledger.
- Publications page now presents scholarly output as a conservative ledger without fake metrics or invented bibliographic claims.
- Main page-level layouts for Research, Tools, Knowledge, and Publications are consolidated in `src/css/style.css` instead of inline page styles.
- Main pages now include descriptions, canonical URLs, Open Graph tags, and Twitter card metadata.
- `public/robots.txt` and `public/sitemap.xml` are present for deployment.
- Main pages now load `src/js/site.js` for reduced-motion-aware scroll reveal on research, tool, knowledge, publication, and homepage entries.
- Homepage Phase 1A shortened the hero headline, changed the primary CTA to `Open Research System`, reduced collage crowding, softened first-frame animation opacity loss, and tightened mobile navigation spacing.
- Homepage Phase 1B rebuilt the first page as a Future Lab OS with atlas hero, semantic route grid, translational research loop, BioTools instrument dock, and signal feed.
- Research Phase 1C rebuilt `/research` as a Future Lab OS module page with a module rail, visual research orbit, module boards, validation route panels, and responsive screenshot QA.
- Tools Phase 1D rebuilt `/tools` as a BioTools Control Room with a runtime console, live stations for ElementPrism and DEG Analysis, an analysis loop, and pathway enrichment as the next instrument.
- Knowledge Phase 1E rebuilt `/knowledge` as a Knowledge Atlas with an existing single-cell integration asset, a search command strip, research-track filters, and an indexed three-track note ledger.
- Publications Phase 1F rebuilt `/publications` as an evidence-led output ledger with a public-record protocol, readiness-aware output records, and a release route for future citations.
