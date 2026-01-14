# Content Map

## Main Pages
- `public/index.html`: **Home**. Hero section, News, Research Highlights.
- `public/research.html`: **Research**. Detailed project descriptions.
- `public/publications.html`: **Publications**. List of papers.
- `public/tools.html`: **Tools**. Bioinformatics software showcase.
- `public/knowledge.html`: **Knowledge Base Index**. Entry point for articles.

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

## Knowledge Base Categories
Located in `public/knowledge/`:

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
- `public/assets/profile.jpg`: User profile photo.
- `public/assets/cv.pdf`: User CV.
