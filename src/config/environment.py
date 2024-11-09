from pathlib import Path
from typing import Dict, Any
import os
from dotenv import load_dotenv
import yaml

class EnvironmentConfig:
    _instance = None
    
    def __new__(cls) -> 'EnvironmentConfig':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        self.env = os.getenv('ENVIRONMENT', 'development')
        self._load_environment()
        self._load_config()
    
    def _load_environment(self) -> None:
        env_file = '.env' if self.env == 'development' else f'.env.{self.env}'
        load_dotenv(env_file)
    
    def _load_config(self) -> None:
        config_path = Path(f"config/{self.env}.yaml")
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
    
    def get_config(self, key: str) -> Any:
        return self.config.get(key)
    
    def get_database_url(self) -> str:
        return os.getenv('DATABASE_URL', '') 