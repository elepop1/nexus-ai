#!/bin/bash
# Deploy NexusAI to cloud

set -e

echo "🚀 Deploying NexusAI..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if git is initialized
if [ ! -d .git ]; then
    echo -e "${BLUE}Initializing git...${NC}"
    git init
    git add .
    git commit -m "Initial commit: NexusAI powered by MiMo V2.5"
fi

echo ""
echo "Deployment options:"
echo "  1. Vercel (Frontend) + Railway (Backend)"
echo "  2. Docker Compose"
echo "  3. Manual deployment"
echo ""
read -p "Select option (1-3): " OPTION

case $OPTION in
    1)
        echo -e "${BLUE}Deploying to Vercel + Railway...${NC}"
        echo ""
        echo "Steps:"
        echo "  1. Push to GitHub"
        echo "  2. Connect Vercel to frontend/ directory"
        echo "  3. Connect Railway to backend/ directory"
        echo "  4. Set environment variables in both dashboards"
        echo ""
        echo "Environment variables:"
        echo "  Frontend: NEXT_PUBLIC_API_URL=<backend-url>"
        echo "  Backend: MIMO_API_BASE, MIMO_API_KEY, MIMO_MODEL"
        ;;
    2)
        echo -e "${BLUE}Deploying with Docker...${NC}"
        docker-compose up -d --build
        echo -e "${GREEN}✓ Deployed!${NC}"
        echo "Frontend: http://localhost:3000"
        echo "Backend: http://localhost:8000"
        ;;
    3)
        echo -e "${BLUE}Manual deployment${NC}"
        echo ""
        echo "Backend:"
        echo "  cd backend && pip install -r requirements.txt"
        echo "  uvicorn main:app --host 0.0.0.0 --port 8000"
        echo ""
        echo "Frontend:"
        echo "  cd frontend && npm install && npm run build"
        echo "  npm start"
        ;;
esac

echo ""
echo -e "${GREEN}Done!${NC}"
