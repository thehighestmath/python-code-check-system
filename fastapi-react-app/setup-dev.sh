#!/bin/bash

echo "🚀 Setting up local development environment..."

# Check if Python 3.11+ is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python version: $PYTHON_VERSION"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

NODE_VERSION=$(node --version)
echo "✅ Node.js version: $NODE_VERSION"

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL is not installed. You can install it with:"
    echo "   brew install postgresql (on macOS)"
    echo "   or use Docker for database"
fi

# Setup backend
echo "📦 Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -e .

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
# Database
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=python_code_check
POSTGRES_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=dev-secret-key-$(openssl rand -hex 16)

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# API
API_V1_STR=/api/v1
PROJECT_NAME=Python Code Check System
VERSION=0.1.0

# Code checking limits
MAX_CODE_LENGTH=10000
MIN_CODE_LENGTH=10
MEMORY_LIMIT_MB=100
TIME_LIMIT_SECONDS=1
EOF
    echo "✅ .env file created"
fi

cd ..

# Setup frontend
echo "📦 Setting up frontend..."
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

# Create .env file for frontend
if [ ! -f ".env" ]; then
    echo "Creating frontend .env file..."
    cat > .env << EOF
REACT_APP_API_URL=http://localhost:8000/api/v1
EOF
    echo "✅ Frontend .env file created"
fi

cd ..

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "To start development:"
echo "1. Start database (PostgreSQL + Redis):"
echo "   docker-compose up db redis -d"
echo ""
echo "2. Start backend:"
echo "   cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo ""
echo "3. Start frontend (in another terminal):"
echo "   cd frontend && npm start"
echo ""
echo "4. Initialize database:"
echo "   cd backend && source venv/bin/activate && python init_db.py"
echo ""
echo "Access points:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:8000"
echo "- API Docs: http://localhost:8000/docs"
