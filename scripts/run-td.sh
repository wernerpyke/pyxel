#!/usr/bin/env bash
# Run td/main.py using the project's .venv pyxel/python when available.
# Usage: ./scripts/run-td.sh [extra pyxel args]

set -euo pipefail

# Resolve repo root (script is located in scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET="$REPO_ROOT/td/main.py"

if [ ! -f "$TARGET" ]; then
  echo "Error: target script not found: $TARGET" >&2
  exit 2
fi

# Ensure the repository root is on PYTHONPATH so local packages (like pyke_pyxel) can be imported
export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"

# Auto-activate the project's virtualenv if an activate script exists.
# This updates PATH and Python environment so installed packages (like pyke_pyxel)
# are available without requiring the user to run `source .venv/bin/activate`.
ACTIVATE="$REPO_ROOT/.venv/bin/activate"
if [ -f "$ACTIVATE" ]; then
  # shellcheck disable=SC1090
  # (sourcing a dynamic path is intentional)
  # Use dot or source depending on shell; script runs with bash so `source` is fine.
  # shellcheck source=/dev/null
  source "$ACTIVATE"
fi

# Prefer the project's venv pyxel
VENV_PYXEL="$REPO_ROOT/.venv/bin/pyxel"
VENV_PYTHON="$REPO_ROOT/.venv/bin/python"

if [ -x "$VENV_PYXEL" ]; then
  echo $VENV_PYXEL
  exec "$VENV_PYXEL" run "$TARGET" "$@"
fi

# Fallback to system pyxel if available
if command -v pyxel >/dev/null 2>&1; then
  echo "Fallback to system pyxel"
  exec pyxel run "$TARGET" "$@"
fi

# Fallback to venv python -m pyxel
if [ -x "$VENV_PYTHON" ]; then
  echo "Fallback to venv python -m pyxel"
  exec "$VENV_PYTHON" -m pyxel run "$TARGET" "$@"
fi

# Fallback to python3/python -m pyxel
if command -v python3 >/dev/null 2>&1; then
  exec python3 -m pyxel run "$TARGET" "$@" || {
    echo "pyxel module not available in python3; trying to run the script directly" >&2
    exec python3 "$TARGET" "$@"
  }
fi

if command -v python >/dev/null 2>&1; then
  exec python -m pyxel run "$TARGET" "$@" || {
    echo "pyxel module not available in python; trying to run the script directly" >&2
    exec python "$TARGET" "$@"
  }
fi

echo "No suitable python/pyxel found. Install pyxel in the project's .venv or in your PATH." >&2
exit 3
