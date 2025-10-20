#!/bin/bash

# TLS Concept - Toyota Production 2.0 Quick Start Script
# This script helps you quickly set up and run the application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}TLS Concept - Toyota Production 2.0${NC}"
echo -e "${BLUE}Quick Start Setup${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3.12 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Found Python $PYTHON_VERSION${NC}\n"

# Check pip
echo -e "${YELLOW}Checking pip...${NC}"
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo -e "${RED}Error: pip is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ pip is installed${NC}\n"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv .venv
    echo -e "${GREEN}✓ Virtual environment created${NC}\n"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}\n"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source .venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}\n"

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip --quiet
echo -e "${GREEN}✓ pip upgraded${NC}\n"

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt --quiet
echo -e "${GREEN}✓ Dependencies installed${NC}\n"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${YELLOW}Note: Please edit .env and add your API keys${NC}\n"
else
    echo -e "${GREEN}✓ .env file already exists${NC}\n"
fi

# Run tests
echo -e "${YELLOW}Running tests...${NC}"
if command -v pytest &> /dev/null; then
    pytest tests/ -v --tb=short
    echo -e "${GREEN}✓ Tests passed${NC}\n"
else
    echo -e "${YELLOW}⚠ pytest not found, skipping tests${NC}\n"
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${BLUE}========================================${NC}\n"

echo -e "To run the application:"
echo -e "  ${GREEN}streamlit run app.py${NC}\n"

echo -e "Or use make commands:"
echo -e "  ${GREEN}make run${NC}        - Run the application"
echo -e "  ${GREEN}make test${NC}       - Run tests"
echo -e "  ${GREEN}make lint${NC}       - Run linters"
echo -e "  ${GREEN}make help${NC}       - Show all available commands\n"

# Ask if user wants to run the app now
read -p "Would you like to start the application now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "\n${GREEN}Starting application...${NC}\n"
    streamlit run app.py
fi
