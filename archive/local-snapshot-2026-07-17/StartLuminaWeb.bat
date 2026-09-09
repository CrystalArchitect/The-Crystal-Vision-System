@echo off
title Lumina — CrystalCore web (localhost only)
cd /d "%~dp0"

set "PY=%LocalAppData%\Programs\Python\Python312\python.exe"
if not exist "%PY%" set "PY=python"

echo.
echo  Lumina web door — http://127.0.0.1:5000
echo  Local only. Ctrl+C to stop.
echo.
"%PY%" clementine_web.py
pause
