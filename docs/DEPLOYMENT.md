# INDUS-AI — Deployment Guide (Hackathon)

Deploy in **under 10 minutes** using one of the options below.

---

## Option 1: Docker on a Cloud VM (Recommended — full app, one URL)

Best for hackathon demos: everything runs on one server.

### Step 1 — Get a free/cheap VM

Use any of these (pick one):

| Provider | Free tier |
|----------|-----------|
| [Oracle Cloud](https://www.oracle.com/cloud/free/) | Always-free ARM VM |
| [Google Cloud](https://cloud.google.com/free) | e2-micro free tier |
| [AWS EC2](https://aws.amazon.com/free/) | t2.micro 12 months |
| [DigitalOcean](https://www.digitalocean.com/) | ~$6/month |

Choose **Ubuntu 22.04**, at least **2 GB RAM**, open ports **3000** and **8000** in the firewall/security group.

### Step 2 — SSH into the server

```bash
ssh ubuntu@YOUR_SERVER_IP
```

### Step 3 — Clone and configure

```bash
sudo apt update && sudo apt install -y git
git clone https://github.com/YOUR_USERNAME/ET-AI-Hackathon-2026-INDUS-AI.git
cd ET-AI-Hackathon-2026-INDUS-AI

cp .env.production.example .env
nano .env
```

Set these in `.env`:

```env
GEMINI_API_KEY=your-actual-gemini-key
SECRET_KEY=any-long-random-string-here
CORS_ORIGINS=http://YOUR_SERVER_IP:3000
```

Get a Gemini key: https://aistudio.google.com/apikey

### Step 4 — Deploy

```bash
chmod +x deploy.sh
./deploy.sh
```

Or manually:

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# Log out and SSH back in, then:
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml exec backend python scripts/seed_demo.py
```

### Step 5 — Open the app

**http://YOUR_SERVER_IP:3000**

Login: `demo@indusai.com` / `demo123`

---

## Option 2: Render.com (no VM management)

Split deploy: backend on Render, frontend on Render static site.

### Backend (Web Service)

1. Push code to **GitHub**
2. Go to [render.com](https://render.com) → **New → Web Service**
3. Connect your repo, set:
   - **Root Directory:** `backend`
   - **Runtime:** Docker
   - **Port:** `8000`
4. Add environment variables:
   - `GEMINI_API_KEY` = your key
   - `SECRET_KEY` = random string
   - `CORS_ORIGINS` = `https://your-frontend.onrender.com`
5. Deploy → note URL, e.g. `https://indus-ai-api.onrender.com`

### Frontend (Static Site)

1. **New → Static Site** → same repo
2. Settings:
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`
3. Environment variable:
   - `VITE_API_URL` = `https://indus-ai-api.onrender.com/api`
4. Deploy → open `https://your-frontend.onrender.com`

> Note: Render free tier sleeps after inactivity. First load may take ~30 seconds.

---

## Option 3: Railway.app (fastest cloud deploy)

1. Push to GitHub
2. Go to [railway.app](https://railway.app) → **New Project → Deploy from GitHub**
3. Add **three services** from the same repo, or use Docker Compose:
   - Deploy `docker-compose.prod.yml` as a project
4. Set env vars: `GEMINI_API_KEY`, `SECRET_KEY`, `CORS_ORIGINS`
5. Railway gives you a public URL automatically

---

## Option 4: Local machine as public demo (ngrok — instant)

If you only need a **shareable link for judging** right now:

**Terminal 1 — Backend**
```powershell
cd backend
.\venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 — Frontend**
```powershell
cd frontend
npm run dev
```

**Terminal 3 — ngrok** (install from https://ngrok.com)
```powershell
ngrok http 5173
```

Share the `https://xxxx.ngrok.io` URL with judges.

For ngrok + separate backend, set in `frontend/.env.local`:
```env
VITE_API_URL=https://YOUR-BACKEND-NGROK-URL/api
```

---

## Firewall checklist

| Port | Service |
|------|---------|
| 3000 | Frontend (Docker prod) |
| 8000 | Backend API (optional direct access) |
| 5173 | Local dev only |

On **Oracle/AWS/GCP**, open these in the **Security Group / Ingress rules**.

---

## Post-deploy checklist

- [ ] `GEMINI_API_KEY` set in environment
- [ ] `CORS_ORIGINS` includes your public frontend URL
- [ ] Port 3000 open in cloud firewall
- [ ] Demo data seeded (`python scripts/seed_demo.py`)
- [ ] Login works: `demo@indusai.com` / `demo123`
- [ ] Upload a document and test AI chat

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ERR_CONNECTION_REFUSED` | Open port 3000 in firewall; check `docker ps` |
| Login fails / CORS error | Add your public URL to `CORS_ORIGINS` in `.env`, restart backend |
| AI gives generic answers | Set `GEMINI_API_KEY` and restart backend |
| Empty knowledge base | Run `docker compose exec backend python scripts/seed_demo.py` |
| Neo4j connection warning | Safe to ignore — app uses in-memory graph fallback |

---

## Quick commands reference

```bash
# Start production
docker compose -f docker-compose.prod.yml up -d --build

# View logs
docker compose -f docker-compose.prod.yml logs -f

# Stop
docker compose -f docker-compose.prod.yml down

# Reseed demo data
docker compose -f docker-compose.prod.yml exec backend python scripts/seed_demo.py
```
