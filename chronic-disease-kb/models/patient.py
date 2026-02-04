"""
Patient data models
"""

from datetime import date, datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class PatientBase(BaseModel):
    """Base patient model"""
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=150)
    gender: Gender
    email: Optional[str] = None
    phone: Optional[str] = None


class PatientCreate(PatientBase):
    """Patient creation model"""
    chronic_conditions: List[str] = Field(default_factory=list)
    allergies: List[str] = Field(default_factory=list)
    current_medications: List[str] = Field(default_factory=list)
    emergency_contact: Optional[Dict[str, str]] = None


class PatientUpdate(BaseModel):
    """Patient update model"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)
    email: Optional[str] = None
    phone: Optional[str] = None
    chronic_conditions: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    current_medications: Optional[List[str]] = None


class PatientProfile(BaseModel):
    """Extended patient profile with health data"""
    patient_id: str
    risk_level: RiskLevel
    primary_conditions: List[str]
    last_checkup: Optional[datetime] = None
    compliance_score: float = Field(default=0.0, ge=0.0, le=100.0)
    health_trends: Dict[str, Any] = Field(default_factory=dict)
    notes: Optional[str] = None


class Patient(PatientBase):
    """Full patient model with ID"""
    id: str
    chronic_conditions: List[str] = Field(default_factory=list)
    allergies: List[str] = Field(default_factory=list)
    current_medications: List[str] = Field(default_factory=list)
    emergency_contact: Optional[Dict[str, str]] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    
    class Config:
        from_attributes = True
