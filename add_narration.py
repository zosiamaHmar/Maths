"""Mix narration audio and burn captions into out/PythagoreanTheorem.mp4."""
import json, re, subprocess

N = json.load(open("narration/narration.json"))
cues = json.load(open("narration/cues.json"))
src, dst = "out/PythagoreanTheorem.mp4", "out/PythagoreanTheorem_narrated.mp4"


def ts(t):
    h, rem = divmod(t, 3600)
    m, sec = divmod(rem, 60)
    return f"{int(h):02}:{int(m):02}:{int(sec):02},{int((sec % 1) * 1000):03}"


def chunks(text, limit=60):
    parts = re.split(r"(?<=[.,:])\s+", text)
    out, cur = [], ""
    for p in parts:
        if cur and len(cur) + len(p) + 1 > limit:
            out.append(cur)
            cur = p
        else:
            cur = f"{cur} {p}".strip()
    return out + [cur] if cur else out


srt, n = [], 1
for k, text in enumerate(N["lines"]):
    start, dur = cues[str(k)], N["durations"][k]
    cs = chunks(text)
    total = sum(len(c) for c in cs)
    t = start
    for c in cs:
        d = dur * len(c) / total
        srt.append(f"{n}\n{ts(t)} --> {ts(t + d)}\n{c}\n")
        n += 1
        t += d
open("out/PythagoreanTheorem.srt", "w").write("\n".join(srt))

inputs, filt = [], []
for k in range(len(N["lines"])):
    inputs += ["-i", f"narration/line{k}.wav"]
    ms = int(cues[str(k)] * 1000)
    filt.append(f"[{k+1}:a]adelay={ms}|{ms}[a{k}]")
mix = "".join(f"[a{k}]" for k in range(len(N["lines"])))
filt.append(f"{mix}amix=inputs={len(N['lines'])}:normalize=0[aud]")
style = "FontName=DejaVu Sans,FontSize=18,Outline=2,Shadow=0,MarginV=24"
filt.append(f"[0:v]subtitles=out/PythagoreanTheorem.srt:force_style='{style}'[vid]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, *inputs, "-filter_complex", ";".join(filt),
                "-map", "[vid]", "-map", "[aud]", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-shortest", dst], check=True)
print("wrote", dst)
