@echo off
rem Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
rem SPDX-License-Identifier: CC-BY-NC-ND-4.0
rem
rem Clementine starter - Windows launcher.
rem Creates a private virtualenv on first run, installs the two small
rem dependencies, runs the doctor, then starts the companion.

setlocal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo Python 3 not found. Install it from python.org - tick "Add to PATH" - then run me again.
    exit /b 1
)

if not exist .venv (
    echo First run: creating a private environment ^(.venv^)...
    python -m venv .venv
    .venv\Scripts\pip install --quiet --upgrade pip
    .venv\Scripts\pip install --quiet -r requirements.txt
)

.venv\Scripts\python doctor.py
if errorlevel 1 exit /b 1
echo.
.venv\Scripts\python clementine.py %*
