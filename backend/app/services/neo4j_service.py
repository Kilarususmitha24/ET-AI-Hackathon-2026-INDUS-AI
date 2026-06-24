import logging
from typing import Optional

from neo4j import GraphDatabase

from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class Neo4jService:
    def __init__(self):
        self._driver = None
        self._connected = False
        try:
            self._driver = GraphDatabase.driver(
                settings.neo4j_uri,
                auth=(settings.neo4j_user, settings.neo4j_password),
            )
            self._driver.verify_connectivity()
            self._connected = True
            self._init_schema()
        except Exception as e:
            logger.warning("Neo4j unavailable, using in-memory graph: %s", e)
            self._fallback_nodes: list[dict] = []
            self._fallback_edges: list[dict] = []

    def _init_schema(self):
        with self._driver.session() as session:
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (n:Entity) REQUIRE n.id IS UNIQUE")

    def close(self):
        if self._driver:
            self._driver.close()

    def add_document_knowledge(
        self,
        document_id: int,
        document_title: str,
        category: str,
        entities: dict,
    ):
        if not self._connected:
            self._add_fallback(document_id, document_title, category, entities)
            return

        with self._driver.session() as session:
            session.run(
                """
                MERGE (d:Document {id: $doc_id})
                SET d.title = $title, d.category = $category
                """,
                doc_id=str(document_id),
                title=document_title,
                category=category,
            )

            for equip in entities.get("equipment", []):
                session.run(
                    """
                    MERGE (e:Equipment {name: $name})
                    MERGE (d:Document {id: $doc_id})
                    MERGE (d)-[:DESCRIBES]->(e)
                    """,
                    name=equip,
                    doc_id=str(document_id),
                )

            for proc in entities.get("procedures", []):
                session.run(
                    """
                    MERGE (p:Procedure {name: $name})
                    MERGE (d:Document {id: $doc_id})
                    MERGE (d)-[:DEFINES]->(p)
                    """,
                    name=proc,
                    doc_id=str(document_id),
                )

            for reg in entities.get("regulations", []):
                session.run(
                    """
                    MERGE (r:Regulation {name: $name})
                    MERGE (d:Document {id: $doc_id})
                    MERGE (d)-[:REFERENCES]->(r)
                    """,
                    name=reg,
                    doc_id=str(document_id),
                )

            for incident in entities.get("incidents", []):
                session.run(
                    """
                    MERGE (i:Incident {name: $name})
                    MERGE (d:Document {id: $doc_id})
                    MERGE (d)-[:REPORTS]->(i)
                    """,
                    name=incident,
                    doc_id=str(document_id),
                )

    def _add_fallback(self, document_id, document_title, category, entities):
        doc_id = f"doc_{document_id}"
        self._fallback_nodes.append({
            "id": doc_id,
            "label": document_title,
            "type": "Document",
            "properties": {"category": category},
        })
        for equip in entities.get("equipment", []):
            eid = f"equip_{equip.replace(' ', '_')}"
            self._fallback_nodes.append({"id": eid, "label": equip, "type": "Equipment", "properties": {}})
            self._fallback_edges.append({"source": doc_id, "target": eid, "label": "DESCRIBES"})
        for reg in entities.get("regulations", []):
            rid = f"reg_{reg.replace(' ', '_')}"
            self._fallback_nodes.append({"id": rid, "label": reg, "type": "Regulation", "properties": {}})
            self._fallback_edges.append({"source": doc_id, "target": rid, "label": "REFERENCES"})

    def get_graph(self) -> dict:
        if not self._connected:
            seen = {}
            nodes = []
            for n in self._fallback_nodes:
                if n["id"] not in seen:
                    seen[n["id"]] = True
                    nodes.append(n)
            return {"nodes": nodes, "edges": self._fallback_edges}

        with self._driver.session() as session:
            result = session.run(
                """
                MATCH (n)
                OPTIONAL MATCH (n)-[r]->(m)
                RETURN n, r, m LIMIT 200
                """
            )
            nodes_map = {}
            edges = []
            for record in result:
                for key in ("n", "m"):
                    node = record[key]
                    if node:
                        nid = f"{list(node.labels)[0]}_{node.element_id}"
                        nodes_map[nid] = {
                            "id": nid,
                            "label": node.get("name") or node.get("title") or list(node.labels)[0],
                            "type": list(node.labels)[0],
                            "properties": dict(node),
                        }
                rel = record["r"]
                if rel:
                    src = f"{list(record['n'].labels)[0]}_{record['n'].element_id}"
                    tgt = f"{list(record['m'].labels)[0]}_{record['m'].element_id}"
                    edges.append({"source": src, "target": tgt, "label": rel.type})

            return {"nodes": list(nodes_map.values()), "edges": edges}

    def search_related(self, entity_name: str) -> list[dict]:
        if not self._connected:
            return [e for e in self._fallback_edges if entity_name.lower() in str(e).lower()]
        with self._driver.session() as session:
            result = session.run(
                """
                MATCH (n)-[r]-(m)
                WHERE toLower(n.name) CONTAINS toLower($name)
                   OR toLower(n.title) CONTAINS toLower($name)
                RETURN n, r, m LIMIT 20
                """,
                name=entity_name,
            )
            return [dict(record) for record in result]


_neo4j_service: Optional[Neo4jService] = None


def get_neo4j_service() -> Neo4jService:
    global _neo4j_service
    if _neo4j_service is None:
        _neo4j_service = Neo4jService()
    return _neo4j_service
