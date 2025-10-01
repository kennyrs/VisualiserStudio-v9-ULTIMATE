@echo off
REM VisualiserStudio v9.0 ULTIMATE - Windows Installation Script

echo ================================================
echo    VisualiserStudio v9.0 ULTIMATE
echo    Complete Windows Installation
echo ================================================
echo.

REM Check Python
echo [1/6] Checking Python...
python --version >nul 2>&1
if %errorlevel% == 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do echo     Found: Python %%i
) else (
    echo     ERROR: Python not found!
    echo     Please install Python 3.8+ from python.org
    echo     Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Check pip
echo.
echo [2/6] Checking pip...
python -m pip --version >nul 2>&1
if %errorlevel% == 0 (
    echo     pip is installed
) else (
    echo     ERROR: pip not found!
    pause
    exit /b 1
)

REM Install dependencies
echo.
echo [3/6] Installing Python packages...
echo     This may take a few minutes...
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt

if %errorlevel% == 0 (
    echo     All packages installed successfully!
) else (
    echo     WARNING: Some packages may have failed to install
    echo     Try running: python -m pip install -r requirements.txt
)

REM Check FFmpeg
echo.
echo [4/6] Checking FFmpeg...
ffmpeg -version >nul 2>&1
if %errorlevel% == 0 (
    echo     FFmpeg is installed
) else (
    echo     WARNING: FFmpeg not found!
    echo     FFmpeg is required for video export.
    echo.
    echo     Installation options:
    echo     1. Using winget: winget install ffmpeg
    echo     2. Using chocolatey: choco install ffmpeg
    echo     3. Manual download: https://ffmpeg.org/download.html
    echo.
    echo     After installing FFmpeg, restart this installation.
)

REM Create directory structure
echo.
echo [5/6] Creating directory structure...
if not exist models mkdir models
if not exist views mkdir views
if not exist views\panels mkdir views\panels
if not exist elements mkdir elements
if not exist core mkdir core
if not exist utils mkdir utils
if not exist projects mkdir projects
if not exist exports mkdir exports
if not exist templates mkdir templates

REM Create __init__.py files
type nul > models\__init__.py
type nul > views\__init__.py
type nul > views\panels\__init__.py
type nul > elements\__init__.py
type nul > core\__init__.py
type nul > utils\__init__.py

echo     Directory structure created

REM Create run.bat launcher
echo.
echo [6/6] Creating launcher...
(
echo @echo off
echo cd /d "%%~dp0"
echo echo Starting VisualiserStudio v9.0 ULTIMATE...
echo python main.py
echo if %%errorlevel%% neq 0 (
echo     echo.
echo     echo Application crashed or closed with error
echo     pause
echo ^)
) > run.bat

echo     Launcher created: run.bat

REM Create desktop shortcut (optional)
echo.
set /p create_shortcut="Create desktop shortcut? (Y/N): "
if /i "%create_shortcut%"=="Y" (
    echo Creating desktop shortcut...
    powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%USERPROFILE%\Desktop\VisualiserStudio.lnk'); $s.TargetPath = '%CD%\run.bat'; $s.WorkingDirectory = '%CD%'; $s.Save()"
    echo     Desktop shortcut created
)

echo.
echo ================================================
echo    Installation Complete!
echo ================================================
echo.
echo Quick Start:
echo   1. Double-click run.bat
echo   2. Or run: python main.py
echo.
echo Directory structure:
echo   projects\  - Save your projects here
echo   exports\   - Exported videos go here
echo   templates\ - Save gradient templates here
echo.
echo Keyboard Shortcuts:
echo   Ctrl+N     - New Project
echo   Ctrl+O     - Open Project
echo   Ctrl+S     - Save Project
echo   Ctrl+E     - Export Video
echo   Space      - Play/Pause
echo   Ctrl+Z/Y   - Undo/Redo
echo.
echo For full documentation, see:
echo   - README.md
echo   - QUICKSTART.md
echo   - TUTORIAL.md
echo.
echo ================================================
echo    Press any key to start VisualiserStudio...
echo ================================================
pause >nul

REM Launch application
start run.bat
