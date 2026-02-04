"""
Query and response models for knowledge base interactions
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """User query request"""
    query: str = Field(..., min_length=1, description="User's natural language query")
    patient_id: Optional[str] = Field(None, description="Optional patient context")
    disease_filter: Optional[List[str]] = Field(None, description="Filter by specific diseases")
    query_type: Optional[str] = Field(None, description="Type: symptoms, treatment, general, emergency")
    language: str = Field(default="zh", description="Query language")
    max_results: int = Field(default=5, ge=1, le=20)
    include_sources: bool = Field(default=True)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "2型糖尿病的早期症状是什么？",
                "patient_id": "patient_123",
                "query_type": "symptoms",
                "language": "zh"
            }
        }


class KnowledgeResult(BaseModel):
    """Single knowledge base result"""
    content: str
    source: str
    disease: Optional[str] = None
    category: Optional[str] = None
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class QueryResponse(BaseModel):
    """Knowledge base query response"""
    query_id: str
    query: str
    answer: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    results: List[KnowledgeResult] = Field(default_factory=list)
    sources: List[str] = Field(default_factory=list)
    related_questions: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    processing_time_ms: int
    timestamp: datetime
    patient_context_applied: bool = False
    
    class Config:
        json_schema_extra = {
            "example": {
                "query_id": "query_456",
                "query": "2型糖尿病的早期症状是什么？",
                "answer": "2型糖尿病的早期症状包括...",
                "confidence": 0.92,
                "results": [],
                "timestamp": "2026-02-04T10:30:00"
            }
        }


class RecommendationRequest(BaseModel):
    """Request for personalized recommendations"""
    patient_id: str
    recommendation_type: str = Field(..., description="lifestyle, medication, diet, exercise")
    context: Optional[str] = None
    constraints: List[str] = Field(default_factory=list)


class RecommendationResponse(BaseModel):
    """Personalized recommendation response"""
    patient_id: str
    recommendations: List[Dict[str, Any]] = Field(default_factory=list)
    priority_level: str
    rationale: str
    cautions: List[str] = Field(default_factory=list)
    timestamp: datetime


class ChatMessage(BaseModel):
    """Chat message for conversational interface"""
    role: str  # user, assistant, system
    content: str
    timestamp: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ChatSession(BaseModel):
    """Chat session model"""
    session_id: str
    patient_id: Optional[str] = None
    messages: List[ChatMessage] = Field(default_factory=list)
    created_at: datetime
    last_updated: datetime
    context: Dict[str, Any] = Field(default_factory=dict)
