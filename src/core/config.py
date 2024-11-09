from typing import Dict, Any, Optional
import os
from pathlib import Path
from dotenv import load_dotenv
import yaml
from src.utils.exceptions import ConfigurationError

class ConfigManager:
    def __init__(self, env: Optional[str] = None):
        self.env = env or os.getenv('ENVIRONMENT', 'development')
        self._load_config()
        
    def _load_config(self) -> None:
        """Load configuration from environment and yaml files"""
        # Load environment variables
        env_file = Path(f'.env.{self.env}')
        if env_file.exists():
            load_dotenv(env_file)
        else:
            load_dotenv()
            
        # Load yaml configuration
        config_file = Path(f'config/{self.env}.yaml')
        if config_file.exists():
            with open(config_file) as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = {}
            
    def get_database_url(self) -> str:
        """Construct database URL from configuration"""
        try:
            return os.getenv('DATABASE_URL') or self._construct_db_url()
        except KeyError as e:
            raise ConfigurationError(f"Missing database configuration: {str(e)}")
            
    def _construct_db_url(self) -> str:
        """Construct database URL from individual components"""
        required_keys = ['DB_DRIVER', 'DB_HOST', 'DB_PORT', 'DB_NAME', 
                        'DB_USER', 'DB_PASSWORD']
        
        # Verify all required keys exist
        missing_keys = [key for key in required_keys if not os.getenv(key)]
        if missing_keys:
            raise ConfigurationError(f"Missing database configuration keys: {missing_keys}")
            
        return (
            f"{os.getenv('DB_DRIVER')}://"
            f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/"
            f"{os.getenv('DB_NAME')}"
        ) 