# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Put this app on `sys.path`, and the companion too if it can be found.

The bot itself needs neither: it reaches the companion over HTTP through
`clementine_api`, which imports `requests` and nothing of the companion's
own. That independence is why this app could move out of the companion's
directory without a line of it changing.

Two of its test files are a different matter, deliberately. They close the
loop between the bot and the API it calls — one runs the handlers against a
real companion app, the other holds every client method against
`api_surface.ROUTES`, so a method calling a route nobody serves fails. That
is worth more than the inconvenience it causes here, and it is the reason
neither was simply deleted when the companion moved out of this repository.

So: point CLEMENTINE_SRC at the `clementine/` directory of a checkout of
CrystalArchitect/Clementine-ai-companion and those tests run. Without it
they skip, with a message saying so. They do not silently pass — a
loop-closing test that quietly stops closing the loop is worse than one
that admits it did not run.

    git clone https://github.com/CrystalArchitect/Clementine-ai-companion.git
    CLEMENTINE_SRC=../Clementine-ai-companion/clementine python -m pytest tests/
"""

import os
import pathlib
import sys

APP_DIR = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_DIR))

#: Set when the companion's source is on the path, so the two loop-closing
#: test files can ask rather than guess.
COMPANION_SRC = os.environ.get("CLEMENTINE_SRC", "").strip()
if COMPANION_SRC:
    src = pathlib.Path(COMPANION_SRC).expanduser().resolve()
    if src.is_dir():
        sys.path.insert(0, str(src))
