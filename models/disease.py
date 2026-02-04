"""
Disease and medical knowledge models
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class DiseaseCategory(str, Enum):
    ENDOCRINE = "endocrine"
    CARDIOVASCULAR = "cardiovascular"
    RESPIRATORY = "respiratory"
    MUSCULOSKELETAL = "musculoskeletal"
    NEUROLOGICAL = "neurological"
    GASTROINTESTINAL = "gastrointestinal"
    OTHER = "other"


class SeverityLevel(str, Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"


class DiseaseBase(BaseModel):
    """Base disease model"""
    name: str = Field(..., min_length=1, max_length=200)
    category: DiseaseCategory
    description: str
    icd10_code: Optional[str] = None


class DiseaseCreate(DiseaseBase):
    """Disease creation model"""
    symptoms: List[str] = Field(default_factory=list)
    risk_factors: List[str] = Field(default_factory=list)
    complications: List[str] = Field(default_factory=list)
    diagnostic_criteria: List[str] = Field(default_factory=list)
    treatment_guidelines: Optional[str] = None
    lifestyle_recommendations: List[str] = Field(default_factory=list)
    monitoring_params: List[str] = Field(default_factory=list)


class DiseaseKnowledge(BaseModel):
    """Comprehensive disease knowledge entry"""
    disease_id: str
    name: str
    category: DiseaseCategory
    overview: str
    symptoms: Dict[str, Any] = Field(default_factory=dict)  # categorized by severity
    causes: List[str] = Field(default_factory=list)
    risk_factors: Dict[str, Any] = Field(default_factory=dict)  # modifiable vs non-modifiable
    diagnosis: Dict[str, Any] = Field(default_factory=dict)  # tests, criteria
    treatments: Dict[str, Any] = Field(default_factory=dict)  # medications, procedures, lifestyle
    complications: List[str] = Field(default_factory=list)
    prevention: List[str] = Field(default_factory=list)
    prognosis: Optional[str] = None
    sources: List[str] = Field(default_factory=list)
    last_updated: datetime


class Disease(DiseaseBase):
    """Full disease model"""
    id: str
    symptoms: List[str] = Field(default_factory=list)
    risk_factors: List[str] = Field(default_factory=list)
    complications: List[str] = Field(default_factory=list)
    diagnostic_criteria: List[str] = Field(default_factory=list)
    treatment_guidelines: Optional[str] = None
    lifestyle_recommendations: List[str] = Field(default_factory=list)
    monitoring_params: List[str] = Field(default_factory=list)
    prevalence: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
