"""
Knowledge Base Management Module
Handles CRUD operations, document chunking, and semantic search
"""

import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
import re
from pathlib import Path

from kb.vector_store import vector_store
from models.disease import DiseaseKnowledge
from config import settings


class DocumentChunker:
    """Split documents into chunks for vector storage"""
    
    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Input text
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        
        while start < len(text):
            # Find chunk end
            end = start + self.chunk_size
            
            if end >= len(text):
                # Last chunk
                chunks.append(text[start:])
                break
            
            # Try to break at sentence or word boundary
            chunk = text[start:end]
            
            # Look for sentence boundary
            sentence_match = re.search(r'[.!?。！？]\s*$', chunk)
            if sentence_match:
                end = start + sentence_match.end()
            else:
                # Look for word boundary
                last_space = chunk.rfind(' ')
                if last_space > self.chunk_size * 0.5:  # At least 50% of chunk size
                    end = start + last_space
            
            chunks.append(text[start:end])
            start = end - self.overlap
        
        return chunks


class KnowledgeBase:
    """
    Knowledge Base Management System
    
    Provides CRUD operations for medical knowledge documents,
    semantic search, and document management.
    """
    
    def __init__(self):
        self.vector_store = vector_store
        self.chunker = DocumentChunker(
            chunk_size=settings.CHUNK_SIZE,
            overlap=settings.CHUNK_OVERLAP
        )
        self._registered_source_ids: Optional[set[str]] = None

    REQUIRED_GOVERNANCE_METADATA_FIELDS = (
        "source_id",
        "document_version",
        "evidence_level",
    )

    SOURCE_REGISTRY_PATH = Path(__file__).resolve().parents[1] / "data" / "sources" / "source_registry.yaml"
    SOURCE_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")
    DOCUMENT_VERSION_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,31}$")
    SOURCE_ID_DECLARATION_PATTERN = re.compile(
        r"source_id:\s*\"?(?P<source_id>[a-z0-9][a-z0-9-]{1,63})\"?"
    )
    ALLOWED_EVIDENCE_LEVELS = {
        "GRADE_HIGH",
        "GRADE_MODERATE",
        "GRADE_LOW",
        "GUIDELINE_CONSENSUS",
        "EXPERT_OPINION",
    }
    FALLBACK_SOURCE_ID = "guideline-consensus-global"
    DEFAULT_SOURCE_IDS_BY_DISEASE = {
        "diabetes_type1": "ada-2026-soc",
        "diabetes_type2": "ada-2026-soc",
        "hypertension": "nice-ng136",
        "copd": "gold-2026-report",
        "asthma": "gina-2025-strategy",
    }

    def _get_registered_source_ids(self) -> set[str]:
        """Load and cache allowed source IDs from the registry file."""
        if self._registered_source_ids is not None:
            return self._registered_source_ids

        if not self.SOURCE_REGISTRY_PATH.exists():
            raise ValueError(
                f"Source registry not found: {self.SOURCE_REGISTRY_PATH}"
            )

        source_ids: set[str] = set()
        content = self.SOURCE_REGISTRY_PATH.read_text(encoding="utf-8")
        for line in content.splitlines():
            match = self.SOURCE_ID_DECLARATION_PATTERN.search(line)
            if match:
                source_ids.add(match.group("source_id"))

        if not source_ids:
            raise ValueError(
                f"No source_id entries found in registry: {self.SOURCE_REGISTRY_PATH}"
            )

        self._registered_source_ids = source_ids
        return source_ids

    def _validate_governance_metadata(self, metadata: Dict[str, Any]) -> None:
        """Validate required governance fields before writing knowledge."""
        missing = [
            field
            for field in self.REQUIRED_GOVERNANCE_METADATA_FIELDS
            if not metadata.get(field)
        ]
        if missing:
            raise ValueError(
                "Knowledge metadata missing required governance fields: "
                + ", ".join(missing)
            )

        source_id = str(metadata["source_id"]).strip().lower()
        document_version = str(metadata["document_version"]).strip()
        evidence_level = str(metadata["evidence_level"]).strip().upper()

        if not self.SOURCE_ID_PATTERN.fullmatch(source_id):
            raise ValueError(
                "Invalid source_id format. Expected lowercase slug like 'ada-2026-soc'"
            )

        if source_id not in self._get_registered_source_ids():
            raise ValueError(
                f"Unknown source_id '{source_id}'. Register it in {self.SOURCE_REGISTRY_PATH}"
            )

        if not self.DOCUMENT_VERSION_PATTERN.fullmatch(document_version):
            raise ValueError(
                "Invalid document_version format. Use alphanumeric version like '2026.1' or 'NG136'"
            )

        if evidence_level not in self.ALLOWED_EVIDENCE_LEVELS:
            allowed = ", ".join(sorted(self.ALLOWED_EVIDENCE_LEVELS))
            raise ValueError(
                f"Invalid evidence_level '{evidence_level}'. Allowed values: {allowed}"
            )

        metadata["source_id"] = source_id
        metadata["document_version"] = document_version
        metadata["evidence_level"] = evidence_level

    def add_knowledge(
        self,
        content: str,
        disease: str,
        category: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Add knowledge document to knowledge base
        
        Args:
            content: Document content
            disease: Disease name/ID
            category: Knowledge category (symptoms, treatment, etc.)
            metadata: Additional metadata
            
        Returns:
            Document ID
        """
        incoming_metadata = dict(metadata or {})
        self._validate_governance_metadata(incoming_metadata)

        doc_id = str(uuid.uuid4())
        
        doc_metadata = {
            'disease': disease,
            'category': category,
            'doc_id': doc_id,
            'created_at': datetime.now().isoformat()
        }

        doc_metadata.update(incoming_metadata)
        
        # Chunk document if it's too long
        if len(content) > settings.CHUNK_SIZE:
            chunks = self.chunker.chunk_text(content)
            chunk_metadatas = []
            
            for i, chunk in enumerate(chunks):
                chunk_meta = doc_metadata.copy()
                chunk_meta['chunk_index'] = str(i)
                chunk_meta['total_chunks'] = str(len(chunks))
                chunk_metadatas.append(chunk_meta)
            
            ids = self.vector_store.add_documents(
                documents=chunks,
                metadatas=chunk_metadatas,
                ids=[f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
            )
        else:
            ids = self.vector_store.add_documents(
                documents=[content],
                metadatas=[doc_metadata],
                ids=[doc_id]
            )
        
        return doc_id
    
    def add_disease_knowledge(self, knowledge: DiseaseKnowledge) -> str:
        """Add comprehensive disease knowledge"""
        if not knowledge.sources:
            raise ValueError("Disease knowledge must include at least one source")

        doc_id = str(uuid.uuid4())
        
        # Create structured content
        content_parts = [
            f"疾病: {knowledge.name}",
            f"分类: {knowledge.category}",
            f"概述: {knowledge.overview}",
        ]
        
        if knowledge.symptoms:
            content_parts.append(f"症状: {knowledge.symptoms}")
        
        if knowledge.causes:
            content_parts.append(f"病因: {', '.join(knowledge.causes)}")
        
        if knowledge.risk_factors:
            content_parts.append(f"风险因素: {knowledge.risk_factors}")

        if knowledge.diagnosis:
            content_parts.append(f"诊断: {knowledge.diagnosis}")
        
        if knowledge.treatments:
            content_parts.append(f"治疗: {knowledge.treatments}")
        
        if knowledge.complications:
            content_parts.append(f"并发症: {', '.join(knowledge.complications)}")
        
        if knowledge.prevention:
            content_parts.append(f"预防: {', '.join(knowledge.prevention)}")

        if knowledge.prognosis:
            content_parts.append(f"预后: {knowledge.prognosis}")
        
        content = "\n\n".join(content_parts)
        
        primary_source = knowledge.sources[0]
        source_year_match = re.search(r"(19|20)\d{2}", primary_source)
        source_year = source_year_match.group(0) if source_year_match else knowledge.last_updated.strftime("%Y")
        source_id = self.DEFAULT_SOURCE_IDS_BY_DISEASE.get(
            knowledge.disease_id,
            self.FALLBACK_SOURCE_ID,
        )

        metadata = {
            'disease_id': knowledge.disease_id,
            'disease_name': knowledge.name,
            'category': knowledge.category.value if hasattr(knowledge.category, 'value') else knowledge.category,
            'last_updated': knowledge.last_updated.isoformat(),
            'sources': knowledge.sources,
            'source_id': source_id,
            'document_version': source_year,
            'evidence_level': 'GUIDELINE_CONSENSUS'
        }
        
        return self.add_knowledge(
            content=content,
            disease=knowledge.name,
            category="comprehensive",
            metadata=metadata
        )
    
    def search(
        self,
        query: str,
        disease_filter: Optional[str] = None,
        category_filter: Optional[str] = None,
        n_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search knowledge base
        
        Args:
            query: Search query
            disease_filter: Filter by disease
            category_filter: Filter by category
            n_results: Number of results
            
        Returns:
            List of search results
        """
        # Build filter
        filter_dict = {}
        if disease_filter:
            filter_dict['disease'] = disease_filter
        if category_filter:
            filter_dict['category'] = category_filter
        
        results = self.vector_store.search(
            query=query,
            n_results=n_results,
            filter_dict=filter_dict if filter_dict else None
        )
        
        return results
    
    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get document by ID"""
        return self.vector_store.get_document(doc_id)
    
    def update_document(
        self,
        doc_id: str,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Update document"""
        return self.vector_store.update_document(doc_id, content, metadata)
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete document"""
        return self.vector_store.delete_document(doc_id)
    
    def get_documents_by_disease(
        self,
        disease: str
    ) -> List[Dict[str, Any]]:
        """Get all documents for a specific disease"""
        return self.vector_store.get_all_documents(
            filter_dict={'disease': disease}
        )
    
    def get_all_diseases(self) -> List[str]:
        """Get list of all diseases in knowledge base"""
        all_docs = self.vector_store.get_all_documents()
        diseases = set()
        
        for doc in all_docs:
            if 'disease' in doc['metadata']:
                diseases.add(doc['metadata']['disease'])
        
        return sorted(list(diseases))

    def get_metadata_summary(self) -> Dict[str, Dict[str, int]]:
        """Summarize document counts by disease and category"""
        all_docs = self.vector_store.get_all_documents()
        disease_counts: Dict[str, int] = {}
        category_counts: Dict[str, int] = {}

        for doc in all_docs:
            metadata = doc.get("metadata", {})
            disease = metadata.get("disease")
            category = metadata.get("category")

            if disease:
                disease_counts[disease] = disease_counts.get(disease, 0) + 1
            if category:
                category_counts[category] = category_counts.get(category, 0) + 1

        return {
            "diseases": dict(sorted(disease_counts.items())),
            "categories": dict(sorted(category_counts.items()))
        }
    
    def count_documents(self, disease: Optional[str] = None) -> int:
        """Count documents in knowledge base"""
        filter_dict = {'disease': disease} if disease else None
        return self.vector_store.count(filter_dict)
    
    def clear(self):
        """Clear all knowledge"""
        self.vector_store.clear()


# Global knowledge base instance
knowledge_base = KnowledgeBase()
