from typing import Any, Dict, Optional
from pathlib import Path
import yaml
from src.utils.exceptions import ConfigurationError
import logging

logger = logging.getLogger(__name__)

class BaseConfig:
    """Base configuration class with common functionality"""
    
    def __init__(self):
        logger.debug("Initializing BaseConfig")
        self._config: Dict[str, Any] = {}
        
    def _load_yaml_config(self, path: Path) -> Dict[str, Any]:
        """Safely load YAML configuration file"""
        try:
            logger.debug(f"Loading config file: {path}")
            with open(path, 'r') as f:
                content = f.read()
                logger.debug(f"Raw config content: {content}")
                config = yaml.safe_load(content)
                logger.debug(f"Parsed config: {config}")
                return config or {}
        except Exception as e:
            logger.error(f"Failed to load config file {path}: {str(e)}")
            raise ConfigurationError(f"Configuration load failed: {str(e)}")
            
    def get(self, key: str, default: Any = None) -> Any:
        """Safely get configuration value"""
        try:
            logger.debug(f"Getting config key: {key}, current config: {self._config}")
            if not self._config:
                logger.warning("Configuration is empty")
                return default
                
            keys = key.split('.')
            value = self._config
            for k in keys:
                if not isinstance(value, dict):
                    logger.debug(f"Value is not a dict at key {k}")
                    return default
                value = value.get(k)
                if value is None:
                    logger.debug(f"No value found for key {k}")
                    return default
            return value
        except Exception as e:
            logger.error(f"Error accessing config key {key}: {str(e)}")
            return default