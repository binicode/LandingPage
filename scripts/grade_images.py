#!/usr/bin/env python3
"""Colour-grade tile photos into the Bridge palette and export responsive images.

The reference design shows every photo as a duotone running from Midnight Merlot
shadows through Solar Orange to Daybreak Yellow highlights. This script applies
that grade to any source photo (colour or grayscale), adds light film grain and
writes square AVIF + WebP files, so real photography can be swapped in later
without touching the HTML or CSS:

    python3 scripts/grade_images.py <source-image> <output-stem> <ember|daybreak>

    e.g. python3 scripts/grade_images.py photos/office.jpg assets/images/workspace ember

Writes <stem>-800.avif, <stem>-800.webp, <stem>-400.avif and <stem>-400.webp
(centre square crop). Requires Pillow >= 11 built with AVIF support.
"""
import random
import sys

from PIL import Image, ImageChops, ImageFilter, ImageOps

# Gradient maps sampled from the reference: (position 0-1, hex colour)
RAMPS = {
    # merlot shadows -> solar orange highlights (interior / close-up shots)
    "ember": [(0, "#120202"), (0.25, "#3a0b08"), (0.5, "#7a2618"), (0.72, "#c4583a"),
              (0.88, "#e6875c"), (1, "#f6c39a")],
    # merlot shadows -> orange mid-tones -> daybreak yellow highlights (sunrise shots)
    "daybreak": [(0, "#1e0705"), (0.22, "#5c2419"), (0.4, "#a35a33"), (0.55, "#cf9a52"),
                 (0.7, "#eccd70"), (0.86, "#f5e08c"), (1, "#fdf2c2")],
}
SIZES = (800, 400)


def _rgb(hex_colour):
    h = hex_colour.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def build_lut(stops):
    """Return a 768-entry RGB lookup table for Image.point()."""
    stops = [(pos, _rgb(col)) for pos, col in stops]
    lut = []
    for channel in range(3):
        for value in range(256):
            t = value / 255
            for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
                if p0 <= t <= p1:
                    k = (t - p0) / (p1 - p0)
                    lut.append(round(c0[channel] + (c1[channel] - c0[channel]) * k))
                    break
    return lut


def add_grain(lum, amount=9, seed=7):
    """Add zero-centred, slightly softened monochrome grain to a luminance image."""
    rnd = random.Random(seed)
    w, h = lum.size
    noise = Image.frombytes("L", (w, h), bytes(rnd.randint(128 - amount, 128 + amount) for _ in range(w * h)))
    noise = noise.filter(ImageFilter.GaussianBlur(0.5))
    return ImageChops.add(lum, noise, scale=1.0, offset=-128)


def grade(src, stem, ramp):
    img = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    side = min(img.size)
    img = ImageOps.fit(img, (side, side), Image.LANCZOS)
    lum = ImageOps.autocontrast(img.convert("L"), cutoff=0.3)
    lum = add_grain(lum)
    graded = Image.merge("RGB", (lum, lum, lum)).point(build_lut(RAMPS[ramp]))
    for size in SIZES:
        out = graded.resize((size, size), Image.LANCZOS)
        out.save(f"{stem}-{size}.avif", quality=60)
        out.save(f"{stem}-{size}.webp", quality=80, method=6)
        print(f"wrote {stem}-{size}.avif and .webp")


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[3] not in RAMPS:
        sys.exit(__doc__)
    grade(*sys.argv[1:])
