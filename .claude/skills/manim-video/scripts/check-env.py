#!/usr/bin/env python3
"""Pre-flight: verify what the manim-video pipeline needs. Exit 0 ok, 1 if a hard requirement is missing."""
from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys

HARD_MODULES = ["manim", "yaml"]
SOFT_MODULES = {"manim_voiceover": "voiceover (--voice)", "gtts": "default gtts voice",
                "pypdf": "--paper with PDFs", "trafilatura": "--paper with web pages"}
HARD_BINS = ["ffmpeg", "ffprobe"]


def has_mod(m: str) -> bool:
    return importlib.util.find_spec(m) is not None


def main() -> int:
    bad, warn = [], []
    if sys.version_info < (3, 9):
        bad.append("python >= 3.9 required")
    for m in HARD_MODULES:
        if not has_mod(m):
            bad.append(f"missing python module: {m}")
    for b in HARD_BINS:
        if not shutil.which(b):
            bad.append(f"missing binary: {b}")
    for m, why in SOFT_MODULES.items():
        if not has_mod(m):
            warn.append(f"missing python module {m} (needed for {why})")
    if not (shutil.which("xelatex") or shutil.which("latex")):
        warn.append("LaTeX not found: MathTex/Tex will fail; planner should use Text")
    if shutil.which("ffmpeg"):
        out = subprocess.run(["ffmpeg", "-hide_banner", "-filters"], capture_output=True, text=True).stdout
        if " xfade " not in out:
            warn.append("ffmpeg lacks xfade (need >= 4.3): scenes will be hard-cut")
    if has_mod("manim") and has_mod("manimlib"):
        warn.append("both Manim Community (manim) and ManimGL (manimlib) installed; this skill targets Manim Community")
    for w in warn:
        print(f"warning: {w}", file=sys.stderr)
    for b in bad:
        print(f"error: {b}", file=sys.stderr)
    if bad:
        print("fix: bash scripts/install.sh", file=sys.stderr)
        return 1
    print("env ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
