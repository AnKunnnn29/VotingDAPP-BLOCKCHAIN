#!/bin/bash
# Quick start script for DApp Voting System infrastructure

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}DApp Voting System - Quick Start${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    echo "Please install Docker from https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed${NC}"
    echo "Please install Docker Compose from https://docs.docker.com/compose/install/"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${YELLOW}⚠ Please edit .env and update SECRET_KEY and JWT_SECRET_KEY before production use!${NC}\n"
fi

# Stop existing containers
echo -e "${BLUE}Stopping existing containers...${NC}"
docker-compose down

# Pull latest images
echo -e "${BLUE}Pulling Docker images...${NC}"
docker-compose pull

# Build backend image
echo -e "${BLUE}Building backend image...${NC}"
docker-compose build backend

# Start services
echo -e "${BLUE}Starting services...${NC}"
docker-compose up -d

# Wait for services to be ready
echo -e "${BLUE}Waiting for services to be ready...${NC}"
sleep 10

# Check service health
echo -e "\n${BLUE}Checking service health...${NC}"

# Check PostgreSQL
if docker-compose exec -T postgres pg_isready -U voting_user &> /dev/null; then
    echo -e "${GREEN}✓ PostgreSQL is ready${NC}"
else
    echo -e "${RED}✗ PostgreSQL is not ready${NC}"
fi

# Check Redis
if docker-compose exec -T redis redis-cli ping &> /dev/null; then
    echo -e "${GREEN}✓ Redis is ready${NC}"
else
    echo -e "${RED}✗ Redis is not ready${NC}"
fi

# Check Backend
if curl -s http://localhost:8000/health &> /dev/null; then
    echo -e "${GREEN}✓ Backend is ready${NC}"
else
    echo -e "${YELLOW}⚠ Backend is starting... (may take a few more seconds)${NC}"
fi

# Run database migrations
echo -e "\n${BLUE}Running database migrations...${NC}"
docker-compose exec -T backend alembic upgrade head
echo -e "${GREEN}✓ Database migrations complete${NC}"

# Create MinIO buckets
echo -e "\n${BLUE}Setting up MinIO buckets...${NC}"
sleep 5
docker-compose exec -T minio mc alias set local http://localhost:9000 minioadmin minioadmin 2>/dev/null || true
docker-compose exec -T minio mc mb local/election-documents 2>/dev/null || echo "Bucket already exists"
docker-compose exec -T minio mc mb local/user-documents 2>/dev/null || echo "Bucket already exists"
docker-compose exec -T minio mc mb local/ml-models 2>/dev/null || echo "Bucket already exists"
echo -e "${GREEN}✓ MinIO buckets ready${NC}"

# Display service URLs
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Services are ready!${NC}"
echo -e "${GREEN}========================================${NC}\n"

echo -e "📡 ${BLUE}Backend API:${NC}        http://localhost:8000"
echo -e "📚 ${BLUE}API Docs:${NC}           http://localhost:8000/api/docs"
echo -e "📊 ${BLUE}Prometheus:${NC}         http://localhost:9090"
echo -e "📈 ${BLUE}Grafana:${NC}            http://localhost:3001 (admin/admin)"
echo -e "💾 ${BLUE}MinIO Console:${NC}      http://localhost:9001 (minioadmin/minioadmin)"

echo -e "\n${YELLOW}View logs:${NC}          docker-compose logs -f"
echo -e "${YELLOW}Stop services:${NC}      docker-compose down"
echo -e "${YELLOW}Restart services:${NC}   docker-compose restart"

echo -e "\n${GREEN}✓ Setup complete! Happy coding! 🚀${NC}\n"
