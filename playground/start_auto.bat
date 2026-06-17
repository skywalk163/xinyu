@echo off
echo ============================================================
echo XinYu Playground - Auto Launcher
echo ============================================================
echo.

REM 检查虚拟环境
if exist "..\.venv\Scripts\activate.bat" (
    echo [Info] Found virtual environment, activating...
    call ..\.venv\Scripts\activate.bat
) else (
    echo [Info] No virtual environment found, using global Python
)

REM 检查Flask
echo Checking Flask installation...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo [Warning] Flask not installed, installing...
    pip install flask flask-cors
    echo.
)

REM 启动服务器
echo Starting Playground server...
echo.
echo Visit: http://localhost:5000
echo Press Ctrl+C to stop
echo ============================================================
echo.
python server.py
