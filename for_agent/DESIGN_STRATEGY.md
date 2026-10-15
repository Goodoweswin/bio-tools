# Design Strategy

## Current Direction: A Researcher's Website
Updated: 2026-10-16. This direction supersedes the previous Future Lab OS design.

Jackson Dai should be the first thing a visitor understands, followed by the research questions, useful tools, and writing. The site is a personal research portfolio, not a fictional operating system.

The Virtual Cell Challenge site (https://virtualcellchallenge.org/) informed the clarity, open composition, and immediate subject recognition. Its brand, illustrations, and content were not copied.

## Voice
- Lead with literal names: Jackson Dai, Research, Tools for biological data, Research notes.
- Explain specialist terms when introducing them. Keep detailed mechanisms in project sections.
- Prefer questions and testable hypotheses to claims about reversing aging or controlling regeneration.
- Remove OS, ledger, runtime, protocol, semantic index, and signal-feed metaphors from visitor-facing navigation.
- Keep English as the main navigation language and Chinese research summaries and notes.
- No invented citations, dates, metrics, outcomes, or affiliations.

## Page Decisions
- Home: full-width conceptual skin illustration, name and plain introduction; separate full-color portrait and biography; two research questions; tools; updates.
- Research: two project questions, approach, full-aspect-ratio scientific figures, captions that distinguish proposed models from demonstrated results; optional supporting diagrams and Chinese summaries.
- Tools: the two existing tool launch links appear immediately. Pathway enrichment remains explicitly planned.
- Notes: search and category filters lead directly into the 12 original articles. This is keyword matching, not semantic search.
- Publications: concise work-in-progress and availability statements, not a hero about publishing rules.
- Article reading: shared light theme, readable code blocks, horizontally scrollable wide tables.
- Assistant: a quiet entry, labeled controls, focus return, Escape dismissal, and no keyboard access to closed content.

## Visual Principles
- White and cool gray surfaces; charcoal text; a restrained green accent.
- Coral and natural portrait colors come from actual imagery, not background effects.
- No glowing grids, scanning lines, decorative dots, stacked glass cards, or grayscale portraits.
- Figures remain square-cornered and uncropped. Captions belong outside the image.
- Section layouts are unframed. Borders separate content; they do not turn every section into a card.
- Type sizes use fixed rem values and explicit breakpoints, never viewport-scaled fonts.
- Content is visible without scroll animation or JavaScript.
- Respect reduced motion. Keep hover feedback short and quiet.

## Checkpoints
Do not advance past a failed checkpoint.

1. Direction and copy: complete. Approved by the owner; direct language and a lighter research-led style.
2. Implementation: complete. Five main pages, shared components, article reading styles, and keyword filtering.
3. Local verification: complete. Production build, 66 browser checks, 40 local links/assets, responsive screenshot review, and sitemap validation passed. See TEST_CHECKLIST.md for evidence and limits.
4. Commit and release: owner authorized commit and push on 2026-10-16. Deployed-site verification remains pending; a successful Git push alone does not close this checkpoint.

## Deliberate Limits
- Tool applications and scientific calculations are unchanged.
- No backend, RAG, provider, or authentication-policy migration.
- Existing scientific bitmaps are not rewritten. Their unresolved labels remain tracked in CONTENT_ACCURACY.md.
- The new homepage image is AI-generated editorial concept art, visibly identified as such, never experimental evidence. Provenance is in ASSET_POLICY.md.
- Citation records and public conference materials still require owner-provided sources.
