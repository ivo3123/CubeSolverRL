@echo off
cd /d "%~dp0"

echo Installing API dependencies...
pip install -r requirements.txt

echo.
echo Starting Rubik's Cube Solver API...
echo API will be available at: http://localhost:8000
echo API documentation will be available at: http://localhost:8000/docs
echo.

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
