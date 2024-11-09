from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os
import pyodbc

class DatabaseConfig:
    """SQL Server configuration"""
    
    # SQL Server connection details
    SERVER = os.getenv('DB_SERVER', 'DESKTOP-PJTAP42')  # Remove SQLEXPRESS from server name
    INSTANCE = os.getenv('DB_INSTANCE', 'SQLEXPRESS')   # Separate instance name
    DATABASE = os.getenv('DB_NAME', 'swarmrag')
    DRIVER = os.getenv('DB_DRIVER', 'SQL Server')       # Use basic SQL Server driver name
    
    @classmethod
    def get_connection_string(cls) -> str:
        """Generate SQL Server connection string"""
        server = f"{cls.SERVER}\\{cls.INSTANCE}" if cls.INSTANCE else cls.SERVER
        params = {
            'DRIVER': f"{{{cls.DRIVER}}}",  # Add curly braces around driver name
            'SERVER': server,
            'DATABASE': cls.DATABASE,
            'Trusted_Connection': 'yes',
            'TrustServerCertificate': 'yes'
        }
        
        connection_str = ';'.join([f'{k}={v}' for k, v in params.items()])
        return f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_str)}"

    @classmethod
    def test_connection(cls) -> bool:
        """Test the database connection"""
        try:
            server = f"{cls.SERVER}\\{cls.INSTANCE}" if cls.INSTANCE else cls.SERVER
            conn_str = (
                f"DRIVER={{{cls.DRIVER}}};"
                f"SERVER={server};"
                f"DATABASE={cls.DATABASE};"
                f"Trusted_Connection=yes;"
                f"TrustServerCertificate=yes"
            )
            print(f"Testing connection with string: {conn_str}")
            conn = pyodbc.connect(conn_str, timeout=5)
            conn.close()
            return True
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            return False

class Config:
    """Application configuration"""
    SQLALCHEMY_DATABASE_URI = DatabaseConfig.get_connection_string()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'max_overflow': 10,
        'pool_timeout': 30,
        'pool_recycle': 1800
    }

def get_engine():
    """Create SQLAlchemy engine"""
    return create_engine(
        DatabaseConfig.get_connection_string(),
        **Config.SQLALCHEMY_ENGINE_OPTIONS
    )

def get_session() -> Generator:
    """Get database session"""
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=get_engine()
    )
    
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()