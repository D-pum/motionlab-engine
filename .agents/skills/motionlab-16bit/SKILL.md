---
name: motionlab-16bit
description: Produce MotionLab 16-bit pixel-art films using indexed palettes, original sprites, game-native storytelling and the existing native Canvas workflow. Use for 16-bit, pixel art or pixel RPG briefs. Freeze episode choices during initial planning and reduce repeated setup, reading and creative reconsideration while preserving visual quality.
---

# MotionLab 16-bit

## Scope
Work inside MotionLab Experiments. Follow the current user brief first. Use the shared Viz3D/HTML stage. Canvas pixel-art inserts are treatments on that timeline. Do not switch production engines. For this workflow, replace older adapter requirements for per-film remote pushes with local delivery and milestone backup. Preserve unrelated rules.

Resolve paths from the project root. Store source under `productions/<number>-<slug>/` and finals under `deliverables/`. Treat actual checked-out rules as authoritative over remembered chat.

## Load once
Read `AGENTS.md`, `SOURCES.md` and `skills/lemo-opuscar-codex/SKILL.md` once per unchanged working context. Use existing `vendor/lemo-opuscar`, pinned at `9eb7739a0fca4c6990fe966cb8b87b1930f7193a` or an intentionally recorded local revision. Preserve local changes.

Read its `AGENTS.md`, `DIRECTOR.md`, `TECHNIQUE.md` and `styles/pixel-rpg/STYLE.md`. Load only relevant supporting files required by those instructions. Do not browse other style families. After context loss, restore the checkpoint and required instructions; do not assume previous reads remain available.

Inspect installed dependencies once. Run setup only for missing prerequisites. Never routinely clone, reinstall, update or query remote status between scenes. Complete local preparation before starting the planning timer. If a prerequisite is missing offline, identify it precisely rather than inventing an engine.

## Plan once
Target three minutes of creative planning after resources and inputs are ready. Honor an approved script. If asked to write or research one, complete that editorial work before freezing visual execution.

Save `production-plan.json` in the production directory with:
- Frozen status, style name, actual upstream revision and approved script path.
- Output dimensions, fps, duration, logical framebuffer, integer scale, stage rectangle and safe areas.
- Exact palette hex values and roles, protected indices, lighting ramps, sprite sizes, font paths and verified language coverage.
- Asset paths and provenance; narration source or explicitly absent voice; captions mode and sound policy.
- Ordered scenes: IDs, frame ranges, purpose, composition, assets, actions, camera coordinates, palette changes and text/audio cues.
- Every transition's effect, duration, parameters, carried object and matched outgoing/incoming positions.
- Exact preview, render, mux and validation commands verified from installed tools.
- Review ranges, acceptance criteria and ordered fallback choices.

Use exact values. Do not defer decisions with "smooth transition", "add polish" or "choose later". Choose a storytelling system appropriate to the subject: inventory for allocation, battle for competing forces, overworld for geography, stats for change. Do not force every topic into a fantasy quest.

If an essential decision cannot be resolved in the target time, record it and finish only the necessary planning. Never sacrifice quality to the timer or claim an unmeasured elapsed time.

After saving the treatment, read `styles/pixel-rpg/DEMO.md`. Inspect only reusable modules needed for that treatment, as permitted upstream. Keep the story and direction original.

## Visual contract
- Render a genuine logical pixel framebuffer and enlarge with nearest-neighbor sampling.
- For full portrait use 180x320 at 6x for 1080x1920. For the preferred 3:4 stage use 180x240 at 6x for 1080x1440 within that portrait. Freeze stage placement and safe rectangles. Never stretch a landscape demo into portrait.
- Use an indexed framebuffer and about 32 fixed colors. Reserve one or two protected colors when continuity needs them. Preserve warm and dark ramps; map color reductions by luminance rather than palette rank.
- Round sprite, camera and each parallax layer to logical pixels. Disable smoothing throughout enlargement. Use integer zoom steps or mosaic transitions instead of fractional scene scaling.
- Use palette ramps, 1-pixel outlines and ordered Bayer dithering. Avoid photographic texture, blur, bloom, scanlines and alpha-blended palette fades in the pixel scene.
- Create original sprites around 20-34 logical pixels tall with recognizable silhouettes and consistent lighting. Use 32x32 portraits when facial acting serves the story. Reuse rigs and sprite sheets.
- Show meaningful state changes: interaction, transfer, transformation, choice, accumulation or consequence. Moving a still image alone does not meet the motion standard.
- Keep floors, hands, props and important action clear of UI and captions. Inspect readability at phone size.

## Motion and transitions
Default to 24 fps output unless overridden. Animate walks at 8 fps and fire/blink cycles up to 12 fps. Evaluate movement from absolute frame/time so seeks reproduce identically. Avoid accumulated real-time simulation and unseeded randomness.

Include anticipation, action, reaction and settle within planned timing. Move cameras and parallax each output frame while remaining on the pixel grid. Use occlusion, layered parallax and palette lighting for depth.

Choose transitions in planning: protected-color object match, integer side-scroll continuation, mosaic reveal, Bayer dissolve or stepped palette fade. Compute both endpoints of a match. Use encounter swirls only for justified conflict. Preserve object identity and screen position; do not add arbitrary effects while executing.

## Text and sound
Follow the brief's captions decision. When captions are requested without another direction, retain bold outlined box-free captions in platform-safe areas. Render them as a deliberate readable output overlay while keeping the art framebuffer crisp. Choose pixel dialogue UI only during planning when requested or justified; avoid duplicate dialogue and captions.

For pixel dialogue use a licensed local font, integer sizes, measured wrapping and adequate reading time. Verify glyph coverage. For Hindi/Bengali use a shaping-capable font/renderer and preserve grapheme clusters. If suitable pixel lettering is unavailable, use the planned readable overlay fallback. Never silently transliterate or display missing-glyph boxes.

Drive animation, audio, dialogue and SRT from one timeline. Synchronize to actual narration when available; mark provisional timing when voice is pending. Preserve the user's narration policy and configured local capabilities.

Default to restrained atmosphere and purposeful Foley. Pixel visuals do not require constant text blips or arcade beeps. Use original chiptune music only when planned. Apply the native mix checks; keep speech clear and peaks unclipped.

## Execute the frozen plan
Use selected upstream framebuffer, palette, font, UI and rig mechanisms where permitted. Follow treatment-before-demo restrictions. Preserve licenses. Do not copy demo plots, characters, shot sequences or melodies.

Use installed native `core/render/still.mjs`, `core/render/video.mjs`, `core/audio/` and `core/render/mux.sh` through the existing wrapper as applicable. Verify command syntax locally once; do not guess arguments.

Save commands in the production directory. Maintain one compact `production-state.json`: plan path, completed scenes, changed files, last successful command, failed check, attempted remedy and next action. Save full logs to disk and surface only relevant excerpts. Read targeted files/diffs rather than repeatedly listing the project.

Do not reopen style selection, rewrite approved narration or redesign accepted scenes during execution. Allow technical reasoning needed to implement the plan. When an unforeseen blocker invalidates it, append one scoped amendment with reason and affected scenes, then resume. Do not substitute weaker work merely to finish.

## Ordered repairs
| Failure | Remedy order |
|---|---|
| Blurred pixels | Disable smoothing; remove fractional transforms; verify integer enlargement; inspect re-export |
| Camera shimmer | Round each layer independently; remove subpixel presentation transforms |
| Muddy palette | Check LUT/ramp mapping; restore warm/dark entries; repair affected palette |
| Text overflow | Measure and rewrap; split within existing timing if readable; use planned overlay fallback; amend timing only if needed |
| Missing asset | Use frozen substitute; otherwise create an original equivalent preserving story function and record it |
| Render failure | Diagnose failing wrapper/dependency/stage; repair it and retain completed outputs |
| Static motion | Restore planned state change, anticipation and reaction; inspect affected range |

Never repeat an unchanged failing command. Retry when a repair or new evidence changes the outcome. After applicable remedies are exhausted, report the exact blocker. Do not run open-ended repair loops.

## Quality and completion
Run a representative look pass covering the opening, smallest text, palette extremes, key transformation and distinct transition mechanisms. Inspect motion clips as well as stills. Repair changed sections and adjacent boundaries, preserving accepted work.

Inspect the complete final film for clarity, pacing, acting, pixel stability, text readability, continuity and sound. Verify dimensions, fps, duration, codecs, full decode, required audio and unintended black/silent intervals. Honor intentionally planned darkness and silence.

Deliver the playable MP4, requested script/SRT, editable source and reproducible commands. Report missing voice and limitations accurately. Keep files local and accessible. Use remote backup/versioning at requested milestones, not per scene or as a prerequisite to local delivery.

## Provenance
Adapt the pixel method from `lemomo-ai/lemo-opuscar/styles/pixel-rpg/STYLE.md` at the pinned revision and the existing MotionLab adapter. Preserve MIT notices for reused code/docs, CC BY attribution for reused demo media and actual asset/font licenses. This skill bundles instructions, not a renderer, fonts or sprites. Do not claim demonstrated visual quality until a film is rendered and reviewed.
