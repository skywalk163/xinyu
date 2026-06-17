@echo off
echo ============================================================
echo XinYu Playground Launcher
echo ============================================================
echo.
echo Checking dependencies...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo [Warning] Flask not installed, installing dependencies...
    pip install flask flask-cors
    echo.
)
echo Starting Playground server...
echo.
echo Visit: http://localhost:5000
echo Press Ctrl+C to stop the server
echo ============================================================
echo.
python server.py
