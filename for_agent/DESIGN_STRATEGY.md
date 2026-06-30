# Design Strategy

## Current Design Read
- **Site type**: Personal academic portfolio plus browser-based bioinformatics toolkit.
- **Audience**: Research collaborators, mentors, clinicians, wet-lab users, and visitors evaluating credibility.
- **Vibe**: Academic cyber-future, restrained, research-driven, not generic dark SaaS.
- **Current issue**: The site is clean and coherent, but still reads a little template-like because the hero, card rhythm, and research structure are conventional.

## Target Dials
- **Design variance**: Move from 6 to 8.
- **Motion intensity**: Move from 2-3 to 5.
- **Visual density**: Keep around 4.

## Signature Upgrade Plan

### Phase 1: Hero Recomposition
Status: implemented on `src/index.html`.

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

### Phase 2: Research Page Editorial Rewrite
Status: implemented on `src/research.html`.

- Reframe each major project as an editorial research brief instead of proposal-style long-form copy.
- For every project, use the same four-part structure:
  - `Core Question`
  - `Model System`
  - `Computational Layer`
  - `Translational Angle`
- Keep bilingual support, but make English the primary scanning layer.
- Move long Chinese explanatory text into secondary notes or compact panels.

### Phase 3: Layout Rhythm Upgrade
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
- Add restrained motion only where it clarifies hierarchy.
- Recommended effects:
  - hero text and visual layer entrance
  - section reveal on first viewport entry
  - image clip or opacity reveal
  - more tactile button and card hover states
- All motion must honor `prefers-reduced-motion`.
- Avoid scroll hijacking or heavy animation libraries unless the page is intentionally rebuilt for scroll storytelling.

### Phase 5: Performance and Deployment Hygiene
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

## Implementation Notes
- Homepage hero now uses a portrait, research image, single-cell dot matrix, and compact research axis.
- Homepage research section now uses a translational loop layout instead of repeated cards.
- Research page now presents each project as a four-part editorial brief with Chinese summaries in compact disclosure panels.
