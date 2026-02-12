"""
Integration tests for knowledge base
"""

import pytest
import sys
sys.path.insert(0, '.')

from kb.knowledge_base import knowledge_base, DocumentChunker
from data.sample_knowledge import DIABETES_TYPE2_KNOWLEDGE, create_disease_knowledge_objects


class TestKnowledgeBase:
    """Test knowledge base operations"""
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Setup and teardown for each test"""
        # Note: In real tests, use a test database
        yield
        # Cleanup if needed
    
    def test_document_chunker(self):
        """Test document chunking"""
        chunker = DocumentChunker(chunk_size=100, overlap=20)
        
        long_text = "This is a test. " * 50  # Create long text
        chunks = chunker.chunk_text(long_text)
        
        assert len(chunks) > 1
        assert all(len(chunk) <= 100 + 20 for chunk in chunks)  # Allow for sentence boundaries
    
    def test_add_knowledge(self):
        """Test adding knowledge to knowledge base"""
        doc_id = knowledge_base.add_knowledge(
            content="Test medical knowledge about diabetes.",
            disease="diabetes_test",
            category="test",
            metadata={
                "source": "test",
                "source_id": "ada-2026-soc",
                "document_version": "2026.1",
                "evidence_level": "GRADE_LOW"
            }
        )
        
        assert doc_id is not None
        assert isinstance(doc_id, str)
    
    def test_search_knowledge(self):
        """Test searching knowledge base"""
        # First add some knowledge
        knowledge_base.add_knowledge(
            content="Diabetes type 2 symptoms include frequent urination and increased thirst.",
            disease="diabetes_type2",
            category="symptoms",
            metadata={
                "language": "en",
                "source_id": "ada-2026-soc",
                "document_version": "2026.1",
                "evidence_level": "GRADE_LOW"
            }
        )
        
        # Search
        results = knowledge_base.search(
            query="diabetes symptoms",
            n_results=3
        )
        
        assert isinstance(results, list)
        # May be empty if no documents match, which is OK for fresh database
    
    def test_get_all_diseases(self):
        """Test getting all diseases"""
        diseases = knowledge_base.get_all_diseases()
        assert isinstance(diseases, list)

    def test_metadata_summary(self):
        """Test metadata summary aggregation"""
        knowledge_base.add_knowledge(
            content="Sample content for summary aggregation.",
            disease="summary_test",
            category="diagnosis",
            metadata={
                "source": "unit_test",
                "source_id": "ada-2026-soc",
                "document_version": "2026.1",
                "evidence_level": "GRADE_LOW"
            }
        )

        summary = knowledge_base.get_metadata_summary()
        assert "diseases" in summary
        assert "categories" in summary
        assert summary["diseases"].get("summary_test", 0) >= 1
        assert summary["categories"].get("diagnosis", 0) >= 1

    def test_reject_missing_governance_metadata(self):
        """Knowledge write should fail when required governance metadata is missing"""
        with pytest.raises(ValueError, match="source_id"):
            knowledge_base.add_knowledge(
                content="Content missing governance metadata.",
                disease="governance_test",
                category="general",
                metadata={
                    "document_version": "2026.1",
                    "evidence_level": "GRADE_LOW"
                }
            )


class TestSampleData:
    """Test sample data loading"""
    
    def test_sample_knowledge_structure(self):
        """Test sample knowledge has correct structure"""
        assert len(DIABETES_TYPE2_KNOWLEDGE) > 0
        
        diabetes = DIABETES_TYPE2_KNOWLEDGE[0]
        assert "name" in diabetes
        assert "overview" in diabetes
        assert "symptoms" in diabetes

    def test_knowledge_objects_include_diagnosis_or_prognosis(self):
        """Ensure enriched knowledge objects retain diagnosis or prognosis data"""
        knowledge_objects = create_disease_knowledge_objects()
        assert len(knowledge_objects) > 0

        has_enriched = any(
            bool(knowledge.diagnosis) or bool(knowledge.prognosis)
            for knowledge in knowledge_objects
        )
        assert has_enriched


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
