#!/bin/bash

echo "🚀 Starting React frontend..."

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "❌ Node modules not found. Please run ./setup-dev.sh first."
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please run ./setup-dev.sh first."
    exit 1
fi

# Start the development server
echo "🌐 Starting React development server on http://localhost:3000"
npm start
