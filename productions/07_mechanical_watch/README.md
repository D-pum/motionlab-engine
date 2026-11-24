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

## Finished review cut

watch_review.mp4 adds crisp full-resolution component labels, beat-specific headings, lock/release callouts and 3D emphasis rings. The final 2.5 seconds contain only movement and SFX. Narration will be added later.

Reproduce it with:

```powershell
.venv/Scripts/python.exe workflows/viz3d/render.py productions/07_mechanical_watch/index.html --audio productions/07_mechanical_watch/audio_mix.wav --duration 42 --fps 60 --output productions/07_mechanical_watch/watch_review.mp4
```


## Narrated master

watch_final_narrated.mp4 is 55.5 seconds at 1080x1920, 60 fps. The user supplied assets/Watch.wav (53.32 seconds). Its natural pace is preserved. narrated_timing.js maps the approved sections to the recording's six spoken sections. Labels fade by 53 seconds and the movement continues through the ticking tail.

The source recording and generated WAV/MP4 files remain local. Reproduce the master after placing the user's recording in assets/Watch.wav:

```powershell
ffmpeg -i productions/07_mechanical_watch/assets/Watch.wav -af "highpass=f=65,loudnorm=I=-16:TP=-2:LRA=7" -ar 48000 -c:a pcm_s24le productions/07_mechanical_watch/narrated/voice_normalized.wav
.venv/Scripts/python.exe productions/07_mechanical_watch/prepare_narrated.py
.venv/Scripts/python.exe tools/audio_mix.py productions/07_mechanical_watch/narrated --duration 55.5 --voice productions/07_mechanical_watch/narrated/voice_normalized.wav
.venv/Scripts/python.exe workflows/viz3d/render.py productions/07_mechanical_watch/narrated.html --audio productions/07_mechanical_watch/narrated/audio_mix.wav --duration 55.5 --fps 60 --output productions/07_mechanical_watch/watch_final_narrated.mp4
```
