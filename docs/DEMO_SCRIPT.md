# INDUS-AI: 3-Minute Demo Script

**Total Time: ~3 minutes | Team: Kilaru Susmitha and Team**

---

## [0:00 – 0:20] Introduction

> "Good morning/afternoon judges. We are **Kilaru Susmitha and Team**, presenting **INDUS-AI** — the Unified Asset & Operations Brain for ET AI Hackathon 2026, Problem Statement 8: AI for Industrial Knowledge Intelligence."

> "Industrial plants generate thousands of maintenance records, safety manuals, and inspection reports — but this knowledge is scattered across silos. Engineers spend hours searching for critical information, leading to downtime and compliance risks."

**[Show Login screen → click 'Use demo account']**

---

## [0:20 – 0:50] Dashboard Overview

> "INDUS-AI transforms scattered industrial documents into a unified, intelligent knowledge system."

**[Navigate to Dashboard]**

> "Our operations dashboard provides real-time analytics — document count, knowledge chunks indexed in our FAISS vector database, compliance score, and open maintenance recommendations. Everything an operator needs at a glance."

---

## [0:50 – 1:20] Document Ingestion

**[Navigate to Documents → show uploaded sample documents]**

> "Users upload PDFs, DOCX files, or scanned documents. Our pipeline automatically runs OCR on scanned content, chunks the text, generates Gemini embeddings, and stores them in FAISS for semantic search."

> "Simultaneously, we extract entities — equipment, procedures, regulations — and build a Neo4j knowledge graph. Compliance and maintenance intelligence are generated automatically."

**[Point to processed status, chunk counts, OCR badges]**

---

## [1:20 – 1:50] AI Knowledge Assistant (RAG)

**[Navigate to AI Assistant]**

> "The core of INDUS-AI is our RAG-powered assistant. Let me ask: *'What are the lockout/tagout procedures for Pump P-101?'*"

**[Type and send the question — wait for response]**

> "Notice the answer is grounded in our uploaded documents, with **source citations** showing exactly which document and page the information came from. This is explainable AI — not a black box."

---

## [1:50 – 2:15] Knowledge Graph & Compliance

**[Navigate to Knowledge Graph]**

> "Our knowledge graph visualizes relationships between equipment, procedures, incidents, and regulations — revealing hidden connections across documents."

**[Navigate to Compliance Dashboard]**

> "The compliance dashboard automatically checks documents against OSHA, ISO, API, NFPA, and EPA standards — flagging gaps before they become violations."

---

## [2:15 – 2:40] Maintenance & Root Cause

**[Navigate to Maintenance Dashboard]**

> "The maintenance engine generates prioritized recommendations with confidence scores and estimated downtime — extracted from inspection reports and manuals."

**[Navigate to Root Cause Analysis]**

> "For incidents, our root cause analyzer uses historical knowledge to identify probable causes, contributing factors, and recommended corrective actions."

**[Quickly fill: Equipment: 'Centrifugal Pump P-101', Incident: 'Excessive vibration during peak load', click Analyze]**

---

## [2:40 – 3:00] Closing

> "INDUS-AI reduces search time by 80%, improves maintenance decisions, and increases compliance readiness — all powered by Gemini, LangChain, FAISS, and Neo4j."

> "It's scalable across manufacturing, oil & gas, energy, and mining. Future plans include IoT integration and predictive failure analytics."

> "Thank you. We're happy to take questions and provide a live demo."

**[Show Thank You / Team slide]**

---

## Demo Checklist (Pre-Demo)

- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] GEMINI_API_KEY configured in `.env`
- [ ] Neo4j running (optional — fallback graph works)
- [ ] Demo data seeded: `python scripts/seed_demo.py`
- [ ] Demo login works: `demo@indusai.com` / `demo123`
- [ ] At least 3 documents show "processed" status

## Backup Talking Points (if demo fails)

- Architecture: React + FastAPI + Gemini + FAISS + Neo4j
- RAG pipeline with citation-backed responses
- Automated compliance gap detection against 6 regulatory frameworks
- Knowledge graph entity extraction from unstructured documents
