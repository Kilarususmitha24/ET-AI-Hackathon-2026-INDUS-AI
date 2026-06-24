from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.models import User
from app.schemas import KnowledgeGraphResponse, GraphNode, GraphEdge
from app.services.neo4j_service import get_neo4j_service

router = APIRouter(prefix="/knowledge-graph", tags=["Knowledge Graph"])


@router.get("/", response_model=KnowledgeGraphResponse)
def get_knowledge_graph(current_user: User = Depends(get_current_user)):
    graph = get_neo4j_service().get_graph()
    nodes = [GraphNode(**n) for n in graph["nodes"]]
    edges = [GraphEdge(**e) for e in graph["edges"]]
    return KnowledgeGraphResponse(nodes=nodes, edges=edges)
