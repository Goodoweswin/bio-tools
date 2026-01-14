# Engineering Handoff: 2026-01-13

**Status**: Stable / Cloudflare Compatible (Offline Package Archived)
**Last Feature**: Scientific Plotting Upgrade & Offline Mirroring
**Repository**: `bio-tools` (Main branch reverted to lightweight state)

## 1. Session Summary
Completed major visual upgrades for publication-grade charts and solved critical deployment constraints.
- **Visuals**: Implemented "Single Metric Mode" and "Sci Palette" for Bar/Box plots, matching top-tier journal aesthetics.
- **Infrastructure**:
    - Encountered Cloudflare 25MB limit with local Scipy wheel.
    - **Solution**: Reverted git to lightweight state (Scipy via CDN) for Cloudflare.
    - **Deliverable**: Generated `bio-tools-server-deploy.zip` (full offline bundle) for private server deployment.

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
- **Git Strategy**: Keep repo lightweight (<100MB). Do NOT commit large wheels (Scipy) directly. Use `enable_offline_mode.py` on server to fetch them.
- **Offline Package**: A full backup is at `/home/cy410080/biotools/bio-tools-server-deploy.zip`.
- **Debugging**: If Cloudflare fails, check if `scipy` was accidentally committed locally.
