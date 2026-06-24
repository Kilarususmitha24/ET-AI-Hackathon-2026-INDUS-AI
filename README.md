# INDUS-AI: Unified Asset & Operations Brain

**ET AI Hackathon 2026 — Problem Statement 8: AI for Industrial Knowledge Intelligence**

INDUS-AI is an AI-powered industrial knowledge intelligence platform that transforms scattered industrial documents into a unified, searchable, and intelligent knowledge system. Built with React, FastAPI, Google Gemini, LangChain, FAISS, and Neo4j.

**Team:** Kilaru Susmitha and Team

---

## Features

| Feature | Description |
|---------|-------------|
| **User Authentication** | JWT-based secure login and registration |
| **Document Upload** | PDF, DOCX, TXT, and scanned images with OCR |
| **RAG Chatbot** | Gemini-powered Q&A with source citations |
| **Knowledge Graph** | Neo4j visualization of equipment, procedures, regulations |
| **Compliance Dashboard** | Automated OSHA, ISO, API, NFPA, EPA gap detection |
| **Maintenance Engine** | AI-generated prioritized maintenance recommendations |
| **Root Cause Analysis** | Incident investigation with knowledge base context |
| **Analytics Dashboard** | Real-time metrics and activity tracking |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, Tailwind CSS, Recharts, react-force-graph-2d |
| Backend | FastAPI, SQLAlchemy, Pydantic |
| AI/ML | Google Gemini 2.0 Flash, LangChain, FAISS |
| Knowledge Graph | Neo4j 5 |
| OCR | Tesseract, pdf2image, PyPDF |
| Auth | JWT (python-jose), bcrypt |
| Database | SQLite (metadata), FAISS (vectors), Neo4j (graph) |

---

## Project Structure

```
INDUS-AI/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry
│   │   ├── config.py            # Settings and environment
│   │   ├── database.py          # SQLAlchemy setup
│   │   ├── models.py            # Database models
│   │   ├── auth.py              # JWT authentication
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── routers/             # API route handlers
│   │   └── services/            # Business logic & AI services
│   ├── scripts/seed_demo.py     # Demo data seeder
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── pages/               # Dashboard, Chat, Documents, etc.
│   │   ├── components/          # Layout, Sidebar
│   │   ├── context/             # Auth context
│   │   └── api.js               # API client
│   ├── package.json
│   └── Dockerfile
├── sample_documents/            # Industrial sample docs
├── docs/
│   ├── ARCHITECTURE.md          # Mermaid architecture diagrams
│   ├── DATABASE_SCHEMA.md       # Database schema documentation
│   ├── PPT_OUTLINE.md           # Presentation outline
│   └── DEMO_SCRIPT.md           # 3-minute demo script
├── docker-compose.yml
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login (returns JWT) |
| GET | `/api/auth/me` | Get current user |
| GET | `/api/documents/` | List user documents |
| POST | `/api/documents/upload` | Upload document |
| DELETE | `/api/documents/{id}` | Delete document |
| POST | `/api/chat/message` | Send chat message (RAG) |
| GET | `/api/chat/sessions` | List chat sessions |
| GET | `/api/knowledge-graph/` | Get knowledge graph data |
| GET | `/api/compliance/` | List compliance records |
| GET | `/api/compliance/summary` | Compliance score summary |
| GET | `/api/maintenance/` | List maintenance recommendations |
| GET | `/api/maintenance/summary` | Maintenance summary |
| POST | `/api/root-cause/analyze` | Root cause analysis |
| GET | `/api/analytics/dashboard` | Dashboard analytics |
| GET | `/api/health` | Health check |

---

## Installation Guide

### Prerequisites

- Python 3.11+
- Node.js 18+
- Google Gemini API Key ([Get one here](https://aistudio.google.com/apikey))
- Tesseract OCR (optional, for scanned documents)
- Neo4j (optional, Docker recommended)

### Option 1: Local Development

#### Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env and set GEMINI_API_KEY

uvicorn app.main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173**

#### Seed Demo Data

```bash
cd backend
python scripts/seed_demo.py
```

### Option 2: Docker

```bash
# Set your Gemini API key
echo "GEMINI_API_KEY=your-key-here" > .env

docker-compose up --build
```

- Frontend: **http://localhost:3000**
- Backend API: **http://localhost:8000**
- Neo4j Browser: **http://localhost:7474**

### Demo Credentials

| Email | Password |
|-------|----------|
| demo@indusai.com | demo123 |

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | (required for full AI) |
| `SECRET_KEY` | JWT signing key | auto-generated |
| `NEO4J_URI` | Neo4j connection URI | bolt://localhost:7687 |
| `NEO4J_USER` | Neo4j username | neo4j |
| `NEO4J_PASSWORD` | Neo4j password | indusai2026 |
| `DATABASE_URL` | SQLite/PostgreSQL URL | sqlite:///./indus_ai.db |
| `CORS_ORIGINS` | Allowed frontend origins | http://localhost:5173 |

---

## Sample Documents

Five industrial sample documents are included in `sample_documents/`:

1. **Pump P-101 Maintenance Manual** — Preventive maintenance, LOTO procedures
2. **Safety Manual - Process Area** — OSHA, NFPA, EPA compliance
3. **Compressor C-204 Inspection Report** — Inspection findings and recommendations
4. **Boiler B-301 Operating Procedure** — SOP with API 510 compliance
5. **Incident Report - Conveyor Belt Failure** — Root cause analysis example

Upload these via the Documents page or run `python scripts/seed_demo.py`.

---

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed Mermaid diagrams.

```
User → React Frontend → FastAPI Backend → Gemini AI
                                      → FAISS Vector DB
                                      → Neo4j Knowledge Graph
                                      → SQLite Metadata DB
```

---

## Hackathon Submission Assets

| Asset | Location |
|-------|----------|
| Presentation Outline (15 slides) | [docs/PPT_OUTLINE.md](docs/PPT_OUTLINE.md) |
| 3-Minute Demo Script | [docs/DEMO_SCRIPT.md](docs/DEMO_SCRIPT.md) |
| Architecture Diagram | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Database Schema | [docs/DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md) |
| Sample Documents | [sample_documents/](sample_documents/) |

---

## License

Built for ET AI Hackathon 2026. All rights reserved by Kilaru Susmitha and Team.
