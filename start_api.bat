@echo off
echo Starting Stock Advisor API...
echo.

REM Check if Python is available
C:/Python313/python.exe --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Change to the script directory
cd /d "%~dp0"

REM Install dependencies if requirements.txt exists
if exist requirements.txt (
    echo Installing dependencies...
    C:/Python313/python.exe -m pip install -r requirements.txt
    echo.
)

REM Start the API server
echo Starting FastAPI server...
echo API will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.

C:/Python313/python.exe app.py

pause
