from fastapi import FastAPI, HTTPException
from src.services.project_service import ProjectService
from src.models.project import ServiceArea
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
app = FastAPI(title="Project Service Area API")

@app.get("/project/{project_id}/exists")
async def check_project_exists(project_id: str) -> Dict[str, bool]:
    """Check if project ID exists"""
    try:
        exists = await ProjectService.check_project_id(project_id)
        return {"exists": exists}
    except Exception as e:
        logger.error(f"Error checking project {project_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/project/{project_id}/service-area")
async def get_service_area(project_id: str) -> Dict[str, Any]:
    """Get project service area details"""
    try:
        service_area = await ProjectService.get_service_area(project_id)
        if not service_area:
            raise HTTPException(status_code=404, detail="Service area not found")
        return service_area
    except Exception as e:
        logger.error(f"Error getting service area for {project_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/project/{project_id}/service-area")
async def update_service_area(project_id: str, mileage: float) -> Dict[str, str]:
    """Update project service area"""
    try:
        await ProjectService.update_service_area(project_id, mileage)
        return {"status": "updated"}
    except Exception as e:
        logger.error(f"Error updating service area for {project_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products")
async def get_products(flag: str = "1") -> Dict[str, Any]:
    """Get CSP products based on flag"""
    try:
        products = await ProjectService.get_products(flag)
        return {"products": products}
    except Exception as e:
        logger.error(f"Error getting products with flag {flag}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 