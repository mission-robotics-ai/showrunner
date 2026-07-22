#!/usr/bin/env python3
"""Asset derivations. Run with: uv run --with pillow image_tools.py

  image_tools.py upscale <in> <out> <factor>   nearest-neighbor (fiducials, pixel art)
  image_tools.py invert <in> <out>             white->black, alpha preserved (logo B&W)
  image_tools.py circle <in> <out> [size]      center-square crop -> circular alpha mask
  image_tools.py trim <in> <out>               crop to alpha bounding box
"""
import sys
from PIL import Image, ImageDraw


def upscale(src, dst, factor):
    im = Image.open(src)
    im.resize((im.width * factor, im.height * factor), Image.NEAREST).save(dst)
    print(f"{dst}: {im.width}x{im.height} -> {im.width*factor}x{im.height*factor} (NEAREST)")


def invert(src, dst):
    im = Image.open(src).convert("RGBA")
    r, g, b, a = im.split()
    inv = Image.merge("RGBA", (r.point(lambda v: 255 - v),
                               g.point(lambda v: 255 - v),
                               b.point(lambda v: 255 - v), a))
    inv.save(dst)
    print(f"{dst}: inverted, alpha preserved — probe for halos")


def circle(src, dst, size=800):
    im = Image.open(src).convert("RGB")
    s = min(im.size)
    left, top = (im.width - s) // 2, (im.height - s) // 2
    im = im.crop((left, top, left + s, top + s)).resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    out.save(dst)
    print(f"{dst}: {size}x{size} circle")


def trim(src, dst):
    im = Image.open(src)
    box = im.getbbox()
    im.crop(box).save(dst)
    print(f"{dst}: trimmed to {box}")


if __name__ == "__main__":
    cmds = {"upscale": lambda a: upscale(a[0], a[1], int(a[2])),
            "invert": lambda a: invert(a[0], a[1]),
            "circle": lambda a: circle(a[0], a[1], int(a[2]) if len(a) > 2 else 800),
            "trim": lambda a: trim(a[0], a[1])}
    if len(sys.argv) < 4 or sys.argv[1] not in cmds:
        print(__doc__)
        sys.exit(2)
    cmds[sys.argv[1]](sys.argv[2:])
