# Shared libraries and provenance

The production engine is `workflows/viz3d/`: the captured Three.js bundle and master renderer. Read root AGENTS.md first. Optional libraries below contribute assets, styles, direction or tools within that engine; they do not select a different engine.

All reusable upstream source available in the captured checkouts is included under `vendor/`, excluding demos, episodes, generated video and model weights. Exact revisions and source URLs are in UPSTREAMS.json. Preserve the license files accompanying reused material. Third-party source retains its original copyright and license; no new blanket license is applied to it.

| Library | Local entry point |
|---|---|
| Lemo-Opuscar | vendor/lemo-opuscar/AGENTS.md and skills/lemo-opuscar-codex/SKILL.md |
| Creator Generalist | vendor/creator-generalist/plugins/3d-generalist/skills/3d-generalist/SKILL.md |
| Bang Motion | vendor/bang-motion/SKILL.md |
| Huashu Art Motion | vendor/huashu-art-motion/SKILL.md |
| Claude Drawing | vendor/claude-drawing/SKILL.md |

Read the selected library's instructions and relevant references before use. Libraries have their own optional dependency manifests. Reuse existing installations and preserve local changes. Do not run optional narration or caption tools. Do not let upstream setup update the pinned vendored source automatically.

For the Lemo adapter, the default library is now vendor/lemo-opuscar. Its source snapshot does not have an independent .git directory. Use the adapter for dependency installation or commands, and use UPSTREAMS.json for revision provenance.
