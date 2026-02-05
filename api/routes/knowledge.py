"""
Knowledge base management endpoints
"""

from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional, Dict, Any

from kb.knowledge_base import knowledge_base
from models.disease import DiseaseKnowledge
from models.knowledge import KnowledgeCreate

router = APIRouter()


@router.get("/knowledge/stats")
async def get_knowledge_stats():
    """Get knowledge base statistics"""
    return {
        "total_documents": knowledge_base.count_documents(),
        "diseases_covered": knowledge_base.get_all_diseases(),
        "categories": [
            "symptoms",
            "treatment",
            "prevention",
            "lifestyle",
            "complications",
            "diagnosis",
            "comprehensive",
            "general"
        ]
    }


@router.get("/knowledge/diseases")
async def get_all_diseases():
    """Get list of all diseases in knowledge base"""
    diseases = knowledge_base.get_all_diseases()
    return {
        "diseases": diseases,
        "count": len(diseases)
    }


@router.get("/knowledge/search")
async def search_knowledge(
    query: str,
    disease: Optional[str] = None,
    category: Optional[str] = None,
    n_results: int = Query(default=5, ge=1, le=20)
):
    """
    Search knowledge base
    
    Args:
        query: Search query string
        disease: Filter by disease name
        category: Filter by category (symptoms, treatment, etc.)
        n_results: Number of results to return
    """
    try:
        results = knowledge_base.search(
            query=query,
            disease_filter=disease,
            category_filter=category,
            n_results=n_results
        )
        
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching knowledge base: {str(e)}"
        )


@router.get("/knowledge/disease/{disease_name}")
async def get_disease_knowledge(disease_name: str):
    """Get all knowledge documents for a specific disease"""
    documents = knowledge_base.get_documents_by_disease(disease_name)
    
    if not documents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No knowledge found for disease: {disease_name}"
        )
    
    return {
        "disease": disease_name,
        "documents": documents,
        "count": len(documents)
    }


@router.post("/knowledge/add", status_code=status.HTTP_201_CREATED)
async def add_knowledge(
    payload: KnowledgeCreate
):
    """
    Add knowledge to knowledge base
    
    Example:
        ```json
        {
            "content": "Type 2 diabetes is a chronic condition...",
            "disease": "diabetes_type2",
            "category": "overview",
            "metadata": {"source": "medical_textbook", "page": 123}
        }
        ```
    """
    try:
        doc_id = knowledge_base.add_knowledge(
            content=payload.content,
            disease=payload.disease,
            category=payload.category,
            metadata=payload.metadata or {}
        )
        
        return {
            "success": True,
            "doc_id": doc_id,
            "message": "Knowledge added successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding knowledge: {str(e)}"
        )


@router.delete("/knowledge/{doc_id}")
async def delete_knowledge(doc_id: str):
    """Delete knowledge document by ID"""
    success = knowledge_base.delete_document(doc_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document not found: {doc_id}"
        )
    
    return {
        "success": True,
        "message": f"Document {doc_id} deleted"
    }


@router.get("/knowledge/categories")
async def get_knowledge_categories():
    """Get available knowledge categories"""
    return {
        "categories": [
            {"id": "symptoms", "name": "症状", "description": "疾病症状和体征"},
            {"id": "treatment", "name": "治疗", "description": "治疗方案和药物"},
            {"id": "prevention", "name": "预防", "description": "预防措施"},
            {"id": "lifestyle", "name": "生活方式", "description": "饮食、运动、生活习惯"},
            {"id": "complications", "name": "并发症", "description": "可能并发症"},
            {"id": "diagnosis", "name": "诊断", "description": "诊断方法和标准"},
            {"id": "comprehensive", "name": "综合", "description": "综合知识条目"},
            {"id": "general", "name": "一般信息", "description": "一般疾病信息"}
        ]
    }
