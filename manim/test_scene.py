from manim import *


class Test(Scene):
    def construct(self):
        eq = MathTex(r"e^{i\pi} + 1 = 0")
        self.play(Write(eq))
        self.play(eq.animate.scale(1.5).set_color(YELLOW))
        self.wait()
