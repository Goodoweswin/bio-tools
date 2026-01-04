# Technical Architecture

## Stack
- **Frontend**: Vite + Vanilla HTML/CSS (Static Site).
- **Backend**: Cloudflare Workers (Serverless Node.js environment).
- **AI Model**: Google Gemini Pro (via API).
- **Database**: Cloudflare Workers KV (for Rate Limiting & Knowledge Base).
- **Build Tool**: Vite (handles bundling, minification, and HTML injection).
- **Hosting**: Cloudflare Pages (Frontend) + Cloudflare Workers (Backend).

## Directory Structure Rules
```
biotools/
├── bio-tools/               # FRONTEND (Static Site)
│   ├── src/                 # Source Code
│   │   ├── components/      # Reusable HTML fragments
│   │   │   ├── chat-widget.html # AI Chat Interface
│   │   │   ├── header.html  # Global Navigation
│   │   │   └── footer.html  # Global Footer
│   │   ├── css/             # Global Styles
│   │   └── ...
│   └── ...
├── sc-chat-api/             # BACKEND (AI Worker)
│   ├── src/
│   │   └── index.js         # Main Worker Logic (Auth, Gemini, KV)
│   ├── wrangler.toml        # Worker Configuration
│   └── package.json         # Backend Dependencies
```

## Design System (CSS Variables)
Defined in `src/css/style.css`:
- `--primary-color`: `#0072B2` (Nature Blue)
- `--accent-color`: `#FF7F50` (Coral)

## Navigation Logic
- **Vite Injection**: We use `vite-plugin-html-inject`.
- **Usage**: `<load src="/components/header.html" />`
- **Benefit**: Edit `src/components/header.html` once, update everywhere.
