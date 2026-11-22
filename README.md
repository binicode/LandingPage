# Bridge Technologies — Landing Page

Static landing page for **Bridge Technologies**, a technology company in Ethiopia.
The layout recreates the reference "profile grid" design: a merlot card with a header
bar and a 3 × 2 grid of tiles, in the reference palette:

| Name             | Hex       |
| ---------------- | --------- |
| Midnight Merlot  | `#480D0E` |
| Solar Orange     | `#DB5E3C` |
| Daybreak Yellow  | `#F2D254` |

No build step, framework or JavaScript: plain HTML + CSS, self-hosted fonts and
pre-optimised AVIF/WebP images.

## Run locally

```bash
# from the project root, either:
npx serve .
# or
python -m http.server 8000
```

Then open the printed URL (e.g. http://localhost:8000). Opening `index.html`
directly from disk also works.

## Structure

```
index.html                 Page markup, SEO meta, JSON-LD, inline SVG brand mark
robots.txt
assets/
  css/styles.css           All styles (design tokens at the top)
  fonts/                   Libre Caslon Text, Space Mono, Inter (woff2) + OFL licences
  images/                  Tile images (AVIF + WebP, 400/800px) and favicon.svg
scripts/
  grade_images.py          Colour-grades any photo into the palette and exports AVIF/WebP
  scenes/*.html            Grayscale source scenes for the current tile images
```

## How the layout scales

Every size inside the card uses container-query units, so the proportions measured
from the reference hold at any width:

- `.profile` is the card container: `100cqi` = card width (1086px in the reference).
- `.tile` is the tile container: `100cqi` = tile width (350px in the reference; tiles are 350 × 357).

The grid shows 3 columns, then 2 columns when the card is under 640px wide, then 1 column under 420px.

## Replacing the images with real photography

The current tile images are illustrated stand-ins, because no stock-photo source
was reachable while building. To use real photos, run them through the same grade
so they match the reference's duotone look:

```bash
pip install "pillow>=11"
python scripts/grade_images.py path/to/photo.jpg assets/images/circuit ember
python scripts/grade_images.py path/to/photo.jpg assets/images/workspace ember
python scripts/grade_images.py path/to/photo.jpg assets/images/first-light daybreak
```

File names stay the same, so no HTML changes are needed. Update the matching `alt`
text in `index.html`.

## Before going live

- **Copy:** the taglines ("Ideas, then systems.", "Design. Build. Repeat.",
  "Building bridges.", "Coffee & code") are placeholders that follow the reference's
  structure. Replace them with approved company messaging.
- **Domain:** once the production URL is known, add `<link rel="canonical">`, `og:url`
  and an absolute `og:image` to `index.html`, and add a `sitemap.xml` (referenced from `robots.txt`).
- **Handle:** `bridge.technologies` in the header bar is a stand-in for the reference's
  social handle. Replace it with the real one.
