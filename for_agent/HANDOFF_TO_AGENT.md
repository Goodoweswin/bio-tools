# Engineering Handoff

Updated: 2026-10-19.

## Current State
- Repository: `/home/y417954/biotools/bio-tools`
- Owner / public name: Jackson Dai
- Live site: https://daiger.top/
- Deployment: GitHub main to Cloudflare Pages.
- Current local change: resume-based content update on the existing light research-led design. See RESUME_CONTENT_UPDATE.md for current checkpoint states.
- Owner authorized commit and push on 2026-10-16. Check Git history and the remote for transport status; do not infer deployment from a local build or a successful push.
- Baseline redesign QA passed in the previous iteration. The 2026-10-19 resume update also passes build, 66 Firefox checks, 40 local links/assets, and desktop/mobile screenshot review. Its release checkpoint remains pending; earlier authorization does not describe a deployment of this update.

## Site Shape
- Home: Jackson Dai / 代杰, master's identity, full-bleed illustration, color portrait, research, tools, projects, education and experience, and confirmed activities.
- Research: two ongoing projects with dates, owner roles and contributions, hypothesis-aware captions, Chinese summaries, optional diagrams, and earlier research training.
- Tools: direct links to ElementPrism and DEG Analysis; pathway enrichment remains planned.
- Notes (existing `/knowledge` route): 12 original articles, keyword search, topic filtering, count, and reset state.
- Activities: resume-supported academic exchange, research, community work, and honors at the unchanged `/publications` route. No invented bibliographic records.
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
- The 2026-10-19 content update is locally verified. Owner requested a local Git commit on 2026-10-19; inspect Git history for its identifier. Push and deployed verification remain pending.
- Local previews are available at http://127.0.0.1:61531/ (development) and http://127.0.0.1:61532/ (production build) while the servers are running.
- After push, verify all five clean public URLs, article routes, tools, CV, and assistant on Cloudflare.
- The assistant's live API and Python/WASM tool runtime require separate deployed checks; a Vite preview does not prove these services work.
- Publication metadata and conference files require owner inputs.
- Existing research bitmaps contain unreviewed labels and depicted outcomes; revise source figures with scientific approval.
- Article scientific accuracy and runnable example code need a separate content review; this change addresses layout only.
