from sqlalchemy import create_engine, text
from contextlib import contextmanager

class DatabaseConnection:
    """Database connection manager for SQL Server"""
    
    def __init__(self, config):
        self.engine = create_engine(
            config.SQLALCHEMY_DATABASE_URI,
            **config.SQLALCHEMY_ENGINE_OPTIONS
        )
    
    @contextmanager
    def get_connection(self):
        """Get database connection"""
        connection = self.engine.connect()
        try:
            yield connection
        finally:
            connection.close()
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            with self.get_connection() as conn:
                conn.execute(text('SELECT 1'))
            return True
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return False 