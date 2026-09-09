#!/bin/sh
# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0
#
# Clementine starter — macOS / Linux launcher.
# Creates a private virtualenv on first run, installs the two small
# dependencies, runs the doctor, then starts the companion.

set -e
cd "$(dirname "$0")"

PY=python3
command -v "$PY" >/dev/null 2>&1 || PY=python
command -v "$PY" >/dev/null 2>&1 || {
    echo "Python 3 not found. Install it from python.org, then run me again."
    exit 1
}

if [ ! -d .venv ]; then
    echo "First run: creating a private environment (.venv)..."
    "$PY" -m venv .venv
    ./.venv/bin/pip install --quiet --upgrade pip
    ./.venv/bin/pip install --quiet -r requirements.txt
fi

./.venv/bin/python doctor.py || exit 1
echo
exec ./.venv/bin/python clementine.py "$@"
