# Reconquista production workflow

Use MotionLab Director to plan the film. Stage spatial action with the local Three.js build in viz3d.js. Compose pixel characters, document inserts, diagrams, ink or photographic material on the same seekable stage when the story calls for them. Build original subjects, sets and visual treatments for each brief; episode reference folders are intentionally outside this system backup.

Give the viewer a landmark or subject to follow across a cut. Block the action and camera in depth. Establish scale through foreground, subject and background. Check the opening, the largest motion, framing at both ends of camera moves, and the final image. Review a timed motion preview across a treatment change before rendering the master. Screen the complete cut with the intended narration and record actual observations, fixes and remaining limitations.

## Master export

Run from the production repository root. The scene exposes a canvas with id stage and OPENER.ready, OPENER.resize(width,height) and OPENER.seek(seconds). Use the actual duration of the approved edit and a finished audio mix starting at time zero. Honor explicit delivery frame rates with --fps. Use --start and --end for a cut preview.

```powershell
.venv/Scripts/python.exe workflows/viz3d/render.py productions/FILM/index.html --audio productions/FILM/mix.wav --duration SECONDS --output productions/FILM/master.mp4
```

The default master is 1080 x 1920 at 60 fps, Chromium Direct3D and WebCodecs H.264, with FFmpeg AAC muxing. Follow the current brief for voice and captions. The user supplies narration and captions. Do not generate either.
