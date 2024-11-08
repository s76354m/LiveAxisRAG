import pytest
from src.services.validation_service import ValidationService
from src.exceptions import ValidationError

def test_project_id_validation():
    """Test project ID validation"""
    validator = ValidationService()
    
    # Test valid project ID
    assert validator.validate_project_id('CACAI20230001') == True
    
    # Test invalid project ID
    with pytest.raises(ValidationError):
        validator.validate_project_id('INVALID12345')

def test_service_area_validation():
    """Test service area validation"""
    validator = ValidationService()
    
    # Test valid service area
    assert validator.validate_service_area(
        mileage=50.5,
        state='CA',
        county='Los Angeles'
    ) == True
    
    # Test invalid mileage
    with pytest.raises(ValidationError):
        validator.validate_service_area(
            mileage=-1,
            state='CA',
            county='Los Angeles'
        )