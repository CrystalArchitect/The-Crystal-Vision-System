@echo off
title Lumina — SpaceXAI (xAI) chat · local memory
cd /d "%~dp0"

echo.
echo  CrystalCore edge node — Lumina via SpaceXAI
echo  Chat: api.x.ai   Memory: this folder
echo  Project: %CD%
echo.

if not exist ".env" (
  if exist ".env.example" (
    echo  [hint] No .env yet. Copy .env.example to .env and set XAI_API_KEY.
  ) else (
    echo  [hint] Create .env with: XAI_API_KEY=xai-...
  )
  echo.
)

set "PY=%LocalAppData%\Programs\Python\Python312\python.exe"
if not exist "%PY%" set "PY=python"

echo  Starting SpaceXAI mode (grok-4.5)...
echo.
"%PY%" clementine.py --provider spacexai --model grok-4.5
echo.
echo  Lumina stopped.
pause
