#!/bin/sh
# Run a native Lemo command with workspace-safe caches and bounded CPU threads.
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(git -C "$HERE" rev-parse --show-toplevel)
LIB=${LEMO_OPUSCAR_HOME:-$ROOT/vendor/lemo-opuscar}
CACHE=$ROOT/tools/cache/lemo-opuscar

[ -f "$LIB/AGENTS.md" ] || {
  echo "error: Lemo is not prepared; run skills/lemo-opuscar-codex/scripts/setup.sh first" >&2
  exit 1
}
[ "$#" -gt 0 ] || {
  echo "usage: sh skills/lemo-opuscar-codex/scripts/run.sh <command> [args...]" >&2
  exit 2
}

mkdir -p "$CACHE/npm" "$CACHE/playwright" "$CACHE/uv" "$CACHE/xdg" "$CACHE/huggingface"
export npm_config_cache=$CACHE/npm
export PLAYWRIGHT_BROWSERS_PATH=$CACHE/playwright
export UV_CACHE_DIR=$CACHE/uv
export XDG_CACHE_HOME=$CACHE/xdg
export HF_HOME=$CACHE/huggingface
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-3}
export OPENBLAS_NUM_THREADS=${OPENBLAS_NUM_THREADS:-3}
export MKL_NUM_THREADS=${MKL_NUM_THREADS:-3}
export NUMEXPR_NUM_THREADS=${NUMEXPR_NUM_THREADS:-3}

cd "$LIB"
exec "$@"
