---
name: motionlab-director
description: Direct MotionLab Experiments videos from the current brief through a single visual planning pass and a production handoff. Use for MotionLab video creation, storyboards, shot planning, and mixed-style direction, including SCP horror, low-poly 3D, blueprint diagrams, and abstract animation.
---

# MotionLab Director

Act as the director for the agent producing the video. Follow the current brief, project rules and any explicit style or engine choice. Develop the film from its own story. Reuse verified production infrastructure and generic assets where useful. Use prior films only for technical implementation checks and only when needed.

## Prepare once

Read the project `AGENTS.md` and `SOURCES.md`. Resolve the current script, source material, requested deliverables and any required research. Preserve approved narration verbatim. Check local tool and asset availability before choosing a dependency. Start new films in workflows/viz3d/README.md. Direct each treatment within the same Viz3D production timeline. Read the relevant style skills and their references. Load the material the production needs and reuse it across scenes.

## Direct in one pass

Target three minutes of creative planning once the brief and resources are ready. Identify the opening image, the story beats and the final payoff. For each beat, state what the viewer should learn or feel and what visible action delivers it. Give the strongest beats the most production effort.

Consider the full range of styles before choosing a treatment for each beat. Include mixed styles wherever the change helps the viewer follow the action, understand an idea, or feel a story turn. Give each change a reason in the edit and carry a subject, shape, movement, color, or sound across the cut when it helps the viewer make the connection. Use this table as a starting point.

| When the viewer needs to… | Use… |
| --- | --- |
| Read scale, navigate a space or see objects move around each other | Low-poly 3D with a grounded scale reference, motivated camera and occlusion. Confirm the native renderer can capture the scene. |
| Feel distance in a scene with little viewpoint change | Layered 2D with foreground occlusion, midground action, background separation and deliberate parallax or light. |
| Understand a rule, route or system | A blueprint, schematic or 2D motion graphic. Animate the relevant change and register it to a recognizable object or landmark when coming from a spatial shot. |
| Follow a rapid exchange, a compressed sequence, or a change of state | Pixel art, drawn animation, or another stylized insert with clear actions and a readable rhythm. |
| Read testimony or evidence | Ink, documents, annotations, or close details that reveal one specific piece of information at a time. |
| Connect a reconstruction to the real place, people, or event | Archival photos or footage when sourced and relevant. Match a recognizable detail or action into the archival shot. |
| Experience an impossible event or unreliable perception | Controlled abstraction. Break an established spatial or visual rule and keep an anchor so the viewer can tell what changed. |

For SCP, establish the ordinary rule before breaking it. Plan where the tangible setting, technical explanation and abstract anomaly each belong if the brief calls for them. Use such changes to escalate the story. For a single-style brief, honor that choice and vary framing, motion, and composition to serve the beats.

## Hand off one plan

Save or update the production's `production-plan.json` under its own directory. Use the chosen style skill's schema when it provides one. Map the following decisions into that same plan. Keep one plan and timeline. For a planning-only request, deliver the plan and stop there.

- Record output dimensions, duration, frame rate, stage and caption layout, script reference, palette, typography, sound and narration approach, selected native tool and relevant style skills.
- For each shot, record frame range, story purpose, treatment, focal subject and depth layers, assets and source or build method, on-screen action, camera, and text and sound cues. State what the treatment contributes to that beat and direct the camera and action accordingly.
- For each transition, give the outgoing and incoming cue, frame count, and the specific object, contour, camera direction or sound that carries across. For a visual match, specify both screen positions. Explicitly place hard cuts where a change in time, point of view or emphasis calls for one.
- Name the preview and final render routes and the planned fallback for any uncertain dependency. When mixing tools, verify how their outputs will join on the same timeline. For a spatial shot, a layered fallback must retain the key landmark, sense of scale and reveal. Verify essential prerequisites before marking the plan ready.
- Set review frames for the opening, strongest spatial beat, mixed-style joins and payoff. Mark the plan frozen before building.

## Carry it through production

Use the frozen plan and the selected native production workflow. Finish the requested video and related deliverables under the project rules. Apply planned fallbacks first. Reopen only the affected shot or dependency when an asset or tool fails, a brief changes, or a preview shows a concrete story or quality failure. Record the change in the same plan and preserve its story purpose and neighboring timing where possible.

Review representative frames and play through the joins. Check that the viewer can read scale and separation in spatial shots, each treatment change advances the story or clarifies how the viewer should read the next beat, the reveal is clear, captions are legible when requested, and sound follows the action. Fix visible problems and verify playback of the final MP4 before delivery.
