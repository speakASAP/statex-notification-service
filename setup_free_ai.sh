#!/bin/bash

# StateX Free AI Services Setup Script
# This script sets up free AI services for testing

echo "🆓 Setting up Free AI Services for StateX..."

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "📥 Installing Ollama..."
    
    # Detect OS and install Ollama
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        echo "🍎 Installing Ollama for macOS..."
        curl -fsSL https://ollama.ai/install.sh | sh
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        echo "🐧 Installing Ollama for Linux..."
        curl -fsSL https://ollama.ai/install.sh | sh
    else
        echo "❌ Unsupported OS. Please install Ollama manually from https://ollama.ai"
        exit 1
    fi
else
    echo "✅ Ollama is already installed"
fi

# Start Ollama service
echo "🚀 Starting Ollama service..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to start
echo "⏳ Waiting for Ollama to start..."
sleep 5

# Download free models
echo "📥 Downloading free AI models..."

# Llama 2 7B (Good for general text generation)
echo "📥 Downloading Llama 2 7B..."
ollama pull llama2:7b

# Mistral 7B (Good for code and analysis)
echo "📥 Downloading Mistral 7B..."
ollama pull mistral:7b

# CodeLlama 7B (Good for technical analysis)
echo "📥 Downloading CodeLlama 7B..."
ollama pull codellama:7b

echo ""
echo "🎉 Free AI Services Setup Complete!"
echo ""
echo "📋 Available Models:"
echo "  • llama2:7b - General text generation"
echo "  • mistral:7b - Code and analysis"
echo "  • codellama:7b - Technical analysis"
echo ""
echo "🔧 To use these models:"
echo "  • Test: ollama run llama2:7b 'Hello, how are you?'"
echo "  • List models: ollama list"
echo "  • Stop service: kill $OLLAMA_PID"
echo ""
echo "🚀 Now you can run: python3 test_workflow_free_ai.py --demo"
