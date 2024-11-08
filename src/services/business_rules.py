from typing import Dict, Any
from src.exceptions import BusinessRuleError

class BusinessRulesEngine:
    def validate(self, data: Dict[str, Any]) -> bool:
        """Validate data against business rules"""
        try:
            # Validate project ID format
            if not data.get("project_id", "").startswith("CACAI"):
                raise BusinessRuleError("Invalid project ID format")
            
            # Validate region
            valid_regions = ["West", "East", "North", "South"]
            if data.get("region") not in valid_regions:
                raise BusinessRuleError("Invalid region")
            
            # Validate service area
            service_area = data.get("service_area", {})
            if service_area.get("state") not in ["CA", "OR", "WA"]:
                raise BusinessRuleError("Invalid state")
                
            if not isinstance(service_area.get("mileage"), (int, float)) or service_area.get("mileage") <= 0:
                raise BusinessRuleError("Invalid mileage")
            
            return True
            
        except BusinessRuleError:
            raise
        except Exception as e:
            raise BusinessRuleError(f"Validation failed: {str(e)}")