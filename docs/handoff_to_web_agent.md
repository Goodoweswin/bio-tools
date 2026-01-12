# Engineering Handoff: Stlite Bio-Analysis Tool

**Date:** 2026-01-06
**Project:** Offline Weight Analysis Tool
**Status:** Tested & Verified Locally (HTTP 8080)

## 1. Project Overview
This is a **Client-Side Only** (Static) web application built with **Stlite** (Streamlit on WebAssembly). It runs Python completely in the user's browser without a backend server.

## 2. File Artifacts for Transfer
Please transfer the entire **`tools/`** directory. It contains three critical subfolders:
*   `tools/weight_analysis/`: The actual application code (`app.py`) and entry point (`index.html`).
*   `tools/assets/`: Local mirror of Pyodide, Stlite, and Python Wheels (`seaborn`, `openpyxl`, etc.). **DO NOT CLEAN OR MINIFY THIS FOLDER**. These files are strictly version-matched.
*   `tools/common/`: Shared styling scripts.
*   `tools/_headers`: Configuration file for Cloudflare Pages (MIME types).

## 3. Deployment Requirements (Cloudflare Pages)

### A. MIME Types (Critical)
Cloudflare Pages must serve `.wasm` and `.whl` files with the correct Content-Type, or the browser will block them.
*   I have created a `_headers` file in the `tools/` directory.
*   **Action**: Ensure this `_headers` file ends up in the **publish directory** (output root) of the website.

### B. Directory Structure & Paths
The application heavily relies on **absolute paths** to load assets.
*   **Current Config**: `index.html` expects assets to be at `/tools/assets/...`.
*   **Requirement**: The `tools` folder **must** be placed at the **root** of the website's public directory.
    *   Correct URL: `https://your-site.com/tools/weight_analysis/index.html`
    *   Correct Asset URL: `https://your-site.com/tools/assets/stlite/...`
*   **If you move it**: If you need to place the tool in a sub-path (e.g., `site.com/apps/tools/...`), you **MUST** perform a Find & Replace in `tools/weight_analysis/index.html`:
    *   Find: `/tools/assets/`
    *   Replace: `/apps/tools/assets/` (or your new relative path)

## 4. Integration Guide
1.  **Copy**: Drop the `tools` folder into your repository's public/static folder.
2.  **Link**: Add a link on your main landing page pointing to `/tools/weight_analysis/index.html`.
3.  **Deploy**: Git push. Cloudflare Pages will handle the rest.

## 5. Potential Pitfalls
*   **Git LFS**: The `tools/assets` folder contains binary files. Check if your repo has size limits.
*   **Caching**: If you update `app.py`, users might see the old version. On Cloudflare, you may need to purge cache or append a query string (e.g., `app.py?v=2`) in `index.html` if updates don't show.
