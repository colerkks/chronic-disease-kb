"""
FastAPI main application
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from api.routes import knowledge, patients, query, recommendations, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("🚀 Starting Chronic Disease Knowledge Base API...")
    print(f"API Version: {settings.API_VERSION}")
    print(f"Debug Mode: {settings.DEBUG}")
    
    yield
    
    # Shutdown
    print("👋 Shutting down API...")


app = FastAPI(
    title="Chronic Disease Knowledge Base API",
    description="AI-powered knowledge base for chronic disease management",
    version=settings.API_VERSION,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(knowledge.router, prefix=settings.API_PREFIX, tags=["Knowledge Base"])
app.include_router(patients.router, prefix=settings.API_PREFIX, tags=["Patients"])
app.include_router(query.router, prefix=settings.API_PREFIX, tags=["Query"])
app.include_router(recommendations.router, prefix=settings.API_PREFIX, tags=["Recommendations"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Chronic Disease Knowledge Base API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "status": "running"
    }


@app.get("/api/v1")
async def api_root():
    """API root endpoint"""
    return {
        "version": settings.API_VERSION,
        "endpoints": {
            "knowledge": "/api/v1/knowledge",
            "patients": "/api/v1/patients",
            "query": "/api/v1/query",
            "recommendations": "/api/v1/recommendations"
        }
    }
