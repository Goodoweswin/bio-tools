# Development Workflow

## 1. Environment Setup
- **Context**: Remote Server Development (Files are NOT local).
- **IDE**: VS Code (Remote - SSH), Cursor, or Antigravity.
- **Stack**: Vite + Vanilla HTML/CSS.
- **Node.js**: Required on the remote server for `npm install` and `npm run dev`.

## 2. Common Tasks

### A. Adding a New Article
**Recommended Method (Automation):**
1. Run the Python script:
   ```bash
   python3 scripts/new_article.py "Article Title" -c "Category-Name"
   ```
2. This creates a new file in `src/knowledge/` with the correct template and navigation.

**Manual Method:**
1. Copy `src/_template.html`.
2. Save as `src/knowledge/<category>/<slug>.html`.
3. Ensure `<load src="/components/header.html" />` is present.

### B. Updating Navigation
1. Edit `src/components/header.html`.
2. **Done!** Vite will automatically update all pages during build. No manual copying needed.

### C. Asset Management
- **Organization**: Do not dump everything into `public/assets/`.
- **Rule**: Create a subfolder for each major project or article.
  - Example: `public/assets/skin_aging/figure1.png`
- **Reference**: In HTML, use `/assets/skin_aging/figure1.png`.

### D. Content Strategy (HTML vs JSON)
- **Decision**: Use **Raw HTML** for `research.html` and complex pages.
- **Reasoning**: Each research project has a unique layout (e.g., 3-pillar vs 4-step workflow). JSON templates are too rigid.
- **Maintenance**: When moving assets, use VS Code "Find & Replace" to update paths globally.

### E. Deploying (Cloudflare Pages)
1. **Configuration (One-time)**:
   - Build command: `npm run build`
   - Build output directory: `dist`
2. **Routine**:
   - `git add .`
   - `git commit -m "Update content"`
   - `git push origin main`
   - Cloudflare handles the build and deployment automatically.

### F. Updating AI Backend (Pages Functions)
- **Location**: `functions/api/chat.js`
- **Deployment**: Automatic via `git push`.
- **Configuration**: See `AI_CONFIG.md` for detailed instructions on switching models and providers.

### G. Configuring AI Backend (Critical)
**Manual Steps Required in Cloudflare Dashboard:**
Since `wrangler.toml` is not used for Pages Functions in this setup, you must configure bindings manually:

1.  **Environment Variables**:
    - Go to **Settings > Environment Variables**.
    - **Authentication**: `ACCESS_PASSWORD`
    - **Cloudflare**: `CF_ACCOUNT_ID`, `AI_GATEWAY_NAME`
    - **AI Provider Config**:
        - `AI_PROVIDER`: `gemini` (default) or `deepseek` / `doubao` etc.
        - `GEMINI_API_KEY`: For Google models.
        - `OPENAI_API_KEY`: For DeepSeek/Doubao/OpenAI models.
        - `OPENAI_BASE_URL`: API Endpoint (e.g., `https://api.deepseek.com`).
        - `OPENAI_MODEL`: Model name (e.g., `deepseek-chat`).

2.  **KV Namespace Bindings**:
    - Go to **Settings > Functions > KV Namespace Bindings**.
    - Bind `RATE_LIMIT` to your Rate Limit KV namespace.

3.  **Redeploy**:
    - After changing settings, go to **Deployments** and trigger a **Retry** on the latest deployment to apply changes.
- **Architecture**: Cloudflare Pages Functions (Serverless).
- **Deploy**: Automatically deployed when you `git push` the frontend.
- **Configuration**:
  - Go to Cloudflare Dashboard -> Pages -> bio-tools -> Settings.
  - **Environment Variables**: 
    - `ACCESS_PASSWORD`: Chat password.
    - `GEMINI_API_KEY`: Google AI Studio Key.
    - `CF_ACCOUNT_ID`: Cloudflare Account ID (for AI Gateway).
    - `AI_GATEWAY_NAME`: Name of your AI Gateway (e.g., `biotools-gateway`).
  - **KV Namespace Bindings**: Bind `RATE_LIMIT` and `KNOWLEDGE_INDEX` to the respective KV namespaces.

## 3. Agent Protocol (For AI Assistants)
- **Source Root**: `src/` is the working directory.
- **Static Assets**: Images/PDFs go in `public/`, referenced as `/assets/file.ext` (Vite resolves this).
- **Components**: ALWAYS use `<load src="..." />` for Header/Footer.
  - **CRITICAL**: Use absolute paths (e.g., `/components/header.html`), NOT relative paths (`./header.html`), to avoid build errors in nested files.
- **Style**: Global styles are in `src/css/style.css`.
