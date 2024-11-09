from typing import Any, Dict, List, Optional, Tuple, Union
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
import logging
from src.utils.exceptions import DatabaseError

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, connection_string: str):
        self._engine = self._create_engine(connection_string)
        self.metadata = MetaData()
        
    def _create_engine(self, connection_string: str) -> Engine:
        """Create SQLAlchemy engine with connection pooling"""
        return create_engine(
            connection_string,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_pre_ping=True  # Enable connection health checks
        )
    
    @contextmanager
    def get_connection(self) -> Connection:
        """Provide a context-managed database connection"""
        conn = self._engine.connect()
        try:
            yield conn
            conn.commit()
        except SQLAlchemyError as e:
            conn.rollback()
            logger.error(f"Database operation failed: {str(e)}")
            raise DatabaseError(f"Database operation failed: {str(e)}")
        finally:
            conn.close()
    
    def execute_query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
        fetch: bool = True
    ) -> Union[List[Dict[str, Any]], None]:
        """Execute a parameterized query safely"""
        with self.get_connection() as conn:
            try:
                result = conn.execute(text(query), parameters=params or {})
                if fetch:
                    return [dict(row) for row in result.fetchall()]
                return None
            except SQLAlchemyError as e:
                logger.error(f"Query execution failed: {str(e)}")
                raise DatabaseError(f"Query execution failed: {str(e)}")
    
    def bulk_insert(
        self,
        table_name: str,
        data: List[Dict[str, Any]]
    ) -> int:
        """Safely perform bulk insert operations"""
        if not data:
            return 0
            
        placeholders = ', '.join(['(:' + str(i) + ')' for i in range(len(data))])
        columns = ', '.join(data[0].keys())
        
        query = f"""
            INSERT INTO {table_name} ({columns})
            VALUES {placeholders}
        """
        
        with self.get_connection() as conn:
            try:
                result = conn.execute(text(query), 
                                    parameters=[{str(i): item[col] 
                                               for col in data[0].keys()} 
                                              for i, item in enumerate(data)])
                return result.rowcount
            except SQLAlchemyError as e:
                logger.error(f"Bulk insert failed: {str(e)}")
                raise DatabaseError(f"Bulk insert failed: {str(e)}")
    
    def execute_procedure(
        self,
        procedure_name: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Optional[List[Dict[str, Any]]]:
        """Execute a stored procedure safely"""
        param_string = ', '.join([f':{key}' for key in (params or {})])
        query = f"EXEC {procedure_name} {param_string}"
        
        return self.execute_query(query, params)
    
    def health_check(self) -> Tuple[bool, str]:
        """Check database connection health"""
        try:
            with self.get_connection() as conn:
                conn.execute(text("SELECT 1"))
                return True, "Database connection is healthy"
        except DatabaseError as e:
            return False, str(e) 