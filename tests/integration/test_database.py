import pytest
from sqlalchemy.orm import Session
from src.models import Project, ServiceArea

def test_project_creation(test_db: Session):
    """Test project database operations"""
    # Create project
    project = Project(
        project_id='CACAI20230001',
        region='West',
        status='Active',
        created_by='test@example.com'
    )
    
    test_db.add(project)
    test_db.commit()
    
    # Query project
    saved_project = test_db.query(Project).filter_by(
        project_id='CACAI20230001'
    ).first()
    
    assert saved_project is not None
    assert saved_project.region == 'West'
    
    # Cleanup
    test_db.delete(saved_project)
    test_db.commit()

def test_service_area_creation(test_db: Session):
    """Test service area database operations"""
    # Create project first
    project = Project(
        project_id='CACAI20230002',
        region='West',
        status='Active',
        created_by='test@example.com'
    )
    
    test_db.add(project)
    test_db.commit()
    
    # Create service area
    service_area = ServiceArea(
        project=project,
        state='CA',
        county='Los Angeles',
        mileage=50.0
    )
    
    test_db.add(service_area)
    test_db.commit()
    
    # Query service area
    saved_service_area = test_db.query(ServiceArea).filter_by(
        project_id=project.id
    ).first()
    
    assert saved_service_area is not None
    assert saved_service_area.state == 'CA'
    assert saved_service_area.county == 'Los Angeles'
    
    # Cleanup
    test_db.delete(service_area)
    test_db.delete(project)
    test_db.commit()