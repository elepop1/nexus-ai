#!/bin/bash
# Start NexusAI (both frontend and backend)

set -e

echo "🚀 Starting NexusAI..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Start backend
echo -e "${BLUE}Starting backend...${NC}"
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# Wait for backend
sleep 3

# Start frontend
echo -e "${BLUE}Starting frontend...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo -e "${GREEN}🎉 NexusAI is running!${NC}"
echo ""
echo "  Frontend: http://localhost:3000"
echo "  Backend:  http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop."
echo ""

# Wait for interrupt
trap "echo ''; echo 'Stopping...'; kill $BACKEND_PID $FRONTEND_PID; exit 0" INT
wait
