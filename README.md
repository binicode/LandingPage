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
  images/favicon.svg
  images/photos/           Original photos (JPEG) + optimised AVIF/WebP copies
scripts/
  optimize_images.py       Re-encodes a photo to AVIF/WebP without cropping or recolouring
```

## How the layout scales

Every size inside the card uses container-query units, so the proportions measured
from the reference hold at any width:

- `.profile` is the card container: `100cqi` = card width (1086px in the reference).
- `.tile` is the tile container: `100cqi` = tile width (350px in the reference; tiles are 350 × 357).

The grid shows 3 columns, then 2 columns when the card is under 640px wide, then 1 column under 420px.

## Photos

| Tile | Theme | File |
| ---- | ----- | ---- |
| Top middle | Ethiopia Going Digital | `assets/images/photos/ethiopia-going-digital.jpg` |
| Bottom left | Ethiopian Digital Lifestyle | `assets/images/photos/ethiopian-digital-lifestyle.jpg` |
| Bottom right | Technology Meets Nature | `assets/images/photos/technology-meets-nature.jpg` |

The photos are used exactly as supplied. The square tile crop is done in CSS
(`object-fit: cover` plus an `object-position` per photo in `styles.css`), and a merlot
gradient overlay at the foot of each photo tile keeps captions legible.

To swap or update a photo, replace the JPEG (keeping its name), then regenerate the web copies:

```bash
pip install "pillow>=11"
python scripts/optimize_images.py assets/images/photos/technology-meets-nature.jpg 448 640 896
python scripts/optimize_images.py assets/images/photos/ethiopian-digital-lifestyle.jpg 448 640 896
python scripts/optimize_images.py assets/images/photos/ethiopia-going-digital.jpg 480
```

If a new photo has different pixel dimensions, update the `width`/`height`
attributes on its `<img>` and the widths in its `srcset`s in `index.html`.

## Before going live

- **Copy:** the taglines ("Ethiopia, going digital.", "Design. Build. Repeat.",
  "Technology meets nature.", "Coffee & code") are placeholders that follow the
  reference's structure. Replace them with approved company messaging.
- **Ethiopia Going Digital photo:** the supplied file is only 480 × 324 px, so it looks
  soft on high-density screens. Use a version at least 800 px tall if you can. The
  original also carries a photographer credit ("Firaol_Debela_lafto") that falls outside
  the tile crop, so confirm you have the right to use it and credit it where required.
- **Domain:** once the production URL is known, add `<link rel="canonical">`, `og:url`
  and an absolute `og:image` to `index.html`, and add a `sitemap.xml` (referenced from `robots.txt`).
- **Handle:** `bridge.technologies` in the header bar is a stand-in for the reference's
  social handle. Replace it with the real one.
