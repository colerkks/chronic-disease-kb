"""
Query endpoints
"""

from fastapi import APIRouter, HTTPException, status
from typing import Optional

from models.query import QueryRequest, QueryResponse, RecommendationRequest, RecommendationResponse
from agents.orchestrator import agent_orchestrator

router = APIRouter()


@router.post("/query", response_model=QueryResponse, status_code=status.HTTP_200_OK)
async def query_knowledge_base(request: QueryRequest):
    """
    Query the knowledge base with natural language
    
    This endpoint processes user queries through the agent system:
    1. QueryAgent analyzes the query intent and extracts entities
    2. RetrievalAgent searches knowledge base and generates answer
    3. Returns synthesized response with sources and recommendations
    
    Example:
        ```json
        {
            "query": "2型糖尿病的早期症状是什么？",
            "patient_id": "patient_123",
            "query_type": "symptoms",
            "max_results": 5
        }
        ```
    """
    try:
        # Get patient context if patient_id provided
        patient = None
        if request.patient_id:
            # TODO: Load patient from database
            pass
        
        # Process query through agent orchestrator
        response = agent_orchestrator.process_query(request, patient)
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )


@router.post("/query/simple")
async def simple_query(query: str, patient_id: Optional[str] = None):
    """Simple query endpoint for quick questions"""
    request = QueryRequest(
        query=query,
        patient_id=patient_id,
        query_type=None,
        disease_filter=None,
        max_results=3
    )
    
    return await query_knowledge_base(request)


@router.get("/query/examples")
async def get_query_examples():
    """Get example queries"""
    return {
        "examples": [
            {
                "query": "2型糖尿病的早期症状是什么？",
                "category": "symptoms",
                "description": "关于糖尿病症状"
            },
            {
                "query": "高血压患者应该如何调整饮食？",
                "category": "lifestyle",
                "description": "饮食建议"
            },
            {
                "query": "哮喘发作时应该怎么办？",
                "category": "emergency",
                "description": "应急处理"
            },
            {
                "query": "二甲双胍有什么副作用？",
                "category": "medication",
                "description": "药物信息"
            }
        ]
    }
