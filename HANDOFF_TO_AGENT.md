# Engineering Handoff: 2026-01-13

**Status**: Stable / Deployed
**Last Feature**: Bar Chart Module & Palette Enhancement
**Repository**: `bio-tools` (Cloudflare Pages)

## 1. Session Summary
Continued enhancing Bio-Analysis Suite with new visualization and UX features.
- **Bar Chart Module**: New `📊 条形图` with aggregation, error bars, and auto-statistcs (Mann-Whitney/Kruskal-Wallis).
- **Palette Upgrade**:
    - Renamed presets to intuitive Chinese names (e.g., "🔴 红蓝经典").
    - Added presets: 色盲友好, 灰度单色, 彩虹渐变.
    - Added "✏️ 自定义..." option for custom hex color input.
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
