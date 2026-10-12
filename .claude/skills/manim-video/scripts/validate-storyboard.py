#!/usr/bin/env python3
"""Validate a storyboard.yaml (schema 0.2.0). Exit 0 ok, 1 on errors (listed on stderr).

See references/storyboard-schema.md.
"""
from __future__ import annotations

import re
import sys

import yaml

QUALITIES = {"low", "medium", "high", "4k"}
VOICES = {"gtts", "openai", "elevenlabs", None}
SOURCES = {"idea", "math", "paper"}
SCENE_CLASSES = {"Scene", "MovingCameraScene", "ThreeDScene", "ZoomedScene", "VoiceoverScene"}
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
PASCAL = re.compile(r"^[A-Z][A-Za-z0-9]*$")
TEXTY = {"Text", "MathTex", "Tex", "MarkupText"}


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def validate(sb) -> tuple[list[str], list[str]]:
    errs: list[str] = []
    warns: list[str] = []
    if not isinstance(sb, dict):
        return ["/: storyboard must be a mapping"], warns
    meta, scenes = sb.get("meta"), sb.get("scenes")
    if not isinstance(meta, dict):
        errs.append("/meta: required mapping")
        meta = {}
    if not isinstance(scenes, list) or not (1 <= len(scenes) <= 30):
        errs.append("/scenes: required list of 1..30 scenes")
        scenes = scenes if isinstance(scenes, list) else []

    ver = str(meta.get("schema_version", ""))
    if ver != "0.2.0":
        errs.append(f"/meta/schema_version: must be '0.2.0' (got {ver!r}); 0.1.x storyboards need migration")
    for k in ("title", "topic"):
        if not isinstance(meta.get(k), str) or not meta[k].strip():
            errs.append(f"/meta/{k}: required non-empty string")
    src = meta.get("source")
    if not isinstance(src, dict) or src.get("kind") not in SOURCES:
        errs.append("/meta/source/kind: must be one of idea|math|paper")
    if meta.get("quality") not in QUALITIES:
        errs.append("/meta/quality: must be one of low|medium|high|4k")
    if meta.get("voice") not in VOICES:
        errs.append("/meta/voice: must be gtts|openai|elevenlabs|null")
    tot = meta.get("total_duration_s")
    if not num(tot) or not (5 <= tot <= 1800):
        errs.append("/meta/total_duration_s: number in 5..1800")
    ts = meta.get("transition_s", 0.7)
    if not num(ts) or not (0.3 <= ts <= 1.5):
        errs.append("/meta/transition_s: number in 0.3..1.5")
    pal = meta.get("palette")
    if pal is not None:
        if not isinstance(pal, dict):
            errs.append("/meta/palette: must be a mapping")
        else:
            for k, v in pal.items():
                if k not in {"primary", "accent", "warn", "bg"} or not (isinstance(v, str) and HEX.match(v)):
                    errs.append(f"/meta/palette/{k}: expected key primary|accent|warn|bg with #RRGGBB value")

    dsum = 0.0
    for i, sc in enumerate(scenes):
        p = f"/scenes/{i}"
        if not isinstance(sc, dict):
            errs.append(f"{p}: must be a mapping")
            continue
        if sc.get("id") != f"scene_{i + 1:02d}":
            errs.append(f"{p}/id: expected 'scene_{i + 1:02d}' (ids must be contiguous from scene_01)")
        for k in ("title", "beat"):
            if not isinstance(sc.get(k), str) or not sc[k].strip():
                errs.append(f"{p}/{k}: required non-empty string")
        d = sc.get("duration_s")
        if not num(d) or not (1 <= d <= 90):
            errs.append(f"{p}/duration_s: number in 1..90")
        else:
            dsum += d
        if sc.get("scene_class", "Scene") not in SCENE_CLASSES:
            errs.append(f"{p}/scene_class: must be one of {sorted(SCENE_CLASSES)}")

        names = set()
        mobs = sc.get("mobjects", [])
        if not isinstance(mobs, list):
            errs.append(f"{p}/mobjects: must be a list")
            mobs = []
        for j, m in enumerate(mobs):
            mp = f"{p}/mobjects/{j}"
            if not isinstance(m, dict) or not PASCAL.match(str(m.get("type", ""))):
                errs.append(f"{mp}/type: PascalCase Manim class name required")
                continue
            if m.get("name"):
                names.add(m["name"])
            if m["type"] in TEXTY and not m.get("content"):
                errs.append(f"{mp}/content: required for {m['type']}")

        anims = sc.get("animations")
        if not isinstance(anims, list) or not anims:
            errs.append(f"{p}/animations: at least one animation required")
            anims = []
        for j, an in enumerate(anims):
            ap = f"{p}/animations/{j}"
            if not isinstance(an, dict):
                errs.append(f"{ap}: must be a mapping")
                continue
            if not PASCAL.match(str(an.get("anim", ""))):
                errs.append(f"{ap}/anim: PascalCase animation name required")
            dur = an.get("duration", 1)
            if not num(dur) or not (0.1 <= dur <= 30):
                errs.append(f"{ap}/duration: number in 0.1..30")
            t = str(an.get("target", ""))
            if not t:
                errs.append(f"{ap}/target: required")
            elif not (t in names or re.match(r"^mobjects\[\d+\]$", t) or t.startswith("VGroup(")):
                errs.append(f"{ap}/target: {t!r} does not match any mobjects[].name in {sc.get('id')}")

        vt = sc.get("voiceover_text")
        if not isinstance(vt, str) or len(vt.split()) < 5:
            errs.append(f"{p}/voiceover_text: required, at least 5 words")
        elif len(vt) > 2000:
            errs.append(f"{p}/voiceover_text: max 2000 chars")
        elif num(d) and len(vt.split()) > 2.5 * d + 6:
            warns.append(f"{p}/voiceover_text: {len(vt.split())} words for {d}s may overflow (target <= 2.5 words/s)")

        for j, c in enumerate(sc.get("captions") or []):
            cp = f"{p}/captions/{j}"
            if not (isinstance(c, dict) and isinstance(c.get("text"), str) and num(c.get("start_s")) and num(c.get("duration_s"))):
                errs.append(f"{cp}: needs text, start_s, duration_s")
            elif num(d) and c["start_s"] + c["duration_s"] > d + 0.01:
                warns.append(f"{cp}: caption ends after scene duration")

    if num(tot) and scenes and abs(dsum - tot) > 1.0:
        errs.append(f"/meta/total_duration_s: {tot} != sum of scene durations {dsum} (tolerance 1s)")
    return errs, warns


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate-storyboard.py <storyboard.yaml>", file=sys.stderr)
        return 2
    try:
        sb = yaml.safe_load(open(sys.argv[1], encoding="utf-8"))
    except (OSError, yaml.YAMLError) as e:
        print(f"cannot read storyboard: {e}", file=sys.stderr)
        return 1
    errs, warns = validate(sb)
    for w in warns:
        print(f"warning: {w}", file=sys.stderr)
    for e in errs:
        print(f"error: {e}", file=sys.stderr)
    if errs:
        return 1
    print("storyboard ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
