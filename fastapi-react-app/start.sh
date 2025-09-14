#!/bin/bash

# Start script for Python Code Check System

echo "Starting Python Code Check System..."

# Create .env file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "Creating .env file..."
    cat > backend/.env << EOF
# Database
POSTGRES_SERVER=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=python_code_check
POSTGRES_PORT=5432

# Redis
REDIS_URL=redis://redis:6379

# Security
SECRET_KEY=your-secret-key-change-in-production-$(openssl rand -hex 32)

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://frontend:3000"]

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
    echo ".env file created"
fi

# Build and start services
echo "Building and starting services..."
docker-compose up --build -d

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Run migrations
echo "Running database migrations..."
docker-compose exec backend python migrate.py

# Initialize database with sample data
echo "Initializing database with sample data..."
docker-compose exec backend python init_db.py

echo ""
echo "🎉 Python Code Check System is now running!"
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Test accounts:"
echo "  Admin: admin / admin123"
echo "  Student: student / student123"
echo ""
echo "To stop the system, run: docker-compose down"
echo "To view logs, run: docker-compose logs -f"
