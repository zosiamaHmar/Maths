---
name: manim
description: 'Write and render math animations with ManimGL (3b1b/manim, package manimgl, import manimlib). Use when the user asks for a manim scene, a 3Blue1Brown-style animation, or to render/debug one. Not for Manim Community Edition.'
license: MIT
---

# manim (ManimGL)

This is 3b1b's version: `from manimlib import *`. It is NOT Manim Community (`from manim import *`). APIs differ.

## Setup (once)

1. `apt-get install -y libpango1.0-dev pkg-config libcairo2-dev ffmpeg`
2. `pip install manimgl` (or `git clone https://github.com/3b1b/manim && pip install -r requirements.txt && pip install -e .`)
3. Optional LaTeX: `apt-get install -y texlive-science texlive-fonts-extra texlive-latex-extra`
4. Check: `python3 -c "import manimlib; print(manimlib.__version__)"`

## Scene template

```python
from manimlib import *

class MyScene(Scene):
    def construct(self):
        circle = Circle()
        self.play(ShowCreation(circle))   # ManimGL: ShowCreation, not Create
        self.play(circle.animate.shift(RIGHT))
        self.wait()
```

## Render

- Video, 720p: `manimgl scene.py MyScene -w -m`
- Video, 1080p: `manimgl scene.py MyScene -w --hd`
- Last frame only (fast check): `manimgl scene.py MyScene -s -w`
- Draft: `-l` (480p). GIF: `-i`. Transparent: `-t`.
- Start at animation N: `-n 3`. Clear cache: `--clear-cache`.
- Needs a GPU/OpenGL. In this cloud container rendering fails with "No suitable graphics adapter found" (tested). Write scenes here; render on a machine with a GPU.

## Differences from Manim Community

- `ShowCreation`, not `Create`.
- `TexText` for text with LaTeX, `Tex` for math, `Text` for Pango text.
- `self.frame` is the camera (`self.frame.animate.reorient(...)`).
- Use `.animate` for property animations, `set_backstroke` for readable labels.

## Rules

1. Check `example_scenes.py` in the repo for working patterns before inventing API.
2. On a GPU machine, render the last frame (`-s -w`) and view it before a full render.
3. If LaTeX is missing, use `Text` instead of `Tex`, or install texlive.
4. On errors, quote file:line, cause, fix. Do not guess APIs: grep `manimlib/` for the class.

Docs: https://3b1b.github.io/manim/
