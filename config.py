"""
Configuration module for chronic disease knowledge base
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API
    API_VERSION: str = "v1"
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "sqlite:///./data/chronic_disease.db"
    VECTOR_DB_PATH: str = "./data/vector_db"
    
    # Knowledge Base
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50
    TOP_K_RESULTS: int = 5
    
    # LLM Configuration
    # Priority order: OpenAI > Claude > Gemini > Local
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    DEFAULT_LLM_PROVIDER: str = "openai"
    DEFAULT_MODEL: str = "gpt-3.5-turbo"
    
    # Agent Configuration
    AGENT_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    ENABLE_MONITORING: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"
    
    # Supported Diseases
    SUPPORTED_DISEASES: List[str] = [
        "diabetes_type1",
        "diabetes_type2", 
        "hypertension",
        "heart_disease",
        "asthma",
        "copd",
        "arthritis_osteo",
        "arthritis_rheumatoid"
    ]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
