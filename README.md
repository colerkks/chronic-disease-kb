# Chronic Disease Management Knowledge Base

> 中文版文档请见：[README.zh-CN.md](README.zh-CN.md)。

An AI-powered knowledge base system for chronic disease management with intelligent agents.

## 🌟 Features

- **Comprehensive Knowledge Base**: Covers diabetes, hypertension, heart disease, asthma, COPD, and arthritis
- **AI Agents**: Query understanding, knowledge retrieval, personalized recommendations
- **Vector Search**: RAG-based medical document retrieval
- **Patient Management**: Track health metrics and treatment plans
- **RESTful API**: Complete API for integration

## 🏗️ Architecture

```
chronic_disease_kb/
├── agents/          # AI Agent implementations
├── api/             # FastAPI REST endpoints
├── core/            # Core business logic
├── db/              # Database models and connections
├── kb/              # Knowledge base management
├── models/          # Pydantic data models
└── config.py        # Configuration
```

## 🚀 Quick Start

### Installation

```bash
# Clone and setup
cd chronic_disease_kb
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Initialize database
python scripts/init_db.py

# Start the server
python -m uvicorn api.main:app --reload
```

### API Usage

```python
# Query the knowledge base
POST /api/v1/query
{
  "query": "What are the symptoms of type 2 diabetes?",
  "patient_id": "patient_123"
}

# Add health metric
POST /api/v1/patients/{id}/metrics
{
  "metric_type": "blood_pressure",
  "value": {"systolic": 120, "diastolic": 80},
  "timestamp": "2026-02-04T10:00:00"
}
```

## 📚 Knowledge Base

The system includes structured medical knowledge for:
- **Diabetes**: Type 1, Type 2, gestational, prediabetes
- **Hypertension**: Primary, secondary, hypertensive crisis
- **Heart Disease**: CAD, heart failure, arrhythmias
- **Respiratory**: Asthma, COPD
- **Musculoskeletal**: Arthritis (osteoarthritis, rheumatoid)

## 🤖 Agents

- **QueryAgent**: Understands natural language health queries
- **RetrievalAgent**: Searches knowledge base with semantic search
- **RecommendationAgent**: Provides personalized health recommendations
- **MonitoringAgent**: Tracks and analyzes patient health trends

## 🛠️ Tech Stack

- **Python 3.9+**
- **FastAPI**: Web framework
- **ChromaDB**: Vector database
- **SQLAlchemy**: ORM for relational data
- **Sentence-Transformers**: Embeddings
- **Pydantic**: Data validation

## 📄 License

MIT License
