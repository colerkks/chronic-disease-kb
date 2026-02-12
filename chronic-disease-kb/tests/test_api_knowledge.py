"""
API tests for knowledge governance validation.
"""

from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_add_knowledge_missing_source_id_returns_400():
    """Missing source_id should be rejected by governance validation."""
    payload = {
        "content": "Test knowledge content.",
        "disease": "diabetes_type2",
        "category": "overview",
        "metadata": {
            "document_version": "2026.1",
            "evidence_level": "GRADE_LOW",
        },
    }

    response = client.post("/api/v1/knowledge/add", json=payload)

    assert response.status_code == 400
    assert "source_id" in response.json().get("detail", "")


def test_add_knowledge_unknown_source_id_returns_400():
    """Unknown source_id should be rejected unless present in source registry."""
    payload = {
        "content": "Test knowledge content.",
        "disease": "diabetes_type2",
        "category": "overview",
        "metadata": {
            "source_id": "unknown-source-id",
            "document_version": "2026.1",
            "evidence_level": "GRADE_LOW",
        },
    }

    response = client.post("/api/v1/knowledge/add", json=payload)

    assert response.status_code == 400
    assert "Unknown source_id" in response.json().get("detail", "")


def test_add_knowledge_invalid_evidence_level_returns_400():
    """Invalid evidence level should return a client error."""
    payload = {
        "content": "Test knowledge content.",
        "disease": "diabetes_type2",
        "category": "overview",
        "metadata": {
            "source_id": "ada-2026-soc",
            "document_version": "2026.1",
            "evidence_level": "UNKNOWN_LEVEL",
        },
    }

    response = client.post("/api/v1/knowledge/add", json=payload)

    assert response.status_code == 400
    assert "Invalid evidence_level" in response.json().get("detail", "")
