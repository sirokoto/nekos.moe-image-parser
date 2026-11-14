#!/usr/bin/env python3
"""
maxpng.py — report the highest-resolution PNG(s) in a directory tree.

Usage: ./maxpng.py [DIRECTORY]
Requires: pip install Pillow
"""
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Error: Pillow required.  pip install Pillow")


def main() -> int:
    directory = sys.argv[1] if len(sys.argv) > 1 else "."

    # case-insensitive glob for .png
    paths = sorted({p for pat in ("*.png", "*.PNG", "*.Png")
                    for p in Path(directory).rglob(pat)})
    if not paths:
        sys.exit(f"No PNG files found under {directory!r}")

    results = []          # (path, width, height, pixels)
    for p in paths:
        try:
            with Image.open(p) as im:
                w, h = im.size
                results.append((p, w, h, w * h))
        except Exception as e:
            print(f"warning: skipped {p}: {e}", file=sys.stderr)

    if not results:
        sys.exit("No readable PNG files.")

    by_px = max(results, key=lambda r: r[3])
    by_w  = max(results, key=lambda r: r[1])
    by_h  = max(results, key=lambda r: r[2])

    print(f"Scanned {len(results)} PNG file(s) under {directory}\n")
    print("Highest total resolution (largest pixel count):")
    print(f"  {by_px[0]}\n    {by_px[1]}x{by_px[2]} = {by_px[3]:,} pixels\n")
    print("Maximum width:")
    print(f"  {by_w[0]}\n    {by_w[1]}x{by_w[2]}\n")
    print("Maximum height:")
    print(f"  {by_h[0]}\n    {by_h[1]}x{by_h[2]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
