from typing import Optional, List, Dict, Any
from src.models.project import Project, ServiceArea
from sqlalchemy import create_engine, text
import logging

logger = logging.getLogger(__name__)

from sqlalchemy.orm import Session
from src.exceptions import ValidationError  # Add this import

class ProjectService:
    def __init__(self, engine=None):
        """Initialize project service"""
        self.engine = engine

    async def validate_project(self, project_data: dict) -> dict:
        """Validate project data"""
        try:
            # Basic validation
            if not project_data.get('project_id') or not project_data.get('region'):
                raise ValidationError("Missing required fields")
                
            # Project ID format validation
            if not project_data['project_id'].startswith('CACAI'):
                raise ValidationError("Invalid project ID format")
                
            # Region validation
            valid_regions = ['West', 'East', 'North', 'South']
            if project_data['region'] not in valid_regions:
                raise ValidationError("Invalid region")
                
            return {'is_valid': True}
        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError(f"Validation failed: {str(e)}")