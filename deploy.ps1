@echo off
echo === INDUS-AI Production Deploy (Windows) ===

if not exist .env (
  copy .env.production.example .env
  echo Created .env - EDIT IT and add your GEMINI_API_KEY, then run again.
  exit /b 1
)

docker compose -f docker-compose.prod.yml up -d --build
timeout /t 10 /nobreak >nul
docker compose -f docker-compose.prod.yml exec -T backend python scripts/seed_demo.py

echo.
echo ============================================
echo   INDUS-AI deployed!
echo   App URL:  http://localhost:3000
echo   API URL:  http://localhost:8000/api/health
echo   Login:    demo@indusai.com / demo123
echo ============================================
