"""PNG helpers copied unchanged from line 2 Wall Step; no CLI or filesystem discovery."""
import struct
import zlib

SIGNATURE = b"\x89PNG\r\n\x1a\n"


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


