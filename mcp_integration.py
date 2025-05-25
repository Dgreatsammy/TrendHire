import os
import logging
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Logger setup
logger = logging.getLogger("mcp_integration")
logging.basicConfig(level=logging.INFO)

# Bright Data Web Unlocker credentials
BRIGHT_DATA_USERNAME = os.getenv("BRIGHT_DATA_USERNAME")
BRIGHT_DATA_PASSWORD = os.getenv("BRIGHT_DATA_PASSWORD")
BRIGHT_DATA_HOST = os.getenv("BRIGHT_DATA_HOST", "brd.superproxy.io")
BRIGHT_DATA_PORT = int(os.getenv("BRIGHT_DATA_PORT", "33335"))

if not all([BRIGHT_DATA_USERNAME, BRIGHT_DATA_PASSWORD]):
    logger.warning("⚠️ Bright Data credentials are missing. Please check your .env file.")
else:
    logger.info("✅ Bright Data credentials loaded successfully.")

def make_request_with_proxy(target_url: str, headers=None, timeout=30) -> str:
    """
    Makes an HTTP GET request to the target URL using Bright Data's Web Unlocker proxy.
    """
    proxy_url = f"http://{BRIGHT_DATA_USERNAME}:{BRIGHT_DATA_PASSWORD}@{BRIGHT_DATA_HOST}:{BRIGHT_DATA_PORT}"
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }

    try:
        response = requests.get(target_url, headers=headers, proxies=proxies, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise

# Example usage (you can remove or comment out this block in production)
if __name__ == "__main__":
    test_url = "https://httpbin.org/ip"
    try:
        result = make_request_with_proxy(test_url)
        print("🔍 Proxy test result:", result)
    except Exception as e:
        print("❌ Proxy request failed:", e)

class SourceConfig:
    """Configuration for a specific data source to crawl"""
    def __init__(self, 
                 name: str, 
                 base_url: str, 
                 search_url_template: str,
                 listing_selector: str,
                 detail_selectors: dict = None,
                 headers: dict = None):
        self.name = name
        self.base_url = base_url
        self.search_url_template = search_url_template
        self.listing_selector = listing_selector
        self.detail_selectors = detail_selectors or {}
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }


class MCPClient:
    """Client for web scraping operations through Bright Data proxy"""
    def __init__(self, api_key=None, username=None, password=None, host=None, port=None):
        """Initialize with credentials (will use environment variables if not provided)"""
        import os
        
        # Use provided values or get from environment
        self.api_key = api_key or os.environ.get("BRIGHT_DATA_API_KEY")
        self.username = username or os.environ.get("BRIGHT_DATA_USERNAME")
        self.password = password or os.environ.get("BRIGHT_DATA_PASSWORD")
        self.host = host or os.environ.get("BRIGHT_DATA_HOST", "brd.superproxy.io")
        self.port = port or int(os.environ.get("BRIGHT_DATA_PORT", "33335"))
        
        # Set up proxy configuration
        self.proxy_url = f"http://{self.username}:{self.password}@{self.host}:{self.port}"
        self.proxies = {
            "http": self.proxy_url,
            "https": self.proxy_url
        }
    
    def fetch(self, url, headers=None):
        """Fetch content from a URL using proxy"""
        import requests
        
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
            print(f"Error fetching {url}: {str(e)}")
            raise


class MCPSourceCrawler:
    """Crawler for specific data sources"""
    def __init__(self, client, source_config):
        """Initialize with MCP client and source configuration"""
        self.client = client
        self.config = source_config
    
    def search(self, query, location=None, max_pages=1):
        """Search for listings"""
        results = []
        
        for page in range(1, max_pages + 1):
            try:
                # Generate search URL for this page
                url = self.config.search_url_template
                url = url.replace("{query}", query)
                if location and "{location}" in url:
                    url = url.replace("{location}", location)
                if "{page}" in url:
                    url = url.replace("{page}", str(page))
                
                # Fetch search results
                print(f"Fetching page {page} from {self.config.name}: {url}")
                response = self.client.fetch(url, headers=self.config.headers)
                
                # This is where you would parse the results
                # For now, just return basic info to show it works
                result = {
                    "source": self.config.name,
                    "url": url,
                    "page": page,
                    "status": "success"
                }
                results.append(result)
                
            except Exception as e:
                print(f"Error searching {self.config.name}: {str(e)}")
                break
                
        return results
