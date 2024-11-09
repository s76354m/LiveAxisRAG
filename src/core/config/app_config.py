from typing import Any, Dict
from pathlib import Path
import os
import re
from dotenv import load_dotenv
from .base_config import BaseConfig
import logging
from .schemas import AppConfigSchema
from pydantic import ValidationError

logger = logging.getLogger(__name__)

class AppConfig(BaseConfig):
    _instance = None
    _initialized = False
    
    def __new__(cls) -> 'AppConfig':
        if cls._instance is None:
            logger.debug("Creating new AppConfig instance")
            cls._instance = super().__new__(cls)
        return cls._instance
        
    def __init__(self):
        if not self._initialized:
            logger.debug("Initializing AppConfig")
            super().__init__()
            self._initialized = True
            self.env = os.getenv('ENVIRONMENT', 'development')
            self._load_environment()
            self._load_configurations()
            logger.debug(f"Initialization complete. Config: {self._config}")
    
    def _interpolate_env_vars(self, value: Any) -> Any:
        """Recursively interpolate environment variables in config values"""
        if isinstance(value, str):
            # Match ${VAR} or $VAR patterns
            pattern = r'\$\{([^}]+)\}|\$([a-zA-Z_][a-zA-Z0-9_]*)'
            matches = re.finditer(pattern, value)
            
            for match in matches:
                env_var = match.group(1) or match.group(2)
                env_value = os.getenv(env_var)
                if env_value is not None:
                    value = value.replace(match.group(0), env_value)
            return value
        elif isinstance(value, dict):
            return {k: self._interpolate_env_vars(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._interpolate_env_vars(item) for item in value]
        return value
    
    def _process_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Process configuration with variable interpolation"""
        return self._interpolate_env_vars(config)
            
    def _load_configurations(self) -> None:
        """Load all configuration files"""
        try:
            config_dir = Path('config')
            config_dir.mkdir(exist_ok=True)
            
            # Load base configuration
            base_config = config_dir / 'base.yaml'
            logger.debug(f"Loading base config from: {base_config}")
            if base_config.exists():
                base_data = self._load_yaml_config(base_config)
                processed_base = self._process_config(base_data)
                logger.debug(f"Processed base config: {processed_base}")
                self._config = processed_base
            
            # Load environment-specific configuration
            env_config = config_dir / f'{self.env}.yaml'
            logger.debug(f"Loading env config from: {env_config}")
            if env_config.exists():
                env_data = self._load_yaml_config(env_config)
                processed_env = self._process_config(env_data)
                logger.debug(f"Processed env config: {processed_env}")
                self._deep_merge(self._config, processed_env)
                
            logger.debug(f"Final config after loading: {self._config}")
        except Exception as e:
            logger.error(f"Error loading configurations: {str(e)}")
            raise
            
    def _deep_merge(self, base: Dict, update: Dict) -> None:
        """Deep merge two dictionaries"""
        for key, value in update.items():
            if (
                key in base 
                and isinstance(base[key], dict) 
                and isinstance(value, dict)
            ):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
        
    def validate_config(self) -> None:
        """Validate configuration against schema"""
        try:
            AppConfigSchema(**self._config)
        except ValidationError as e:
            logger.error(f"Configuration validation failed: {e}")
            raise