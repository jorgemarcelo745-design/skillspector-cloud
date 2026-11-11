#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON:-$ROOT/.venv/bin/python}"
if [[ ! -x "$PYTHON" ]]; then
  echo 'BLOQUEADO: Python do ambiente isolado ausente.' >&2
  exit 2
fi
exec "$PYTHON" "$ROOT/scripts/verificar_skill.py" "$@"
