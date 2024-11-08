import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.models import Base
from src.services.validation_service import ValidationService
from src.services.business_rules import BusinessRulesEngine
from src.api.main import app
from src.utils.database import DatabaseManager
from src.config.config_manager import ConfigManager

@pytest.fixture
def client():
    """Provide test client"""
    return TestClient(app)

@pytest.fixture
def validator():
    """Provide validation service instance"""
    return ValidationService()

@pytest.fixture
def rules_engine():
    """Provide business rules engine instance"""
    return BusinessRulesEngine()

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

@pytest.fixture
def sample_service_area():
    """Provide sample service area data"""
    return {
        'state': 'CA',
        'mileage': 50.0,
        'county': 'Los Angeles'
    }

@pytest.fixture
def project_service(test_db):
    """Provide project service instance"""
    return ProjectService(engine=test_db.bind)

@pytest.fixture(scope="session")
def db_manager(config):
    return DatabaseManager(config.get_database_url())