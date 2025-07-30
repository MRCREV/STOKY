@echo off
echo =====================================
echo    Stock Advisor - Complete Setup
echo =====================================
echo.

echo This script will start both the backend API and frontend dashboard.
echo.

REM Check if Python is available
C:/Python313/python.exe --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js not found. Please install Node.js 18 or higher.
    pause
    exit /b 1
)

echo Both Python and Node.js are available!
echo.

REM Start the backend API in a new window
echo Starting Backend API Server...
start "Stock Advisor API" cmd /k "cd /d "%~dp0" && C:/Python313/python.exe app.py"

REM Wait a moment for the API to start
echo Waiting for API to initialize...
timeout /t 5 >nul

REM Start the frontend in a new window
echo Starting Frontend Dashboard...
start "Stock Advisor Frontend" cmd /k "cd /d "%~dp0\frontend" && npm run dev"

echo.
echo =====================================
echo Stock Advisor is starting up!
echo.
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend: http://localhost:3000
echo.
echo Both services are running in separate windows.
echo Close this window when you're done.
echo =====================================

pause
