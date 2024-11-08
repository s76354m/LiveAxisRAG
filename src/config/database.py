from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os

class DatabaseConfig:
    """SQL Server configuration"""
    
    # SQL Server connection details
    SERVER = 'DESKTOP-PJTAP42'  # Remove SQLEXPRESS from server name
    INSTANCE = 'SQLEXPRESS'     # Specify instance separately
    DATABASE = 'ndar'
    DRIVER = '{SQL Server}'     # Use exact driver name in braces
    
    @classmethod
    def get_connection_string(cls) -> str:
        """Generate SQL Server connection string"""
        server = f"{cls.SERVER}\\{cls.INSTANCE}"
        params = {
            'DRIVER': cls.DRIVER,
            'SERVER': server,
            'DATABASE': cls.DATABASE,
            'Trusted_Connection': 'yes',
            'TrustServerCertificate': 'yes'
        }
        
        connection_str = ';'.join([f'{k}={v}' for k, v in params.items()])
        return f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_str)}"

    @classmethod
    def get_pyodbc_string(cls) -> str:
        """Get raw connection string for testing"""
        server = f"{cls.SERVER}\\{cls.INSTANCE}"
        return (
            f"DRIVER={cls.DRIVER};"
            f"SERVER={server};"
            f"DATABASE={cls.DATABASE};"
            f"Trusted_Connection=yes;"
            f"TrustServerCertificate=yes"
        )

class Config:
    """Application configuration"""
    SQLALCHEMY_DATABASE_URI = DatabaseConfig.get_connection_string()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_timeout': 30,
        'pool_recycle': 1800
    } 

def get_db_url() -> str:
    """Get database URL from environment or config"""
    return os.getenv(
        'DATABASE_URL',
        'sqlite:///./test.db'  # Default to SQLite for testing
    )

def get_engine():
    """Create SQLAlchemy engine"""
    return create_engine(get_db_url())

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