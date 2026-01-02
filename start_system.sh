#!/bin/bash
# Startup script for the compliance monitoring system

set -e  # Exit on error

echo "🚀 Starting Compliance Monitoring System"
echo "=========================================="

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

# Step 1: Start Docker containers
echo -e "\n${YELLOW}Step 1: Starting Docker containers (PostgreSQL, Kafka, Zookeeper)...${NC}"
docker compose up -d

# Step 2: Wait for services to be healthy
echo -e "\n${YELLOW}Step 2: Waiting for services to be healthy...${NC}"
echo "This may take 30-60 seconds..."

max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    attempt=$((attempt + 1))
    
    # Check if all services are healthy
    postgres_healthy=$(docker inspect --format='{{.State.Health.Status}}' compliance_db 2>/dev/null || echo "starting")
    kafka_healthy=$(docker inspect --format='{{.State.Health.Status}}' compliance_kafka 2>/dev/null || echo "starting")
    zookeeper_healthy=$(docker inspect --format='{{.State.Health.Status}}' compliance_zookeeper 2>/dev/null || echo "starting")
    
    if [ "$postgres_healthy" = "healthy" ] && [ "$kafka_healthy" = "healthy" ] && [ "$zookeeper_healthy" = "healthy" ]; then
        echo -e "${GREEN}✅ All services are healthy!${NC}"
        break
    fi
    
    echo "Attempt $attempt/$max_attempts: PostgreSQL=$postgres_healthy, Kafka=$kafka_healthy, Zookeeper=$zookeeper_healthy"
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    echo -e "${RED}❌ Services failed to become healthy. Check logs with: docker-compose logs${NC}"
    exit 1
fi

# Step 3: Display service status
echo -e "\n${YELLOW}Step 3: Service Status${NC}"
docker compose ps

# Step 4: Instructions
echo -e "\n${GREEN}=========================================="
echo "✅ Infrastructure is ready!"
echo "==========================================${NC}"
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Install Python dependencies (if not already done):"
echo "   ${YELLOW}pip install -r requirements.txt${NC}"
echo ""
echo "2. Start the Compliance Engine (in terminal 1):"
echo "   ${YELLOW}python compliance_engine.py${NC}"
echo ""
echo "3. Start the Telemetry Producer (in terminal 2):"
echo "   ${YELLOW}python producer.py${NC}"
echo ""
echo "4. Monitor the database:"
echo "   ${YELLOW}docker exec -it compliance_db psql -U admin -d compliance_system${NC}"
echo ""
echo "5. Stop the system:"
echo "   ${YELLOW}./stop_system.sh${NC}"
echo ""
echo "📚 For more information, see COMPLIANCE_README.md"
