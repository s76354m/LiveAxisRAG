import pytest
from src.repositories.base import BaseRepository
from src.models.core import Project
from src.exceptions import RepositoryError

def test_base_repository_get(session, sample_project):
    """Test base repository get operation"""
    repo = BaseRepository(Project)
    project = repo.get_by_id(sample_project.id)
    
    assert project is not None
    assert project.project_id == sample_project.project_id

def test_base_repository_create(session):
    """Test base repository create operation"""
    repo = BaseRepository(Project)
    project = repo.create(
        project_id='NEW123456789',
        region='South',
        status='Pending',
        created_by='test@example.com'
    )
    
    assert project.id is not None
    assert project.project_id == 'NEW123456789'

def test_base_repository_update(session, sample_project):
    """Test base repository update operation"""
    repo = BaseRepository(Project)
    updated = repo.update(
        sample_project.id,
        region='Updated Region'
    )
    
    assert updated.region == 'Updated Region' 