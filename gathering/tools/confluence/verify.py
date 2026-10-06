#!/usr/bin/env python3
"""Read-only verification of this gathering's wall and original cave pixels."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import hashlib
import json
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'shared/confluence'))
from wall_step import png


def main():
    wall = ROOT / 'artifacts/gathering/wall.png'
    w, h, c, pixels = png(wall)
    bw, bh, bc, base = png(ROOT / '.imd/reads/artifacts/cave')
    if (w, h, c) != (bw, bh, bc) or w != h or w < 1024 or c != 3:
        raise ValueError('invalid wall dimensions or format')
    obj = json.loads((ROOT / 'dist/gathering/01.json').read_text())
    expected_traits = [dict(trait_type='Wall', value='Gathering'),
                       dict(trait_type='Number', value=1),
                       dict(trait_type='Left behind', value='Confluence')]
    if set(obj) != {'name', 'image', 'attributes'} or not isinstance(obj['name'], str) or not obj['name'] or obj['attributes'] != expected_traits:
        raise ValueError('record schema')
    digest = hashlib.sha256(wall.read_bytes()).hexdigest()
    if obj['image'] != 'https://api.imd.fun/artifacts/' + digest:
        raise ValueError('hash mismatch')
    changed = 0
    for y in range(h):
        for x in range(w):
            i = (y*w+x)*3
            if pixels[i:i+3] != base[i:i+3]:
                if not (330 <= x < 920 and 330 <= y < 920):
                    raise ValueError('rock changed outside mark')
                changed += 1
    if changed == 0:
        raise ValueError('no new mark')
    print(f'PASS: {w}x{h} RGB PNG, CRCs and decoded pixels; record hash {digest}; {changed} changed pixels, zero outside mark')
    print('Visual review is separate; see gathering/README.md.')


if __name__ == '__main__':
    main()
