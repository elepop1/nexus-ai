#!/bin/bash
# NexusAI Setup Script

set -e

echo "🚀 Setting up NexusAI..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check dependencies
echo -e "${BLUE}Checking dependencies...${NC}"

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.10+"
    exit 1
fi

echo -e "${GREEN}✓ Dependencies OK${NC}"
echo ""

# Setup backend
echo -e "${BLUE}Setting up backend...${NC}"
cd backend

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Created .env from example. Please edit with your API key."
fi

echo -e "${GREEN}✓ Backend ready${NC}"
echo ""

cd ..

# Setup frontend
echo -e "${BLUE}Setting up frontend...${NC}"
cd frontend

npm install

if [ ! -f .env.local ]; then
    cp .env.local.example .env.local
    echo "⚠️  Created .env.local from example."
fi

echo -e "${GREEN}✓ Frontend ready${NC}"
echo ""

cd ..

echo ""
echo -e "${GREEN}🎉 Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Edit backend/.env with your MiMo API key"
echo "  2. Start backend: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "  3. Start frontend: cd frontend && npm run dev"
echo "  4. Open http://localhost:3000"
echo ""
