"""
Health metrics and monitoring models
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum
from pydantic import BaseModel, Field


class MetricType(str, Enum):
    """Types of health metrics"""
    BLOOD_PRESSURE = "blood_pressure"
    BLOOD_GLUCOSE = "blood_glucose"
    WEIGHT = "weight"
    HEIGHT = "height"
    BMI = "bmi"
    HEART_RATE = "heart_rate"
    OXYGEN_SATURATION = "oxygen_saturation"
    TEMPERATURE = "temperature"
    HBA1C = "hba1c"
    CHOLESTEROL = "cholesterol"
    STEPS = "steps"
    SLEEP = "sleep"
    MEDICATION_ADHERENCE = "medication_adherence"
    CUSTOM = "custom"


class MetricUnit(str, Enum):
    """Units for health metrics"""
    MMHG = "mmHg"
    MG_DL = "mg/dL"
    MMOL_L = "mmol/L"
    KG = "kg"
    CM = "cm"
    BMI_UNIT = "kg/m2"
    BPM = "bpm"
    PERCENT = "%"
    CELSIUS = "°C"
    MG = "mg"
    STEPS = "steps"
    HOURS = "hours"


class BloodPressure(BaseModel):
    """Blood pressure measurement"""
    systolic: int = Field(..., ge=0, le=300)
    diastolic: int = Field(..., ge=0, le=200)
    unit: str = "mmHg"
    
    def is_normal(self) -> bool:
        return 90 <= self.systolic <= 120 and 60 <= self.diastolic <= 80
    
    def get_category(self) -> str:
        if self.systolic < 90 or self.diastolic < 60:
            return "hypotension"
        elif self.systolic <= 120 and self.diastolic <= 80:
            return "normal"
        elif self.systolic <= 129 and self.diastolic <= 84:
            return "elevated"
        elif self.systolic <= 139 or self.diastolic <= 89:
            return "stage1_hypertension"
        else:
            return "stage2_hypertension"


class BloodGlucose(BaseModel):
    """Blood glucose measurement"""
    value: float = Field(..., ge=0, le=1000)
    unit: str = "mg/dL"
    context: str = Field(default="random")  # fasting, postprandial, random
    
    def is_normal(self) -> bool:
        if self.context == "fasting":
            return 70 <= self.value <= 100
        elif self.context == "postprandial":
            return self.value <= 140
        return 70 <= self.value <= 140
    
    def get_category(self) -> str:
        if self.context == "fasting":
            if self.value < 70:
                return "hypoglycemia"
            elif self.value <= 100:
                return "normal"
            elif self.value <= 125:
                return "prediabetes"
            else:
                return "diabetes"
        return "unknown"


class HealthMetricBase(BaseModel):
    """Base health metric"""
    metric_type: MetricType
    value: Dict[str, Any]
    unit: MetricUnit
    timestamp: datetime


class HealthMetricCreate(HealthMetricBase):
    """Health metric creation"""
    device_id: Optional[str] = None
    notes: Optional[str] = None
    context: Optional[str] = None  # e.g., "morning", "before_meal", "after_exercise"


class HealthMetric(HealthMetricBase):
    """Full health metric model"""
    id: str
    patient_id: str
    device_id: Optional[str] = None
    notes: Optional[str] = None
    context: Optional[str] = None
    is_abnormal: bool = False
    alert_generated: bool = False
    created_at: datetime
    
    class Config:
        from_attributes = True


class MetricTrend(BaseModel):
    """Trend analysis for health metrics"""
    metric_type: MetricType
    period_start: datetime
    period_end: datetime
    data_points: int
    average_value: float
    min_value: float
    max_value: float
    trend_direction: str  # improving, stable, worsening, fluctuating
    trend_percentage: float
    alerts_count: int
    recommendations: List[str] = Field(default_factory=list)
