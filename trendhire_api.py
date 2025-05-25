from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import os
import logging
from functools import lru_cache
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse

# Configure logging to prevent sensitive data exposure
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Create a settings management class
class Settings:
    def __init__(self):
        # Critical credentials - never log these values
        self.bright_data_username = os.getenv("BRIGHT_DATA_USERNAME")
        self.bright_data_password = os.getenv("BRIGHT_DATA_PASSWORD")
        self.bright_data_host = os.getenv("BRIGHT_DATA_HOST")
        self.bright_data_port = os.getenv("BRIGHT_DATA_PORT")
        self.bright_data_api_key = os.getenv("BRIGHT_DATA_API_KEY")
        self.sentry_dsn = os.getenv("SENTRY_DSN")  
        self.database_url = os.getenv("DATABASE_URL")

        # Validate critical environment variables
        self._validate_config()

    def _validate_config(self):
        """Validate that all required configuration variables are set."""
        missing_vars = []
        for var_name in [
            "BRIGHT_DATA_USERNAME", 
            "BRIGHT_DATA_PASSWORD",
            "BRIGHT_DATA_HOST", 
            "BRIGHT_DATA_PORT",
            "BRIGHT_DATA_API_KEY",
            "DATABASE_URL"
        ]:
            if not os.getenv(var_name):
                missing_vars.append(var_name)
        
        if missing_vars:
            # Log missing vars without including their values
            logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        logger.info("✅ Configuration validated successfully")

    def get_db_connection_params(self):
        """
        Returns database connection parameters without exposing the full URL
        This method parses the DATABASE_URL and returns components safely
        """
        # This is a safer way to provide DB info without exposing credentials
        try:
            # Simplified representation. In a real app, you'd parse the actual connection URL
            db_parts = self.database_url.split('@')[1].split('/')
            host = db_parts[0].split(':')[0]
            db_name = db_parts[1].split('?')[0]
            return {"host": host, "db_name": db_name}
        except Exception:
            return {"host": "configured", "db_name": "configured"}

@lru_cache()
def get_settings():
    """
    Creates and returns a cached Settings object to avoid 
    reading environment variables for every request
    """
    return Settings()

# Import from mcp_integration with better error handling
try:
    from mcp_integration import SourceConfig
    logger.info("✅ Successfully imported SourceConfig from mcp_integration")
except ImportError as e:
    logger.error(f"Failed to import SourceConfig: {str(e)}")
    # Define a fallback SourceConfig if the import fails
    class SourceConfig:
        def __init__(self, source_type, **kwargs):
            self.source_type = source_type
            for key, value in kwargs.items():
                setattr(self, key, value)

# Create a Pydantic model for the API
class PydanticSourceConfig(BaseModel):
    source_type: str
    url: Optional[str] = None
    keywords: Optional[List[str]] = None
    options: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_source_config(cls, source_config: SourceConfig):
        return cls(
            source_type=source_config.source_type,
            url=getattr(source_config, 'url', None),
            keywords=getattr(source_config, 'keywords', None),
            options=getattr(source_config, 'options', None),
        )

class CrawlRequest(BaseModel):
    sources: List[PydanticSourceConfig]
    task_name: Optional[str] = "data_collection"

class CrawlResponse(BaseModel):
    status: str
    task_name: str
    job_id: str = Field(..., description="Unique identifier for the crawl job")

# Initialize FastAPI
app = FastAPI(
    title="TrendHire API",
    description="API for TrendHire data collection and management",
    version="1.0.0"
)

# Create dependency for credentials
def get_credentials(settings: Settings = Depends(get_settings)):
    """
    Return credentials in a structured way for services that need them.
    This prevents credentials from being passed around as separate variables.
    """
    return {
        "bright_data": {
            "username": settings.bright_data_username,
            "password": settings.bright_data_password,
            "host": settings.bright_data_host,
            "port": settings.bright_data_port,
            "api_key": settings.bright_data_api_key
        }
    }

# Startup event handler to validate configuration
@app.on_event("startup")
async def startup_event():
    logger.info("Starting TrendHire API")
    # Validate settings on startup
    settings = get_settings()
    
    # Log non-sensitive configuration info
    db_info = settings.get_db_connection_params()
    logger.info(f"Connected to database: {db_info['db_name']} on {db_info['host']}")
    
    # Log that credentials are configured, but don't log the values
    if settings.bright_data_api_key:
        logger.info("✅ Bright Data API key is configured")
    
    if settings.sentry_dsn:
        logger.info("✅ Sentry monitoring is configured")
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.post("/crawl", response_model=CrawlResponse)
async def start_crawl(
    request: CrawlRequest,
    credentials: dict = Depends(get_credentials)
):
    """
    Start a new crawl job based on the specified sources and configurations.
    """
    try:
        # Convert PydanticSourceConfig objects back to SourceConfig objects
        source_configs = []
        for src in request.sources:
            source_config = SourceConfig(
                source_type=src.source_type,
                url=src.url,
                keywords=src.keywords,
                options=src.options
            )
            source_configs.append(source_config)
        
        # Log operations without sensitive data
        logger.info(f"Starting crawl job with {len(source_configs)} sources")
        
        # Your existing crawl job logic here
        # Instead of this:
        # print(f"DEBUG API KEY: {credentials['bright_data']['api_key']}")
        # You would do something like:
        # crawler.start_job(source_configs, credentials)
        
        # Generate a job ID (in a real app, you'd get this from your job system)
        import uuid
        job_id = str(uuid.uuid4())
        
        return {
            "status": "Crawl job submitted successfully",
            "task_name": request.task_name,
            "job_id": job_id
        }
    
    except Exception as e:
        logger.error(f"Error starting crawl job: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to start crawl job: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Simple health check endpoint that returns the status of the API
    """
    return {"status": "healthy"}

# Add your other API endpoints here