# Design System

Updated: 2026-10-30. Personal showcase with distinct editorial and reading typography.

## Character
Clear, contemporary, human, and research-led. Scientific content carries the identity; interface decoration stays quiet.

## Tokens
Defined in `src/css/style.css`:
- Background: `#ffffff`
- Secondary surface: `#f3f6f5`
- Primary text: `#202b29`
- Secondary text: `#45534d`
- Muted text: `#596760`
- Accent and links: `#126750`
- Border: `#dce3df`; stronger control border: `#a1b4ab`
- Body/UI: self-hosted Source Sans 3, regular and semibold.
- Display: self-hosted Source Serif 4, regular and semibold. Chinese fallbacks explicitly name Noto CJK, PingFang/Microsoft YaHei for sans, and Noto Serif CJK/Songti for display.
- Control radius: 3px; framed tools: 4px; scientific images: 0px

## Typography
- Homepage name: 4rem desktop, Source Serif 4 regular; smaller fixed sizes at compact breakpoints.
- Page titles: 3.5rem desktop and 2.5rem mobile.
- Section headings: 2rem Source Serif 4 semibold; descriptive labels replace slogans.
- Institution and project titles: approximately 20-22px Source Sans 3 semibold, with smaller fixed sizes for dense interfaces.
- Body: 17px desktop and 16px mobile.
- Dates/status: 13-14px; dates and numeric metadata use tabular numerals.
- Keep the M.D. student identity secondary on Home. Institution, graduation, and CV belong to About; author order and measured contributions belong to research detail records.
- Use sans-serif for article headings and dense tool/note interfaces. Licenses and source URLs live under `public/assets/fonts/`.
- No negative or expanded letter spacing. No viewport-relative type sizes.
- Chinese notes retain their original titles; specialist English abbreviations remain searchable.

## Layout
- Shared content width: up to 1200px, with 20px mobile gutters.
- Main header: 80px desktop and 66px compact; accessible collapsed menu at 700px and below.
- Sections use full-width bands or unframed constrained content.
- Homepage image is full-bleed concept art with a clear annotation, not an experimental figure.
- Portrait is separate, in original color; no grayscale, blend mode, or colored overlays.
- Mobile About stacks the portrait above full-width biography text.
- Home has four sections: compact introduction, three selected works, three note links, and brief About/contact. Do not restore the resume timeline, methods inventory, or talks feed on Home.
- Primary navigation is Home / Work / Notes / About. Research, tools, and publication records retain their URLs under the Work navigation group.
- Project media uses uncropped owner schematics, actual screenshots, or clearly typographic wordmarks. Never present a wordmark as a product screenshot.
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
