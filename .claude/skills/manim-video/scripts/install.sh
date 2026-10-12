#!/usr/bin/env bash
# Install manim-video dependencies (Linux/macOS). Uses the current Python env; activate a venv first if you want isolation.
set -euo pipefail

if command -v apt-get >/dev/null 2>&1; then
  SUDO=""; [ "$(id -u)" -ne 0 ] && SUDO="sudo"
  $SUDO apt-get update
  $SUDO apt-get install -y ffmpeg libpango1.0-dev pkg-config libcairo2-dev python3-pip
elif command -v brew >/dev/null 2>&1; then
  brew install ffmpeg pango pkg-config cairo
else
  echo "Install ffmpeg, pango, cairo manually, then re-run." >&2
fi

python3 -m pip install manim manim-voiceover gTTS pyyaml pypdf trafilatura

python3 "$(dirname "$0")/check-env.py"
