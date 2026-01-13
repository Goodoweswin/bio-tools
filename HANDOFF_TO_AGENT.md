# Engineering Handoff: 2026-01-12

**Status**: Stable / Deployed
**Last Feature**: Upgraded to Bio-Analysis Suite v4.0 & Added DEG Tool Scaffold
**Repository**: `bio-tools` (Cloudflare Pages)

## 1. Session Summary
We upgraded the analysis capabilities and optimized the deployment architecture.
- **Upgrade**: `stat_analysis` is now **Bio-Analysis Suite v4.0** (Survival, Heatmap, PCA).
- **Architecture**: Implemented **Hybrid Loading**:
    - **CDN**: Standard heavy libraries (scipy, pandas, numpy) load from jsDelivr (Bypasses 25MB limit).
    - **Local**: Custom logic (`app.py`) and small wheels (`pypi/`) load from `public/tools/assets/`.
- **New Tool**: Created `public/tools/deg/` (Volcano Plot) scaffold.

## 2. Current Architecture
- **Frontend**: Vite + HTML/JS.
- **Tools**: Client-side Python (Pyodide/Stlite) via Hybrid Loading.
    - **Workbench**: `/tools/stat_analysis/index.html` -> `app.py` (v4.0).
    - **DEG Tool**: `/tools/deg/index.html` -> `app.py` (Placeholder).
- **Backend**: Cloudflare Pages Functions (`/api/chat`).

## 3. Next Steps (Prioritized)

### A. DEG Tool Development (Immediate)
- The file `public/tools/deg/app.py` is currently a basic template.
- **Action**: Implement full Volcano Plot logic (using matplotlib/seaborn) similar to `stat_analysis`.
- **Assets**: Reuse `tools/assets` for local wheels if needed.

### B. RAG Implementation
- (Carry over from previous) Enable Cloudflare Vectorize and build ingestion script for `public/knowledge/`.

### C. Content & UI
- Populate `public/knowledge` (Feed the RAG).
- Improve Chat UI (Add Markdown rendering/Highlight.js).

## 4. Operational Notes
- **Git**: `.gitignore` is updated. Do not commit large system/cache files.
- **Deploy**: Cloudflare Pages builds automatically on push to `main`.
- **Debugging**: If tool fails to load, check Browser Console for CDN connectivity issues.
