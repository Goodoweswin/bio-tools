# Project Changelog

All notable changes to the **Bio-Tools** project will be documented in this file.

## [Unreleased]
- **Planned**: Interactive Volcano Plot tool (`tools/deg.html`).
- **Planned**: Publications page population.

## [2026-01-20] - Phase 5.4: Bar Chart V2.0 & High-Impact Styling
### Added
- **Statistical Powerhouse**:
    - **Wide Mode**: Native support for multi-metric analysis (e.g., Weight + Glucose side-by-side).
    - **Rigorous Alignment**: Standardized statistical tests across all modes. NOW: >2 groups automatically triggers **Kruskal-Wallis + Dunn's Test (Holm)** for "CNS-level" validity.
    - **Transparency**: Added "📊 Statistical Methodology Report" panel to expose exact p-values and test logic.
- **Aesthetic "Pixel-Perfect" Control**:
    - **Group Shapes**: New toggle to distinguish groups by shape (Circle, Square, Triangle) + Color.
    - **Fine-Tuning**: Added granular controls for **Y-axis Font Size**, **Significance Line Width**, and **Line Height** (Bracket vs Flat).
    - **Clean Style**: Option to remove black bar edges.

### Changed
- **UX**: Fixed `DuplicateWidgetID` errors and optimized layout for multi-metric views (auto-rotating X-labels).

## [2026-01-14] - Phase 5.2: Scientific Styling & Infrastructure Hardening
### Added
- **Scientific Visualization Upgrade**:
    - **Single Metric Mode**: Optimized layout for single-variable data (metric as X-axis label, grouping by color).
    - **New Styling**: Added `🧬 科研柔和 (Sci)` palette, stripplot overlay, and auto-adjusted p-value formats.
    - **Manual Controls**: Added width sliders for both Barplot and Boxplot to fine-tune visual density.
- **Infrastructure Hardening**:
    - **Offline Deployment Package**: Generated full offline archive `bio-tools-server-deploy.zip` (~300MB) containing all dependencies.
    - **Dual-Mode Support**: Included `enable_offline_mode.py` for one-click conversion from Cloudflare mode to 100% offline mode on private servers.

### Changed
- **Renaming**: "Difference Analysis" module formally renamed to "Boxplot" (`📊 箱线图`).
- **Optimization**: Reverted git repository to Cloudflare-compatible state (remote Scipy) to ensure free hosting stability, while preserving offline capabilities via external script.

## [2026-01-14 Evening] - Phase 5.3: Layout Perfection & Deployment
### Added
- **Manual Tuning Guide**: Created `CODE_STYLE_ADJUSTMENT.md` for users to fine-tune chart physics (padding, spacing).
- **Offline Sync**: Auto-synced latest layout algorithms to the private server deployment package.

### Changed
- **Chart Alignment**: Refactored Single Metric Mode to use a "Conservative Alignment" strategy (Fixed physical width + Variable visual padding) to ensuring 100% alignment between Bar/Box and Stripplot.
- **Visual Polish**: Increased separation between P-value brackets and data points to prevent overlapping.


## [2026-01-13] - Phase 5.1: Bar Chart Module & Palette Enhancement
### Added
- **Bar Chart Module**: 
    - **UI Control**: Added manual **Bar Width Slider** for precise spacing control.
    - **Layout Upgrade**: Added "Single Metric Mode" (Metric on X-axis, Group in Legend).
    - **Scientific Styling**: Added "🧬 科研柔和" palette, data points overlay (stripplot), and italic labeling.
- **Boxplot (formerly Difference Analysis)**: 
    - **Renaming**: Module renamed to `📊 箱线图 (Boxplot)` for clarity.
    - **Features**: Added Hue selector, "Single Metric Mode", and manual **Box Width Slider**.
    - Upgraded with scientific styling (points overlay, p-value format).
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
