# MotionLab production

## Production foundation

Start every new film in the Reconquista remake workflow documented in `workflows/viz3d/README.md`. Use its local Three.js runtime, one seekable Chromium stage and the shared master renderer. Carry the approved workflow forward across batches. A change of visual treatment happens on that timeline. Change engines only on an explicit request from the user. Preserve older films with their original build paths for reproduction.

## Start each production

Read the brief, the Viz3D workflow, SOURCES.md and the MotionLab Director skill. Use the Director pass to choose staging, shot scale, camera, edit and sound within Viz3D. Use the 16-bit skill for pixel-art beats. Upstream examples can inform individual treatments. Start with a new production directory, an original scene and the shared renderer. When GPU capture fails, diagnose the scene and capture the same stage using the remake's software WebGL route if necessary. Work within this repository.

## Mandatory MotionLab Director gates

1. **Before building or resuming production**, complete the Director pass in `production-plan.json`. For each story beat, record what the viewer sees happen, how the camera reveals it, and what carries across the cut. For resumed work, check the existing plan against these gates and revise any missing or inadequate direction before advancing, even if the plan is marked frozen. For a planning-only brief, complete this gate and deliver the plan.
2. **Choose the style for the story beat.** Consider the full range of treatments in the Director pass. Mix them where a change helps the viewer understand what happened, feel the stakes, or follow a change in time, place, or point of view. Use 3D where space, scale, or physical action carries the beat. Record what each chosen treatment contributes and what connects it to the adjacent shots.
3. **Before the full render**, review a representative motion preview that crosses at least one cut. Time it against the narration or a scratch read of the approved script when final voiceover is pending. Check that the action and camera carry the story across the cut. Revise and review again if the sequence plays like a series of illustrated slides.
4. **Before delivery**, watch the complete cut against the narration or scratch read and verify that the visuals carry the major story turns. Record the preview and full-cut review outcomes in the production plan or delivery notes. Still frames and export checks are separate checks for legibility and file integrity.

## Original briefs and narration handoff

Set the runtime by the story and its pacing unless the user specifies a duration.
For a narrated short, save the exact narration and planned cue timing, then share them with the user before building or rendering the visuals so they can generate TTS in parallel.

## Creative ownership
Use the upstream materials to learn and make your own directing decisions for the current story. Carry the film through animation, synchronized sound, visual review, revision and final MP4 delivery. Do not stop at the first working render.
Develop the visual language from the supplied story. Use recurring subjects, color, camera direction, or sound to keep the edit coherent across treatments.
Proceed autonomously when the brief is sufficient. Honor the user's supplied script, scope and explicit creative directions. Ask only when an essential missing input genuinely blocks completion.
An approved script is editorial input: preserve it unless the user requests changes or research. Asset sourcing and technical checks do not authorize rewriting the narration.

## Output defaults
Follow production-specific instructions first. Otherwise, portrait output defaults to 1080x1920 at 60 fps, H.264 MP4 with AAC audio. The 3:4 animation stage and caption layout are preferences that may be deliberately varied to serve a film.
When captions are requested, default to bold outlined text without background boxes, with spoken-word emphasis and platform-safe placement. Honor requests for no captions.
Reuse configured narration capabilities when appropriate. If voiceover is unavailable, complete the usable animation/audio deliverable and clearly identify what remains.
Render and inspect representative moments and transitions, revise visible weaknesses, and run the applicable native checks. Report actual outputs and remaining limitations honestly.

## Project hygiene
Keep each production in its own directory with editable source, reproducible commands, dependency versions, upstream revisions and attribution.
Keep upstream tools scoped to the project; avoid duplicate global installations. Preserve licenses and use project-local dependency environments.
Commit source and delivery notes. Follow existing explicit delivery exceptions when an MP4 is tracked in deliverables/; otherwise keep large renders, downloaded tools, caches and secrets out of git. Make the completed MP4 accessible to the user.

## Story and production direction

For new films apply the story, worldbuilding, evidence, asset sourcing and motion-review guidance in docs/DIRECTOR-NOTES.md. The user may supply a premise or a script with optional bracketed direction cues. The director owns the remaining decisions.

## User preference for scripts, voices and captions

Keep script research, critique and revisions at the text stage. The user handles narration and captions. Do not generate narration with Piper, Kokoro or another tool, generate subtitle files, or burn captions into video. This instruction supersedes earlier production defaults.

## Locked video formats

For snappy visual what-ifs, follow formats/snappy-visual-what-if.md. This format uses one clear rule, escalating visual consequences and a payoff, with sound design and minimal functional on-screen information.

For SCP and conspiracy stories, follow formats/scp-and-conspiracy-stories.md. Use incidents, character objectives, evidence-driven discoveries and consequences. Preserve source accuracy and distinguish factual evidence, allegations, fiction and reconstruction.

For mechanical visual explainers, follow formats/mechanical-visual-explainer.md. For journalist explainers, follow formats/journalist-explainer.md. These are separate locked formats. The user's standing narration and caption preference applies to both.
