from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.projects import ProjectCreate, ProjectResponse
from ..database.models import Project
from .base import BaseService

class ProjectService(BaseService[Project, ProjectCreate, ProjectCreate]):
    async def get_project_by_id(self, db: Session, project_id: str) -> Optional[Project]:
        return db.query(Project).filter(Project.project_id == project_id).first()

    async def get_projects_by_status(
        self, db: Session, status: str, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        return (
            db.query(Project)
            .filter(Project.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    async def get_projects_by_region(
        self, db: Session, region: str, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        return (
            db.query(Project)
            .filter(Project.region == region)
            .offset(skip)
            .limit(limit)
            .all()
        )

project_service = ProjectService(Project) 