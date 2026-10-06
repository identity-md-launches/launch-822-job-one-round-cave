#!/usr/bin/env python3
"""Offline PNG stamp and contribution-record checker for Pepeolithic line 2."""

import argparse
import hashlib
import json
import struct
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
WALL = ROOT / "artifacts/line-2/wall.png"
RECORDS = ROOT / "dist/line-2"
SIGNATURE = b"\x89PNG\r\n\x1a\n"


def inside_workspace(value):
    path = Path(value)
    if path.is_absolute():
        raise ValueError("use a workspace-relative path")
    resolved = (ROOT / path).resolve()
    if not resolved.is_relative_to(ROOT):
        raise ValueError("path escapes this workspace")
    return resolved


def png(path):
    data = path.read_bytes()
    if not data.startswith(SIGNATURE):
        raise ValueError(f"{path}: not a PNG")
    pos = len(SIGNATURE)
    header = None
    compressed = []
    ended = False
    while pos < len(data):
        if pos + 12 > len(data):
            raise ValueError("truncated PNG chunk")
        size = struct.unpack_from(">I", data, pos)[0]
        kind = data[pos + 4:pos + 8]
        end = pos + 12 + size
        if end > len(data):
            raise ValueError("truncated PNG data")
        body = data[pos + 8:pos + 8 + size]
        expected = struct.unpack_from(">I", data, pos + 8 + size)[0]
        actual = zlib.crc32(kind + body) & 0xffffffff
        if expected != actual:
            raise ValueError("bad PNG chunk CRC")
        if kind == b"IHDR":
            if header is not None or size != 13:
                raise ValueError("invalid PNG header")
            width, height, depth, color, comp, filt, interlace = struct.unpack(">IIBBBBB", body)
            if depth != 8 or color not in (2, 6) or comp or filt or interlace:
                raise ValueError("PNG must be noninterlaced 8-bit RGB or RGBA")
            if width < 1 or height < 1 or width * height > 16_000_000:
                raise ValueError("invalid or oversized PNG")
            header = (width, height, 3 if color == 2 else 4)
        elif kind == b"IDAT":
            compressed.append(body)
        elif kind == b"IEND":
            ended = True
            break
        pos = end
    if not header or not ended or not compressed:
        raise ValueError("incomplete PNG")
    width, height, channels = header
    stride = width * channels
    raw = zlib.decompress(b"".join(compressed))
    if len(raw) != height * (stride + 1):
        raise ValueError("incorrect PNG pixel count")
    pixels = bytearray(height * stride)
    previous = bytearray(stride)
    for y in range(height):
        offset = y * (stride + 1)
        method = raw[offset]
        row = bytearray(raw[offset + 1:offset + 1 + stride])
        if method > 4:
            raise ValueError("unsupported PNG filter")
        for i in range(stride):
            left = row[i - channels] if i >= channels else 0
            above = previous[i]
            upper_left = previous[i - channels] if i >= channels else 0
            if method == 1:
                prediction = left
            elif method == 2:
                prediction = above
            elif method == 3:
                prediction = (left + above) // 2
            elif method == 4:
                p = left + above - upper_left
                distances = (abs(p - left), abs(p - above), abs(p - upper_left))
                prediction = (left, above, upper_left)[distances.index(min(distances))]
            else:
                prediction = 0
            row[i] = (row[i] + prediction) & 255
        pixels[y * stride:(y + 1) * stride] = row
        previous = row
    return width, height, channels, pixels


def chunk(kind, body):
    return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body) & 0xffffffff)


def write_rgb(path, width, height, pixels):
    stride = width * 3
    scanlines = b"".join(b"\0" + pixels[y * stride:(y + 1) * stride] for y in range(height))
    data = SIGNATURE
    data += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    data += chunk(b"IDAT", zlib.compress(scanlines, 9))
    data += chunk(b"IEND", b"")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def stamp(args):
    base = inside_workspace(args.base)
    mark = inside_workspace(args.mark)
    output = inside_workspace(args.out)
    if not output.is_relative_to(ROOT / "artifacts/line-2"):
        raise ValueError("stamp output must be under artifacts/line-2")
    bw, bh, bc, background = png(base)
    mw, mh, mc, ink = png(mark)
    if bc != 3 or mc != 4:
        raise ValueError("base must be RGB and transparent mark must be RGBA")
    if bw != bh or bw < 1024:
        raise ValueError("base wall must be square and at least 1024 pixels wide")
    target_width = args.width
    target_height = round(mh * target_width / mw)
    if target_width < 1 or target_height < 1:
        raise ValueError("invalid mark size")
    touched = 0
    for dy in range(target_height):
        by = args.y + dy
        if not 0 <= by < bh:
            continue
        sy = min(mh - 1, int((dy + 0.5) * mh / target_height))
        for dx in range(target_width):
            bx = args.x + dx
            if not 0 <= bx < bw:
                continue
            sx = min(mw - 1, int((dx + 0.5) * mw / target_width))
            si = (sy * mw + sx) * 4
            alpha = ink[si + 3]
            if alpha == 0:
                continue
            bi = (by * bw + bx) * 3
            for color in range(3):
                background[bi + color] = (ink[si + color] * alpha + background[bi + color] * (255 - alpha) + 127) // 255
            touched += 1
    if touched == 0:
        raise ValueError("mark did not touch wall")
    write_rgb(output, bw, bh, background)
    print(f"stamped {touched} pixels; {bw}x{bh} RGB PNG: {output.relative_to(ROOT)}")


def numbered_records():
    records = sorted(RECORDS.glob("[0-9][0-9].json")) if RECORDS.exists() else []
    for number, path in enumerate(records, 1):
        if path.name != f"{number:02d}.json":
            raise ValueError("record numbers are not consecutive")
    return records


def record(args):
    records = numbered_records()
    number = len(records) + 1
    if number > 21:
        raise ValueError("line already has 21 records")
    width, height, channels, _ = png(WALL)
    if width != height or width < 1024 or channels != 3:
        raise ValueError("wall must be a square RGB PNG of at least 1024 pixels")
    digest = hashlib.sha256(WALL.read_bytes()).hexdigest()
    value = {
        "name": args.name,
        "image": "https://api.imd.fun/artifacts/" + digest,
        "attributes": [
            {"trait_type": "Wall", "value": "Line 2"},
            {"trait_type": "Number", "value": number},
            {"trait_type": "Left behind", "value": args.tool},
        ],
    }
    RECORDS.mkdir(parents=True, exist_ok=True)
    destination = RECORDS / f"{number:02d}.json"
    with destination.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    print(f"wrote {destination.relative_to(ROOT)} with SHA-256 {digest}")


def verify(_args):
    records = numbered_records()
    if not records:
        raise ValueError("no line-2 records")
    record_path = records[-1]
    data = json.loads(record_path.read_text(encoding="utf-8"))
    if set(data) != {"name", "image", "attributes"} or not isinstance(data["name"], str):
        raise ValueError("record has wrong top-level fields")
    attrs = data["attributes"]
    if not isinstance(attrs, list) or len(attrs) != 3:
        raise ValueError("record must have exactly three attributes")
    if any(not isinstance(a, dict) or set(a) != {"trait_type", "value"} for a in attrs):
        raise ValueError("invalid attribute")
    traits = {a["trait_type"]: a["value"] for a in attrs}
    if traits.get("Wall") != "Line 2" or traits.get("Number") != len(records) or not traits.get("Left behind"):
        raise ValueError("record traits do not match this line and step")
    if set(traits) != {"Wall", "Number", "Left behind"}:
        raise ValueError("unexpected record trait")
    width, height, channels, _ = png(WALL)
    if width != height or width < 1024 or channels != 3:
        raise ValueError("wall must be a square RGB PNG of at least 1024 pixels")
    digest = hashlib.sha256(WALL.read_bytes()).hexdigest()
    expected = "https://api.imd.fun/artifacts/" + digest
    if data["image"] != expected:
        raise ValueError("record image does not match wall SHA-256")
    print(f"OK: {record_path.relative_to(ROOT)} -> {width}x{height} RGB PNG, SHA-256 {digest}")
    print(f"Tool left behind: {traits['Left behind']}; {len(records)} consecutive record(s)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("stamp", help="place a transparent PNG mark on a wall")
    add.add_argument("--base", required=True, help="workspace-relative RGB PNG")
    add.add_argument("--mark", required=True, help="workspace-relative RGBA PNG")
    add.add_argument("--out", default="artifacts/line-2/wall.png")
    add.add_argument("--x", type=int, required=True)
    add.add_argument("--y", type=int, required=True)
    add.add_argument("--width", type=int, required=True)
    add.set_defaults(run=stamp)
    add = commands.add_parser("record", help="write next numbered metadata record")
    add.add_argument("--name", required=True)
    add.add_argument("--tool", required=True)
    add.set_defaults(run=record)
    add = commands.add_parser("verify", help="check latest record and wall")
    add.set_defaults(run=verify)
    args = parser.parse_args()
    try:
        args.run(args)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        parser.exit(1, f"error: {error}\n")


if __name__ == "__main__":
    main()
