#!/bin/bash

# Navigate to the API directory
cd "$(dirname "$0")"

# Install dependencies if not already installed
echo "Installing API dependencies..."
pip install -r requirements.txt

# Start the FastAPI server
echo "Starting Rubik's Cube Solver API..."
echo "API will be available at: http://localhost:8000"
echo "API documentation will be available at: http://localhost:8000/docs"
echo ""

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
