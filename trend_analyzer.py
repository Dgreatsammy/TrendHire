# trendhire_api.py
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import asyncio
import logging
from datetime import datetime
import os

# Import the MCP integration
from mcp_integration import MCPClient, MCPSourceCrawler, SourceConfig, SourceType, AuthType

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("trendhire_api")

# Initialize FastAPI app
app = FastAPI(
    title="TrendHire API",
    description="Discover the future of hiring—before it happens.",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get API key from environment
API_KEY = os.getenv("BRIGHT_DATA_API_KEY")
if not API_KEY:
    logger.warning("BRIGHT_DATA_API_KEY not set in environment variables")

# Active background jobs
active_jobs = {}

# Models
class TrendHireTask(BaseModel):
    task_id: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    result_summary: Optional[Dict] = None

class CrawlRequest(BaseModel):
    sources: List[SourceConfig]
    task_name: Optional[str] = "data_collection"

class TrendAnalysisRequest(BaseModel):
    job_title: Optional[str] = None
    skills: Optional[List[str]] = None
    location: Optional[str] = None
    time_range: Optional[str] = "last_30_days"

# Dependency for MCP client
async def get_mcp_client():
    client = MCPClient(api_key=API_KEY)
    try:
        yield client
    finally:
        await client.client.aclose()

# Endpoints
@app.get("/")
async def root():
    return {"message": "Welcome to TrendHire API - Discover the future of hiring before it happens"}

@app.post("/crawl", response_model=TrendHireTask)
async def start_crawl(request: CrawlRequest, background_tasks: BackgroundTasks):
    """Start a crawling task to collect data from specified sources"""
    task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    active_jobs[task_id] = {
        "task_id": task_id,
        "status": "started",
        "created_at": datetime.now(),
        "completed_at": None,
        "result_summary": None
    }
    
    background_tasks.add_task(run_crawl_task, task_id, request.sources)
    
    return TrendHireTask(
        task_id=task_id,
        status="started",
        created_at=datetime.now()
    )

@app.get("/tasks/{task_id}", response_model=TrendHireTask)
async def get_task_status(task_id: str):
    """Get the status of a running or completed task"""
    if task_id not in active_jobs:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return TrendHireTask(**active_jobs[task_id])

@app.get("/trends/velocity", response_model=Dict)
async def get_trend_velocity(skill: Optional[str] = None, job_title: Optional[str] = None):
    """Get the velocity index for skills or job titles"""
    # Placeholder - would integrate with your trend analysis logic
    return {
        "trend_velocity": 0.85,
        "change_30d": "+15%",
        "source_breakdown": {
            "job_boards": 0.78,
            "reddit": 0.92,
            "tech_forums": 0.88,
            "learning_platforms": 0.81
        }
    }

@app.get("/skill-map")
async def get_skill_opportunity_map(current_skills: str):
    """Map existing skills to trending job opportunities"""
    skills_list = [s.strip() for s in current_skills.split(",")]
    
    # Placeholder - would integrate with your skill mapping logic
    return {
        "matching_roles": [
            {"title": "RAG Engineer", "match_score": 0.85, "missing_skills": ["LangChain", "Vector DBs"]},
            {"title": "AI Product Manager", "match_score": 0.72, "missing_skills": ["User Research", "Prompt Engineering"]}
        ],
        "skill_recommendations": [
            {"skill": "LangChain", "demand_score": 0.91, "learning_difficulty": "Medium"},
            {"skill": "Vector Databases", "demand_score": 0.89, "learning_difficulty": "Medium"}
        ]
    }

@app.post("/analyze/gap")
async def analyze_skill_gap(request: TrendAnalysisRequest):
    """Analyze gaps between job market needs and education content"""
    # Placeholder - would integrate with your gap analysis logic
    return {
        "market_needs_score": 0.92,
        "education_coverage_score": 0.67,
        "gap_score": 0.25,
        "recommendations": [
            "More courses needed on RAG implementation",
            "Additional content on multimodal LLMs required",
            "Practical projects in LLM fine-tuning underrepresented"
        ]
    }

# Background task function
async def run_crawl_task(task_id: str, sources: List[SourceConfig]):
    """Run the crawling task in the background"""
    try:
        mcp_client = MCPClient(api_key=API_KEY)
        crawler = MCPSourceCrawler(mcp_client)
        
        results = []
        for source_config in sources:
            result = await crawler.crawl_source(source_config)
            results.append(result)
        
        # Update task status
        active_jobs[task_id]["status"] = "completed"
        active_jobs[task_id]["completed_at"] = datetime.now()
        active_jobs[task_id]["result_summary"] = {
            "sources_processed": len(results),
            "successful_crawls": sum(1 for r in results if "error" not in r),
            "failed_crawls": sum(1 for r in results if "error" in r),
        }
        
        # Here you would typically store the results in a database
        # and trigger any analysis or processing jobs
        logger.info(f"Task {task_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Task {task_id} failed: {str(e)}")
        active_jobs[task_id]["status"] = "failed"
        active_jobs[task_id]["result_summary"] = {"error": str(e)}
    finally:
        await mcp_client.client.aclose()

# Main function to run the API with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("trendhire_api:app", host="0.0.0.0", port=8000, reload=True)
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class JobTrend(Base):
    __tablename__ = "job_trends"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    skills = Column(JSON)
    source = Column(String)
    timestamp = Column(DateTime)

import faiss
import numpy as np

def build_faiss_index(embeddings: list[np.ndarray]):
    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return index

def search_similar_skills(index, query_embedding, top_k=5):
    D, I = index.search(np.array([query_embedding]), top_k)
    return I

import requests

def analyze_skill_gap(profile_skills, market_skills):
    prompt = f"""
    A user knows these skills: {profile_skills}.
    Based on the market demand: {market_skills}.
    What skills should they learn next to stay ahead?
    """
    res = requests.post("http://localhost:11434/api/generate", json={
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    })
    return res.json()['response']

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.IndexFlatL2(384)  # Vector size for the above model
id_map = []

def add_to_index(text, id):
    vector = model.encode([text])
    index.add(np.array(vector).astype("float32"))
    id_map.append(id)

def search(query, top_k=5):
    vector = model.encode([query])
    D, I = index.search(np.array(vector).astype("float32"), top_k)
    return [id_map[i] for i in I[0]]
