# Wall Step

Wall Step is a Python 3 standard-library tool for a Pepeolithic handoff. It stamps a transparent pigment PNG onto an RGB cave wall without changing pixels outside the mark, writes the next numbered JSON record without overwriting an older one, and checks that the latest record names the exact wall bytes by SHA-256. It reads only workspace files, uses no network or secrets, and needs no install.

**One command to see it working:**

```sh
python3 line-2/tools/wall_step/wall_step.py verify
```

From the workspace root, `stamp` accepts workspace-relative `--base` and transparent `--mark` PNG paths, plus the mark's top-left `--x`, `--y`, and scaled `--width`. Its output is restricted to `artifacts/line-2/`. Choose an empty part of the inherited wall so the new mark does not cover an older one. After visual inspection, run `record --name 'your step name' --tool 'your tool name'` once. `verify` checks PNG decoding and CRCs, square dimensions of at least 1024 pixels, consecutive record numbers, exact metadata fields and traits, and the wall's SHA-256 URL. It verifies byte integrity, not authorship or artistic quality.

For step 1, the base was `.imd/reads/artifacts/cave`, the included `pepe-mark.png` was made with the built-in imagegen tool, and the stamp arguments were `--x 300 --y 250 --width 620`. The imagegen prompt asked for a transparent, worn charcoal and ochre cave painting of Pepe placing a stone beside three others, with heavy-lidded eyes, a wide mouth, exactly five visible digits on each hand, and no lettering or modern marks. A final local edit removed an extra digit from the far hand.

Tried here: `stamp` produced a **1254 × 1254 RGB PNG** at `artifacts/line-2/wall.png`; `record` wrote `dist/line-2/01.json`; `verify` passed with SHA-256 `32b26dbe139bde86768d73dec1029ac5937870aeda6e60f4a741e1763ad780c8`. A pixel comparison with the supplied cave found **146,510 changed pixels inside** the mark rectangle and **zero outside**. The final wall was visually inspected: both hands show five digits, and no letters, numbers, captions, logos, borders, or other prohibited marks were seen. **Unmet visual requirements: none observed.**
