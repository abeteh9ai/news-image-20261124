#!/usr/bin/env python3
"""Copy the bundled front-page image to the grading output folder.

The image itself is drawn by render.py and shipped in this repo as
entry.png. This entry point only validates the file (PNG signature,
size, dimensions) and copies it byte for byte, so both grading runs
write identical output. Standard library only; no network, no clock,
no randomness — the same input always yields the same output.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SOURCE = ROOT / "entry.png"
MAX_BYTES = 1_048_576
MAX_EDGE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(msg):
    print(f"main.py: {msg}", file=sys.stderr)
    return 1


def check_png(blob):
    """Return (width, height) or raise SystemExit with a message."""
    if blob[:8] != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG file")
    if len(blob) > MAX_BYTES:
        raise SystemExit(f"entry.png is {len(blob)} bytes, over 1 MiB")
    if len(blob) < 24 or blob[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    w = int.from_bytes(blob[16:20], "big")
    h = int.from_bytes(blob[20:24], "big")
    if w > MAX_EDGE or h > MAX_EDGE:
        raise SystemExit(f"entry.png is {w}x{h}, over 1024 on a side")
    return w, h


def run():
    try:
        blob = SOURCE.read_bytes()
    except OSError as exc:
        return fail(f"cannot read entry.png: {exc}")
    try:
        w, h = check_png(blob)
    except SystemExit as exc:
        return fail(str(exc))
    dest_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "entry.png"
    shutil.copyfile(SOURCE, dest)
    digest = hashlib.sha256(blob).hexdigest()
    print(f"entry.png ({w}x{h}, {len(blob)} bytes, sha256 {digest}) "
          f"-> {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
