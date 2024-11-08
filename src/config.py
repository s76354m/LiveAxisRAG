from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()

class BaseConfig:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session config
    SESSION_TYPE = 'redis'
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    
    # O365 config
    O365_CLIENT_ID = os.getenv('O365_CLIENT_ID')
    O365_CLIENT_SECRET = os.getenv('O365_CLIENT_SECRET')
    
    # Timer config
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = "UTC"

class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://localhost/app_dev'
    )

class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'TEST_DATABASE_URL',
        'postgresql://localhost/app_test'
    )
    
    # Use memory for session in tests
    SESSION_TYPE = 'filesystem'
    
    # Disable scheduler in tests
    SCHEDULER_API_ENABLED = False

class Config(BaseConfig):
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
    MAX_REPORT_SECTIONS = None  # Set to None for all sections, or number for limit
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
