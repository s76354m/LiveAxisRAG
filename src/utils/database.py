from typing import Any, Dict, List
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, connection_string: str):
        self.engine = create_engine(
            connection_string,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30
        )
    
    @contextmanager
    def get_connection(self):
        """Provide managed database connection"""
        conn = self.engine.connect()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database operation failed: {str(e)}")
            raise
        finally:
            conn.close()
    
    def execute_parameterized_query(
        self, 
        query: str, 
        params: Dict[str, Any]
    ) -> Any:
        """Execute parameterized query safely"""
        with self.get_connection() as conn:
            return conn.execute(text(query), params)