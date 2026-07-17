# Content Map

## Main Pages
- `src/index.html`: **Home**. Future Lab OS landing page with atlas hero, research loop, BioTools dock, and signal feed.
- `src/research.html`: **Research**. Future Lab OS module page with research orbit, module rail, visual project boards, validation routes, and Chinese summaries.
- `src/publications.html`: **Publications**. Public-facing scholarly output placeholder and future list.
- `src/tools.html`: **Tools**. BioTools Control Room with runtime console, live instrument stations, analysis loop, and next-instrument panel.
- `src/knowledge.html`: **Knowledge Base Index**. Entry point for articles.

## Components (`src/components/`)
- `header.html`: Global navigation bar.
- `footer.html`: Global footer.
- `chat-widget.html`: **AI Assistant**. Floating chat interface connecting to internal API (`/api/chat`).

## Backend (`functions/`)
- `api/chat.js`: **Universal AI Handler**. 
    - Supports **Google Gemini** (via `callGemini`).
    - Supports **OpenAI Compatible** (DeepSeek, Doubao, etc. via `callOpenAICompatible`).
    - Handles Auth, Rate Limiting, and AI Gateway routing.

## Documentation
- `AI_CONFIG.md`: **Critical Guide**. Instructions for configuring AI providers and models in Cloudflare Dashboard.
- `DESIGN_STRATEGY.md`: **Design Roadmap**. Taste-skill based plan for the next signature design upgrade.
- `DESIGN_SYSTEM.md`: **Visual System**. Tokens, layout rules, motion rules, and copy rules.
- `DEPLOYMENT.md`: **Deployment Guide**. Cloudflare Pages workflow and live smoke checks.
- `SEO_CHECKLIST.md`: **SEO Guide**. Metadata, route, and search hygiene.
- `ASSET_POLICY.md`: **Asset Guide**. Image optimization and deployable asset policy.
- `TEST_CHECKLIST.md`: **QA Guide**. Build, link, visual, and live verification checklist.
- `PROJECT_MANIFEST.md`: **Project identity and status**.
- `CONTENT_MAP.md`: **Page, component, and asset index**.

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
- `public/assets/cv.pdf`: User CV.

## Tools
- `public/tools/stat_analysis/index.html`: ElementPrism entry page.
- `public/tools/stat_analysis/app.py`: ElementPrism Stlite application.
- `public/tools/deg/index.html`: DEG Analysis entry page.
- `public/tools/deg/app.py`: DEG Analysis Stlite application.
