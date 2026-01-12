# Project Changelog

All notable changes to the **Bio-Tools** project will be documented in this file.

## [Unreleased]
- **Planned**: Interactive Volcano Plot tool (`tools/deg.html`).
- **Planned**: Publications page population.

## [2026-01-09] - Phase 5: Interactive Tools Integration
### Added
- **Statistical Analysis Workbench**: Integrated client-side Python application (Stlite/WASM) for statistical analysis at `/tools/stat_analysis/index.html`.
- **MIME Configuration**: Added `public/_headers` to support `.wasm` and `.whl` files on Cloudflare Pages.
- **Navigation**: Added entry card in `src/tools.html` and a "Back to Home" floating button in the tool interface.

### Changed
- **Directory Structure**: Migrated tool artifacts to `public/tools/` to ensure correct absolute path resolution.
- **Optimization**: Switched Stlite/Pyodide to load from `cdn.jsdelivr.net` instead of local assets.
    - *Reason*: Cloudflare Pages has a 25MB file size limit (caused by `scipy.whl`).
    - *Benefit*: Reduces repo size by ~200MB and improves global load times.

## [2026-01-04] - Phase 4: AI Integration & Architecture Upgrade
### Added
- **Universal AI Backend**: Refactored `functions/api/chat.js` to support **any OpenAI-compatible provider** (DeepSeek, Doubao, Moonshot) in addition to Google Gemini.
- **AI Configuration Guide**: Created `AI_CONFIG.md` to document how to switch models and providers via environment variables.
- **Diagnostic Tool**: Added `/debug` command in chat to diagnose API connections and list available models.
- **System Persona**: Updated AI System Prompt to include the website owner's identity (PhD Candidate) and fallback logic for general knowledge.

### Changed
- **Architecture**: Migrated from standalone Worker to Cloudflare Pages Functions (`/api/chat`) to resolve GFW blocking.
- **AI Gateway**: Integrated Cloudflare AI Gateway for **both** Gemini and DeepSeek/OpenAI providers to enable unified logging and caching.
- **Model Upgrade**: Updated default Gemini model to `gemini-2.0-flash` (from deprecated `gemini-pro`).

### Fixed
- **Connectivity**: Resolved "Connection Refused" errors by moving API to same-origin (`/api/chat`).
- **404/429 Errors**: Fixed Gemini API errors by correcting model versioning and implementing provider switching.
- **DeepSeek Integration**: Fixed 401 errors by correctly routing DeepSeek requests through the `deepseek` provider path in AI Gateway.

### Deprecated
- **sc-chat-api**: The standalone Cloudflare Worker project is now deprecated.

## [2026-01-02] - Phase 3: Content & Asset Organization
### Added
- **Research Page**: Populated `src/research.html` with two major research projects:
    1. "Skin Aging" (Deciphering the Vascular-Skin Axis).
    2. "Alopecia Assembloids" (Restoring Angio-Follicular Crosstalk).
- **Asset Structure**: Created structured subdirectories in `public/assets/`:
    - `public/assets/skin_aging/`
    - `public/assets/vHFO_exos/`
- **Documentation**: Added `CHANGELOG.md` for history tracking.

### Changed
- **Refactoring**: Moved flat asset files into project-specific folders.
- **Code Update**: Updated all image paths in `src/research.html` to reflect the new folder structure.
- **Workflow**: Updated `WORKFLOW.md` to establish the "HTML-first" content strategy and asset management rules.
- **Manifest**: Updated `PROJECT_MANIFEST.md` to reflect Phase 3 status.

## [2026-01-01] - Phase 2: Modernization
### Added
- **Vite Integration**: Migrated from static HTML to Vite build system.
- **Components**: Created `header.html` and `footer.html` for reusable layout.
- **Automation**: Added `scripts/new_article.py` for generating knowledge base articles.
- **Deployment**: Configured Cloudflare Pages deployment settings.

### Fixed
- **CSS**: Fixed profile image aspect ratio in `style.css`.
