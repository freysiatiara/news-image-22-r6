#!/usr/bin/env python3
"""Entry program: write the committed front page to the output directory.

The picture itself (entry.png, drawn by draw.py) sits beside this file in
the repository. The program only copies those bytes, so every run writes
exactly the same file. Standard library only; no network.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = (os.environ.get("MAKEFUN_OUTPUT_DIR")
               or os.environ.get("OUTPUT_DIR")
               or "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
