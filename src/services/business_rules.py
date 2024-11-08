from typing import Dict, Any, List
from src.exceptions import BusinessRuleError
import logging

logger = logging.getLogger(__name__)

class BusinessRulesEngine:
    """Business rules processing engine"""
    
    def __init__(self):
        self.state_rules = {
            'CA': {
                'min_mileage': 0.1,
                'max_mileage': 100.0,
                'requires_county': True
            },
            'TX': {
                'min_mileage': 0.1,
                'max_mileage': 150.0,
                'requires_county': True
            },
            'NY': {
                'min_mileage': 0.1,
                'max_mileage': 75.0,
                'requires_county': True
            }
        }
    
    def apply_service_area_rules(self, 
                               service_area: Dict[str, Any]) -> Dict[str, Any]:
        """Apply business rules to service area"""
        state = service_area.get('state')
        if not state or state not in self.state_rules:
            raise BusinessRuleError(f"Invalid state: {state}")
            
        rules = self.state_rules[state]
        
        # Validate mileage
        mileage = service_area.get('mileage', 0)
        if not (rules['min_mileage'] <= mileage <= rules['max_mileage']):
            raise BusinessRuleError(
                f"Mileage must be between "
                f"{rules['min_mileage']} and {rules['max_mileage']}"
            )
        
        # Check county requirement
        if rules['requires_county'] and not service_area.get('county'):
            raise BusinessRuleError(f"County is required for state: {state}")
        
        return service_area
    
    def calculate_adjusted_mileage(self, 
                                 mileage: float, 
                                 state: str) -> float:
        """Calculate adjusted mileage based on state rules"""
        if state not in self.state_rules:
            raise BusinessRuleError(f"Invalid state: {state}")
            
        # Add state-specific adjustments here
        return mileage
    
    def validate_workflow_requirements(self, 
                                    project_data: Dict[str, Any], 
                                    target_state: str) -> List[str]:
        """Validate requirements for workflow state transition"""
        requirements = []
        
        if target_state.lower() == 'active':
            if not project_data.get('service_area'):
                requirements.append("Service area is required")
            if not project_data.get('mileage'):
                requirements.append("Mileage is required")
        
        return requirements 