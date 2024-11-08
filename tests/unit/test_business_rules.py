import pytest
from src.services.business_rules import BusinessRulesEngine
from src.exceptions import BusinessRuleError

def test_service_area_rules():
    """Test service area business rules"""
    engine = BusinessRulesEngine()
    
    # Test valid service area
    service_area = {
        'state': 'CA',
        'mileage': 50.0,
        'county': 'Los Angeles'
    }
    
    result = engine.apply_service_area_rules(service_area)
    assert result == service_area
    
    # Test invalid mileage
    invalid_service_area = {
        'state': 'CA',
        'mileage': 200.0,  # Too high for CA
        'county': 'Los Angeles'
    }
    
    with pytest.raises(BusinessRuleError):
        engine.apply_service_area_rules(invalid_service_area) 