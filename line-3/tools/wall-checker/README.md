# Wall checker

This dependency-free Python script checks the current line-3 wall and its numbered JSON record. It reports the PNG dimensions, format, SHA-256, record fields, and the visual requirements that cannot be certified mechanically (such as whether the cave figure is recognizably Pepe and whether each hand has five digits).

Run it from the repository root:

```sh
python3 line-3/tools/wall-checker/check_wall.py artifacts/line-3/wall.png dist/line-3/01.json
```

When tried for this step, it found a square PNG at least 1024×1024, a matching lowercase SHA-256 artifact URL, and the required `Wall`, `Number`, and `Left behind` traits. Visual review remains required for the cave-painting style, no-writing rule, retained marks, and five-digit hands.
