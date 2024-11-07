from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # Model configurations
    CLAUDE_MODEL = "claude-3-5-sonnet-20241022"
    EMBEDDING_MODEL = "text-embedding-3-large"
    EMBEDDING_DIMENSIONS = 1536
    
    # Processing settings
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # Page settings
    try:
        _max_pages_env = os.getenv("MAX_PAGES")
        MAX_PAGES = int(_max_pages_env) if _max_pages_env and _max_pages_env.lower() != 'none' else None
    except (ValueError, TypeError):
        MAX_PAGES = None  # Default to None if invalid value or not set
    
    # Report length settings
    MAX_REPORT_SECTIONS = 2  # Set to None for all sections, or number for limit
    REPORT_SECTIONS = [
        "Executive Summary",
        "System Architecture",
        "Technical Requirements",
        "Implementation Guidelines",
        "API Documentation",
        "Data Models",
        "Integration Patterns",
        "Security Considerations",
        "Performance Optimization",
        "Testing Requirements",
        "Deployment Guidelines",
        "Maintenance Procedures",
        "Troubleshooting Guidelines",
        "Edge Cases",
        "Error Handling"
    ]
    
    @classmethod
    def get_max_pages(cls):
        if cls.MAX_PAGES is None or cls.MAX_PAGES == -1:
            return float('inf')
        return max(1, int(cls.MAX_PAGES))
    
    @classmethod
    def get_report_sections(cls):
        if cls.MAX_REPORT_SECTIONS is None:
            return cls.REPORT_SECTIONS
        return cls.REPORT_SECTIONS[:cls.MAX_REPORT_SECTIONS]
