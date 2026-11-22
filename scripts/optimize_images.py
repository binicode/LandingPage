#!/usr/bin/env python3
"""Export web-optimised AVIF + WebP copies of a photo without altering it.

No cropping, colour grading or other edits: the image is only re-encoded and,
where it is wider than a target width, scaled down (never up). Cropping for the
tiles is done in CSS (object-fit / object-position), so the originals stay intact.

    python3 scripts/optimize_images.py <source.jpg> [width ...]

    e.g. python3 scripts/optimize_images.py assets/images/photos/technology-meets-nature.jpg 448 896

Writes <source-stem>-<width>.avif and .webp next to the source.
Requires Pillow >= 11 built with AVIF support.
"""
import sys
from pathlib import Path

from PIL import Image, ImageOps


def optimize(src, widths):
    src = Path(src)
    img = ImageOps.exif_transpose(Image.open(src))
    icc = img.info.get("icc_profile")
    for width in sorted(set(min(w, img.width) for w in widths)):
        height = round(img.height * width / img.width)
        out = img if width == img.width else img.resize((width, height), Image.LANCZOS)
        for ext, opts in (("avif", {"quality": 72}), ("webp", {"quality": 86, "method": 6})):
            dest = src.with_name(f"{src.stem}-{width}.{ext}")
            out.save(dest, icc_profile=icc, **opts) if icc else out.save(dest, **opts)
            print(f"wrote {dest} ({width}x{height}, {dest.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    optimize(sys.argv[1], [int(w) for w in sys.argv[2:]])
