#!/bin/bash

echo "=========================================="
echo "Starting Flask Backend Server"
echo "=========================================="
echo ""

cd "$(dirname "$0")/server"

echo "Checking Python dependencies..."
pip install -q -r requirements.txt

echo ""
echo "Starting Flask server on port 5000..."
echo "API will be available at: http://localhost:5000/api"
echo ""

python3 app.py
