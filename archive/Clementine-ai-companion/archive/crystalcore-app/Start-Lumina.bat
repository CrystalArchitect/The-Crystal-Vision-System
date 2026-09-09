@echo off
title Lumina — LOCAL (wait for reply)
cd /d "C:\Users\Admin\The-Crystal-Vision"

echo.
echo  ============================================
echo   LUMINA — local Ollama mode
echo  ============================================
echo   After "You:" type a short message and Enter.
echo   Then WAIT — she shows "thinking" then replies.
echo   First answer: often 10-60 seconds. Do not close.
echo   Quit: type /exit
echo  ============================================
echo.

where ollama >nul 2>&1
if errorlevel 1 (
  echo  [FAIL] Ollama not found. Install https://ollama.com
  pause
  exit /b 1
)

set "PY=%LocalAppData%\Programs\Python\Python312\python.exe"
if not exist "%PY%" set "PY=python"

echo  Warming model llama3.1:8b (one-time load)...
ollama run llama3.1:8b "say hi" >nul 2>&1

echo  Starting Lumina...
echo.
"%PY%" clementine.py --provider ollama --model llama3.1:8b
echo.
echo  Lumina stopped.
pause
