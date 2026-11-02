# bio-tools
**Personal Academic Website & Bioinformatics Toolkit**

A static website built with Vite, showcasing research in Plastic Surgery, Single-Cell Omics, and AI4Med.
Features a custom **AI Research Assistant** powered by Cloudflare Workers and Google Gemini.

## Tech Stack
- **Frontend**: HTML5, CSS3, JavaScript (Vite)
- **Backend**: Cloudflare Pages Functions (Serverless API at `/api/chat`)
- **AI Engine**: Universal Handler (Gemini 2.0 + DeepSeek V3 + Any OpenAI Compatible)
- **AI Gateway**: Cloudflare AI Gateway (Logging & Caching)
- **Hosting**: Cloudflare Pages

## Roadmap
- [x] **Phase 1**: Static Site Migration (Vite)
- [x] **Phase 2**: Content & Asset Organization
- [x] **Phase 3**: AI Chat Integration (Universal Backend)
- [ ] **Phase 4**: RAG Implementation (Vector Search)
    - [ ] Cloudflare Vectorize Index
    - [ ] Document Ingestion Script
    - [ ] Context-Aware Chat
- [ ] **Phase 5**: Interactive Tools (Volcano Plot)

## Quick Start
```bash
npm install
npm run dev
```

## Life Calendar

Open `/life.html` for a minimal, graphite and ice-blue time-dot component,
also shown as the second slide of the homepage hero alongside the vascular-aging
illustration. Both slides share the introduction and frame. Use the arrow/dot
controls or swipe horizontally on touch screens. Automatic rotation pauses on
hover, keyboard focus, offscreen and hidden tabs; a pause control is always
available. Reduced motion starts with automatic rotation off. `/#time` opens the
time slide directly. Switch between life in weeks and the year in days.
Hover to inspect dates; the current dot breathes softly and nearby dots react to
the pointer. The owner-confirmed birthday is 2000-09-05. The scale uses the World
Bank 2024 China male life expectancy at birth, 75.249 years (displayed as 75.25).
The value, year, source link, and population-statistic limitation are labeled.
All visitors see the same owner timeline; old local profiles do not override it.
Calculations include leap days and fractional years. See
`docs/LIFE_CALENDAR_REFERENCE.md` for the source and calculation method.

Reuse `src/components/time-field.html` with the `/js/life.js` module and shared
stylesheet. Rendering pauses outside the viewport and in background tabs; reduced
motion disables the reveal, breathing, and parallax. No new dependencies.

Run `npm test` for calendar arithmetic checks. For browser checks,
start the Vite server and Firefox with `--headless --remote-debugging-port 9224`,
then run `node scripts/check-life-ui.mjs` (Node 22+). `BASE_URL`, `BIDI_URL`, and
`QA_OUTPUT` override the default local endpoints and screenshot directory.
