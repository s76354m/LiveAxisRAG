import pytest
from src.models.core import Project, Competitor
from src.exceptions import ValidationError

def test_project_creation(session):
    """Test project creation"""
    project = Project(
        project_id='TEST123456789',
        region='North',
        status='Active',
        created_by='test@example.com'
    )
    session.add(project)
    session.commit()
    
    assert project.id is not None
    assert project.project_id == 'TEST123456789'
    assert project.status == 'Active'

def test_project_validation(session):
    """Test project validation rules"""
    with pytest.raises(ValidationError):
        project = Project(
            project_id='SHORT',  # Too short
            created_by='invalid'  # Invalid email
        )
        session.add(project)
        session.commit()

def test_competitor_creation(session, sample_project):
    """Test competitor creation"""
    competitor = Competitor(
        project_id=sample_project.project_id,
        product='Test Product',
        status='Draft',
        created_by='test@example.com'
    )
    session.add(competitor)
    session.commit()
    
    assert competitor.id is not None
    assert competitor.project is not None 