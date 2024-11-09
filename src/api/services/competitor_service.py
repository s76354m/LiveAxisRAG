from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.competitors import CompetitorCreate, CompetitorResponse
from ..database.models import Competitor
from .base import BaseService

class CompetitorService(BaseService[Competitor, CompetitorCreate, CompetitorCreate]):
    async def get_competitors_by_project(
        self, db: Session, project_id: str, skip: int = 0, limit: int = 100
    ) -> List[Competitor]:
        return (
            db.query(Competitor)
            .filter(Competitor.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    async def get_competitors_by_status(
        self, db: Session, status: str, skip: int = 0, limit: int = 100
    ) -> List[Competitor]:
        return (
            db.query(Competitor)
            .filter(Competitor.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

competitor_service = CompetitorService(Competitor) 