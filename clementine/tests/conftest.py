# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Put the app on `sys.path` for the tests.

In this repository the companion and its crystalcore package sit together
under clementine/, so one root is enough — unlike the monorepo these tests
came from, where the mind lived in a separate core/ tree.
"""

import pathlib
import sys

APP_DIR = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_DIR))
