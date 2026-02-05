"""
Knowledge base request/response models
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class KnowledgeCreate(BaseModel):
    """Payload for adding a knowledge document"""
    content: str = Field(..., min_length=1)
    disease: str = Field(..., min_length=1)
    category: str = Field(default="general", min_length=1)
    metadata: Optional[Dict[str, Any]] = None
