#!/usr/bin/env python3
"""First gathering's fixed, offline pigment placement; preserves bare rock."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import hashlib
import json
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'shared/confluence'))
from wall_step import png, write_rgb


def main():
    wall = ROOT / 'artifacts/gathering/wall.png'
    record = ROOT / 'dist/gathering/01.json'
    if wall.exists() or record.exists():
        raise ValueError('first-step assembler refuses to overwrite a wall or record')
    w, h, channels, original = png(ROOT / '.imd/reads/artifacts/cave')
    mw, mh, mc, ink = png(ROOT / 'gathering/tools/confluence/mark.png')
    if w != h or w < 1024 or channels != 3 or mc != 4:
        raise ValueError('expected square RGB cave and RGBA mark')
    pixels = bytearray(original)
    x, y, width = 330, 330, 590
    height = round(mh * width / mw)
    changed = 0
    for dy in range(height):
        for dx in range(width):
            sx = min(mw - 1, int((dx + .5) * mw / width))
            sy = min(mh - 1, int((dy + .5) * mh / height))
            si = (sy * mw + sx) * 4
            bi = ((y + dy) * w + x + dx) * 3
            alpha = ink[si + 3]
            for c in range(3):
                pixels[bi+c] = (ink[si+c] * alpha + pixels[bi+c] * (255-alpha) + 127) // 255
    for py in range(h):
        for px in range(w):
            i = (py*w+px)*3
            if pixels[i:i+3] != original[i:i+3]:
                if not (x <= px < x+width and y <= py < y+height):
                    raise ValueError('changed rock outside placement')
                changed += 1
    if not changed:
        raise ValueError('empty mark')
    write_rgb(wall, w, h, pixels)
    digest = hashlib.sha256(wall.read_bytes()).hexdigest()
    obj = dict(name='Pepe the Gatherer — Four Stones, One Bowl',
               image='https://api.imd.fun/artifacts/' + digest,
               attributes=[dict(trait_type='Wall', value='Gathering'),
                           dict(trait_type='Number', value=1),
                           dict(trait_type='Left behind', value='Confluence')])
    record.parent.mkdir(parents=True, exist_ok=True)
    with record.open('x') as stream:
        json.dump(obj, stream, indent=2, ensure_ascii=False)
        stream.write('\n')
    print(f'{w}x{h} RGB PNG; {changed} changed pixels inside placement; zero outside; SHA-256 {digest}')


if __name__ == '__main__':
    main()
