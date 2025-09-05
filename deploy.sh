#!/bin/bash

# Beehiiv Integration Backend Deployment Script
# This script builds and deploys the application to Google Cloud Functions

set -e  # Exit on any error

# Configuration
PROJECT_ID="brsocial"
FUNCTION_NAME="beehiiv-integration"
REGION="us-central1"
IMAGE_NAME="gcr.io/$PROJECT_ID/$FUNCTION_NAME"

echo "🚀 Starting deployment of Beehiiv Integration Backend..."

# Check if required environment variables are set
if [ -z "$BEEHIIV_API_KEY" ]; then
    echo "❌ Error: BEEHIIV_API_KEY environment variable is not set"
    echo "Please set it with: export BEEHIIV_API_KEY=your_api_key"
    exit 1
fi

if [ -z "$BEEHIIV_PUBLICATION_ID" ]; then
    echo "❌ Error: BEEHIIV_PUBLICATION_ID environment variable is not set"
    echo "Please set it with: export BEEHIIV_PUBLICATION_ID=your_publication_id"
    exit 1
fi

echo "✅ Environment variables are set"

# Build Docker image
echo "🔨 Building Docker image..."
docker build -t $IMAGE_NAME:latest .

# Push to Container Registry
echo "📤 Pushing image to Container Registry..."
docker push $IMAGE_NAME:latest

# Deploy to Cloud Functions
echo "🚀 Deploying to Cloud Functions..."
gcloud functions deploy $FUNCTION_NAME \
    --gen2 \
    --runtime=python311 \
    --trigger-http \
    --allow-unauthenticated \
    --source=. \
    --entry-point=app_handler \
    --region=$REGION \
    --set-env-vars="BEEHIIV_API_KEY=$BEEHIIV_API_KEY,BEEHIIV_PUBLICATION_ID=$BEEHIIV_PUBLICATION_ID"

echo "✅ Deployment completed successfully!"
echo "🌐 Your function is available at:"
gcloud functions describe $FUNCTION_NAME --region=$REGION --format="value(serviceConfig.uri)"
