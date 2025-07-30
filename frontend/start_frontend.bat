@echo off
echo Starting Stock Advisor Frontend...
echo.

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js not found. Please install Node.js 18 or higher.
    pause
    exit /b 1
)

REM Change to the script directory
cd /d "%~dp0"

REM Install dependencies if node_modules doesn't exist
if not exist node_modules (
    echo Installing dependencies...
    npm install
    echo.
)

REM Start the development server
echo Starting Next.js development server...
echo Frontend will be available at: http://localhost:3000
echo.

npm run dev

pause
