# Test Checklist

## Reproducible Browser Check
`scripts/check-ui.mjs` uses Node 22+ and Firefox WebDriver BiDi without adding production dependencies. Run against a production preview as well as the dev server.

Build first, then start the preview in a separate terminal:
```bash
npm run build
npm run preview -- --host 127.0.0.1 --port 4173 --strictPort
```

Start a dedicated test browser profile in another terminal; do not use a personal profile:
```bash
mkdir -p /tmp/daiger-ui-profile
firefox --headless --no-remote --profile /tmp/daiger-ui-profile --remote-debugging-port 9224 about:blank
```

Run the checks:
```bash
BASE_URL=http://127.0.0.1:4173 node scripts/check-ui.mjs
```

- `BIDI_URL` overrides the default `ws://127.0.0.1:9224/session`.
- `QA_OUTPUT` overrides the default `/tmp/daiger-ui` screenshot and JSON report folder.
- Nonzero exit status blocks the local verification checkpoint.
- Inspect the screenshots too: DOM overflow tests cannot detect artwork behind text.
- Current suite also checks all four self-hosted font faces, M.D. student identity, submitted-work role/status, and full-width mobile biography. The next-section hint uses the first About content element, including the stacked portrait on mobile.
- Stop the dedicated Firefox process after verification.
- The script mocks assistant success and 401 responses. It does not validate the live AI provider or run Python/WASM calculations.

Coverage: five pages at 320, 390, 768, 1440, and 1920px; short-screen homepage checks; mobile menu/Escape; keyword and topic filters; empty reset; all 12 articles; full-aspect-ratio research images; local links/assets; assistant focus and response rendering.

## Latest Local Verification: 2026-10-16
- Production build passed, along with `git diff --check` and `xmllint --noout public/sitemap.xml`.
- `scripts/check-ui.mjs` completed with 66/66 checks passing against `http://127.0.0.1:61532/`.
- 40 unique local links/assets passed, including image and PDF content-type checks and internal anchors.
- Five primary pages checked at 320, 390, 768, 1440, and 1920px widths; no horizontal overflow or missing current-page state.
- Short-screen homepage checked at 320x568, 390x667, and 1440x768; next-section content remains visible.
- All 12 articles loaded with the light reading layer; batch-correction table overflow was fixed.
- All research figures and homepage lazy-loaded images decoded; scientific image proportions were preserved.
- Mobile menu, Escape/focus return, English/Chinese search, topic filters, empty reset, assistant success and 401 UI states passed.
- Core text/control contrast pairs are 14.59:1, 6.49:1, 4.69:1, and 6.81:1. This is not a claim of a full accessibility audit.
- Screenshots and machine-readable report: `/tmp/daiger-ui-production/`. These are local artifacts; rerun the script to regenerate.
- Known limits: Firefox-only visual verification; no live deployment, real assistant API, or Python/WASM calculations were tested in this pass. Tool application files and backend are unchanged.

## Before Every Commit
```bash
npm run build
```

Check:
- build completes without Vite HTML parse errors
- no missing local references in generated HTML
- no accidental changes to unrelated files

## Static Checks
Recommended scans:
```bash
rg "href=\"#\"" src public
rg "DAIGER|NEVER BORED" src public
rg "—|–" src public
```

Interpret carefully:
- Tool Python code may contain emojis or UI strings by design.
- Generated `dist/` should not be edited directly.

## Main Page Smoke Test
Local:
- `/`
- `/research.html`
- `/tools.html`
- `/knowledge.html`
- `/publications.html`

Live:
- `https://daiger.top/`
- `https://daiger.top/research`
- `https://daiger.top/tools`
- `https://daiger.top/knowledge`
- `https://daiger.top/publications`

## Knowledge Page Smoke Test
Verify at least:
- `/knowledge.html`
- `/knowledge/ai-single-cell/annotation`
- `/knowledge/skin-aging/fibroblast`
- `/knowledge/ai4med/drug-screening`

Confirm:
- search accepts English, Chinese, and method-specific terms
- each segmented track filter updates the visible-note count and hides empty groups
- all 12 note links still point to their original article pages
- article CSS loads
- back link works
- code blocks are readable
- no broken local assets

## Publications Page Smoke Test
Verify:
- `/publications.html`
- manuscript, conference, and technical-method anchors work
- technical-method record still links to `/tools`

Confirm:
- no citation count, venue claim, or bibliographic record is shown without a public source
- readiness labels remain explicit
- desktop and mobile record layouts do not overlap

## Tool Smoke Test
Verify:
- `/tools/stat_analysis/`
- `/tools/deg/`

Check:
- entry page loads
- back-to-tools link works
- loading state is visible
- app starts or fails with a readable error

## Visual QA
Desktop:
- nav remains one line
- hero fits initial viewport
- CTAs are visible without scrolling
- cards and images do not overlap

Mobile:
- nav remains usable
- hero text does not overflow
- buttons do not wrap awkwardly
- research images remain legible

## Live Verification Commands
Use when network access is available:
```bash
curl -L -o /dev/null -s -w "%{http_code} %{url_effective}\n" https://daiger.top/
curl -L -o /dev/null -s -w "%{http_code} %{url_effective}\n" https://daiger.top/research.html
curl -L -o /dev/null -s -w "%{http_code} %{url_effective}\n" https://daiger.top/tools.html
curl -L -o /dev/null -s -w "%{http_code} %{url_effective}\n" https://daiger.top/knowledge/ai-single-cell/annotation.html
```
