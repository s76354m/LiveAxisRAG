import pytest
from src.services.project_service import ProjectService
from src.exceptions import ValidationError

@pytest.mark.asyncio
async def test_project_service(test_db):
    """Test project service operations"""
    service = ProjectService(engine=test_db.bind)
    
    # Test valid project
    project_data = {
        'project_id': 'CACAI20230001',
        'region': 'West',
        'status': 'Active',
        'created_by': 'test@example.com'
    }
    
    result = await service.validate_project(project_data)
    assert result['is_valid'] == True
    
    # Test invalid project ID format
    with pytest.raises(ValidationError, match="Invalid project ID format"):
        await service.validate_project({
            'project_id': 'INVALID',
            'region': 'Invalid'
        })
    
    # Test invalid region
    with pytest.raises(ValidationError, match="Invalid region"):
        await service.validate_project({
            'project_id': 'CACAI20230001',
            'region': 'Invalid'
        })
    
    # Test missing fields
    with pytest.raises(ValidationError, match="Missing required fields"):
        await service.validate_project({})