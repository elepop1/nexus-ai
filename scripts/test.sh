#!/bin/bash
# Test NexusAI API endpoints

set -e

API_URL="http://localhost:8000"

echo "🧪 Testing NexusAI API..."
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Health check
echo -n "Testing health endpoint... "
RESPONSE=$(curl -s "$API_URL/health")
if echo "$RESPONSE" | grep -q "healthy"; then
    echo -e "${GREEN}✓ PASS${NC}"
else
    echo -e "${RED}✗ FAIL${NC}"
    echo "Response: $RESPONSE"
    exit 1
fi

# Chat endpoint
echo -n "Testing chat endpoint... "
RESPONSE=$(curl -s -X POST "$API_URL/api/chat" \
    -H "Content-Type: application/json" \
    -d '{"message": "Hello", "reasoning": true}')
if echo "$RESPONSE" | grep -q "response"; then
    echo -e "${GREEN}✓ PASS${NC}"
else
    echo -e "${RED}✗ FAIL${NC}"
    echo "Response: $RESPONSE"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 All tests passed!${NC}"
