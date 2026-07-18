# Engineering Handoff

## Current Status
- **Project**: Jackson Dai personal research website plus browser BioTools.
- **Repository**: `/home/y417954/biotools/bio-tools`.
- **Public URL**: `https://daiger.top/`.
- **Deployment**: GitHub main branch to Cloudflare Pages.
- **Latest verified build command**: `./node_modules/.bin/vite build`.

## Current Site Shape
- `/` is a Future Lab OS-style landing page with atlas hero, route grid, research loop, BioTools dock, and signal feed.
- `/research` is a Future Lab OS-style module page with research orbit, module rail, visual project boards, validation routes, and compact Chinese summaries.
- `/tools` is a BioTools Control Room with runtime console, live instrument stations, analysis loop, and next-instrument panel.
- `/knowledge` is a Knowledge Atlas with a real single-cell integration visual, a search command strip, segmented filters, research routes, and a grouped index of 12 research notes.
- `/publications` is a conservative scholarly output ledger.
- `/tools/stat_analysis/index.html` serves ElementPrism.
- `/tools/deg/index.html` serves DEG Analysis.

## Design System Notes
- Primary design language: academic, precise, restrained, research-led.
- Avoid generic SaaS softness, large rounded cards, fake metrics, and decorative hype.
- Main styling is centralized in `src/css/style.css`.
- Main pages should not reintroduce page-local `<style>` blocks unless there is a strong reason.
- Shape language:
  - small controls: 3px radius
  - panels: 6px radius
  - large visual panels: 8px radius
  - research images should generally stay square or near-square
  - tags and dot markers may stay fully rounded
- Motion is handled by `src/js/site.js` and must continue to honor `prefers-reduced-motion`.

## Files To Know
- `src/index.html`: homepage content structure.
- `src/research.html`: research project structure.
- `src/tools.html`: BioTools workbench page.
- `src/knowledge.html`: searchable Knowledge Atlas and grouped note ledger.
- `src/publications.html`: scholarly output ledger.
- `src/css/style.css`: central visual system.
- `src/js/site.js`: lightweight scroll reveal.
- `public/robots.txt`: search crawler policy.
- `public/sitemap.xml`: public route map.
- `for_agent/DESIGN_STRATEGY.md`: design plan and implementation notes.
- `for_agent/DESIGN_SYSTEM.md`: visual rules.
- `for_agent/SEO_CHECKLIST.md`: SEO status.
- `for_agent/DEPLOYMENT.md`: deployment notes.
- `for_agent/ASSET_POLICY.md`: image and asset policy.
- `for_agent/TEST_CHECKLIST.md`: verification checklist.

## Verification Checklist
Run before pushing:
```bash
./node_modules/.bin/vite build
git diff --check
xmllint --noout public/sitemap.xml
```

After pushing, check:
- `https://daiger.top/`
- `https://daiger.top/research`
- `https://daiger.top/tools`
- `https://daiger.top/knowledge`
- `https://daiger.top/publications`
- `https://daiger.top/robots.txt`
- `https://daiger.top/sitemap.xml`

## Known Open Work
- Phase 1B homepage Future Lab OS redesign has been implemented and locally verified with 1440px desktop and 390px mobile screenshots.
- Phase 1C Research OS module redesign has been implemented and locally verified with 1440px desktop, 1440px tall desktop, and 390px mobile screenshots.
- Phase 1D Tools Control Room redesign has been implemented and locally verified with 1440px desktop, 1440px tall desktop, and 390px mobile screenshots.
- Phase 1E Knowledge Atlas redesign has been implemented and locally verified with 1440px desktop, 390px mobile, and 390px tall mobile screenshots. It must be committed, pushed, and checked on the deployed site before Publications work begins.
- Phase 1A homepage hero sharpening has been implemented and locally verified with 1440px desktop and 390px mobile screenshots.
- Phase 2 content accuracy has started: public text now reframes `NRX` as candidate endothelial regulators, while image-embedded labels remain unchanged until image assets are revised.
- After deployment, recheck the live homepage and research page at `https://daiger.top/` to confirm Cloudflare has served the new build.
- Do not begin the Publications OS work until the Knowledge Atlas checkpoint is committed, pushed, and verified at `https://daiger.top/knowledge`.
- Decide whether image-embedded `NRX` labels should be revised in the underlying figure assets.
- Add real publications, posters, abstracts, or links when cleared for public sharing.
- Add tool documentation for accepted input formats, demo datasets, and validation assumptions.
- Consider adding a pathway enrichment module as the next BioTools entry.
- Consider per-article SEO descriptions for `src/knowledge/**`.
- Consider generating `sitemap.xml` automatically once content grows.

## Git Notes
- Do not revert user changes without explicit permission.
- Keep unrelated dirty files out of commits.
- If push fails due GitHub credentials in the agent environment, ask the user to run:
```bash
cd /home/y417954/biotools/bio-tools
git push origin main
```
