"""
Unit tests for chronic disease knowledge base
"""

import pytest
from datetime import datetime

# Test imports
from models.patient import Patient, PatientCreate, Gender
from models.disease import Disease, DiseaseCreate, DiseaseCategory
from models.query import QueryRequest, QueryResponse
from models.metric import HealthMetric, HealthMetricCreate, MetricType, MetricUnit


class TestPatientModels:
    """Test patient data models"""
    
    def test_patient_creation(self):
        """Test patient creation"""
        patient = Patient(
            id="patient_123",
            name="张三",
            age=55,
            gender=Gender.MALE,
            chronic_conditions=["diabetes_type2", "hypertension"],
            allergies=["penicillin"],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        assert patient.name == "张三"
        assert patient.age == 55
        assert len(patient.chronic_conditions) == 2
        assert patient.gender == Gender.MALE
    
    def test_patient_create_validation(self):
        """Test patient create model validation"""
        patient_data = {
            "name": "李四",
            "age": 45,
            "gender": "female",
            "email": "lisi@example.com",
            "chronic_conditions": ["asthma"]
        }
        
        patient = PatientCreate(**patient_data)
        assert patient.name == "李四"
        assert patient.age == 45


class TestDiseaseModels:
    """Test disease data models"""
    
    def test_disease_knowledge(self):
        """Test disease knowledge model"""
        disease = Disease(
            id="disease_001",
            name="2型糖尿病",
            category=DiseaseCategory.ENDOCRINE,
            description="一种慢性代谢性疾病",
            symptoms=["多尿", "口渴", "疲劳"],
            icd10_code="E11",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        assert disease.name == "2型糖尿病"
        assert disease.category == DiseaseCategory.ENDOCRINE
        assert len(disease.symptoms) == 3
    
    def test_disease_category_enum(self):
        """Test disease category enumeration"""
        assert DiseaseCategory.ENDOCRINE.value == "endocrine"
        assert DiseaseCategory.CARDIOVASCULAR.value == "cardiovascular"


class TestQueryModels:
    """Test query models"""
    
    def test_query_request(self):
        """Test query request model"""
        query = QueryRequest(
            query="2型糖尿病的早期症状是什么？",
            patient_id="patient_123",
            query_type="symptoms",
            max_results=5
        )
        
        assert query.query == "2型糖尿病的早期症状是什么？"
        assert query.patient_id == "patient_123"
        assert query.max_results == 5
    
    def test_query_response(self):
        """Test query response model"""
        response = QueryResponse(
            query_id="query_001",
            query="糖尿病症状",
            answer="常见症状包括多尿、口渴、疲劳等。",
            confidence=0.92,
            processing_time_ms=1500,
            timestamp=datetime.now()
        )
        
        assert response.confidence == 0.92
        assert response.answer is not None


class TestMetricModels:
    """Test health metric models"""
    
    def test_blood_pressure(self):
        """Test blood pressure model"""
        from models.metric import BloodPressure
        
        bp = BloodPressure(systolic=120, diastolic=80)
        assert bp.is_normal() == True
        assert bp.get_category() == "normal"
        
        bp_high = BloodPressure(systolic=150, diastolic=95)
        assert bp_high.is_normal() == False
        assert bp_high.get_category() == "stage1_hypertension"
    
    def test_blood_glucose(self):
        """Test blood glucose model"""
        from models.metric import BloodGlucose
        
        bg = BloodGlucose(value=95, context="fasting")
        assert bg.is_normal() == True
        assert bg.get_category() == "normal"
        
        bg_high = BloodGlucose(value=140, context="fasting")
        assert bg_high.is_normal() == False
        assert bg_high.get_category() == "diabetes"

        bg_post = BloodGlucose(value=160, context="postprandial")
        assert bg_post.get_category() == "prediabetes"

        bg_random = BloodGlucose(value=220, context="random")
        assert bg_random.get_category() == "diabetes"
    
    def test_health_metric(self):
        """Test health metric model"""
        metric = HealthMetric(
            id="metric_001",
            patient_id="patient_123",
            metric_type=MetricType.BLOOD_PRESSURE,
            value={"systolic": 120, "diastolic": 80},
            unit=MetricUnit.MMHG,
            timestamp=datetime.now(),
            is_abnormal=False,
            alert_generated=False,
            created_at=datetime.now()
        )
        
        assert metric.metric_type == MetricType.BLOOD_PRESSURE
        assert metric.is_abnormal == False


class TestConfiguration:
    """Test configuration"""
    
    def test_settings_exist(self):
        """Test settings are accessible"""
        from config import settings
        
        assert settings.API_VERSION is not None
        assert settings.DATABASE_URL is not None
        assert settings.EMBEDDING_MODEL is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
