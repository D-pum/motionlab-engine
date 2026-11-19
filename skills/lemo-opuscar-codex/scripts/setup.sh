#!/bin/sh
# Prepare the pinned Lemo-Opuscar library for this repository, then delegate
# dependency and demo operations to its native setup script.
set -eu

PIN=9eb7739a0fca4c6990fe966cb8b87b1930f7193a
UPSTREAM=${LEMO_OPUSCAR_REPO:-https://github.com/lemomo-ai/lemo-opuscar.git}
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(git -C "$HERE" rev-parse --show-toplevel)
LIB=${LEMO_OPUSCAR_HOME:-$ROOT/vendor/lemo-opuscar}
CACHE=$ROOT/tools/cache/lemo-opuscar

# Managed Codex environments may expose a read-only home directory. Keep every
# package-manager and browser cache in the repository's ignored tools area.
mkdir -p "$CACHE/npm" "$CACHE/playwright" "$CACHE/uv" "$CACHE/xdg" "$CACHE/huggingface"
export npm_config_cache=$CACHE/npm
export PLAYWRIGHT_BROWSERS_PATH=$CACHE/playwright
export UV_CACHE_DIR=$CACHE/uv
export XDG_CACHE_HOME=$CACHE/xdg
export HF_HOME=$CACHE/huggingface

case "$LIB" in
  /*|[A-Za-z]:[/\\]*) ;;
  *) LIB=$ROOT/$LIB ;;
esac

is_library() {
  [ -f "$1/AGENTS.md" ] && [ -d "$1/core/render" ] && [ -f "$1/plugin/skills/lemo-opuscar/scripts/setup.sh" ]
}

is_library "$LIB" || { echo "error: shared vendored Lemo source missing: $LIB" >&2; exit 1; }

# Vendored snapshot: revision provenance is recorded in root UPSTREAMS.json.
# Reuse the model already validated in this repository. The int8 ONNX model is
# accepted by kokoro-onnx and avoids a second large download.
if [ "${1:-}" = deps ]; then
  for arg in "$@"; do
    if [ "$arg" = voice ] && [ -f "$ROOT/tools/kokoro-models/kokoro-v1.0.int8.onnx" ] && [ -f "$ROOT/tools/kokoro-models/voices-v1.0.bin" ]; then
      [ -e "$LIB/core/tts/kokoro-v1.0.onnx" ] || ln -s ../../../kokoro-models/kokoro-v1.0.int8.onnx "$LIB/core/tts/kokoro-v1.0.onnx"
      [ -e "$LIB/core/tts/voices-v1.0.bin" ] || ln -s ../../../kokoro-models/voices-v1.0.bin "$LIB/core/tts/voices-v1.0.bin"
    fi
  done
fi

if [ "${1:-}" = demo ]; then echo "Demo assets are outside this system snapshot; use the pinned upstream separately." >&2; exit 1; fi
LEMO_OPUSCAR_HOME=$LIB sh "$LIB/plugin/skills/lemo-opuscar/scripts/setup.sh" "$@"
echo "PIN=$PIN"
