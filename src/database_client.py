from typing import Optional
from src.core.database import DatabaseManager
from src.core.config import ConfigManager
from src.utils.exceptions import DatabaseError
import logging

logger = logging.getLogger(__name__)

class DatabaseClient:
    _instance: Optional['DatabaseClient'] = None
    
    def __new__(cls) -> 'DatabaseClient':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        """Initialize database connection"""
        try:
            config = ConfigManager()
            self.db = DatabaseManager(config.get_database_url())
            logger.info("Database client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database client: {str(e)}")
            raise
            
    def check_health(self) -> bool:
        """Check database connection health"""
        is_healthy, message = self.db.health_check()
        if not is_healthy:
            logger.warning(f"Database health check failed: {message}")
        return is_healthy 