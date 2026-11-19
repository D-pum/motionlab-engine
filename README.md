# MotionLab engine

Unified source backup of the current MotionLab production system, captured 19 November 2026. The production engine is Reconquista Viz3D: a local Three.js runtime, a seekable Chromium stage, native WebCodecs H.264 capture and FFmpeg audio muxing.

Start with [AGENTS.md](AGENTS.md), [Director notes](docs/DIRECTOR-NOTES.md), [sources](SOURCES.md), and [the renderer workflow](workflows/viz3d/README.md). The four approved formats live in `formats/`. The user supplies narration and captions; produce neither automatically.

## Restore on Windows

Install Python 3.11 or newer, Git, and FFmpeg (including ffprobe) on PATH. The captured machine used Python 3.14.6, Playwright 1.51.0 and FFmpeg 8.1.1. The master renderer currently targets Windows/Direct3D. A compatible GPU and Chromium H.264 WebCodecs support are required for that route.

```powershell
git clone https://github.com/D-pum/motionlab-engine.git
cd motionlab-engine
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m playwright install chromium
.venv/Scripts/python.exe workflows/viz3d/render.py --help
```

For a new film, create an ignored `productions/<slug>/` folder. Copy `templates/stage.html` to its `index.html` as a technical starting point, change its script path to `../../workflows/viz3d/viz3d.js`, and build an original scene. The template is a renderer contract demonstration, not a creative production template. Supply the finished SFX/audio mix at time zero, then run:

```powershell
.venv/Scripts/python.exe workflows/viz3d/render.py productions/FILM/index.html --audio productions/FILM/mix.wav --duration SECONDS --output productions/FILM/master.mp4
```

Use `--fps`, `--start` and `--end` when needed. Default export is 1080×1920 at 60 fps. Runtime, edit, assets, sound and direction come from each new brief.

## Included system

- `workflows/viz3d/`: actual shared renderer, bundled Three.js runtime and license.
- `.agents/skills/`: Director, pixel-art and scriptwriting instructions.
- `formats/`: visual what-ifs, SCP/conspiracies, mechanical and journalist explainers.
- `docs/`: shared story direction, production lessons and backup verification.
- `vendor/`: local reusable Lemo-Opuscar source and 67 style directories, Creator Generalist plugins, Bang Motion, Huashu Art Motion and Claude Drawing, with their original licenses.
- `UPSTREAMS.json`: exact captured upstream revisions and inclusion scope.
- `BACKUP-MANIFEST.json`: SHA-256 hashes of the backed-up files.

Vendored libraries are references and supporting tools within the chosen Viz3D timeline. Their upstream defaults do not override root AGENTS.md or authorize changing the engine, generating narration or captions, or using paid services. Read the relevant skill before applying it. Each upstream library retains its own optional dependency requirements. The Python environment above restores the main renderer; it does not install every optional upstream tool.

Episodes, production packs, rendered media, model weights, caches, credentials, installed environments and old Git history are excluded. Existing projects and repositories on this PC are preserved. Production scripts that existed only inside episode folders are outside this system snapshot.
