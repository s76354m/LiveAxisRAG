import pytest
from src.services.validation_service import ValidationService
from src.exceptions import ValidationError

def test_project_id_validation():
    validator = ValidationService()
    
    # Valid project ID
    assert validator.validate_project_id('CACAI20230001') == True
    
    # Invalid project IDs
    with pytest.raises(ValidationError):
        validator.validate_project_id('INVALID12345')
    
    with pytest.raises(ValidationError):
        validator.validate_project_id('XXCAI20230001')  # Invalid state code

def test_service_area_validation():
    validator = ValidationService()
    
    # Valid service area
    assert validator.validate_service_area(
        mileage=50.5,
        state='CA',
        county='Los Angeles'
    ) == True
    
    # Invalid mileage
    with pytest.raises(ValidationError):
        validator.validate_service_area(
            mileage=-1,
            state='CA',
            county='Los Angeles'
        )
    
    # Invalid state
    with pytest.raises(ValidationError):
        validator.validate_service_area(
            mileage=50.5,
            state='XX',
            county='Invalid'
        ) 