from typing import Optional
from src.models.core import Project
from src.exceptions import ProjectValidationError

class ProjectService:
    @staticmethod
    def validate_project_id(project_id: str) -> bool:
        """Maps to PowerApps CheckProjectID"""
        if not project_id or len(project_id) != 12:
            raise ProjectValidationError("Invalid project ID format")
            
        project = Project.query.filter_by(project_id=project_id).first()
        if not project:
            raise ProjectValidationError("Project not found")
            
        return True
        
    @staticmethod
    def get_project_status(project_id: str) -> Optional[str]:
        """Maps to PowerApps GetProjectStatus"""
        project = Project.query.filter_by(project_id=project_id).first()
        return project.status if project else None 