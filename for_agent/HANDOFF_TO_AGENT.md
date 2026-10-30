# Engineering Handoff

Updated: 2026-10-30.

## Current State
- Repository: `/home/y417954/biotools/bio-tools`
- Owner / public name: Jackson Dai
- Live site: https://daiger.top/
- Deployment: GitHub main to Cloudflare Pages.
- Current change: personal-showcase structure replacing the resume-heavy homepage. See PERSONAL_SHOWCASE_UPDATE.md for current gates. Owner authorized implementation, commit, and push on 2026-10-30.
- Owner authorized commit and push for this update on 2026-10-30. Check Git history and the remote for transport status; do not infer deployment from a local build or a successful push.
- Current local QA passed: production build, 119 Firefox checks, 51 local links/assets, fonts loaded, seven public pages, sitemap XML, and desktop/mobile/short-screen screenshots. Current report: `/tmp/daiger-showcase-qa/`. Live deployment still requires independent verification.

## Site Shape
- Home: brief introduction, secondary M.D. student identity, three selected works, three note links, and personal About/contact. Credentials remain off the homepage.
- Work: new `/work` index; direct launch links for working tools, research details, and studio link.
- About: new `/about` biography and bilingual CV, with optional collapsed background and contact.
- Research: two ongoing projects with dates, owner roles and contributions, hypothesis-aware captions, Chinese summaries, optional diagrams, and earlier research training.
- Tools: direct links to ElementPrism and DEG Analysis; pathway enrichment remains planned.
- Notes (existing `/knowledge` route): 12 original articles, keyword search, topic filtering, count, and reset state.
- Research records: existing `/publications` route and incoming anchors retain manuscript/conference detail; credential-only public lists have been removed. Primary navigation groups these and Research/Tools under Work.
- Articles: light reading style; code and wide tables scroll within the page.
- Assistant: existing `/api/chat` contract; light UI, nonmodal dialog, labeled controls, Escape and focus handling. No backend changes.

## Files To Know
- `src/index.html`, `work.html`, `about.html`, `research.html`, `tools.html`, `knowledge.html`, `publications.html`
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
- Current presentation gates are tracked in PERSONAL_SHOWCASE_UPDATE.md; no historical resume plan should restore the removed homepage lists.
- The 2026-10-29 update is authorized for commit/push after local QA; track its current gates in MD_TYPOGRAPHY_UPDATE.md. Current PDFs supersede older source facts, including identity and football results.
- Previous resume and bilingual-CV updates were pushed as `096893f` and `0ae0647`. The current update's transport status belongs in Git history; deployed verification remains open.
- Local previews are available at http://127.0.0.1:61531/ (development) and http://127.0.0.1:61532/ (production build) while the servers are running.
- After push, verify all five clean public URLs, article routes, tools, CV, and assistant on Cloudflare.
- The assistant's live API and Python/WASM tool runtime require separate deployed checks; a Vite preview does not prove these services work.
- The submitted-work contribution and conference titles are supplied in the current resumes. A full citation, journal/DOI, and public conference files still require primary records.
- Existing research bitmaps contain unreviewed labels and depicted outcomes; revise source figures with scientific approval.
- Article scientific accuracy and runnable example code need a separate content review; this change addresses layout only.
