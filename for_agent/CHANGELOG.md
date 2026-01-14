# Project Changelog

All notable changes to the **Bio-Tools** project will be documented in this file.

## [Unreleased]
- **Planned**: Interactive Volcano Plot tool (`tools/deg.html`).
- **Planned**: Publications page population.

## [2026-01-13] - Phase 5.1: Bar Chart Module & Palette Enhancement
### Added
- **Bar Chart Module**: 
    - **Layout Upgrade**: Added "Single Metric Mode" (Metric on X-axis, Group in Legend) and fixed bar width issues.
    - **Scientific Styling**: Added "🧬 科研柔和" palette, data points overlay (stripplot), and italic labeling.
    - **Statistics**: Display actual p-values (e.g., `p=0.001`) instead of just stars.
- **Difference Analysis (Boxplot)**: 
    - **Layout Upgrade**: Added Hue selector and "Single Metric Mode" support.
    - Upgraded with scientific styling (points overlay, p-value format) matching the bar chart.
- **Custom Color Input**: Users can now select "✏️ 自定义..." and input custom hex colors.

### Changed
- **Palette Presets**: Renamed all presets with intuitive Chinese names (e.g., "🔴 红蓝经典", "🤎 色盲友好").
- **New Presets Added**: 蓝色渐变, 色盲友好 (colorblind-safe), 灰度单色, 彩虹渐变.

## [2026-01-09] - Phase 5: Interactive Tools Integration
### Added
- **Statistical Analysis Workbench (v4.0)**: Upgraded `/tools/stat_analysis` to Bio-Analysis Suite v4.0 (Survival, Heatmap, PCA).
- **DEG Analysis Tool**: Added scaffold for Volcano Plot tool at `/tools/deg/index.html`.
- **MIME Configuration**: Added `public/_headers` to support `.wasm` and `.whl` files.

### Changed
- **Optimization**: Switched Stlite/Pyodide to load standard libraries (scipy, pandas) from `cdn.jsdelivr.net`.
    - *Reason*: Fixed Cloudflare Pages 25MB file size limit.
    - *Action*: Removed heavy local wheels, kept custom wheels in `assets/pypi/`.
- **Renaming**: Renamed `weight_analysis` to `stat_analysis` to reflect broader v4.0 capabilities.
- **Cleanup**: Moved temporary documentation to `docs/`.

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
