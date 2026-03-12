#!/bin/bash
echo "Deploying Enterprise AI Agent to Production Environment..."

# Pull latest code (setup assumes this is an EC2 or similar server with git installed)
git pull origin main

# Build and restart containers using the main and override files for production monitoring
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d --build

echo "Deployment complete! Agent API is running on port 8000."
echo "Grafana monitoring available on port 3000."
