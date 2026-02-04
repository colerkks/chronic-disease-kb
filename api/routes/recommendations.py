"""
Recommendations endpoints
"""

from fastapi import APIRouter, HTTPException, status
from typing import List

from models.query import RecommendationRequest, RecommendationResponse
from agents.orchestrator import agent_orchestrator

router = APIRouter()


@router.post("/recommendations", response_model=RecommendationResponse, status_code=status.HTTP_200_OK)
async def get_recommendations(request: RecommendationRequest):
    """
    Get personalized health recommendations
    
    Provides evidence-based recommendations tailored to patient profile:
    - Lifestyle modifications
    - Medication adherence
    - Diet and exercise
    - Monitoring schedules
    
    Example:
        ```json
        {
            "patient_id": "patient_123",
            "recommendation_type": "lifestyle",
            "context": "newly_diagnosed_type2_diabetes",
            "constraints": ["vegetarian_diet", "limited_mobility"]
        }
        ```
    """
    try:
        # Get patient and metrics
        patient = None
        metrics = []
        
        if request.patient_id:
            # TODO: Load from database
            pass
        
        # Generate recommendations
        response = agent_orchestrator.get_recommendations(request, patient, metrics)
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating recommendations: {str(e)}"
        )


@router.get("/recommendations/types")
async def get_recommendation_types():
    """Get available recommendation types"""
    return {
        "types": [
            {
                "id": "lifestyle",
                "name": "生活方式建议",
                "description": "日常生活习惯改进建议"
            },
            {
                "id": "diet",
                "name": "饮食建议",
                "description": "个性化饮食计划"
            },
            {
                "id": "exercise",
                "name": "运动建议",
                "description": "适合的运动类型和强度"
            },
            {
                "id": "medication",
                "name": "用药建议",
                "description": "药物服用时间和注意事项"
            },
            {
                "id": "monitoring",
                "name": "监测建议",
                "description": "健康指标监测频率和方法"
            }
        ]
    }


@router.post("/recommendations/diet/{patient_id}")
async def get_diet_recommendations(patient_id: str, constraints: List[str] = []):
    """Get diet recommendations for specific patient"""
    request = RecommendationRequest(
        patient_id=patient_id,
        recommendation_type="diet",
        constraints=constraints or []
    )
    return await get_recommendations(request)


@router.post("/recommendations/exercise/{patient_id}")
async def get_exercise_recommendations(patient_id: str, constraints: List[str] = []):
    """Get exercise recommendations for specific patient"""
    request = RecommendationRequest(
        patient_id=patient_id,
        recommendation_type="exercise",
        constraints=constraints or []
    )
    return await get_recommendations(request)
