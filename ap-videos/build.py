#!/usr/bin/env python3
"""Build the AP videos: offline TTS (espeak-ng) -> Manim render -> ffmpeg mix/export.

usage: build.py [question numbers...]   (default: all)
"""
import hashlib, json, os, re, subprocess, sys, wave, math, struct
from pathlib import Path
import content

ROOT = Path(__file__).parent.resolve()
WORK = ROOT / "work"
OUT = ROOT / "out"
PY = os.environ.get("MANIM_PY", "/tmp/mv/bin/python")
for d in (WORK, OUT, WORK / "audio"):
    d.mkdir(parents=True, exist_ok=True)

SUBMAP = {c: str(i) for i, c in enumerate("₀₁₂₃₄₅₆₇₈₉")}
SUBMAP.update({"ₙ": "n", "ₘ": "m", "ₚ": "p", "₊": " plus ", "₋": " minus "})
SUPS = {"²": " squared ", "³": " cubed "}
LETTER_A = re.compile(r"\ba\b(?=\s*(?:$|[=+−×,.)\]²]|and\b|to\b|from\b|is\b|on\b|cancels|alone|terms|minus|plus|times|equals|over|cancels))")


def speak(s, math=True):
    s = s.lstrip("!").replace("★", "star").replace("✓", "").replace("—", ",")
    s = re.sub(r"\.\.\.\s*\((\d)\)", r", equation \1", s)
    s = s.replace("(★)", "equation star").replace("(star)", "equation star")
    s = re.sub(r"[₀-₉ₙₘₚ₊₋]+", lambda m: " " + "".join(SUBMAP[c] for c in m.group(0)) + " ", s)
    for k, v in SUPS.items():
        s = s.replace(k, v)
    s = s.replace("₹", "rupees ").replace("½", " and a half")
    s = re.sub(r"\{([^{}|]+)\|([^{}|]+)\}", r", \1 over \2, ", s)
    s = re.sub(r"([\w\)])\s*\(", r"\1 times (", s)
    s = re.sub(r"\)\s*(?=[A-Za-z\d])", ") times ", s)
    s = s.replace("−", " minus ").replace("+", " plus ").replace("×", " times ")
    s = s.replace("÷", " divided by ").replace("=", " equals ").replace("/", " over ")
    s = s.replace("…", " and so on ").replace(":", " to ")
    s = re.sub(r"[()\[\]]", " ", s)
    s = re.sub(r"\bAPs?\b", lambda m: "A P" + ("s" if m.group(0).endswith("s") else ""), s)
    s = LETTER_A.sub("[a](/eɪ/)", s)
    s = re.sub(r"(?<=\d)\s*\.\s*\.\s*", " ", s)
    return re.sub(r"\s+", " ", s).strip(" ,")


def say_text(s):
    """Narration of a caption sentence (prose with embedded symbols)."""
    return speak(s)


_K = None


def kokoro():
    global _K
    if _K is None:
        from kokoro_onnx import Kokoro
        _K = Kokoro(str(WORK / "kokoro" / "kokoro-v1.0.int8.onnx"), str(WORK / "kokoro" / "voices-v1.0.bin"))
    return _K


def tts(text):
    """Offline Kokoro-82M voice (af_heart)."""
    import soundfile as sf
    h = hashlib.md5(("k1" + text).encode()).hexdigest()[:16]
    p = WORK / "audio" / f"{h}.wav"
    if not p.exists():
        samples, sr = kokoro().create(text, voice="af_heart", speed=0.95, lang="en-us")
        sf.write(str(p), samples, sr)
    with wave.open(str(p)) as w:
        dur = w.getnframes() / w.getframerate()
    return str(p), dur


def make_sfx():
    p = WORK / "chime.wav"
    if p.exists():
        return str(p)
    sr = 22050
    frames = []
    for i in range(int(sr * 1.2)):
        t = i / sr
        env = math.exp(-3.5 * t)
        v = env * (math.sin(2 * math.pi * 784 * t) + 0.6 * math.sin(2 * math.pi * 1175 * t) + 0.3 * math.sin(2 * math.pi * 1568 * t)) * 0.18
        frames.append(struct.pack("<h", int(v * 32767)))
    with wave.open(str(p), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(b"".join(frames))
    return str(p)


def make_music():
    p = WORK / "music.wav"
    if p.exists():
        return str(p)
    sr = 22050
    L = 24
    chords = [(220, 277.2, 329.6), (174.6, 220, 261.6), (196, 246.9, 293.7), (164.8, 207.7, 246.9)]
    out = bytearray()
    for i in range(int(sr * L)):
        t = i / sr
        c = chords[int(t // 6) % 4]
        seg = (t % 6) / 6
        env = math.sin(math.pi * seg) ** 0.5
        v = sum(math.sin(2 * math.pi * f * t) for f in c) / 3 * env * 0.5
        out += struct.pack("<h", int(v * 32767))
    with wave.open(str(p), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(bytes(out))
    return str(p)


def beat(kind, caption=None, narr=None, **kw):
    ev = dict(kind=kind, caption=caption or "", **kw)
    if narr:
        ev["audio"], ev["dur"] = tts(narr)
    else:
        ev["dur"] = 0.4
    return ev


def build_events(pb):
    ev = []
    ev.append(beat("hook", "Can you add this AP without adding every term? Stay till the end!",
                   "Hi, welcome to Maths by Zosiama! Can you add this A P, without adding every single term? "
                   "Stay till the end, and I will show you every step."))
    ev.append(beat("know_title", "Know first: the formulas we need", "First, know these formulas. We will use them in every step."))
    for key in pb["know"]:
        line, desc = content.K[key]
        ev.append(beat("know_line", desc, say_text(desc) + ". " + speak(line), math=line))
    ev.append(dict(kind="know_end", caption="", dur=0.2))
    for p in pb["parts"]:
        lab = p["label"]
        intro = (f"Part {lab.strip('()')}. " if lab else "") + speak(p["stmt"])
        ev.append(beat("part_title", p["stmt"], intro, label=lab, stmt=p["stmt"], short=p["short"]))
        for say, lines in p["steps"]:
            ev.append(beat("say", say, say_text(say)))
            for ln in lines:
                ev.append(beat("line", say, speak(ln), math=ln))
        ev.append(beat("answer", "Answer: " + p["ans"].replace("{", "").replace("|", "/").replace("}", ""),
                       "So the answer is. " + speak(p["ans"]), math="!" + p["ans"], sfx=make_sfx()))
        if p["check"]:
            ev.append(beat("check_start", "Let's check our answer", "Let's check our answer."))
            for say, lines in p["check"]:
                ev.append(beat("say", say, say_text(say)))
                for ln in lines:
                    ev.append(beat("line", say, speak(ln), math=ln))
            ev.append(dict(kind="check_end", caption="", dur=0.2))
    ev.append(beat("end", "Follow Maths by Zosiama", "Thanks for watching! Follow Maths by Zosiama, for more maths made easy."))
    return ev


def srt_time(t):
    ms = int(t * 1000)
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


def solutions_md(pb):
    out = [f"# Question {pb['q']} — {pb['title']}\n"]
    for p in pb["parts"]:
        out.append(f"## {p['label']} {p['stmt']}\n")
        for say, lines in p["steps"]:
            out.append(f"- **{say}**")
            for ln in lines:
                out.append(f"  - `{ln.lstrip('!')}`")
        out.append(f"\n**Answer:** `{p['ans']}`\n")
        for say, lines in p["check"]:
            out.append(f"- *Check — {say}*: " + "; ".join(f"`{l}`" for l in lines))
        out.append("")
    return "\n".join(out)


def build(q):
    pb = next(p for p in content.PROBLEMS if p["q"] == q)
    name = f"Q{q:02d}"
    ev = build_events(pb)
    data = dict(q=q, title=pb["title"], hook=pb["hook"], events=ev)
    jp = WORK / f"{name}.json"
    jp.write_text(json.dumps(data, ensure_ascii=False))
    (OUT / f"{name}_solutions.md").write_text(solutions_md(pb))
    env = dict(os.environ, AP_JSON=str(jp))
    raw = WORK / "media" / "videos" / "scene" / "720p30" / f"{name}_raw.mp4"
    subprocess.run([PY, "-m", "manim", "render", "-qm", "--fps", "30", "-r", "1280,720", "--disable_caching",
                    "--media_dir", str(WORK / "media"), "-o", f"{name}_raw", str(ROOT / "scene.py"), "APVideo"],
                   check=True, env=env, stdout=subprocess.DEVNULL, stderr=open(WORK / f"{name}.log", "w"))
    # captions (.srt) from the recorded timeline
    times = json.loads(Path(str(jp) + ".times").read_text())
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(raw)]))
    srt, i = [], 1
    for k, (t, txt) in enumerate(times):
        end = times[k + 1][0] if k + 1 < len(times) else dur
        if txt and end - t > 0.05:
            srt.append(f"{i}\n{srt_time(t)} --> {srt_time(end)}\n{txt}\n")
            i += 1
    (OUT / f"{name}.srt").write_text("\n".join(srt))
    final = OUT / f"{name}_{re.sub(r'[^A-Za-z0-9]+', '_', pb['title']).strip('_')}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-stream_loop", "-1", "-i", make_music(),
                    "-filter_complex", "[0:a]aresample=48000,volume=1.0[v];[1:a]aresample=48000,volume=0.07,"
                    f"afade=t=out:st={dur - 2:.2f}:d=2[m];[v][m]amix=inputs=2:duration=first:normalize=0[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
                    "-crf", "20", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-movflags", "+faststart",
                    "-metadata", "author=Maths by Zosiama", "-metadata", f"title=Q{q} {pb['title']} - Maths by Zosiama",
                    "-shortest", str(final)], check=True)
    print(name, f"{dur:.0f}s", final.name, flush=True)


if __name__ == "__main__":
    qs = [int(a) for a in sys.argv[1:]] or [p["q"] for p in content.PROBLEMS]
    for q in qs:
        build(q)
