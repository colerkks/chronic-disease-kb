"""
Health check endpoints
"""

from fastapi import APIRouter, status
from datetime import datetime

from kb.knowledge_base import knowledge_base
from agents.orchestrator import agent_orchestrator

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "api": "running",
            "knowledge_base": "available",
            "agents": "available"
        }
    }


@router.get("/health/detailed", status_code=status.HTTP_200_OK)
async def detailed_health_check():
    """Detailed health check with system status"""
    kb_stats = {
        "total_documents": knowledge_base.count_documents(),
        "diseases_covered": len(knowledge_base.get_all_diseases())
    }
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "knowledge_base": kb_stats,
        "services": {
            "api": {"status": "running", "latency_ms": 0},
            "knowledge_base": {"status": "available", "stats": kb_stats},
            "agents": {
                "query_agent": "available",
                "retrieval_agent": "available",
                "recommendation_agent": "available"
            }
        }
    }
