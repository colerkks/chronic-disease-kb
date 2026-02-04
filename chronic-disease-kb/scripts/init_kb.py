"""
Script to initialize the knowledge base with sample data
"""

import sys
sys.path.insert(0, '.')

from kb.knowledge_base import knowledge_base
from data.sample_knowledge import create_disease_knowledge_objects


def init_knowledge_base():
    """Initialize knowledge base with sample medical data"""
    print("🚀 Initializing Knowledge Base...")
    
    # Get sample knowledge
    print("📚 Loading sample medical knowledge...")
    knowledge_objects = create_disease_knowledge_objects()
    
    print(f"Found {len(knowledge_objects)} disease knowledge documents")
    
    # Add to knowledge base
    added_count = 0
    for knowledge in knowledge_objects:
        try:
            doc_id = knowledge_base.add_disease_knowledge(knowledge)
            print(f"  ✓ Added: {knowledge.name} (ID: {doc_id})")
            added_count += 1
        except Exception as e:
            print(f"  ✗ Error adding {knowledge.name}: {e}")
    
    print(f"\n✅ Successfully added {added_count} documents")
    print(f"📊 Total documents in knowledge base: {knowledge_base.count_documents()}")
    
    # Test search
    print("\n🧪 Testing search functionality...")
    test_queries = [
        "糖尿病症状",
        "高血压饮食建议",
        "哮喘治疗"
    ]
    
    for query in test_queries:
        try:
            results = knowledge_base.search(query, n_results=2)
            print(f"\n  Query: '{query}'")
            print(f"  Found {len(results)} results")
            for i, result in enumerate(results[:1], 1):
                print(f"    {i}. {result['metadata'].get('disease', 'Unknown')} - Score: {1.0 - result['distance']:.3f}")
        except Exception as e:
            print(f"  ✗ Error testing '{query}': {e}")
    
    print("\n🎉 Knowledge base initialization complete!")


if __name__ == "__main__":
    init_knowledge_base()