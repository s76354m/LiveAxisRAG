import pytest
from src import create_app, db
from src.models.core import Project, Competitor

@pytest.fixture
def app():
    """Create application for the tests."""
    app = create_app('testing')
    
    # Setup app context
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client"""
    return app.test_client()

@pytest.fixture
def session(app):
    """Database session"""
    with app.app_context():
        yield db.session

@pytest.fixture
def sample_project(session):
    """Create sample project"""
    project = Project(
        project_id='TEST123456789',
        region='North',
        status='Active',
        created_by='test@example.com'
    )
    session.add(project)
    session.commit()
    return project

@pytest.fixture
def sample_competitor(session, sample_project):
    """Create sample competitor"""
    competitor = Competitor(
        project_id=sample_project.project_id,
        product='Test Product',
        status='Draft',
        created_by='test@example.com'
    )
    session.add(competitor)
    session.commit()
    return competitor 