from typing import Optional, Dict, Any
from src.exceptions import ValidationError
import re
import logging

logger = logging.getLogger(__name__)

class ValidationService:
    """Comprehensive validation service"""
    
    def __init__(self):
        self.state_codes = {
            'CA': 'California',
            'TX': 'Texas',
            'NY': 'New York'
            # Add other states as needed
        }
    
    def validate_project_id(self, project_id: str) -> bool:
        """Validate project ID format"""
        if not project_id:
            raise ValidationError("Project ID cannot be empty")
            
        pattern = r'^[A-Z]{2}CAI\d{8}$'
        if not re.match(pattern, project_id):
            raise ValidationError(
                "Project ID must be in format: XXCAI20230000 "
                "(XX=state code, followed by CAI and 8 digits)"
            )
            
        state_code = project_id[:2]
        if state_code not in self.state_codes:
            raise ValidationError(f"Invalid state code: {state_code}")
            
        return True
    
    def validate_service_area(self, 
                            mileage: float, 
                            state: str, 
                            county: Optional[str] = None) -> bool:
        """Validate service area data"""
        if not isinstance(mileage, (int, float)):
            raise ValidationError("Mileage must be a number")
            
        if mileage <= 0:
            raise ValidationError("Mileage must be greater than 0")
            
        if state not in self.state_codes:
            raise ValidationError(f"Invalid state: {state}")
            
        # Add county validation if needed
        return True
    
    def validate_workflow_state(self, 
                              current_state: str, 
                              next_state: str, 
                              project_data: Dict[str, Any]) -> bool:
        """Validate workflow state transitions"""
        valid_transitions = {
            'draft': ['pending'],
            'pending': ['active', 'rejected'],
            'active': ['completed', 'cancelled'],
            'rejected': ['draft'],
            'cancelled': [],
            'completed': []
        }
        
        current_state = current_state.lower()
        next_state = next_state.lower()
        
        if current_state not in valid_transitions:
            raise ValidationError(f"Invalid current state: {current_state}")
            
        if next_state not in valid_transitions[current_state]:
            raise ValidationError(
                f"Invalid state transition from {current_state} to {next_state}"
            )
            
        return True 