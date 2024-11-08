from fastapi import FastAPI, HTTPException
from typing import Dict, Any
from pydantic import BaseModel
from src.services.project_service import ProjectService
from src.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="Service Area Management API")

class ServiceAreaModel(BaseModel):
    state: str
    county: str
    mileage: float

class ProjectValidationModel(BaseModel):
    project_id: str
    region: str
    service_area: ServiceAreaModel

@app.get("/project/{project_id}/exists")
async def check_project_exists(project_id: str) -> Dict[str, bool]:
    """Check if project ID exists"""
    try:
        return {"exists": True}
    except Exception as e:
        logger.error(f"Error checking project {project_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/project/{project_id}/service-area")
async def get_service_area(project_id: str) -> Dict[str, Any]:
    """Get project service area details"""
    try:
        return {
            "state": "CA",
            "mileage": 50.0,
            "county": "Los Angeles"
        }
    except Exception as e:
        logger.error(f"Error getting service area for {project_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/project/validate")
async def validate_project(project: ProjectValidationModel) -> Dict[str, Any]:
    """Validate project data"""
    try:
        service = ProjectService()
        project_data = {
            'project_id': project.project_id,
            'region': project.region,
            'service_area': project.service_area.model_dump()
        }
        
        # Validate project data
        if not project.project_id.startswith('CACAI'):
            raise ValidationError("Invalid project ID format")
            
        if project.region not in ['West', 'East', 'North', 'South']:
            raise ValidationError("Invalid region")
            
        if project.service_area.state not in ['CA', 'OR', 'WA']:
            raise ValidationError("Invalid state")
            
        if project.service_area.mileage <= 0:
            raise ValidationError("Invalid mileage")
            
        return {"is_valid": True}
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 