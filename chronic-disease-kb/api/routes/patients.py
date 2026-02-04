"""
Patient management endpoints
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional, Dict, Any
from datetime import datetime

from models.patient import Patient, PatientCreate, PatientUpdate, PatientProfile
from models.metric import HealthMetric, HealthMetricCreate

router = APIRouter()

# In-memory storage for demo (replace with database in production)
patients_db = {}
metrics_db = {}


@router.post("/patients", response_model=Patient, status_code=status.HTTP_201_CREATED)
async def create_patient(patient: PatientCreate):
    """
    Create a new patient record
    
    Example:
        ```json
        {
            "name": "张三",
            "age": 55,
            "gender": "male",
            "email": "zhangsan@example.com",
            "chronic_conditions": ["diabetes_type2", "hypertension"],
            "allergies": ["penicillin"],
            "current_medications": ["metformin", "amlodipine"]
        }
        ```
    """
    import uuid
    
    patient_id = f"patient_{uuid.uuid4().hex[:8]}"
    
    new_patient = Patient(
        id=patient_id,
        name=patient.name,
        age=patient.age,
        gender=patient.gender,
        email=patient.email,
        phone=patient.phone,
        chronic_conditions=patient.chronic_conditions,
        allergies=patient.allergies,
        current_medications=patient.current_medications,
        emergency_contact=patient.emergency_contact,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    patients_db[patient_id] = new_patient
    
    return new_patient


@router.get("/patients", response_model=List[Patient])
async def list_patients(
    skip: int = 0,
    limit: int = 100,
    disease_filter: Optional[str] = None
):
    """List all patients with optional filtering"""
    patient_list = list(patients_db.values())
    
    if disease_filter:
        patient_list = [
            p for p in patient_list 
            if disease_filter in p.chronic_conditions
        ]
    
    return patient_list[skip:skip + limit]


@router.get("/patients/{patient_id}", response_model=Patient)
async def get_patient(patient_id: str):
    """Get patient by ID"""
    if patient_id not in patients_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient not found: {patient_id}"
        )
    
    return patients_db[patient_id]


@router.put("/patients/{patient_id}", response_model=Patient)
async def update_patient(patient_id: str, update: PatientUpdate):
    """Update patient information"""
    if patient_id not in patients_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient not found: {patient_id}"
        )
    
    patient = patients_db[patient_id]
    
    # Update fields
    if update.name:
        patient.name = update.name
    if update.age:
        patient.age = update.age
    if update.email:
        patient.email = update.email
    if update.phone:
        patient.phone = update.phone
    if update.chronic_conditions:
        patient.chronic_conditions = update.chronic_conditions
    if update.allergies:
        patient.allergies = update.allergies
    if update.current_medications:
        patient.current_medications = update.current_medications
    
    patient.updated_at = datetime.now()
    
    return patient


@router.delete("/patients/{patient_id}")
async def delete_patient(patient_id: str):
    """Delete patient record"""
    if patient_id not in patients_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient not found: {patient_id}"
        )
    
    del patients_db[patient_id]
    
    return {"success": True, "message": f"Patient {patient_id} deleted"}


@router.post("/patients/{patient_id}/metrics", status_code=status.HTTP_201_CREATED)
async def add_health_metric(patient_id: str, metric: HealthMetricCreate):
    """
    Add health metric for patient
    
    Example:
        ```json
        {
            "metric_type": "blood_pressure",
            "value": {"systolic": 120, "diastolic": 80},
            "unit": "mmHg",
            "timestamp": "2026-02-04T10:00:00",
            "notes": "Morning measurement"
        }
        ```
    """
    if patient_id not in patients_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient not found: {patient_id}"
        )
    
    import uuid
    
    metric_id = f"metric_{uuid.uuid4().hex[:8]}"
    
    # Create metric record
    new_metric = {
        "id": metric_id,
        "patient_id": patient_id,
        "metric_type": metric.metric_type,
        "value": metric.value,
        "unit": metric.unit,
        "timestamp": metric.timestamp,
        "device_id": metric.device_id,
        "notes": metric.notes,
        "context": metric.context,
        "created_at": datetime.now()
    }
    
    # Check if abnormal (simplified logic)
    is_abnormal = False
    if metric.metric_type.value == "blood_pressure":
        if metric.value.get("systolic", 0) > 140 or metric.value.get("diastolic", 0) > 90:
            is_abnormal = True
    elif metric.metric_type.value == "blood_glucose":
        if metric.value.get("value", 0) > 180:
            is_abnormal = True
    
    new_metric["is_abnormal"] = is_abnormal
    new_metric["alert_generated"] = is_abnormal
    
    if patient_id not in metrics_db:
        metrics_db[patient_id] = []
    
    metrics_db[patient_id].append(new_metric)
    
    return {
        "success": True,
        "metric_id": metric_id,
        "is_abnormal": is_abnormal,
        "message": "Health metric added successfully"
    }


@router.get("/patients/{patient_id}/metrics")
async def get_patient_metrics(
    patient_id: str,
    metric_type: Optional[str] = None,
    limit: int = 50
):
    """Get health metrics for patient"""
    if patient_id not in patients_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient not found: {patient_id}"
        )
    
    metrics = metrics_db.get(patient_id, [])
    
    if metric_type:
        metrics = [m for m in metrics if m["metric_type"] == metric_type]
    
    # Sort by timestamp descending
    metrics = sorted(metrics, key=lambda x: x["timestamp"], reverse=True)
    
    return {
        "patient_id": patient_id,
        "metrics": metrics[:limit],
        "count": len(metrics[:limit])
    }


@router.get("/patients/{patient_id}/profile")
async def get_patient_profile(patient_id: str):
    """Get comprehensive patient profile with health trends"""
    if patient_id not in patients_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient not found: {patient_id}"
        )
    
    patient = patients_db[patient_id]
    metrics = metrics_db.get(patient_id, [])
    
    # Calculate simple health trends
    recent_metrics = sorted(metrics, key=lambda x: x["timestamp"], reverse=True)[:10]
    abnormal_count = sum(1 for m in recent_metrics if m["is_abnormal"])
    
    risk_level = "low"
    if patient.chronic_conditions:
        if len(patient.chronic_conditions) > 2 or abnormal_count > 3:
            risk_level = "high"
        elif len(patient.chronic_conditions) > 0 or abnormal_count > 0:
            risk_level = "moderate"
    
    profile = {
        "patient_id": patient_id,
        "basic_info": {
            "name": patient.name,
            "age": patient.age,
            "gender": patient.gender
        },
        "medical_info": {
            "chronic_conditions": patient.chronic_conditions,
            "allergies": patient.allergies,
            "current_medications": patient.current_medications
        },
        "risk_level": risk_level,
        "recent_metrics_count": len(recent_metrics),
        "abnormal_metrics_count": abnormal_count,
        "last_updated": patient.updated_at.isoformat()
    }
    
    return profile