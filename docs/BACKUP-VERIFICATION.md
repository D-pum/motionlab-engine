# System snapshot verification

Captured 2026-11-19 from the active MotionLab Experiments workspace and the installed shared upstream checkouts. See UPSTREAMS.json for revisions. No old repository history was imported.

Verified locally before upload:

- Main renderer parses and its command-line interface loads with the existing Playwright 1.51.0 environment.
- A generic seekable Three.js stage exported successfully through the copied master renderer: 1 second, 12 frames, 1080×1920, H.264 video and 48 kHz AAC audio.
- FFmpeg decoded the complete smoke export without errors. An extracted frame was visually inspected and showed the expected rendered cube.
- The technical smoke MP4, WAV and frame are in ignored tools/ and are excluded from the repository.
- Backup payload was checked for episode/deliverable directories, video files and model weights. Common credential/private-key patterns were checked without exposing values; none were found.

Backup-specific adjustments: shared Director notes moved out of an episode folder into docs/; stale episode and narration references were replaced with current root policy; the pixel-art skill now explicitly stays on the shared Viz3D timeline; the Lemo adapters resolve to included vendor source instead of requiring an external checkout. Added a neutral stage contract example, restore instructions, dependency pin and file hashes. The master renderer and Viz3D bundle were copied unchanged.

This validates the main native renderer on the existing Windows machine. It does not certify every optional vendored tool or a fresh machine dependency installation. Optional demos and episode-specific scripts are intentionally omitted. Read vendor licenses and asset provenance before reusing their material.
