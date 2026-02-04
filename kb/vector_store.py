"""
Vector database module using ChromaDB for knowledge base storage
"""

import os
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer

from config import settings


class VectorStore:
    """Vector database store for medical knowledge"""
    
    def __init__(self):
        self.client = None
        self.collection = None
        self.embedding_model = None
        self._initialize()
    
    def _initialize(self):
        """Initialize ChromaDB client and embedding model"""
        # Create directory if not exists
        os.makedirs(settings.VECTOR_DB_PATH, exist_ok=True)
        
        # Initialize ChromaDB
        self.client = chromadb.Client(
            ChromaSettings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=settings.VECTOR_DB_PATH
            )
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="medical_knowledge",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        Add documents to vector store
        
        Args:
            documents: List of text documents
            metadatas: Optional metadata for each document
            ids: Optional custom IDs
            
        Returns:
            List of document IDs
        """
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in documents]
        
        if metadatas is None:
            metadatas = [{} for _ in documents]
        
        # Add timestamps
        for metadata in metadatas:
            metadata["added_at"] = datetime.now().isoformat()
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(documents).tolist()
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        return ids
    
    def search(
        self,
        query: str,
        n_results: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search vector store for relevant documents
        
        Args:
            query: Search query
            n_results: Number of results to return
            filter_dict: Optional metadata filters
            
        Returns:
            List of results with content, metadata, and distance
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query]).tolist()
        
        # Search
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results,
            where=filter_dict
        )
        
        # Format results
        formatted_results = []
        if results['ids'] and results['ids'][0]:
            for i, doc_id in enumerate(results['ids'][0]):
                formatted_results.append({
                    'id': doc_id,
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i]
                })
        
        return formatted_results
    
    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific document by ID"""
        result = self.collection.get(ids=[doc_id])
        
        if result['ids']:
            return {
                'id': result['ids'][0],
                'content': result['documents'][0],
                'metadata': result['metadatas'][0]
            }
        return None
    
    def update_document(
        self,
        doc_id: str,
        document: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Update a document"""
        try:
            updates = {}
            
            if document:
                updates['documents'] = [document]
                updates['embeddings'] = self.embedding_model.encode([document]).tolist()
            
            if metadata:
                metadata['updated_at'] = datetime.now().isoformat()
                updates['metadatas'] = [metadata]
            
            if updates:
                self.collection.update(
                    ids=[doc_id],
                    **updates
                )
            return True
        except Exception as e:
            print(f"Error updating document: {e}")
            return False
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document"""
        try:
            self.collection.delete(ids=[doc_id])
            return True
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False
    
    def get_all_documents(
        self,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Get all documents with optional filtering"""
        results = self.collection.get(where=filter_dict)
        
        formatted_results = []
        for i, doc_id in enumerate(results['ids']):
            formatted_results.append({
                'id': doc_id,
                'content': results['documents'][i],
                'metadata': results['metadatas'][i]
            })
        
        return formatted_results
    
    def count(self, filter_dict: Optional[Dict[str, Any]] = None) -> int:
        """Count documents in collection"""
        return self.collection.count(where=filter_dict)
    
    def clear(self):
        """Clear all documents from collection"""
        self.client.delete_collection("medical_knowledge")
        self.collection = self.client.create_collection(
            name="medical_knowledge",
            metadata={"hnsw:space": "cosine"}
        )


# Global vector store instance
vector_store = VectorStore()