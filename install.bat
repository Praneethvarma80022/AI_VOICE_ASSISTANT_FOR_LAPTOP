@echo off
echo ========================================
echo MSI AI Voice Assistant - Installation
echo ========================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo.
echo Installing required packages...
echo This may take a few minutes...
echo.

pip install --upgrade pip
echo.
echo [1/11] Installing customtkinter...
pip install customtkinter
echo [2/11] Installing pyttsx3...
pip install pyttsx3
echo [3/11] Installing SpeechRecognition...
pip install SpeechRecognition
echo [4/11] Installing PyAudio...
pip install PyAudio
echo [5/11] Installing psutil...
pip install psutil
echo [6/11] Installing pycaw...
pip install pycaw
echo [7/11] Installing comtypes...
pip install comtypes
echo [8/11] Installing screen-brightness-control...
pip install screen-brightness-control
echo [9/11] Installing pyautogui...
pip install pyautogui
echo [10/11] Installing winshell...
pip install winshell
echo [11/11] Installing requests...
pip install requests

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo NEW FEATURES ADDED:
echo ✅ Beautiful UI with customtkinter
echo ✅ Open files by name
echo ✅ Telegram and WhatsApp integration
echo ✅ Real-time system monitoring
echo.
echo You can now run MSI:
echo - UI Version: run_msi_ui.bat
echo - Console: run_msi.bat
echo.
echo Make sure to run as Administrator!
echo.
pause
