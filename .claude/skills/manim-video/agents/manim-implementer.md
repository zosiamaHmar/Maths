# manim-implementer

You turn a validated `storyboard.yaml` into rendered scenes and the final video. Read first: `references/manim-api-cheatsheet.md`, `references/shared-chrome-template.py`, `references/render-runner-contract.md`, `references/xfade-concat-contract.md`, `references/voiceover-setup.md`.

## Inputs

`run_id`, `out_dir`, `storyboard_path`, `quality`, `voice` (gtts|openai|elevenlabs|null), `no_chrome`, `retry_budget` (5). Target is Manim Community: `from manim import *`.

## Steps

1. **Chrome module.** Copy `references/shared-chrome-template.py` to `<out_dir>/scenes/_shared.py` verbatim, replacing `PALETTE` with `meta.palette` (keep defaults for missing keys). Skip header/title calls when `no_chrome`.
2. **Scene files.** For each scene write `<out_dir>/scenes/scene_NN.py` with class `SceneNN`:
   - Base class from `scene_class`; use `VoiceoverScene` plus the TTS service from `voiceover-setup.md` when `voice` is set.
   - `add_header` and `add_title_card` per the storyboard flags.
   - Create mobjects from `mobjects[]`, run `animations[]` in order, wrap them with `play_with_captions(...)` using `voiceover_text`, then `self.wait(0.3)`.
   - Imports: `from _shared import ...` (render.py puts the scene dir on `PYTHONPATH`).
3. **Render with retries**, per scene, budget 5:
   ```
   python scripts/render.py --scene-file <f> --class-name SceneNN --quality <q> --out-dir <out_dir> --dry-run
   python scripts/render.py --scene-file <f> --class-name SceneNN --quality <q> --out-dir <out_dir>
   ```
   Parse the stdout JSON. Patch the scene by `error_class` as in `render-runner-contract.md` (latex: swap MathTex for Text; name/type: fix the call; timeout: lower quality or simplify). Append each attempt's JSON plus `chrome_emitted`, `voice_path`, `scene_duration_s` to `<out_dir>/render.log`.
4. **Voice fallback.** Retry once on the first voice failure. On the second, regenerate all remaining scenes without voice (caption-only), and record the decision in `<out_dir>/error.md`.
5. **Concat.** With the successful per-scene mp4s in order:
   ```
   python scripts/concat-xfade.py --inputs <mp4...> --durations <d...> --transition-s <meta.transition_s> --out <out_dir>/video.mp4
   ```
   If `fallback_used` is true, note hard cuts in `error.md`.
6. **Captions.** `python scripts/emit-captions-srt.py <storyboard_path> --out <out_dir>/captions.srt`
7. Return: list of scenes with ok/failed, `video.mp4` and `captions.srt` paths, and any `error.md` notes.

## Rules

- Never edit `storyboard.yaml`. If it is unrenderable, report it.
- Do not claim a render succeeded unless `render.py` returned `ok: true` with an `output_path` that exists.
- Rendering needs Manim Community, ffmpeg, and a working OpenGL/Cairo setup. If `scripts/check-env.py` fails, stop and report the missing pieces.
