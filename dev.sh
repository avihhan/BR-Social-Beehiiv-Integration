#!/bin/bash

# Beehiiv Integration Backend Development Script
# This script runs the application locally for development

set -e  # Exit on any error

echo "🔧 Starting Beehiiv Integration Backend in development mode..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Creating .env from env.example..."
    cp env.example .env
    echo "📝 Please edit .env file with your actual API keys"
    echo "Then run this script again"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check if required environment variables are set
if [ -z "$BEEHIIV_API_KEY" ] || [ "$BEEHIIV_API_KEY" = "your_beehiiv_api_key_here" ]; then
    echo "❌ Error: BEEHIIV_API_KEY is not set in .env file"
    echo "Please edit .env file with your actual Beehiiv API key"
    exit 1
fi

if [ -z "$BEEHIIV_PUBLICATION_ID" ] || [ "$BEEHIIV_PUBLICATION_ID" = "your_publication_id_here" ]; then
    echo "❌ Error: BEEHIIV_PUBLICATION_ID is not set in .env file"
    echo "Please edit .env file with your actual publication ID"
    exit 1
fi

echo "✅ Environment variables loaded"

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

echo "📦 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Run the application
echo "🚀 Starting FastAPI development server..."
echo "🌐 API will be available at: http://localhost:8000"
echo "📚 API documentation at: http://localhost:8000/docs"
echo "🔍 Health check at: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"

uvicorn main:app --reload --host 0.0.0.0 --port 8000
