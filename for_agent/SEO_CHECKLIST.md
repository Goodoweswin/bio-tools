# SEO Checklist

## Current URL Model
- Cloudflare Pages serves pretty URLs.
- `.html` URLs may redirect to extensionless paths.
- Keep existing route names stable unless a migration plan exists.

## Required Per Main Page
Each main HTML page should have:
- [x] descriptive `<title>`
- [x] `meta charset`
- [x] `meta viewport`
- [x] consistent favicon
- [x] semantic `h1`
- [x] clear internal navigation

Priority pages:
- `/`
- `/research`
- `/tools`
- `/knowledge`
- `/publications`

## Main Page Meta
Implemented for `/`, `/research`, `/tools`, `/knowledge`, and `/publications`:
- [x] `meta name="description"`
- [x] Open Graph tags:
  - [x] `og:title`
  - [x] `og:description`
  - [x] `og:type`
  - [x] `og:url`
  - [x] `og:image`
- [x] Twitter card tags
- [x] canonical links for pretty URLs

## Knowledge Articles
For every article in `src/knowledge/**`:
- title should match article topic
- first `h1` should match the page title
- internal link back to knowledge index should work
- external links should be real, not `href="#"`
- if article content becomes important for search, add page-specific meta description

## Technical SEO
- [x] Add `robots.txt` if not already present.
- [x] Add `sitemap.xml` once page structure stabilizes.
- Ensure 404 behavior is acceptable on Cloudflare Pages.
- Avoid breaking route slugs after they are indexed.

## Content Quality
- Avoid placeholder pages where possible.
- Publications page should eventually list real outputs or explicitly say selected outputs are pending public release.
- Research pages should use concrete research claims and avoid over-broad marketing language.
