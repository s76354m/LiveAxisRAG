import pytest
from src.services.business_rules import BusinessRulesEngine
from src.exceptions import BusinessRuleError

def test_business_rules_engine():
    """Test business rules engine"""
    engine = BusinessRulesEngine()
    
    # Test valid case
    valid_data = {
        "project_id": "CACAI20230001",
        "region": "West",
        "service_area": {
            "state": "CA",
            "county": "Los Angeles",
            "mileage": 50.0
        }
    }
    assert engine.validate(valid_data)
    
    # Test invalid state
    invalid_state = valid_data.copy()
    invalid_state["service_area"]["state"] = "XX"
    with pytest.raises(BusinessRuleError):
        engine.validate(invalid_state)
    
    # Test invalid mileage
    invalid_mileage = valid_data.copy()
    invalid_mileage["service_area"]["mileage"] = -1
    with pytest.raises(BusinessRuleError):
        engine.validate(invalid_mileage) 