from src.core.config.app_config import AppConfig
from src.core.config.secrets_manager import SecretsManager

def initialize_configuration():
    # Initialize configuration
    config = AppConfig()
    secrets = SecretsManager()
    
    try:
        # Validate configuration
        config.validate_config()
        
        # Access configuration values
        db_host = config.get('database.host')
        log_level = config.get('logging.level')
        
        # Access secrets
        db_password = secrets.get_secret('DB_PASSWORD')
        api_key = secrets.get_secret('API_KEY')
        
        return True
        
    except Exception as e:
        logger.error(f"Configuration initialization failed: {str(e)}")
        return False 