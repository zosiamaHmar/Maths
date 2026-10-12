#!/usr/bin/env python3
"""Write captions.srt from storyboard.yaml with cumulative offsets across scenes.

Usage: emit-captions-srt.py <storyboard.yaml> --out <captions.srt> [--transition-s T]
Scene i starts at sum(duration_0..i-1) - T*i (matches concat-xfade.py). Prints one JSON line.
"""
from __future__ import annotations

import argparse
import json
import sys

import yaml


def ts(t: float) -> str:
    t = max(0.0, t)
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def chunk(text: str, dur: float, words_per: int = 10):
    words = text.split()
    chunks = [" ".join(words[i:i + words_per]) for i in range(0, len(words), words_per)] or [text]
    step = dur / len(chunks)
    return [{"text": c, "start_s": i * step, "duration_s": step} for i, c in enumerate(chunks)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard")
    ap.add_argument("--out", required=True)
    ap.add_argument("--transition-s", type=float, default=None)
    a = ap.parse_args()

    sb = yaml.safe_load(open(a.storyboard, encoding="utf-8"))
    T = a.transition_s if a.transition_s is not None else sb["meta"].get("transition_s", 0.7)
    T = min(1.5, max(0.3, float(T)))
    lines, n, cum = [], 0, 0.0
    for idx, sc in enumerate(sb["scenes"]):
        base = max(0.0, cum - T * idx)
        caps = sc.get("captions") or chunk(sc.get("voiceover_text", ""), sc["duration_s"])
        for c in caps:
            n += 1
            start = base + float(c["start_s"])
            end = start + float(c["duration_s"])
            lines += [str(n), f"{ts(start)} --> {ts(end)}", c["text"], ""]
        cum += sc["duration_s"]
    open(a.out, "w", encoding="utf-8").write("\n".join(lines))
    print(json.dumps({"ok": True, "captions": n, "out": a.out}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
