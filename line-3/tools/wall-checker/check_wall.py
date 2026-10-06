#!/usr/bin/env python3
"""Check a Pepeolithic wall PNG and its record using only the Python stdlib."""
import hashlib
import json
import struct
import sys
from pathlib import Path


def png_info(path):
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    if data[12:16] != b"IHDR":
        raise ValueError("PNG has no IHDR")
    width, height, depth, color_type, compression, filter_method, interlace = struct.unpack(
        ">IIBBBBB", data[16:29]
    )
    return data, width, height, depth, color_type


def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} WALL.png RECORD.json", file=sys.stderr)
        return 2
    wall, record = map(Path, sys.argv[1:])
    try:
        data, width, height, depth, color_type = png_info(wall)
        obj = json.loads(record.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        return 1
    digest = hashlib.sha256(data).hexdigest()
    expected = {"name", "image", "attributes"}
    traits = {item.get("trait_type"): item.get("value") for item in obj.get("attributes", [])}
    checks = {
        "square PNG >= 1024": width == height and width >= 1024 and height >= 1024,
        "record keys exact": set(obj) == expected,
        "artifact hash matches": obj.get("image") == "https://api.imd.fun/artifacts/" + digest,
        "required traits": {"Wall", "Number", "Left behind"}.issubset(traits),
    }
    print(f"wall: {width}x{height}, bit depth {depth}, color type {color_type}, format PNG")
    print(f"sha256: {digest}")
    for label, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'}: {label}")
    print("REVIEW: cave figure, no letters/numbers, retained marks, and five-digit hands require visual inspection")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
