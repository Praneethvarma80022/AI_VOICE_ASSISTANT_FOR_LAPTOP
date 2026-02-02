@echo off
title MSI AI Voice Assistant
color 0A

echo ========================================
echo     MSI AI Voice Assistant
echo     Complete Laptop Control System
echo ========================================
echo.
echo Starting MSI...
echo.

python main.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start MSI
    echo Make sure all packages are installed
    echo Run install.bat first if needed
    echo.
    pause
)
