# Engineering Handoff

Updated: 2026-10-16.

## Current State
- Repository: `/home/y417954/biotools/bio-tools`
- Owner / public name: Jackson Dai
- Live site: https://daiger.top/
- Deployment: GitHub main to Cloudflare Pages.
- Current local change: light, research-led redesign replacing Future Lab OS.
- Owner authorized commit and push on 2026-10-16. Check Git history and the remote for transport status; do not infer deployment from a local build or a successful push.
- Checkpoint 3 (local QA) is complete: production build, 66 browser checks, 40 local links/assets, screenshot review, and sitemap validation passed. Checkpoint 4 is authorized but remains open until deployed-site verification.

## Site Shape
- Home: Jackson Dai, skin-aging introduction, full-bleed conceptual illustration, original-color portrait, research questions, tools, updates.
- Research: two questions with readable approaches, hypothesis-aware captions, Chinese summaries and optional diagrams.
- Tools: direct links to ElementPrism and DEG Analysis; pathway enrichment remains planned.
- Notes (existing `/knowledge` route): 12 original articles, keyword search, topic filtering, count, and reset state.
- Publications: concise current availability, no invented bibliographic records.
- Articles: light reading style; code and wide tables scroll within the page.
- Assistant: existing `/api/chat` contract; light UI, nonmodal dialog, labeled controls, Escape and focus handling. No backend changes.

## Files To Know
- `src/index.html`, `research.html`, `tools.html`, `knowledge.html`, `publications.html`
- `src/css/style.css`: central visual system, responsive rules, reduced motion.
- `src/js/site.js`: mobile menu, current route, notes keyword filtering.
- `src/styles/article.css`: shared reading layer for all 12 notes.
- `src/components/`: header, footer, assistant.
- `public/assets/skin-microvasculature-concept.webp`: new AI-generated editorial image.
- `for_agent/DESIGN_STRATEGY.md`: current design direction and checkpoints.
- `for_agent/DESIGN_SYSTEM.md`: current tokens and UI rules.
- `for_agent/CONTENT_ACCURACY.md`: scientific asset debt and required owner records.
- `for_agent/TEST_CHECKLIST.md`: verification scope.

## Guardrails
- Do not restore OS/ledger/system jargon from old roadmap entries.
- Keep the portrait in color and scientific diagrams uncropped.
- Do not silently change labels baked into scientific assets.
- No citation, journal, DOI, date, or result without a primary source.
- Keep the original note routes and working tool URLs.
- Do not revert user changes, change the backend, or modify tool calculations as part of styling.
- Never put tokens in chat or project files.

## Remaining Work
- Local QA is complete and commit/push is authorized. Local preview is available at http://127.0.0.1:61532/ while the preview server is running.
- After push, verify all five clean public URLs, article routes, tools, CV, and assistant on Cloudflare.
- The assistant's live API and Python/WASM tool runtime require separate deployed checks; a Vite preview does not prove these services work.
- Publication metadata and conference files require owner inputs.
- Existing research bitmaps contain unreviewed labels and depicted outcomes; revise source figures with scientific approval.
- Article scientific accuracy and runnable example code need a separate content review; this change addresses layout only.
