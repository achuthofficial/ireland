#!/bin/bash

echo "=========================================="
echo "Starting React Frontend (Vite)"
echo "=========================================="
echo ""

cd "$(dirname "$0")/client"

if [ ! -d "node_modules" ]; then
  echo "Installing npm dependencies..."
  npm install
fi

echo ""
echo "Starting Vite dev server..."
echo "Frontend will be available at: http://localhost:5173"
echo ""

npm run dev
