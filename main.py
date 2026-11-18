#!/usr/bin/env python3
"""Entrypoint for the 17 November 2026 news-image bounty.

Copies the pre-rendered infographic (entry.png, produced by render.py)
to the output directory. Stdlib only, no network, no wall-clock input.
"""
import os
import shutil
import sys


def main():
    if len(sys.argv) < 2:
        print("usage: main.py <output-dir>", file=sys.stderr)
        return 2
    out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
