# Design System

## Design Read
The site should feel like a personal academic research system, not a generic dark SaaS template.

Target language:
- academic
- precise
- cyber-future
- restrained
- research-led

Avoid:
- AI-purple gradients
- heavy neon glow
- repeated three-card sections
- fake metrics or social proof
- decorative status dots
- ornamental scroll cues

## Core Tokens
Defined in `src/css/style.css`.

- **Primary accent**: cyan/teal, currently `--accent-color: #20c7b5`
- **Primary text**: off-white, currently `--text-color: #eef7fb`
- **Secondary text**: muted blue-gray, currently `--text-secondary: #9cb1bd`
- **Background**: off-black, currently `--bg-color: #081013`
- **Surface**: translucent dark panels, currently `--surface-bg`
- **Border**: low-contrast cool border, currently `--border-color`

## Typography
- Use the existing sans-serif stack unless a future font migration is planned.
- Do not introduce serif display fonts by default.
- Keep body copy readable and compact.
- Hero headings should be strong, but not oversized to the point of wrapping into four lines.

## Shape
- Buttons: `--radius-sm`, currently 3px.
- Cards/panels: `--radius-md`, currently 6px.
- Large visual panels: `--radius-lg`, currently 8px.
- Research image assets: square corners or near-square corners.
- Pills/tags and circular data marks: full radius.

Use this shape system consistently. The site should feel precise and research-led, so avoid soft 12-20px rounded rectangles around scientific figures.

## Layout Rules
- Homepage hero should remain distinctive and research-led.
- Research page should prioritize scanning: core question, model system, computational layer, translational angle.
- Use cards only where the card itself communicates a grouped object.
- Prefer mixed section rhythms over repeated grids.
- Keep navigation one line on desktop.

## Motion
Allowed motion:
- opacity and transform entry transitions
- subtle hover translation
- image clip or opacity reveal

Rules:
- Honor `prefers-reduced-motion`.
- Do not animate layout properties like width, height, top, or left.
- Do not add scroll hijacking unless a full scroll-story page is intentionally designed.

## Copy Rules
- Use `Jackson Dai` as the public pen name.
- Avoid fake metrics and fake social proof.
- Avoid visible em dashes and en dashes.
- Button labels should be short and specific.
- The site voice should be clear, academic, and concrete.

## Images
- Use WebP for public-facing large images.
- Keep original editing assets outside deployable `public/` when possible.
- Do not use div-based fake screenshots.
- Major landing/portfolio sections need real visuals.
