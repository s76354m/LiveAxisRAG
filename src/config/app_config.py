from pathlib import Path
import os
from dotenv import load_dotenv

class AppConfig:
    """Application configuration"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        load_dotenv()
        self.environment = os.getenv('ENVIRONMENT', 'development')
        self.debug = os.getenv('DEBUG', 'False').lower() == 'true'
        self.app_name = os.getenv('APP_NAME', 'SwarmRAG') 