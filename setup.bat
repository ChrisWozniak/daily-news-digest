@echo off
:: Daily News Digest — one-click setup
:: Run this once as Administrator to install packages and register the 9am task.

setlocal
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "PYTHON_SCRIPT=%SCRIPT_DIR%\digest.py"
set "TASK_NAME=DailyNewsDigest"

echo.
echo ═══════════════════════════════════════════
echo  Daily News Digest — Setup
echo ═══════════════════════════════════════════
echo.

:: ── 1. Install Python packages ────────────────────────────────────────────────
echo [1/3] Installing Python packages...
pip install -r "%SCRIPT_DIR%\requirements.txt"
if errorlevel 1 (
    echo ERROR: pip install failed. Make sure Python is installed and on PATH.
    pause
    exit /b 1
)

:: ── 2. Remove old task if it exists ──────────────────────────────────────────
echo.
echo [2/3] Registering Windows Task Scheduler job (9:00 AM daily)...
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1

:: ── 3. Create the task ────────────────────────────────────────────────────────
:: Find python.exe location
for /f "delims=" %%i in ('where python') do set "PYTHON_EXE=%%i" & goto :found_python
:found_python

schtasks /create ^
  /tn "%TASK_NAME%" ^
  /tr "\"%PYTHON_EXE%\" \"%PYTHON_SCRIPT%\"" ^
  /sc DAILY ^
  /st 09:00 ^
  /ru "%USERNAME%" ^
  /rl HIGHEST ^
  /f

if errorlevel 1 (
    echo ERROR: Could not create scheduled task. Try running as Administrator.
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════
echo  Setup complete!
echo.
echo  NEXT STEPS:
echo  1. Edit config.py — add your Anthropic API key + Gmail app password
echo  2. Test it now:  python "%PYTHON_SCRIPT%"
echo  3. It will run automatically at 9:00 AM every day.
echo ═══════════════════════════════════════════
echo.
pause
