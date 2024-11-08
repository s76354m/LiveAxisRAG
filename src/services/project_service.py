from typing import Optional, List, Dict, Any
from src.models.project import Project, ServiceArea
from sqlalchemy import create_engine, text
import logging

logger = logging.getLogger(__name__)

class ProjectService:
    """Core business logic implementation"""
    
    def __init__(self, engine):
        self.engine = engine
        
    async def process_project_data(self, project_id: str) -> Dict[str, Any]:
        """Process project data with SwarmRAG insights"""
        try:
            # 1. Validate project existence
            project_exists = await self.check_project_id(project_id)
            
            # 2. Get service area details
            service_area = await self.get_service_area(project_id)
            
            # 3. Apply business rules from SwarmRAG analysis
            validated_data = self.apply_business_rules(service_area)
            
            # 4. Update with new requirements
            await self.update_service_area(project_id, validated_data)
            
            return {
                "status": "success",
                "project_id": project_id,
                "processed_data": validated_data
            }
            
        except Exception as e:
            logger.error(f"Error processing project {project_id}: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def get_project(self, project_id: str) -> Optional[Project]:
        """Get project details"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("EXEC usp_CS_EXP_Check_ProjectID @ProjectID = :project_id"),
                    {"project_id": project_id}
                ).scalar()
                
                if result:
                    # Fetch additional project details
                    pass
                return None
        except Exception as e:
            logger.error(f"Error fetching project: {str(e)}")
            return None
    
    async def update_service_area(self, service_area: ServiceArea) -> bool:
        """Update project service area"""
        try:
            with self.engine.connect() as conn:
                conn.execute(
                    text("""
                        EXEC usp_CS_EXP_Project_ServiceArea_Edit 
                        @ProjID = :proj_id, 
                        @Mileage = :mileage, 
                        @Flag = :flag
                    """),
                    {
                        "proj_id": service_area.project_id,
                        "mileage": service_area.mileage,
                        "flag": 1
                    }
                )
                return True
        except Exception as e:
            logger.error(f"Error updating service area: {str(e)}")
            return False 