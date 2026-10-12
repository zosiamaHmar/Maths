"""Generic Manim scene: plays a timeline JSON (events + audio) produced by build.py."""
import json
import os
import re
import textwrap

from manim import *

BG = "#0F1B2D"
PANEL = "#18294A"
INK = "#F4F1DE"
GOLD = "#F2C14E"
TEAL = "#3DB2A5"
CORAL = "#EF6F6C"
BLUE = "#7DB8F0"
MUTED = "#8FA3BF"

Text.set_default(font="DejaVu Sans")
FRAC = re.compile(r"\{([^{}|]+)\|([^{}|]+)\}")
LEFT_X = -6.0
TOP_Y = 2.3
BOTTOM_Y = -2.45
MAX_W = 12.0


def piece(s, fs, color):
    """Glyphs of s, vertically aligned on a shared baseline frame (parens trick)."""
    full = Text("(" + s + ")", font_size=fs, color=color).move_to(ORIGIN)
    return VGroup(*full.submobjects[1:-1]), full.height


def build_row(s, fs=34, color=INK):
    """Build a math line; returns (VGroup, row_height). {a|b} -> stacked fraction."""
    parts = []
    pos = 0
    for m in FRAC.finditer(s):
        if s[pos:m.start()].strip():
            parts.append(("t", s[pos:m.start()].strip()))
        parts.append(("f", m.group(1).strip(), m.group(2).strip()))
        pos = m.end()
    if s[pos:].strip():
        parts.append(("t", s[pos:].strip()))
    ref = Text("(=)", font_size=fs).move_to(ORIGIN)
    axis = ref.submobjects[1].get_center()[1]
    _, h = piece("x", fs, color)
    has_frac = any(p[0] == "f" for p in parts)
    items = VGroup()
    cursor = 0.0
    gap = 0.16 * fs / 34
    for p in parts:
        if p[0] == "t":
            g, _ = piece(p[1], fs, color)
            g.shift(RIGHT * (cursor - g.get_left()[0]))
            cursor += g.width + gap
            items.add(g)
        else:
            nfs = int(fs * 0.8)
            ng, nh = piece(p[1], nfs, color)
            dg, _ = piece(p[2], nfs, color)
            w = max(ng.width, dg.width) + 0.16
            off = nh * 0.5 + 0.04
            ng.shift(RIGHT * (cursor + w / 2 - ng.get_center()[0]), UP * (axis + off))
            dg.shift(RIGHT * (cursor + w / 2 - dg.get_center()[0]), UP * (axis - off))
            bar = Line([cursor, axis, 0], [cursor + w, axis, 0], color=color, stroke_width=2.5)
            items.add(VGroup(ng, bar, dg))
            cursor += w + gap
    row_h = (h * 2 * 0.8 + 0.22) if has_frac else h * 1.25
    if items.width > MAX_W:
        items.scale(MAX_W / items.width)
    return items, row_h


def wrapped(s, width, fs, color=INK, lines=3):
    t = textwrap.fill(s, width)
    return Text(t, font_size=fs, color=color, line_spacing=0.9)


class APVideo(Scene):
    def construct(self):
        self.camera.background_color = BG
        data = json.load(open(os.environ["AP_JSON"]))
        self.data = data
        self.cap = None
        self.rows = VGroup()
        self.cursor = TOP_Y
        self.strip = None
        self.chrome(data)
        self.times = []
        for ev in data["events"]:
            getattr(self, "ev_" + ev["kind"])(ev)
        json.dump(self.times, open(os.environ["AP_JSON"] + ".times", "w"))

    # ------------------------------------------------------------ chrome
    def chrome(self, data):
        bar = Rectangle(width=14.4, height=0.7, fill_color=PANEL, fill_opacity=1, stroke_width=0).to_edge(UP, buff=0)
        title = Text(f"Q{data['q']} · {data['title']}", font_size=26, color=GOLD).move_to(bar).align_to(bar, LEFT).shift(RIGHT * 0.5)
        chip = Text("Arithmetic Progressions · Sum of n terms", font_size=18, color=MUTED).move_to(bar).align_to(bar, RIGHT).shift(LEFT * 0.4)
        self.brand = Text("Maths by Zosiama", font_size=20, color=MUTED).to_corner(DR, buff=0.2)
        self.add(bar, title, chip, self.brand)
        self.bar = bar

    def beat_audio(self, ev):
        if ev.get("audio"):
            self.add_sound(ev["audio"])

    def set_caption(self, text):
        self.times.append((self.renderer.time, text))
        if self.cap is not None:
            self.remove(self.cap)
            self.cap = None
        if not text:
            return
        t = textwrap.fill(text, 78)
        txt = Text(t, font_size=24, color=INK, line_spacing=0.9)
        box = RoundedRectangle(corner_radius=0.12, width=txt.width + 0.5, height=txt.height + 0.26,
                               fill_color="#000000", fill_opacity=0.55, stroke_width=0)
        g = VGroup(box, txt)
        txt.move_to(box)
        g.move_to([0, -3.15, 0])
        self.cap = g
        self.add(g)

    def hold(self, ev, used):
        self.wait(max(0.05, ev["dur"] + 0.25 - used))

    # ------------------------------------------------------------ events
    def ev_hook(self, ev):
        terms = self.data["hook"]
        mx = max(abs(x) for x in terms) or 1
        bars = VGroup()
        for i, v in enumerate(terms):
            hgt = 1.6 * abs(v) / mx + 0.15
            r = Rectangle(width=0.9, height=hgt, fill_color=TEAL if v >= 0 else CORAL, fill_opacity=0.9, stroke_color=INK, stroke_width=2)
            r.move_to([(i - (len(terms) - 1) / 2) * 1.45, -0.6 + (hgt / 2 if v >= 0 else -hgt / 2), 0])
            lab = Text(f"{v}".replace("-", "−"), font_size=26, color=INK).next_to(r, UP if v >= 0 else DOWN, buff=0.08)
            bars.add(VGroup(r, lab))
        q = Text("Can you add this AP\nwithout adding every term?", font_size=38, color=GOLD, line_spacing=0.9).move_to([0, 2.3, 0])
        self.beat_audio(ev)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.25, run_time=1.5), FadeIn(q, shift=DOWN * 0.3, run_time=1.0))
        self.set_caption(ev["caption"])
        self.hold(ev, 1.5)
        self.play(FadeOut(bars), FadeOut(q), run_time=0.4)

    def ev_know_title(self, ev):
        self.beat_audio(ev)
        self.know = VGroup()
        self.kt = Text("Know first", font_size=48, color=GOLD).move_to([0, 2.5, 0])
        self.play(FadeIn(self.kt, shift=DOWN * 0.2), run_time=0.5)
        self.set_caption(ev["caption"])
        self.know_y = 1.4
        self.hold(ev, 0.5)

    def ev_know_line(self, ev):
        self.beat_audio(ev)
        row, rh = build_row(ev["math"], fs=40, color=INK)
        row.move_to([0, self.know_y - 0.1, 0])
        box = SurroundingRectangle(row, color=TEAL, buff=0.2, corner_radius=0.12, stroke_width=2.5)
        self.set_caption(ev["caption"])
        self.play(FadeIn(row, shift=UP * 0.15), Create(box), run_time=0.6)
        self.know.add(row, box)
        self.know_y -= max(rh, 0.8) + 0.65
        self.hold(ev, 0.6)

    def ev_know_end(self, ev):
        self.play(FadeOut(self.know), FadeOut(self.kt), run_time=0.4)

    def ev_part_title(self, ev):
        self.clear_board(0.0)
        self.beat_audio(ev)
        lab = Text(f"Question {self.data['q']} {ev['label']}".strip(), font_size=44, color=GOLD).move_to([0, 2.2, 0])
        st = wrapped(ev["stmt"], 52, 34).move_to([0, 0.4, 0])
        if st.width > 12:
            st.scale(12 / st.width)
        self.set_caption(ev["caption"])
        self.play(FadeIn(lab, shift=DOWN * 0.2), FadeIn(st), run_time=0.7)
        self.hold(ev, 0.7)
        self.play(FadeOut(lab), FadeOut(st), run_time=0.4)
        short = (ev["label"] + " " + ev["short"]).strip()
        strip = Text(textwrap.fill(short, 100), font_size=21, color=BLUE, line_spacing=0.85)
        strip.move_to([0, 3.0, 0])
        self.strip = strip
        self.play(FadeIn(strip), run_time=0.3)
        self.cursor = TOP_Y

    def clear_board(self, rt=0.35):
        anims = []
        if len(self.rows):
            anims.append(FadeOut(self.rows))
        if self.strip is not None:
            anims.append(FadeOut(self.strip))
            self.strip = None
        if anims:
            self.play(*anims, run_time=max(rt, 0.3))
        self.rows = VGroup()
        self.cursor = TOP_Y

    def ev_say(self, ev):
        self.beat_audio(ev)
        self.set_caption(ev["caption"])
        self.hold(ev, 0.0)

    def ev_line(self, ev):
        s = ev["math"]
        hl = s.startswith("!")
        s = s.lstrip("!")
        color = GOLD if hl else INK
        row, rh = build_row(s, fs=34, color=color)
        if self.cursor - rh < BOTTOM_Y:  # page is full: start a fresh board
            self.play(FadeOut(self.rows), run_time=0.3)
            self.rows = VGroup()
            self.cursor = TOP_Y
        indent = 0.7 if s.startswith("=") and not hl else (0.7 if s.startswith("=") else 0)
        row.shift(RIGHT * (LEFT_X + indent - row.get_left()[0]), UP * (self.cursor - rh / 2))
        self.cursor -= rh + 0.08
        self.beat_audio(ev)
        self.set_caption(ev["caption"])
        anims = [FadeIn(row, shift=RIGHT * 0.25)]
        if hl:
            anims.append(Indicate(row, color=GOLD, scale_factor=1.04))
        self.play(*anims, run_time=0.6)
        self.rows.add(row)
        self.hold(ev, 0.6)

    def ev_answer(self, ev):
        self.beat_audio(ev)
        if ev.get("sfx"):
            self.add_sound(ev["sfx"])
        row, rh = build_row(ev["math"].lstrip("!"), fs=46, color=GOLD)
        lab = Text("Answer", font_size=30, color=TEAL)
        grp = VGroup(lab, row).arrange(DOWN, buff=0.3)
        box = RoundedRectangle(corner_radius=0.2, width=max(grp.width + 1, 5), height=grp.height + 0.7,
                               fill_color=TEAL, fill_opacity=0.18, stroke_color=TEAL, stroke_width=4)
        card = VGroup(box, grp)
        grp.move_to(box)
        card.move_to([0, 0.2, 0])
        self.set_caption(ev["caption"])
        self.play(FadeOut(self.rows), FadeIn(card, scale=0.8), run_time=0.6)
        self.rows = VGroup()
        self.hold(ev, 0.6)
        self.card = card

    def ev_check_start(self, ev):
        self.beat_audio(ev)
        self.set_caption(ev["caption"])
        self.hold(ev, 0.0)
        self.cursor = TOP_Y
        self.play(self.card.animate.scale(0.55).move_to([0, 2.2, 0]), run_time=0.5)
        self.cursor = 1.3

    def ev_check_end(self, ev):
        if len(self.rows):
            self.play(FadeOut(self.rows), run_time=0.3)
            self.rows = VGroup()
        self.play(FadeOut(self.card), run_time=0.3)
        self.set_caption("")

    def ev_end(self, ev):
        self.clear_board(0.3)
        self.set_caption("")
        self.beat_audio(ev)
        a = Text("Follow", font_size=70, color=INK)
        b = Text("Maths by Zosiama", font_size=84, color=GOLD)
        c = Text("Like  ·  Share  ·  Subscribe", font_size=30, color=MUTED)
        g = VGroup(a, b, c).arrange(DOWN, buff=0.4).move_to([0, 0.2, 0])
        self.remove(self.brand)
        self.play(FadeIn(a, shift=DOWN * 0.3), run_time=0.6)
        self.play(FadeIn(b, scale=0.8), run_time=0.7)
        self.play(FadeIn(c), run_time=0.4)
        self.play(Indicate(b, color=TEAL, scale_factor=1.06), run_time=0.8)
        self.wait(max(0.5, ev["dur"] + 1.2 - 2.5))
