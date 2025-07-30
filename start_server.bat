@echo off
cd "C:\Users\LL3922\Desktop\VS Code\private projects\STOKY"
echo Starting STOKY Backend Server...
echo Server will be accessible at: http://10.105.22.220:8001
echo.
python -m uvicorn app:app --host 0.0.0.0 --port 8001 --reload
pause
