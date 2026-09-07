#!/usr/bin/env python3
"""Turn a figure into a publication teaser sized for the card's 200px plate.

Scales the image to fit the plate at retina density and palette-quantises it,
which typically cuts a figure screenshot by 80% or more with no visible loss at
the size it actually renders.

Usage:
    python3 tools/teaser.py figure.png indicsafeeval
    python3 tools/teaser.py figure.png mcstcnn --crop 900x700+40+120

`--crop` takes an ImageMagick-style geometry — WxH+X+Y, in source pixels —
and is applied before scaling. Crop first, to the one panel that reads at
thumbnail size; a whole multi-panel figure never will.

Requires ffmpeg on PATH. The rest of the build is standard library only.
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / 'images' / 'pubs'

# The plate is 200x150 CSS px; 480x360 covers it at well over 2x.
MAX_W, MAX_H = 480, 360
COLORS = 128

CROP_RE = re.compile(r'^(\d+)x(\d+)\+(\d+)\+(\d+)$')


def run(args):
    proc = subprocess.run(args, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(f'ffmpeg failed:\n{proc.stderr.strip()}')


def probe_size(path):
    out = subprocess.run(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
         '-show_entries', 'stream=width,height', '-of', 'csv=p=0:s=x', str(path)],
        capture_output=True, text=True)
    if out.returncode != 0:
        return None
    w, h = out.stdout.strip().split('x')
    return int(w), int(h)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('source', help='figure to convert')
    ap.add_argument('name', help='output name, without extension (e.g. indicsafeeval)')
    ap.add_argument('--crop', help='WxH+X+Y in source pixels, applied before scaling')
    ap.add_argument('--colors', type=int, default=COLORS, help=f'palette size (default {COLORS})')
    args = ap.parse_args()

    if not shutil.which('ffmpeg'):
        sys.exit('ffmpeg not found on PATH — install it, or resize the figure by hand '
                 f'to fit {MAX_W}x{MAX_H} and drop it in images/pubs/.')

    src = Path(args.source)
    if not src.is_file():
        sys.exit(f'no such file: {src}')

    filters = []
    if args.crop:
        m = CROP_RE.match(args.crop)
        if not m:
            sys.exit(f'--crop must look like 900x700+40+120, got {args.crop!r}')
        w, h, x, y = m.groups()
        filters.append(f'crop={w}:{h}:{x}:{y}')

    # force_original_aspect_ratio=decrease fits inside the box without distorting;
    # force_divisible_by=2 keeps the scaler happy on odd dimensions.
    filters.append(f'scale={MAX_W}:{MAX_H}:force_original_aspect_ratio=decrease'
                   f':force_divisible_by=2:flags=lanczos')
    chain = ','.join(filters)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    dest = OUT_DIR / f'{args.name}.png'

    run(['ffmpeg', '-v', 'error', '-y', '-i', str(src),
         '-vf', f'{chain},split[a][b];'
                f'[a]palettegen=max_colors={args.colors}[p];'
                f'[b][p]paletteuse=dither=none',
         str(dest)])

    before, after = src.stat().st_size, dest.stat().st_size
    size = probe_size(dest)
    dims = f'{size[0]}x{size[1]}' if size else 'unknown'
    saved = 100 - after * 100 // before if before else 0
    print(f'  + {dest.relative_to(ROOT)}  {dims}  '
          f'{before:,} → {after:,} bytes ({saved}% smaller)')
    print(f'\nAdd to data/publications.js:\n'
          f"    image: 'images/pubs/{args.name}.png',\n"
          f"    imageAlt: 'Describe what the figure shows.',")


if __name__ == '__main__':
    main()
