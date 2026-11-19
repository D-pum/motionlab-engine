---
name: lemo-opuscar-codex
description: Produce a complete code-made film with the native Lemo-Opuscar style library in this MotionLab repository. Use for an explicit request to make, create, produce or render a promo, explainer, short film or animation with Lemo or one of its 66 styles.
---

# Lemo-Opuscar for Codex

This is the Codex adapter for Lemo-Opuscar. It keeps Lemo's native style, directing, Canvas/WebGL/Three.js, sound and rendering workflow. It does not translate a Lemo production into Huashu, Remotion or Bang.

## Prepare the pinned library

Run:

```sh
sh skills/lemo-opuscar-codex/scripts/setup.sh
sh skills/lemo-opuscar-codex/scripts/setup.sh deps voice
```

The script installs the pinned library under `vendor/lemo-opuscar`, keeps dependencies inside that ignored checkout and reuses this repository's existing Kokoro model when available. It prints `LIB=<absolute path>` and `PIN=<commit>`.

Before a production, read completely:

1. `$LIB/AGENTS.md`
2. `$LIB/DIRECTOR.md`
3. `$LIB/TECHNIQUE.md`
4. `$LIB/styles/<chosen-style>/STYLE.md`

Read a style's `DEMO.md` and fetch its demo source only where the upstream workflow permits it. Preserve Lemo's treatment-first rule.

## MotionLab decisions

These project decisions override conflicting upstream interaction defaults:

- A normal explicit production prompt is sufficient. Infer routine creative choices and proceed through the finished video.
- Write the complete narration script first. It establishes the story, timing and visual direction before treatment or animation.
- For viral or promotional openings, use the user's three-beat structure when it fits: **context → lean → snap**. The snap must overturn the expectation created by the lean.
- If the user did not name a style, choose the strongest style from the full library for the story. State the choice and reason in one short progress update, then continue. Do not make the user browse all 66 styles.
- Do not ask the upstream language or workflow menu questions when the prompt already supplies enough context. Ask only for information that materially blocks the film.
- Do not pause for storyboard approval unless the user explicitly asks to review a storyboard.
- Default to vertical 1080×1920, 24 fps, H.264/AAC and a duration below 60 seconds. An explicit brief or a style's essential frame-rate requirement wins.
- Use Lemo's local Kokoro path for narration. Cast a suitable installed voice; `am_michael` is the established fallback for English.
- Captions are optional. Follow the brief; do not burn narration captions into the picture unless requested or essential to the selected style.
- Build each film under `productions/<number>-<slug>/` and place the final downloadable MP4 under `deliverables/`.
- Use one preview/look check, one final render and focused delivery checks for routine short work. Add deeper evidence, ASR or forensic checks only when the story or a detected problem needs them.
- A completed requested production includes editable source, reproducible commands, the rendered MP4, a Git commit, a push to the repository's GitHub branch and verification that the remote file matches the reviewed local file.

## Native execution

Use Lemo's own tools from the pinned library:

- `core/render/still.mjs` for look and representative-frame checks
- `core/render/video.mjs` for deterministic frame rendering
- `core/tts/tts.py` for Kokoro narration
- `core/audio/` for score and synchronized foley
- `core/render/mux.sh` for loudness-normalized delivery
- the selected style's native Canvas, WebGL or Three.js techniques

Run native commands through the Codex environment wrapper so browser, package and model caches remain in writable workspace storage and CPU-heavy libraries use bounded threads:

```sh
sh skills/lemo-opuscar-codex/scripts/run.sh node core/render/still.mjs <project> 0 2 4 --size 1080x1920
sh skills/lemo-opuscar-codex/scripts/run.sh .venv/bin/python core/tts/tts.py <lines.json> <voice-output>
```

One shared timeline must drive visuals, narration, score and sound cues. Preserve the style's invariants while adapting its composition to portrait framing; do not crop a landscape layout into vertical after rendering.

## Delivery threshold

Before delivery, verify the final file's duration, dimensions, frame rate, codecs, full decode, audio presence, black frames and representative visual moments. Watch or inspect the beginning, the snap/turn, the main transition and the final call to action. Report limitations honestly and avoid generating redundant reports.

## Upstream provenance

The adapter pins Lemo-Opuscar commit `9eb7739a0fca4c6990fe966cb8b87b1930f7193a`.

Lemo's code and documentation are MIT-licensed. Demo films and stills are CC BY 4.0, with excluded third-party and online-TTS voice assets documented upstream. New films made with the library do not require a LemoLab screen credit. Preserve the upstream license and credit any demo material or third-party assets actually reused.
