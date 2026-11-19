#!/usr/bin/env python3
"""news-image-20261118 v3 entry (Python 3.13, standard library only).

The entry image is entry.png beside this file: a 46-story newspaper front
page for Wednesday 18 November 2026, rendered locally by render.py. Copy
it, byte for byte, to /output/entry.png so the judge sees exactly those
bytes.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
TARGET = OUTPUT_DIR / "entry.png"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    if not SOURCE.is_file():
        raise FileNotFoundError(f"entry image missing: {SOURCE}")
    with open(SOURCE, "rb") as fh:
        if fh.read(8) != b"\x89PNG\r\n\x1a\n":
            raise RuntimeError("entry image is not a PNG file")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    # Deterministic output: both runs must write the same bytes, so the
    # copy has to match the source exactly, byte for byte.
    if TARGET.stat().st_size != SOURCE.stat().st_size:
        raise RuntimeError("copied entry.png has the wrong size")
    if TARGET.stat().st_size > 1048576:
        raise RuntimeError("entry image exceeds the 1 MiB limit")
    if sha256(TARGET) != sha256(SOURCE):
        raise RuntimeError("copied entry.png does not match the source")


if __name__ == "__main__":
    main()
