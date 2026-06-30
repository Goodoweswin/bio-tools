# Deployment Guide

## Production
- **Live domain**: `https://daiger.top/`
- **Hosting**: Cloudflare Pages
- **Source branch**: `main`
- **Build command**: `npm run build`
- **Build output**: `dist/`

## Local Workflow
```bash
npm install
npm run dev
npm run build
```

## Pre-Deploy Checklist
- Run `npm run build`.
- Confirm `dist/` includes:
  - `index.html`
  - `research.html`
  - `tools.html`
  - `knowledge.html`
  - all `dist/knowledge/**/*.html` article pages
  - `tools/stat_analysis/index.html`
  - `tools/deg/index.html`
- Run a local asset reference check for generated HTML.
- Confirm no visible placeholder links remain, especially `href="#"`.
- Confirm no old identity strings remain, such as `DAIGER` or `NEVER BORED`.

## Live Smoke Test
After Cloudflare Pages deploys, verify:
- `https://daiger.top/`
- `https://daiger.top/research`
- `https://daiger.top/tools`
- `https://daiger.top/knowledge`
- `https://daiger.top/knowledge/ai-single-cell/annotation`
- `https://daiger.top/tools/stat_analysis/`
- `https://daiger.top/tools/deg/`
- `https://daiger.top/assets/cv.pdf`

Cloudflare Pages may redirect `.html` URLs to pretty URLs, for example `/research.html` to `/research`. This is expected.

## Tool Runtime Notes
- Tool apps are under `public/tools/`.
- Stlite/Pyodide is loaded through local Stlite assets plus CDN Pyodide, depending on the tool entry page.
- Do not remove `public/tools/assets/` without testing both tools.

## Deployment Risks
- Large public assets increase Cloudflare upload and cache size.
- The Python tools may depend on CDN access for first load.
- Knowledge articles must be added to `vite.config.js` if new standalone HTML pages are created under `src/knowledge/`.
