# INDUS-AI Database Schema

## Overview

INDUS-AI uses **SQLite** (development) for relational metadata and **FAISS** for vector storage. **Neo4j** stores the knowledge graph.

---

## Entity Relationship Diagram

```mermaid
erDiagram
    users ||--o{ documents : owns
    users ||--o{ chat_sessions : has
    chat_sessions ||--o{ chat_messages : contains
    documents ||--o{ compliance_records : generates
    documents ||--o{ maintenance_records : sources
    documents ||--o{ incident_records : references

    users {
        int id PK
        string email UK
        string full_name
        string hashed_password
        string role
        boolean is_active
        datetime created_at
    }

    documents {
        int id PK
        string title
        string filename
        string file_path
        string file_type
        string doc_category
        string status
        int page_count
        int chunk_count
        boolean ocr_applied
        text extracted_text_preview
        json metadata_json
        int user_id FK
        datetime created_at
        datetime processed_at
    }

    chat_sessions {
        int id PK
        string title
        int user_id FK
        datetime created_at
    }

    chat_messages {
        int id PK
        int session_id FK
        string role
        text content
        json citations
        datetime created_at
    }

    compliance_records {
        int id PK
        string regulation
        text requirement
        string status
        string severity
        int document_id FK
        text evidence
        text gap_description
        datetime last_checked
    }

    maintenance_records {
        int id PK
        string equipment
        text recommendation
        string priority
        float confidence
        int source_document_id FK
        float estimated_downtime_hours
        datetime next_due_date
        string status
        datetime created_at
    }

    incident_records {
        int id PK
        string title
        string equipment
        text description
        string severity
        text root_cause
        text corrective_action
        int document_id FK
        datetime occurred_at
    }
```

---

## Neo4j Graph Schema

```cypher
// Node Labels
(:Document {id, title, category})
(:Equipment {name})
(:Procedure {name})
(:Regulation {name})
(:Incident {name})

// Relationships
(Document)-[:DESCRIBES]->(Equipment)
(Document)-[:DEFINES]->(Procedure)
(Document)-[:REFERENCES]->(Regulation)
(Document)-[:REPORTS]->(Incident)
```

---

## FAISS Vector Store

| Field | Type | Description |
|-------|------|-------------|
| document_id | int | Source document reference |
| document_title | string | Document title for citations |
| chunk_index | int | Chunk sequence number |
| text | string | Chunk text content |
| page | int | Approximate page number |
| embedding | float[768] | Gemini text-embedding-004 vector |

---

## Document Status Flow

```
pending → processing → processed
                    ↘ failed
```

## Compliance Status Values

- `compliant` — Full evidence found
- `partial` — Partial evidence
- `gap` — Missing documentation

## Maintenance Priority Levels

- `high` — Immediate action required
- `medium` — Schedule within 30 days
- `low` — Routine maintenance
