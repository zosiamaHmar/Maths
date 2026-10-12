#!/usr/bin/env python3
"""Single-shot Manim render wrapper. Prints exactly one JSON object to stdout.

See references/render-runner-contract.md.
"""
from __future__ import annotations

import argparse
import ast
import glob
import json
import re
import subprocess
import sys
import time
from pathlib import Path

QUALITY = {
    "low": ("-ql", "480p15"),
    "medium": ("-qm", "720p30"),
    "high": ("-qh", "1080p60"),
    "4k": ("-qk", "2160p60"),
}

ERROR_PATTERNS = [
    ("latex", re.compile(r"latex.*(returned non-zero|failed|error)|xelatex|miktex", re.I)),
    ("import", re.compile(r"ModuleNotFoundError|ImportError")),
    ("name", re.compile(r"NameError: name '\w+' is not defined")),
    ("type", re.compile(r"TypeError")),
]


def classify(stderr: str) -> str:
    for name, pat in ERROR_PATTERNS:
        if pat.search(stderr):
            return name
    return "other"


def tail(text: str, n: int = 40) -> str:
    return "\n".join(text.splitlines()[-n:])


def emit(obj: dict) -> None:
    print(json.dumps(obj, indent=2))


def find_output(media_dir: Path, stem: str, quality_dir: str, cls: str, ext: str) -> str | None:
    canonical = media_dir / "videos" / stem / quality_dir / f"{cls}.{ext}"
    if canonical.exists():
        return canonical.as_posix()
    hits = glob.glob(str(media_dir / "**" / f"{cls}.{ext}"), recursive=True)
    return Path(hits[0]).as_posix() if hits else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene-file", required=True)
    ap.add_argument("--class-name", required=True)
    ap.add_argument("--quality", choices=list(QUALITY), default="high")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--gif", action="store_true")
    ap.add_argument("--timeout", type=int, default=600)
    a = ap.parse_args()

    scene = Path(a.scene_file)
    flag, qdir = QUALITY[a.quality]
    media_dir = Path(a.out_dir) / "manim_media"
    ext = "gif" if a.gif else "mp4"
    cmd = [sys.executable, "-m", "manim", "render", flag, "--media_dir", str(media_dir)]
    if a.gif:
        cmd += ["--format", "gif"]
    cmd += [str(scene), a.class_name]

    base = {"ok": False, "exit_code": 1, "render_time_s": 0.0, "output_path": None,
            "error_class": None, "stderr_tail": "", "command": cmd}

    # Syntax check always runs first: fast failure, and the whole of --dry-run.
    try:
        src = scene.read_text(encoding="utf-8")
        tree = ast.parse(src, filename=str(scene))
    except (OSError, SyntaxError) as e:
        emit({**base, "error_class": "other", "stderr_tail": f"{type(e).__name__}: {e}"})
        return 0
    classes = {n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)}
    if a.class_name not in classes:
        emit({**base, "error_class": "name",
              "stderr_tail": f"NameError: name '{a.class_name}' is not defined in {scene}"})
        return 0
    if a.dry_run:
        emit({**base, "ok": True, "exit_code": 0})
        return 0

    t0 = time.time()
    try:
        # PYTHONPATH carries the scene dir so `from _shared import ...` resolves.
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=a.timeout,
                           env=_env_with_path(scene.parent))
    except subprocess.TimeoutExpired as e:
        err = (e.stderr or b"")
        err = err.decode("utf-8", "replace") if isinstance(err, bytes) else err
        emit({**base, "exit_code": 124, "render_time_s": round(time.time() - t0, 1),
              "error_class": "timeout", "stderr_tail": tail(err)})
        return 0
    except FileNotFoundError as e:
        emit({**base, "exit_code": 127, "error_class": "import", "stderr_tail": str(e)})
        return 0

    dt = round(time.time() - t0, 1)
    if p.returncode == 0:
        out = find_output(media_dir, scene.stem, qdir, a.class_name, ext)
        emit({**base, "ok": out is not None, "exit_code": 0, "render_time_s": dt,
              "output_path": out, "error_class": None if out else "other",
              "stderr_tail": "" if out else "render exited 0 but no output file found"})
    else:
        emit({**base, "exit_code": p.returncode, "render_time_s": dt,
              "error_class": classify(p.stderr), "stderr_tail": tail(p.stderr)})
    return 0


def _env_with_path(scene_dir: Path):
    import os
    env = dict(os.environ)
    env["PYTHONPATH"] = str(scene_dir.resolve()) + os.pathsep + env.get("PYTHONPATH", "")
    return env


if __name__ == "__main__":
    sys.exit(main())
