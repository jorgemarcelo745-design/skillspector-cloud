#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
REV=5f0f73dd204ad2454cca4ad63b06e60ad1ec3648
python3 -m venv "$ROOT/.venv"
"$ROOT/.venv/bin/python" -m pip install --no-compile "git+https://github.com/NVIDIA/SkillSpector.git@$REV"
mkdir -p "$ROOT/reports"
"$ROOT/.venv/bin/python" -m pip show skillspector > "$ROOT/reports/installed-version.txt"
"$ROOT/.venv/bin/skillspector" scan --help > "$ROOT/reports/installed-scan-help.txt"
for flag in --no-llm --format --fail-on-findings --fail-on-incomplete; do
  grep -F -- "$flag" "$ROOT/reports/installed-scan-help.txt" >/dev/null
done
