from pydantic import BaseModel, HttpUrl, Field
from typing import List, Dict, Any, Optional


class SourceConfig(BaseModel):
    source_type: str
    url: HttpUrl
    keywords: List[str]
    id: Optional[str] = None
    options: Optional[Dict[str, Any]] = Field(default_factory=dict)

    class Config:
        schema_extra = {
            "example": {
                "source_type": "reddit",
                "url": "https://www.reddit.com/r/artificial",
                "keywords": ["ai", "jobs", "future"],
                "id": "reddit_ai",
                "options": {
                    "subreddit_filter": "weekly"
                }
            }
        }


class CrawlRequest(BaseModel):
    sources: List[SourceConfig]
    task_name: str = "data_collection"

    class Config:
        schema_extra = {
            "example": {
                "sources": [
                    {
                        "source_type": "reddit",
                        "url": "https://www.reddit.com/r/artificial",
                        "keywords": ["ai", "jobs", "future"],
                        "id": "reddit_ai",
                        "options": {
                            "subreddit_filter": "weekly"
                        }
                    }
                ],
                "task_name": "data_collection"
            }
        }


class CrawlResponse(BaseModel):
    status: str
    task_name: str
    job_id: str
