@echo off
title MSI AI Voice Assistant - UI Version
color 0A

echo ========================================
echo     MSI AI Voice Assistant
echo     UI Version with Advanced Features
echo ========================================
echo.
echo Starting MSI UI...
echo.

python msi_ui.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start MSI UI
    echo Make sure all packages are installed:
    echo pip install customtkinter pyttsx3 speechrecognition
    echo pip install pyaudio psutil pycaw comtypes
    echo pip install screen-brightness-control pyautogui
    echo.
    pause
)
