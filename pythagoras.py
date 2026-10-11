from manimlib import *
import json


NARRATION = json.load(open("narration/narration.json"))
PAD = 0.6  # silence after each narrated line


class PythagoreanTheorem(Scene):
    def cue(self, k):
        self.cues[k] = self.time

    def hold(self, k):
        """Wait until line k has finished speaking."""
        self.wait(max(0.01, self.cues[k] + NARRATION["durations"][k] + PAD - self.time))

    def construct(self):
        self.cues = {}
        self.cue(0)
        # ---------- Intro ----------
        title = Text("The Pythagorean Theorem", font_size=56)
        title.to_edge(UP)
        self.play(Write(title))
        formula = Tex("a^2 + b^2 = c^2", font_size=72)
        formula.next_to(title, DOWN, buff=0.8)
        self.play(FadeIn(formula, shift=UP))
        self.hold(0)

        # ---------- Right triangle ----------
        a, b = 1.8, 2.4
        c = (a * a + b * b) ** 0.5  # 3.0
        A = np.array([0.0, 0.0, 0.0])
        B = np.array([b, 0.0, 0.0])
        C = np.array([0.0, a, 0.0])
        tri = Polygon(A, B, C, color=YELLOW, fill_color=YELLOW, fill_opacity=0.35)
        tri_group = VGroup(tri)
        tri_group.move_to(DOWN * 0.8)
        la = Tex("a", color=BLUE).next_to(tri.get_vertices()[0] * 0.5 + tri.get_vertices()[2] * 0.5, LEFT)
        lb = Tex("b", color=GREEN).next_to(tri.get_vertices()[0] * 0.5 + tri.get_vertices()[1] * 0.5, DOWN)
        lc = Tex("c", color=RED).next_to(tri.get_vertices()[1] * 0.5 + tri.get_vertices()[2] * 0.5, UR, buff=0.1)
        box = Square(side_length=0.3, color=WHITE).move_to(tri.get_vertices()[0] + np.array([0.15, 0.15, 0]))
        self.cue(1)
        self.play(
            FadeOut(formula),
            ShowCreation(tri),
            FadeIn(box),
        )
        self.play(Write(la), Write(lb), Write(lc))
        self.hold(1)
        self.play(FadeOut(VGroup(tri, la, lb, lc, box)))

        # ---------- Proof by rearrangement ----------
        s = a + b
        origin = np.array([-s / 2 - 3.6, -s / 2 - 0.3, 0.0])

        def P(x, y):
            return origin + np.array([x, y, 0.0])

        outer = Square(side_length=s, color=WHITE, stroke_width=3)
        outer.move_to(P(s / 2, s / 2))
        self.cue(2)
        self.play(ShowCreation(outer))

        # Arrangement 1: four triangles in the corners, tilted c-square left over
        p1, p2, p3, p4 = P(a, 0), P(s, a), P(s - a, s), P(0, s - a)
        arr1 = [
            [P(0, 0), p1, p4],
            [P(s, 0), p2, p1],
            [P(s, s), p3, p2],
            [P(0, s), p4, p3],
        ]
        tris = VGroup(*[
            Polygon(*v, color=YELLOW, fill_color=YELLOW, fill_opacity=0.4, stroke_width=2)
            for v in arr1
        ])
        self.play(LaggedStartMap(FadeIn, tris, lag_ratio=0.4))
        self.hold(2)

        csq = Polygon(p1, p2, p3, p4, color=RED, fill_color=RED, fill_opacity=0.5)
        clab = Tex("c^2", color=RED, font_size=60).move_to(csq)
        self.cue(3)
        self.play(FadeIn(csq), Write(clab))
        eq1 = Tex("(a+b)^2 - 4 \\cdot \\tfrac{1}{2}ab = c^2", font_size=40)
        eq1.move_to(np.array([2.6, 1.6, 0]))
        self.play(Write(eq1))
        self.hold(3)

        # Arrangement 2: same triangles, two squares left over
        arr2 = [
            [P(a, 0), P(s, 0), P(s, a)],
            [P(a, 0), P(a, a), P(s, a)],
            [P(0, a), P(a, a), P(a, s)],
            [P(0, a), P(0, s), P(a, s)],
        ]
        new_tris = VGroup(*[
            Polygon(*v, color=YELLOW, fill_color=YELLOW, fill_opacity=0.4, stroke_width=2)
            for v in arr2
        ])
        self.cue(4)
        self.play(
            FadeOut(csq), FadeOut(clab),
            *[Transform(t, nt) for t, nt in zip(tris, new_tris)],
            run_time=3,
        )
        self.hold(4)
        self.cue(5)

        asq = Square(side_length=a, color=BLUE, fill_color=BLUE, fill_opacity=0.5, stroke_width=2)
        asq.move_to(P(a / 2, a / 2))
        bsq = Square(side_length=b, color=GREEN, fill_color=GREEN, fill_opacity=0.5, stroke_width=2)
        bsq.move_to(P(a + b / 2, a + b / 2))
        alab = Tex("a^2", color=BLUE, font_size=48).move_to(asq)
        blab = Tex("b^2", color=GREEN, font_size=60).move_to(bsq)
        self.play(FadeIn(asq), FadeIn(bsq), Write(alab), Write(blab))
        eq2 = Tex("(a+b)^2 - 4 \\cdot \\tfrac{1}{2}ab = a^2 + b^2", font_size=40)
        eq2.next_to(eq1, DOWN, buff=0.6)
        self.play(Write(eq2))
        self.hold(5)

        # ---------- Conclusion ----------
        self.cue(6)
        final = Tex("a^2 + b^2 = c^2", font_size=84, color=YELLOW)
        final.move_to(np.array([2.6, -1.4, 0]))
        self.play(Write(final))
        self.play(Indicate(final, scale_factor=1.2))
        self.hold(6)
        json.dump(self.cues, open('narration/cues.json', 'w'))
