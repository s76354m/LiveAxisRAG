import pytest
from sqlalchemy import text
from src.utils.database import DatabaseManager
from src.utils.connection_test import ConnectionTester

@pytest.fixture
def setup_test_tables(test_db):
    """Setup test tables"""
    with test_db.bind.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS projects (
                project_id VARCHAR(255) PRIMARY KEY,
                region VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        conn.commit()

def test_database_manager(test_db, setup_test_tables):
    """Test database manager functionality"""
    manager = DatabaseManager(test_db.bind)
    
    # Test connection check
    assert manager.check_connection() is True
    
    # Test table listing
    tables = manager.get_tables()
    assert isinstance(tables, list)
    assert "projects" in tables
    
    # Test column information
    columns = manager.get_columns("projects")
    assert isinstance(columns, list)
    assert any(col["name"] == "project_id" for col in columns)

@pytest.mark.asyncio
async def test_connection_tester(test_db, setup_test_tables):
    """Test connection testing utilities"""
    tester = ConnectionTester(test_db.bind)
    
    # Test async connection test
    async_result = await tester.test_connection()
    assert async_result["status"] == "success"
    assert "latency" in async_result
    assert async_result["latency"] >= 0