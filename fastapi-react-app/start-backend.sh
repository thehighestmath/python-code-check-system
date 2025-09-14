#!/bin/bash

echo "🚀 Starting FastAPI backend..."

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run ./setup-dev.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please run ./setup-dev.sh first."
    exit 1
fi

# Run migrations
echo "📊 Running database migrations..."
alembic upgrade head

# Start the server
echo "🌐 Starting FastAPI server on http://localhost:8000"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
