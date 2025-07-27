#!/bin/bash

# Deploy to Elastic Beanstalk
echo "🚀 Deploying to Elastic Beanstalk..."

# Check if EB CLI is installed
if ! command -v eb &> /dev/null; then
    echo "❌ EB CLI not found. Please install it first:"
    echo "pip install awsebcli"
    exit 1
fi

# Build Docker image
echo "📦 Building Docker image..."
docker build -t auto-podcast-backend:latest .

# Create application bundle
echo "📋 Creating application bundle..."
mkdir -p .ebextensions
cp -r .ebextensions/ ./
cp Dockerrun.aws.json ./
cp Dockerfile ./
cp requirements.txt ./
cp app.py ./
cp index.html ./
cp style.css ./
cp script.js ./
cp -r assets/ ./
cp nginx.conf ./

# Create ZIP file
echo "🗜️ Creating deployment package..."
zip -r auto-podcast-eb.zip . -x "*.git*" "*.DS_Store*" "data/*" "*.csv" "*.db"

# Deploy to EB
echo "🌐 Deploying to Elastic Beanstalk..."
eb deploy

echo "✅ Deployment completed!"
echo "🌍 Your application should be available at:"
eb status | grep CNAME 