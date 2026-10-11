"""Generate narration audio (espeak-ng) and timing for pythagoras.py."""
import json, subprocess, pathlib

LINES = [
    "The Pythagorean theorem says that, in a right triangle, the squares of the two shorter sides add up to the square of the longest side.",
    "Here is a right triangle. The two shorter sides, a and b, are called the legs. The longest side, c, is the hypotenuse.",
    "To prove it, take four copies of this triangle, and place them inside a big square whose side is a plus b.",
    "The triangles leave a tilted square in the middle, with side c. So the big square's area is the four triangles, plus c squared.",
    "Now slide the triangles to new spots. The total area does not change.",
    "This time, the leftover space is two squares: one with side a, and one with side b.",
    "Same big square, same four triangles. So c squared must equal a squared plus b squared. That is the Pythagorean theorem.",
]

out = pathlib.Path("narration")
out.mkdir(exist_ok=True)
durs = []
for i, text in enumerate(LINES):
    wav = out / f"line{i}.wav"
    subprocess.run(["espeak-ng", "-v", "en-us+f3", "-s", "150", "-p", "55", "-w", str(wav), text], check=True)
    d = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(wav)]))
    durs.append(d)
json.dump({"lines": LINES, "durations": durs}, open(out / "narration.json", "w"), indent=1)
print([round(d, 1) for d in durs])
