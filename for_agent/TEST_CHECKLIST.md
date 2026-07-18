# Test Checklist

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
