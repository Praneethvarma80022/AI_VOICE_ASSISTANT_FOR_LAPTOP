@echo off
title MSI AI Voice Assistant - Master Launcher
color 0B

:: ================== MSI MASTER LAUNCHER ==================
:: This is the ONLY batch file you need to run MSI
:: =======================================================

:MENU
cls
echo.
echo  ███╗   ███╗███████╗██╗     
echo  ████╗ ████║██╔════╝██║     
echo  ██╔████╔██║███████╗██║     
echo  ██║╚██╔╝██║╚════██║██║     
echo  ██║ ╚═╝ ██║███████║██║     
echo  ╚═╝     ╚═╝╚══════╝╚═╝     
echo.
echo  AI VOICE ASSISTANT - MASTER LAUNCHER
echo  =====================================
echo.
echo  [1] Install Dependencies
echo  [2] Run MSI (Integrated App)
echo  [3] Run MSI (Console Mode)
echo  [4] Check Python Version
echo  [5] Check Dependencies
echo  [6] Exit
echo.
set /p choice="Select option (1-6): "

if "%choice%"=="1" goto INSTALL
if "%choice%"=="2" goto RUN_INTEGRATED
if "%choice%"=="3" goto RUN_CONSOLE
if "%choice%"=="4" goto CHECK_PYTHON
if "%choice%"=="5" goto CHECK_DEPS
if "%choice%"=="6" goto EXIT
goto MENU

:: ================ INSTALL DEPENDENCIES ================
:INSTALL
cls
echo.
echo ========================================
echo  INSTALLING MSI DEPENDENCIES
echo ========================================
echo.
echo Checking Python installation...
python --version
if errorlevel 1 (
    echo.
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    goto MENU
)

echo.
echo Installing required packages...
echo.

:: Core packages
python -m pip install --upgrade pip
python -m pip install pyttsx3
python -m pip install SpeechRecognition
python -m pip install pyaudio
python -m pip install psutil
python -m pip install pyautogui
python -m pip install customtkinter
python -m pip install screen-brightness-control
python -m pip install pycaw
python -m pip install comtypes
python -m pip install Pillow
python -m pip install requests

echo.
echo ========================================
echo  INSTALLATION COMPLETE!
echo ========================================
echo.
echo All dependencies have been installed.
echo You can now run MSI using option [2] or [3].
echo.
pause
goto MENU

:: ================ RUN MSI INTEGRATED ================
:RUN_INTEGRATED
cls
echo.
echo ========================================
echo  LAUNCHING MSI INTEGRATED APP
echo ========================================
echo.
echo Starting MSI with GUI interface...
echo.

if not exist "msi_integrated.py" (
    echo [ERROR] msi_integrated.py not found!
    echo Please make sure you're in the correct directory.
    pause
    goto MENU
)

python msi_integrated.py
if errorlevel 1 (
    echo.
    echo [ERROR] MSI crashed or failed to start!
    echo.
    echo Common issues:
    echo  - Missing dependencies (use option 1 to install)
    echo  - Microphone not connected
    echo  - Python version too old (requires 3.8+)
    echo.
    pause
)
goto MENU

:: ================ RUN MSI CONSOLE ================
:RUN_CONSOLE
cls
echo.
echo ========================================
echo  LAUNCHING MSI CONSOLE MODE
echo ========================================
echo.
echo Starting MSI without GUI...
echo.

if not exist "main.py" (
    echo [ERROR] main.py not found!
    echo Please make sure you're in the correct directory.
    pause
    goto MENU
)

python main.py
if errorlevel 1 (
    echo.
    echo [ERROR] MSI crashed or failed to start!
    echo.
    pause
)
goto MENU

:: ================ CHECK PYTHON VERSION ================
:CHECK_PYTHON
cls
echo.
echo ========================================
echo  PYTHON VERSION CHECK
echo ========================================
echo.
python --version
echo.
python -c "import sys; print(f'Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"
echo.
python -c "import sys; print('64-bit' if sys.maxsize > 2**32 else '32-bit')"
echo.
echo Required: Python 3.8 or higher
echo Recommended: Python 3.10+
echo.
pause
goto MENU

:: ================ CHECK DEPENDENCIES ================
:CHECK_DEPS
cls
echo.
echo ========================================
echo  DEPENDENCY STATUS CHECK
echo ========================================
echo.
python -c "import importlib; packages = ['pyttsx3', 'speech_recognition', 'psutil', 'pyautogui', 'customtkinter', 'screen_brightness_control', 'pycaw', 'comtypes', 'PIL']; print('\n'.join([f'{p}: ✓ INSTALLED' if importlib.util.find_spec(p.replace('_', '')) else f'{p}: ✗ MISSING' for p in packages]))"
echo.
echo If any packages show "MISSING", use option [1] to install them.
echo.
pause
goto MENU

:: ================ EXIT ================
:EXIT
cls
echo.
echo ========================================
echo  MSI AI VOICE ASSISTANT
echo ========================================
echo.
echo Thank you for using MSI!
echo.
timeout /t 2 >nul
exit
