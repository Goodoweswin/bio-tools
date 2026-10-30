# Content Map

## Main Pages
- `src/index.html`: **Home**. Compact introduction, exactly three selected projects, three existing notes, and brief personal About/contact. No CV, timeline, methods inventory, authorship details, or talks list in the main homepage content.
- `src/work.html`: **Work**. Visual index for research, ElementPrism, and Pilotus; direct launch links for both working tools, and optional research-record/detail links.
- `src/about.html`: **About**. Concise biography, accurate M.D. student identity and expected graduation, bilingual CV, collapsed background, and WeChat contact.
- `src/research.html`: **Research**. Two ongoing projects, dates, owner contributions, hypothesis-aware scientific figures, Chinese summaries, and earlier training.
- `src/publications.html`: **Research records**. Existing detail route retaining manuscript/conference anchors and supported claims. Credential-only training/scores/football results are no longer listed here; background links to About/CV. Active primary navigation: Work.
- `src/tools.html`: **Tools**. Direct launch links for the two existing tools; pathway enrichment is planned.
- `src/knowledge.html`: **Research notes**. Immediate keyword search, topic filters, and 12 original article links.

## Components (`src/components/`)
- `header.html`: Global navigation bar.
- `selected-projects.html`: Shared three-project showcase used by Home and Work.
- `footer.html`: Global footer.
- `chat-widget.html`: **AI Assistant**. Floating chat interface connecting to internal API (`/api/chat`).

## Backend (`functions/`)
- `api/chat.js`: **Universal AI Handler**. 
    - Supports **Google Gemini** (via `callGemini`).
    - Supports **OpenAI Compatible** (DeepSeek, Doubao, etc. via `callOpenAICompatible`).
    - Handles Auth, Rate Limiting, and AI Gateway routing.

## Documentation
- `AI_CONFIG.md`: **Critical Guide**. Instructions for configuring AI providers and models in Cloudflare Dashboard.
- `DESIGN_STRATEGY.md`: **Design Direction**. Current research-led redesign and gated checkpoints.
- `HERO_ASSET_PROVENANCE.md`: **Image Provenance**. Homepage concept-art source, prompt, role, and limitations.
- `DESIGN_SYSTEM.md`: **Visual System**. Tokens, layout rules, motion rules, and copy rules.
- `DEPLOYMENT.md`: **Deployment Guide**. Cloudflare Pages workflow and live smoke checks.
- `SEO_CHECKLIST.md`: **SEO Guide**. Metadata, route, and search hygiene.
- `ASSET_POLICY.md`: **Asset Guide**. Image optimization and deployable asset policy.
- `TEST_CHECKLIST.md`: **QA Guide**. Build, link, visual, and live verification checklist.
- `PROJECT_MANIFEST.md`: **Project identity and status**.
- `CONTENT_MAP.md`: **Page, component, and asset index**.
- `CONTENT_ACCURACY.md`: **Content Register**. Editable-copy decisions, image-label debt, and owner inputs required for public records.
- `RESUME_CONTENT_UPDATE.md`: **Resume Update**. Source decisions and sequential acceptance checkpoints for the 2026-10-19 content update.
- `MD_TYPOGRAPHY_UPDATE.md`: **Previous Update**. M.D. identity correction, resume source decisions, and typography baseline.
- `PERSONAL_SHOWCASE_UPDATE.md`: **Current Presentation**. Personal-showcase structure, content exclusions, new pages, legacy navigation grouping, and release checkpoints.

## Knowledge Base Categories
Located in `src/knowledge/` and included in the Vite build via `vite.config.js`:

### 1. AI x Single-Cell (`ai-single-cell/`)
- `annotation.html`: AI-driven cell type annotation.
- `batch-correction.html`: Batch effect correction methods.
- `grn-inference.html`: Gene Regulatory Network inference.
- `trajectory.html`: Trajectory inference.

### 2. Skin Aging (`skin-aging/`)
- `aging-clock.html`: Epigenetic/Transcriptomic clocks.
- `fibroblast.html`: Fibroblast heterogeneity.
- `hes1-klf6.html`: Specific gene pathways.
- `il17-signaling.html`: Immune pathways in aging.

### 3. AI4Med (`ai4med/`)
- `clinical-decision.html`
- `drug-screening.html`
- `multi-omics.html`
- `skin-imaging.html`

### 4. Plastic Surgery (`plastic-surgery/`)
- *(Currently Empty)*

## Assets
- `src/assets/profile-hero.webp`: Optimized homepage portrait.
- `public/assets/*.webp`: Optimized public research images used by main pages.
- `public/assets/cv.pdf`: Chinese CV, owner-provided revision 2026-10-27; legacy public URL retained.
- `public/assets/cv-en.pdf`: English CV, owner-provided revision 2026-10-27.
- `public/assets/fonts/`: Self-hosted Adobe Source Sans 3 / Source Serif 4, licenses, and source provenance.
- `public/assets/showcase/`: Actual ElementPrism entry-page screenshot and media provenance.

## Tools
- `public/tools/stat_analysis/index.html`: ElementPrism entry page.
- `public/tools/stat_analysis/app.py`: ElementPrism Stlite application.
- `public/tools/deg/index.html`: DEG Analysis entry page.
- `public/tools/deg/app.py`: DEG Analysis Stlite application.
