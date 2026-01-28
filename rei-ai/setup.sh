#!/bin/bash

echo "=================================="
echo "REI-AI Automated Setup"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python
echo -e "${YELLOW}Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"
else
    echo -e "${RED}✗ Python 3 not found. Please install Python 3.11+${NC}"
    exit 1
fi

# Check Node.js
echo -e "${YELLOW}Checking Node.js installation...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js $NODE_VERSION found${NC}"
else
    echo -e "${RED}✗ Node.js not found. Please install Node.js 18+${NC}"
    exit 1
fi

echo ""
echo "=================================="
echo "Setting up Backend"
echo "=================================="
echo ""

cd backend

# Create virtual environment
echo -e "${YELLOW}Creating Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo -e "${GREEN}✓ Backend dependencies installed${NC}"

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating backend .env file...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ Created backend/.env (please add your API keys)${NC}"
fi

# Initialize database
echo -e "${YELLOW}Initializing database...${NC}"
python scripts/init_db.py
echo -e "${GREEN}✓ Database initialized with sample data${NC}"

cd ..

echo ""
echo "=================================="
echo "Setting up Frontend"
echo "=================================="
echo ""

cd frontend

# Install dependencies
echo -e "${YELLOW}Installing Node.js dependencies...${NC}"
npm install --silent
echo -e "${GREEN}✓ Frontend dependencies installed${NC}"

# Create .env.local if it doesn't exist
if [ ! -f .env.local ]; then
    echo -e "${YELLOW}Creating frontend .env.local file...${NC}"
    cp .env.example .env.local
    echo -e "${GREEN}✓ Created frontend/.env.local${NC}"
fi

cd ..

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo -e "${GREEN}To start the application:${NC}"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload --port 8000"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then visit: http://localhost:3000"
echo ""
echo -e "${YELLOW}Note: The app works with sample data.${NC}"
echo -e "${YELLOW}Add API keys in .env files for real data.${NC}"
echo ""
