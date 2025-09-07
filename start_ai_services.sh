#!/bin/bash

# StateX AI Services Startup Script
# This script starts the AI services for real AI processing

echo "🚀 Starting StateX AI Services..."

# Navigate to AI services directory
cd /Users/sergiystashok/Documents/GitHub/statex/statex-ai

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: docker-compose.yml not found in statex-ai directory"
    echo "Please ensure you're in the correct directory"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your API keys before running the services"
    echo "Required: OPENAI_API_KEY, ANTHROPIC_API_KEY, etc."
    exit 1
fi

# Start AI services
echo "🐳 Starting AI services with Docker Compose..."
docker compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo "🔍 Checking service health..."

# AI Orchestrator (Port 8010)
if curl -s http://localhost:8010/health > /dev/null; then
    echo "✅ AI Orchestrator (8010) - Ready"
else
    echo "❌ AI Orchestrator (8010) - Not ready"
fi

# NLP Service (Port 8011)
if curl -s http://localhost:8011/health > /dev/null; then
    echo "✅ NLP Service (8011) - Ready"
else
    echo "❌ NLP Service (8011) - Not ready"
fi

# ASR Service (Port 8012)
if curl -s http://localhost:8012/health > /dev/null; then
    echo "✅ ASR Service (8012) - Ready"
else
    echo "❌ ASR Service (8012) - Not ready"
fi

# Document AI Service (Port 8013)
if curl -s http://localhost:8013/health > /dev/null; then
    echo "✅ Document AI Service (8013) - Ready"
else
    echo "❌ Document AI Service (8013) - Not ready"
fi

# Prototype Generator (Port 8014)
if curl -s http://localhost:8014/health > /dev/null; then
    echo "✅ Prototype Generator (8014) - Ready"
else
    echo "❌ Prototype Generator (8014) - Not ready"
fi

# Template Repository (Port 8015)
if curl -s http://localhost:8015/health > /dev/null; then
    echo "✅ Template Repository (8015) - Ready"
else
    echo "❌ Template Repository (8015) - Not ready"
fi

echo ""
echo "🎉 AI Services startup complete!"
echo "You can now run: python3 test_workflow_real_ai.py --demo"
echo ""
echo "To stop services: docker compose down"
echo "To view logs: docker compose logs -f"
