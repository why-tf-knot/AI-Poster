#!/bin/bash
# Stop script for the compliance monitoring system

set -e  # Exit on error

echo "⏹️  Stopping Compliance Monitoring System"
echo "=========================================="

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Stop Docker containers
echo -e "\n${YELLOW}Stopping Docker containers...${NC}"
docker compose down

echo -e "\n${GREEN}✅ System stopped successfully!${NC}"
echo ""
echo "📋 To remove all data (including database):"
echo "   ${YELLOW}docker compose down -v${NC}"
echo ""
echo "📋 To restart the system:"
echo "   ${YELLOW}./start_system.sh${NC}"
