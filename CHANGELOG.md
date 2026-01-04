# Project Changelog

All notable changes to the **Bio-Tools** project will be documented in this file.

## [Unreleased]
- **Planned**: Interactive Volcano Plot tool (`tools/deg.html`).
- **Planned**: Publications page population.

## [2026-01-04] - Phase 4: AI Integration
### Added
- **Backend API**: Created `sc-chat-api` (Cloudflare Workers) to handle AI requests securely.
    - Features: Google Gemini integration, HTTP Basic Auth, IP Rate Limiting.
- **Frontend Widget**: Created `src/components/chat-widget.html` for user interaction.
    - Features: Floating UI, Password protection, Markdown rendering.
- **Integration**: Injected the chat widget into `src/components/footer.html` for global visibility.

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
