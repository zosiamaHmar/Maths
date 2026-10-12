#!/usr/bin/env python3
"""Chain scene mp4s with ffmpeg xfade/acrossfade. Prints one JSON object.

See references/xfade-concat-contract.md.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def tail(text: str, n: int = 50) -> str:
    return "\n".join(text.splitlines()[-n:])


def has_xfade() -> bool:
    try:
        p = subprocess.run(["ffmpeg", "-hide_banner", "-filters"], capture_output=True, text=True, timeout=30)
        return " xfade " in p.stdout
    except (OSError, subprocess.SubprocessError):
        return False


def probe_has_audio(path: str) -> bool:
    try:
        p = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "a",
             "-show_entries", "stream=codec_type", "-of", "csv=p=0", path],
            capture_output=True, text=True, timeout=30)
        return "audio" in p.stdout
    except (OSError, subprocess.SubprocessError):
        return False


def build_command(inputs, durations, T, out, audio):
    cmd = ["ffmpeg", "-y", "-hide_banner"]
    for i in inputs:
        cmd += ["-i", i]
    parts, vlab, cum = [], "[0:v]", 0.0
    for i in range(1, len(inputs)):
        cum += durations[i - 1]
        offset = max(0.0, cum - T * i)
        lab = f"[v{i}]"
        parts.append(f"{vlab}[{i}:v]xfade=transition=fade:duration={T}:offset={offset:.3f}{lab}")
        vlab = lab
    alab = "[0:a]"
    if audio:
        for i in range(1, len(inputs)):
            lab = f"[a{i}]"
            parts.append(f"{alab}[{i}:a]acrossfade=duration={T}{lab}")
            alab = lab
    cmd += ["-filter_complex", ";".join(parts), "-map", vlab]
    if audio:
        cmd += ["-map", alab, "-c:a", "aac"]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", out]
    return cmd


def run(cmd, timeout):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stderr
    except subprocess.TimeoutExpired:
        return 124, "ffmpeg timed out"
    except FileNotFoundError:
        return 127, "ffmpeg not found on PATH"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", nargs="+", required=True)
    ap.add_argument("--durations", nargs="+", type=float, required=True)
    ap.add_argument("--transition-s", type=float, default=0.7)
    ap.add_argument("--out", required=True)
    ap.add_argument("--timeout", type=int, default=120)
    a = ap.parse_args()

    if len(a.inputs) != len(a.durations):
        print(json.dumps({"ok": False, "exit_code": 2, "total_duration_s": 0, "command": [],
                          "fallback_used": False,
                          "stderr_tail": "--inputs and --durations must have equal length"}))
        return 0
    T = min(1.5, max(0.3, a.transition_s))
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    if len(a.inputs) == 1:
        shutil.copyfile(a.inputs[0], out)
        print(json.dumps({"ok": True, "exit_code": 0, "total_duration_s": a.durations[0],
                          "command": ["copy", a.inputs[0], str(out)], "fallback_used": False,
                          "stderr_tail": ""}, indent=2))
        return 0

    audio = all(probe_has_audio(i) for i in a.inputs)
    total_x = sum(a.durations) - T * (len(a.inputs) - 1)
    cmd, err, code = [], "", 1
    if has_xfade():
        cmd = build_command(a.inputs, a.durations, T, str(out), audio)
        code, err = run(cmd, a.timeout)
        if code == 0:
            print(json.dumps({"ok": True, "exit_code": 0, "total_duration_s": round(total_x, 2),
                              "command": cmd, "fallback_used": False, "stderr_tail": ""}, indent=2))
            return 0

    # Fallback: plain concat demuxer, hard cuts.
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        for i in a.inputs:
            f.write(f"file '{Path(i).resolve().as_posix()}'\n")
        lst = f.name
    fcmd = ["ffmpeg", "-y", "-hide_banner", "-f", "concat", "-safe", "0", "-i", lst,
            "-c", "copy", str(out)]
    fcode, ferr = run(fcmd, a.timeout)
    Path(lst).unlink(missing_ok=True)
    print(json.dumps({"ok": fcode == 0, "exit_code": fcode,
                      "total_duration_s": round(sum(a.durations), 2), "command": fcmd,
                      "fallback_used": True, "stderr_tail": tail(ferr if fcode else err)}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
