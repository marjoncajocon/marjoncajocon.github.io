#!/usr/bin/env python3
"""Generates WebP derivatives of every site image.

The screenshots and 3D captures are 200-1000 KB PNGs. Displaying those directly
in an 11rem gallery cell made project pages ~2.5 MB, which is a Largest
Contentful Paint problem and therefore a ranking problem.

This writes two derivatives next to each source PNG:

    foo.png  ->  foo.thumb.webp   (max 720px wide, for the gallery grid)
                 foo.hero.webp    (max 1600px wide, for the hero / wide slots)

The full-size PNG is kept and stays the lightbox target, so clicking a thumbnail
still shows the original at full quality.

    python tools/make_thumbs.py

Idempotent: re-running only rewrites derivatives older than their source.
"""

import pathlib
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required:  python -m pip install Pillow")

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"

# (suffix, max width, quality). Quality 82 is the point where screenshot text
# stays crisp; below ~75 the board coordinates start to smear.
VARIANTS = [(".thumb.webp", 720, 82), (".hero.webp", 1600, 84)]


def derive(src: pathlib.Path, suffix: str, max_w: int, quality: int) -> bool:
    out = src.with_suffix("")
    out = out.parent / (out.name + suffix)
    if out.exists() and out.stat().st_mtime >= src.stat().st_mtime:
        return False

    with Image.open(src) as im:
        im = im.convert("RGB")
        if im.width > max_w:
            h = round(im.height * max_w / im.width)
            im = im.resize((max_w, h), Image.LANCZOS)
        im.save(out, "WEBP", quality=quality, method=6)
    return True


def main():
    if not IMG.exists():
        sys.exit(f"no image dir at {IMG}")

    before = after = 0
    made = 0
    for src in sorted(IMG.rglob("*.png")):
        before += src.stat().st_size
        for suffix, max_w, q in VARIANTS:
            if derive(src, suffix, max_w, q):
                made += 1
        thumb = src.parent / (src.with_suffix("").name + ".thumb.webp")
        after += thumb.stat().st_size

    print(f"  wrote {made} derivatives")
    print(f"  source PNGs      {before / 1024 / 1024:6.1f} MB")
    print(f"  thumb.webp total {after / 1024 / 1024:6.1f} MB"
          f"   ({after / before:.0%} of the originals)")


if __name__ == "__main__":
    main()
