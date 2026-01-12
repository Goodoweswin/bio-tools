# Engineering Handoff: 2026-01-09

**Status**: Stable / Deployed
**Last Feature**: Integrated "Weight Analysis Tool" (Stlite/WASM)
**Repository**: `bio-tools` (Cloudflare Pages)

## 1. Session Summary
We successfully integrated the offline-capable Python analysis tool into the main website. 
- **Migration**: Moved Stlite app to `public/tools/stat_analysis/`.
- **Infrastructure**: Configured `_headers` for WASM MIME types.
- **Critical Fix**: Encountered Cloudflare's 25MB file limit with local Pyodide wheels. **Switched to Hybrid Architecture**:
    - `app.py` & custom wheels -> Hosted locally.
    - Pyodide Runtime & SciPy/NumPy -> Loaded via CDN (`cdn.jsdelivr.net`).
- **Docs**: Updated `CHANGELOG.md`, `PROJECT_MANIFEST.md`, and created `public/tools/ARCHITECTURE_NOTE.md`.

## 2. Current Architecture
- **Frontend**: Vite + HTML/JS.
- **Tools**: Client-side Python (Pyodide/Stlite).
    - Config: `public/tools/stat_analysis/index.html` (Points to CDN).
    - Code: `public/tools/stat_analysis/app.py`.
- **Backend (Chat)**: Cloudflare Pages Functions (`/api/chat`).

## 3. Next Steps (Prioritized)

### A. RAG Implementation (Top Priority)
The chat assistant needs knowledge base access.
1.  **Infrastructure**: Enable Cloudflare Vectorize in Dash.
2.  **Ingestion**: Write a script (Node.js/Python) to:
    - Read Markdown/HTML in `public/knowledge/`.
    - Chunk text.
    - Generate Embeddings (via Workers AI `bge-base-en-v1.5`).
    - Upsert to Vectorize.
3.  **Retrieval**: Modify `functions/api/chat.js` to query Vectorize before calling the LLM.

### B. New Tool: DEG Analysis (Volcano Plot)
Reficate the success of the Weight Tool.
- Use the **same `public/tools/` structure**.
- Copy `stat_analysis/index.html` as a template (keep the CDN config!).
- Implement `app.py` for Volcano Plots (using `matplotlib` or `altair`).

### C. Content & UI
- Populate `public/knowledge` (Feed the RAG).
- Improve Chat UI (Add Markdown rendering/Highlight.js).

## 4. Operational Notes
- **Git**: `.gitignore` is updated. Do not commit large system/cache files.
- **Deploy**: Cloudflare Pages builds automatically on push to `main`.
- **Debugging**: If tool fails to load, check Browser Console for CDN connectivity issues.
