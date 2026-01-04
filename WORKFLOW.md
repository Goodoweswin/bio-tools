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

### F. Updating AI Backend (sc-chat-api)
- **Location**: `../sc-chat-api/`
- **Logic**: `src/index.js` contains the API logic (Gemini call, Auth, Rate Limit).
- **Deploy**:
  ```bash
  cd ../sc-chat-api
  npm run deploy
  ```
- **Note**: The frontend (`chat-widget.html`) connects to the live Worker URL. If you change the Worker URL, update the frontend config.

## 3. Agent Protocol (For AI Assistants)
- **Source Root**: `src/` is the working directory.
- **Static Assets**: Images/PDFs go in `public/`, referenced as `/assets/file.ext` (Vite resolves this).
- **Components**: ALWAYS use `<load src="..." />` for Header/Footer.
  - **CRITICAL**: Use absolute paths (e.g., `/components/header.html`), NOT relative paths (`./header.html`), to avoid build errors in nested files.
- **Style**: Global styles are in `src/css/style.css`.
