#!/usr/bin/env python3
"""Merged print runs. Run with: uv run --with pypdf pdf_runs.py

  pdf_runs.py build <manifest.json>    build every run file from the manifest
  pdf_runs.py verify <manifest.json>   page-count runs vs manifest; nonzero on mismatch

Manifest: {"tabloid-run.pdf": [["s01.pdf", 2], ["s02.pdf", 1]], ...}
Paths resolve relative to the manifest's directory.
"""
import json
import os
import sys
from pypdf import PdfReader, PdfWriter


def load(path):
    with open(path) as f:
        m = json.load(f)
    return m, os.path.dirname(os.path.abspath(path))


def build(path):
    manifest, root = load(path)
    for run, parts in manifest.items():
        w = PdfWriter()
        for src, qty in parts:
            for _ in range(qty):
                w.append(os.path.join(root, src))
        out = os.path.join(root, run)
        with open(out, "wb") as f:
            w.write(f)
        print(f"{run}: {len(w.pages)} pages")


def verify(path):
    manifest, root = load(path)
    ok = True
    for run, parts in manifest.items():
        expected = sum(qty * len(PdfReader(os.path.join(root, src)).pages)
                       for src, qty in parts)
        got = len(PdfReader(os.path.join(root, run)).pages)
        status = "OK" if expected == got else "MISMATCH"
        ok &= expected == got
        print(f"{run}: expected {expected}, got {got} — {status}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] in ("build", "verify"):
        (build if sys.argv[1] == "build" else verify)(sys.argv[2])
    else:
        print(__doc__)
        sys.exit(2)
