# Add this to trendhire_api.py or create a separate configs.py file
from mcp_integration import SourceConfig

linkedin_config = SourceConfig(
    name="LinkedIn",
    base_url="https://www.linkedin.com",
    search_url_template="https://www.linkedin.com/jobs/search/?keywords={query}&location={location}&start={page}",
    listing_selector=".job-card-container",
    detail_selectors={
        "title": ".job-card-list__title",
        "company": ".job-card-container__company-name",
        "location": ".job-card-container__metadata-item",
        "posted_date": ".job-card-container__posted-date",
        "job_link": ".job-card-list__title a"
    }
)

indeed_config = SourceConfig(
    name="Indeed",
    base_url="https://www.indeed.com",
    search_url_template="https://www.indeed.com/jobs?q={query}&l={location}&start={page}",
    listing_selector=".jobsearch-ResultsList > li",
    detail_selectors={
        "title": ".jobTitle span",
        "company": ".companyName",
        "location": ".companyLocation",
        "salary": ".salary-snippet-container",
        "job_link": ".jobTitle a"
    }
)