@echo off
cd /d "%~dp0"

echo Installing API dependencies...
pip install -r requirements.txt

echo.
echo Starting Rubik's Cube Solver API...
echo API will be available at: http://localhost:8001
echo API documentation will be available at: http://localhost:8001/docs
echo.

uvicorn main:app --host 127.0.0.1 --port 8001 --reload
