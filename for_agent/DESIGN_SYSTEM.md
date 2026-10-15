# Design System

Updated: 2026-10-16. Replaces the dark Future Lab OS system.

## Character
Clear, contemporary, human, and research-led. Scientific content carries the identity; interface decoration stays quiet.

## Tokens
Defined in `src/css/style.css`:
- Background: `#ffffff`
- Secondary surface: `#f3f6f5`
- Primary text: `#202b29`
- Secondary text: `#53615d`
- Muted text: `#64716c`
- Accent and links: `#126750`
- Border: `#dce3df`; stronger control border: `#a1b4ab`
- Font: Aptos, Segoe UI, Roboto, Helvetica, Arial, sans-serif
- Control radius: 3px; framed tools: 4px; scientific images: 0px

## Typography
- Homepage name: 4.5rem desktop; smaller fixed sizes at compact breakpoints.
- Page titles: 3.5rem desktop and 2.5rem mobile.
- Section headings: 2.25rem; product headings and rows are smaller.
- Body: 17px desktop and 16px mobile.
- No negative or expanded letter spacing. No viewport-relative type sizes.
- Chinese notes retain their original titles; specialist English abbreviations remain searchable.

## Layout
- Shared content width: up to 1200px, with 20px mobile gutters.
- Main header: 80px desktop and 66px compact; accessible collapsed menu at 700px and below.
- Sections use full-width bands or unframed constrained content.
- Homepage image is full-bleed concept art with a clear annotation, not an experimental figure.
- Portrait is separate, in original color; no grayscale, blend mode, or colored overlays.
- Scientific images retain their full aspect ratio; each links to the original image for inspection.
- Tools and Notes show useful entries immediately; do not add large decorative introductions.

## Interaction
- Current-page navigation uses an underline and `aria-current`.
- Mobile menu exposes `aria-expanded`, closes on Escape, and restores focus.
- Search combines substring matching with a topic filter; live count and empty reset state remain available.
- Assistant uses hidden closed content, labeled inputs, Escape dismissal, and focus restoration.
- Skip link targets main content.
- All content remains visible without reveal observers; no essential information depends on animation.
- Hover transitions are 180ms; reduced-motion disables transitions and smooth scrolling.

## Content Integrity
- Use Jackson Dai as the public name.
- Do not invent publications, numbers, roles, claims, or science results.
- AI-generated editorial art must be distinguishable from evidence.
- Never use unrelated scientific art as an alleged screenshot of a tool.
- Publication policy belongs in project documentation, not a decorative public hero.
