#!/bin/bash

echo "🗄️ Starting database services..."

# Start PostgreSQL and Redis
docker-compose -f docker-compose.dev.yml up -d

echo "✅ Database services started!"
echo ""
echo "PostgreSQL: localhost:5432"
echo "Redis: localhost:6379"
echo ""
echo "To stop: docker-compose -f docker-compose.dev.yml down"
