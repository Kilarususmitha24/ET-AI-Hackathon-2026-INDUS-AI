#!/bin/bash
set -e

echo "=== INDUS-AI Production Deploy ==="

if [ ! -f .env ]; then
  echo "Creating .env from .env.production.example — EDIT IT and add GEMINI_API_KEY!"
  cp .env.production.example .env
  exit 1
fi

# Install Docker if missing (Ubuntu/Debian)
if ! command -v docker &> /dev/null; then
  echo "Installing Docker..."
  curl -fsSL https://get.docker.com | sh
  sudo usermod -aG docker "$USER"
  echo "Log out and back in, then re-run this script."
  exit 0
fi

echo "Building and starting containers..."
docker compose -f docker-compose.prod.yml up -d --build

echo "Waiting for backend..."
sleep 8

echo "Seeding demo data..."
docker compose -f docker-compose.prod.yml exec -T backend python scripts/seed_demo.py || true

PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null || hostname -I | awk '{print $1}')

echo ""
echo "============================================"
echo "  INDUS-AI deployed successfully!"
echo "  App URL:  http://${PUBLIC_IP}:3000"
echo "  API URL:  http://${PUBLIC_IP}:8000/api/health"
echo "  Login:    demo@indusai.com / demo123"
echo "============================================"
echo ""
echo "Open port 3000 in your cloud firewall/security group!"
