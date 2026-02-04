"""
Treatment and medication models
"""

from datetime import date, datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class TreatmentType(str, Enum):
    MEDICATION = "medication"
    LIFESTYLE = "lifestyle"
    PROCEDURE = "procedure"
    THERAPY = "therapy"
    SURGERY = "surgery"
    MONITORING = "monitoring"


class MedicationFrequency(str, Enum):
    ONCE_DAILY = "once_daily"
    TWICE_DAILY = "twice_daily"
    THREE_TIMES_DAILY = "three_times_daily"
    FOUR_TIMES_DAILY = "four_times_daily"
    AS_NEEDED = "as_needed"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class MedicationBase(BaseModel):
    """Base medication model"""
    name: str = Field(..., min_length=1, max_length=200)
    dosage: str
    frequency: MedicationFrequency
    route: str = Field(default="oral")  # oral, injection, topical, etc.


class MedicationCreate(MedicationBase):
    """Medication creation"""
    purpose: str
    side_effects: List[str] = Field(default_factory=list)
    contraindications: List[str] = Field(default_factory=list)
    drug_interactions: List[str] = Field(default_factory=list)
    special_instructions: Optional[str] = None


class Medication(MedicationBase):
    """Full medication model"""
    id: str
    purpose: str
    side_effects: List[str] = Field(default_factory=list)
    contraindications: List[str] = Field(default_factory=list)
    drug_interactions: List[str] = Field(default_factory=list)
    special_instructions: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class TreatmentBase(BaseModel):
    """Base treatment model"""
    name: str = Field(..., min_length=1, max_length=200)
    type: TreatmentType
    description: str
    target_conditions: List[str] = Field(default_factory=list)


class TreatmentCreate(TreatmentBase):
    """Treatment creation"""
    efficacy_rate: Optional[float] = Field(None, ge=0.0, le=100.0)
    duration_weeks: Optional[int] = None
    medications: List[MedicationCreate] = Field(default_factory=list)
    lifestyle_changes: List[str] = Field(default_factory=list)
    monitoring_requirements: List[str] = Field(default_factory=list)
    follow_up_frequency: Optional[str] = None


class Treatment(TreatmentBase):
    """Full treatment model"""
    id: str
    efficacy_rate: Optional[float] = None
    duration_weeks: Optional[int] = None
    medications: List[Medication] = Field(default_factory=list)
    lifestyle_changes: List[str] = Field(default_factory=list)
    monitoring_requirements: List[str] = Field(default_factory=list)
    follow_up_frequency: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TreatmentPlan(BaseModel):
    """Personalized treatment plan for patient"""
    plan_id: str
    patient_id: str
    disease_id: str
    treatments: List[Treatment] = Field(default_factory=list)
    start_date: date
    end_date: Optional[date] = None
    goals: List[str] = Field(default_factory=list)
    milestones: List[Dict[str, Any]] = Field(default_factory=list)
    status: str = "active"  # active, completed, discontinued, on_hold
    adherence_rate: float = Field(default=0.0, ge=0.0, le=100.0)
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
