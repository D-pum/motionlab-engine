# How a Mechanical Watch Keeps Time With ZERO Batteries

42-second portrait 8-bit-styled Viz3D production, with deterministic Three.js geometry, a one-third-resolution 3D framebuffer and nearest-neighbour upscale. The authored narration and cue times are preserved in production-plan.json. preview_sfx.mp4 contains SFX only.

From the repository root:

```powershell
.venv/Scripts/python.exe productions/07_mechanical_watch/gen_sfx.py
.venv/Scripts/python.exe tools/audio_mix.py productions/07_mechanical_watch --duration 42
.venv/Scripts/python.exe tools/verify.py productions/07_mechanical_watch
.venv/Scripts/python.exe tools/verify.py productions/07_mechanical_watch --landscape
.venv/Scripts/python.exe tools/render.py productions/07_mechanical_watch --preview --start 9.5 --end 13.5
.venv/Scripts/python.exe tools/render.py productions/07_mechanical_watch --audio productions/07_mechanical_watch/audio_mix.wav
```

tools/render.py delegates to workflows/viz3d/render.py. Portrait defaults are preserved. Add --landscape to render a full landscape master. stage.safeBox() and verification are local to this production; no second production engine is installed.

Contact sheets, sample frames, WAV mixes and rendered MP4s are generated outputs. Recreate the reversed sample using:
`ffmpeg -i assets/sfx/fan_interval.wav -af areverse assets/sfx/watch_rewind.wav`

The escapement is an explanatory schematic following the requested one-tooth-per-impulse visual. Pallet contacts and gear ratios are representative. Physical Swiss lever geometry, balance inertia and manufacturing tolerances are simplified. The mainspring energy-release burst is a dramatization. At 8 ticks/second the nominal daily count is 691,200; the supplied script remains verbatim. Eight beats means four complete balance oscillations per second. Reference for frequency and real-world rate variation: https://www.grand-seiko.com/se-en/-/media/Files/Common/GrandSeiko/instructions/English/9S25_en.pdf

Review passed deterministic seeking, impulse synchronization, portrait/landscape sheets, transition sequencing, complete video decoding and sampled visual inspection across the cut. This is an SFX preview pending the user's recording.
