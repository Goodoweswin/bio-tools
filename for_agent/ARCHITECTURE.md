# Technical Architecture

## Stack
- **Frontend**: Vite + Vanilla HTML/CSS (Static Site).
- **Backend**: Cloudflare Pages Functions (Serverless Node.js environment).
- **AI Model**: Google Gemini Pro (via Cloudflare AI Gateway).
- **Database**: Cloudflare Workers KV (for Rate Limiting & Knowledge Base).
- **Vector Search (Planned)**: Cloudflare Vectorize + Workers AI (Embeddings).
- **Build Tool**: Vite (handles bundling, minification, and HTML injection).
- **Hosting**: Cloudflare Pages (Frontend + Backend).

## Directory Structure Rules
```
biotools/
├── bio-tools/               # FULL STACK PROJECT
│   ├── src/                 # Frontend Source Code
│   │   ├── components/      # Reusable HTML fragments
│   │   │   ├── chat-widget.html # AI Chat Interface (calls /api/chat)
│   │   │   ├── header.html  # Global Navigation
│   │   │   └── footer.html  # Global Footer
│   │   ├── css/             # Global Styles
│   │   └── ...
│   ├── functions/           # Backend Source Code (Pages Functions)
│   │   └── api/
│   │       └── chat.js      # Main API Logic (Auth, Gemini, KV, AI Gateway)
│   └── ...
├── sc-chat-api/             # DEPRECATED (Standalone Worker - Do Not Use)
│   └── ...
```

## Design System (CSS Variables)
Defined in `src/css/style.css`:
- `--primary-color`: `#0072B2` (Nature Blue)
- `--accent-color`: `#FF7F50` (Coral)

## Navigation Logic
- **Vite Injection**: We use `vite-plugin-html-inject`.
- **Usage**: `<load src="/components/header.html" />`
- **Benefit**: Edit `src/components/header.html` once, update everywhere.
