"""
Master Control Program (MCP) Integration for TrendHire
This module provides integration with Bright Data proxy services for web scraping operations.
"""

import os
import logging
import aiohttp
import asyncio
import requests
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_integration")

class SourceConfig:
    """Configuration for a specific data source to crawl"""
    def __init__(self, 
                 name: str, 
                 base_url: str, 
                 search_url_template: str,
                 listing_selector: str,
                 detail_selectors: Dict[str, str] = None,
                 headers: Dict[str, str] = None):
        self.name = name
        self.base_url = base_url
        self.search_url_template = search_url_template
        self.listing_selector = listing_selector
        self.detail_selectors = detail_selectors or {}
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    def get_search_url(self, query: str, location: str = None, page: int = 1) -> str:
        """Generate search URL based on template and parameters"""
        url = self.search_url_template
        url = url.replace("{query}", query)
        if location and "{location}" in url:
            url = url.replace("{location}", location)
        if "{page}" in url:
            url = url.replace("{page}", str(page))
        
        # Ensure the URL is properly joined if it's a relative path
        if not url.startswith("http"):
            url = urljoin(self.base_url, url)
            
        return url


class MCPClient:
    """
    Master Control Program Client for managing web scraping operations
    through Bright Data proxy services.
    """
    
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 host: Optional[str] = None,
                 port: Optional[int] = None):
        """
        Initialize the MCP Client with Bright Data credentials
        
        Args:
            api_key: Bright Data API key
            username: Bright Data username
            password: Bright Data password
            host: Bright Data proxy host
            port: Bright Data proxy port
        """
        # Load credentials from environment variables if not provided
        self.api_key = api_key or os.environ.get("BRIGHT_DATA_API_KEY")
        self.username = username or os.environ.get("BRIGHT_DATA_USERNAME")
        self.password = password or os.environ.get("BRIGHT_DATA_PASSWORD")
        self.host = host or os.environ.get("BRIGHT_DATA_HOST", "brd.superproxy.io")
        self.port = port or int(os.environ.get("BRIGHT_DATA_PORT", "33335"))
        
        if not all([self.api_key, self.username, self.password, self.host, self.port]):
            raise ValueError("Missing required Bright Data credentials")
        
        logger.info("✅ Bright Data credentials loaded successfully.")
        
        # Configure proxy settings for requests
        self.proxy_url = f"http://{self.username}:{self.password}@{self.host}:{self.port}"
        self.proxies = {
            "http": self.proxy_url,
            "https": self.proxy_url
        }
        
        # Session for making API requests
        self.session = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
            self.session = None
    
    def fetch(self, url: str, headers: Dict[str, str] = None) -> requests.Response:
        """
        Fetch content from a URL using Bright Data proxy
        
        Args:
            url: The URL to fetch
            headers: Optional request headers
            
        Returns:
            requests.Response object
        """
        try:
            response = requests.get(
                url,
                headers=headers,
                proxies=self.proxies,
                timeout=30
            )
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            raise
    
    async def fetch_async(self, url: str, headers: Dict[str, str] = None) -> str:
        """
        Asynchronously fetch content from a URL using Bright Data proxy
        
        Args:
            url: The URL to fetch
            headers: Optional request headers
            
        Returns:
            Response content as text
        """
        if not self.session:
            raise RuntimeError("Session not initialized. Use as async context manager.")
            
        proxy_auth = aiohttp.BasicAuth(self.username, self.password)
        
        try:
            async with self.session.get(
                url,
                headers=headers,
                proxy=f"http://{self.host}:{self.port}",
                proxy_auth=proxy_auth,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                response.raise_for_status()
                return await response.text()
        except aiohttp.ClientError as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            raise
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get Bright Data account information
        
        Returns:
            Dict containing account information
        """
        url = f"https://api.brightdata.com/accounts/me"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching account info: {str(e)}")
            raise


class MCPSourceCrawler:
    """
    Crawler for specific data sources using the MCP client
    """
    
    def __init__(self, client: MCPClient, source_config: SourceConfig):
        """
        Initialize the crawler with MCP client and source configuration
        
        Args:
            client: Initialized MCPClient
            source_config: Configuration for the data source
        """
        self.client = client
        self.config = source_config
    
    def search(self, query: str, location: str = None, max_pages: int = 1) -> List[Dict[str, Any]]:
        """
        Search the data source for listings
        
        Args:
            query: Search query term
            location: Optional location filter
            max_pages: Maximum number of pages to crawl
            
        Returns:
            List of listing details
        """
        results = []
        
        for page in range(1, max_pages + 1):
            try:
                # Generate search URL for this page
                url = self.config.get_search_url(query, location, page)
                
                # Fetch search results
                logger.info(f"Fetching page {page} from {self.config.name}: {url}")
                response = self.client.fetch(url, headers=self.config.headers)
                
                # Process results (this is a placeholder - you would typically use BeautifulSoup or similar here)
                # For a real implementation, you'd parse the HTML and extract data based on the selectors
                logger.info(f"Successfully retrieved page {page}")
                
                # Example placeholder for results processing
                # In a real implementation, you would extract data based on self.config.listing_selector
                # and self.config.detail_selectors
                sample_result = {
                    "source": self.config.name,
                    "url": url,
                    "page": page,
                    "query": query,
                    "location": location,
                    "results_count": 0  # This would be populated with actual results count
                }
                results.append(sample_result)
                
            except Exception as e:
                logger.error(f"Error searching {self.config.name}: {str(e)}")
                break
                
        return results
    
    async def search_async(self, query: str, location: str = None, max_pages: int = 1) -> List[Dict[str, Any]]:
        """
        Asynchronously search the data source for listings
        
        Args:
            query: Search query term
            location: Optional location filter
            max_pages: Maximum number of pages to crawl
            
        Returns:
            List of listing details
        """
        results = []
        tasks = []
        
        # Create tasks for all pages
        for page in range(1, max_pages + 1):
            url = self.config.get_search_url(query, location, page)
            task = asyncio.create_task(self._fetch_page(url, page, query, location))
            tasks.append(task)
        
        # Wait for all tasks to complete
        completed_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for result in completed_results:
            if isinstance(result, Exception):
                logger.error(f"Error in async search: {str(result)}")
            else:
                results.extend(result)
                
        return results
    
    async def _fetch_page(self, url: str, page: int, query: str, location: str) -> List[Dict[str, Any]]:
        """
        Fetch and process a single page of results
        
        Args:
            url: The URL to fetch
            page: Page number
            query: Search query
            location: Location filter
            
        Returns:
            List of listings from this page
        """
        try:
            logger.info(f"Fetching page {page} from {self.config.name}: {url}")
            content = await self.client.fetch_async(url, headers=self.config.headers)
            
            # Process results (placeholder)
            # In a real implementation, you would parse the HTML and extract data
            sample_result = {
                "source": self.config.name,
                "url": url,
                "page": page,
                "query": query,
                "location": location,
                "results_count": 0  # This would be populated with actual results
            }
            
            return [sample_result]
            
        except Exception as e:
            logger.error(f"Error fetching page {page} from {self.config.name}: {str(e)}")
            raise
