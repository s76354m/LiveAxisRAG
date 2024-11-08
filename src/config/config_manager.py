from typing import Any, Dict
from pathlib import Path
import yaml
import os
from dotenv import load_dotenv

class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        load_dotenv()
        self._load_config()
        
    def _load_config(self):
        config_path = Path("config/config.yaml")
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
            
        # Override with environment variables
        self.config['database'] = {
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'),
            'name': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        } 