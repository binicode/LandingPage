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

The page is full-bleed: the header bar spans the top of the window and the tile
grid fills the rest of the viewport edge to edge, with no outer frame.

- **Columns:** 3 × 2 on landscape screens, 2 × 3 on portrait or narrow screens
  (under 640px wide, or aspect ratio 5:4 or taller), and 1 column on phones (under 560px).
- **Row height:** fills the space under the header, clamped between 0.75× and
  1.02× the tile width so tiles never get too squat or too tall.
- **Tile contents:** sized in `cqmin` (the tile's smaller side), so the proportions
  measured from the reference (350px tile) hold at any tile size.
- **Tokens:** `--bar-h` (header height) and `--gutter` (gap between tiles) at the
  top of `styles.css`. Set `--gutter: 0` for seamless tiles.

## Photos

| Tile | Theme | File |
| ---- | ----- | ---- |
| Top middle | Ethiopia Going Digital | `assets/images/photos/ethiopia-going-digital-crop.jpg` (cropped from `ethiopia-going-digital.jpg`) |
| Bottom left | Ethiopian Digital Lifestyle | `assets/images/photos/ethiopian-digital-lifestyle.jpg` |
| Bottom right | Technology Meets Nature | `assets/images/photos/technology-meets-nature.jpg` |

The lifestyle and nature photos are used exactly as supplied. The Addis Ababa photo
is cropped to 370 × 324 to drop the corner watermark; the original stays in the repo
and the photographer is credited on the page ("Photo · Firaol Debela Lafto"). The square tile crop is done in CSS
(`object-fit: cover` plus an `object-position` per photo in `styles.css`), and a merlot
gradient overlay at the foot of each photo tile keeps captions legible.

To swap or update a photo, replace the JPEG (keeping its name), then regenerate the web copies:

```bash
pip install "pillow>=11"
python scripts/optimize_images.py assets/images/photos/technology-meets-nature.jpg 448 640 896
python scripts/optimize_images.py assets/images/photos/ethiopian-digital-lifestyle.jpg 448 640 896
python scripts/optimize_images.py assets/images/photos/ethiopia-going-digital-crop.jpg 370
```

If a new photo has different pixel dimensions, update the `width`/`height`
attributes on its `<img>` and the widths in its `srcset`s in `index.html`.

## Before going live

- **Copy:** the taglines ("Ethiopia, going digital.", "Design. Build. Repeat.",
  "Technology meets nature.", "Coffee & code") are placeholders that follow the
  reference's structure. Replace them with approved company messaging.
- **Ethiopia Going Digital photo:** the supplied file is only 480 × 324 px, so it looks
  soft on large and high-density screens. Ask the photographer (Firaol Debela Lafto)
  for permission and a higher-resolution original, and keep the on-page credit.
- **Handle:** `bridge.technologies` in the header bar is a stand-in for the reference's
  social handle. Replace it with the real one.

## Screenshots

- `screenshots/upwork/`: 2000 × 1500 (4:3) JPEG presentation images for an Upwork
  portfolio. Use `01-cover-responsive.jpg` as the project cover, followed by the
  desktop, tablet and mobile images. All are well under Upwork's 10 MB limit and
  stay sharp at its 1000 × 750 display size.
- `screenshots/raw/`: unframed high-resolution captures (desktop 1440 × 900 @2x,
  tablet 820 × 1180 and 1180 × 820 @2x, mobile 390 × 844 and full page @3x).
