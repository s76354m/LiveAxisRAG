import pyodbc
from sqlalchemy import create_engine, text
import logging
from src.config.database import DatabaseConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_sql_connection():
    """Test SQL Server connection using both pyodbc and SQLAlchemy"""
    
    # Test PyODBC connection
    logger.info("Testing PyODBC connection...")
    try:
        conn_str = DatabaseConfig.get_pyodbc_string()
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        logger.info(f"SQL Server Version: {version}")
        cursor.close()
        conn.close()
        logger.info("PyODBC connection successful")
    except Exception as e:
        logger.error(f"PyODBC connection failed: {str(e)}")
        return False

    # Test SQLAlchemy connection
    logger.info("\nTesting SQLAlchemy connection...")
    try:
        engine = create_engine(DatabaseConfig.get_connection_string())
        with engine.connect() as connection:
            # Use text() for SQL queries in SQLAlchemy
            result = connection.execute(text("SELECT @@VERSION")).scalar()
            logger.info(f"SQLAlchemy connection successful")
            logger.info(f"SQL Server Version: {result}")
            
            # Test stored procedure existence
            logger.info("\nChecking stored procedures...")
            proc_result = connection.execute(text("""
                SELECT name 
                FROM sys.procedures 
                WHERE schema_id = SCHEMA_ID('dbo')
            """)).fetchall()
            
            procs = [row[0] for row in proc_result]
            logger.info(f"Found {len(procs)} stored procedures:")
            for proc in procs:
                logger.info(f"  - {proc}")
                
        return True
    except Exception as e:
        logger.error(f"SQLAlchemy connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Starting SQL Server connection test...")
    success = test_sql_connection()
    if success:
        logger.info("\nAll connection tests passed successfully")
    else:
        logger.error("\nConnection tests failed") 