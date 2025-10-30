@echo off
REM AUTOLEADAI Module 1 - Quick Start Script for Windows
REM This script activates the virtual environment and starts the web demo

echo ============================================================
echo   AUTOLEADAI Module 1 - Demo Launcher
echo   Call Handling and Speech Processing
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.py first:
    echo   python setup.py
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Start Flask application
echo Starting web server...
echo.
echo ============================================================
echo   Access the dashboard at: http://localhost:5000
echo   Press Ctrl+C to stop the server
echo ============================================================
echo.

python app.py

pause

