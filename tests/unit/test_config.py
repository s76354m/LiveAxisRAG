import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.models import Base

@pytest.fixture(scope="session")
def test_db():
    """Create test database"""
    # Use SQLite for testing
    TEST_DB_URL = "sqlite:///./test.db"
    engine = create_engine(TEST_DB_URL)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session factory
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    
    db = TestingSessionLocal()
    yield db
    
    # Cleanup after tests
    Base.metadata.drop_all(bind=engine)
    db.close()

def test_database_connection(test_db):
    """Test database connection"""
    assert test_db is not None
    result = test_db.execute(text("SELECT 1")).scalar()
    assert result == 1