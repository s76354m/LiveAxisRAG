from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from ..models.competitors import CompetitorCreate, CompetitorResponse
from ..database import get_db
from ..services import competitor_service

router = APIRouter()

@router.post("/competitors/", response_model=CompetitorResponse, status_code=status.HTTP_201_CREATED)
async def create_competitor(competitor: CompetitorCreate, db: Session = Depends(get_db)):
    return await competitor_service.create_competitor(db=db, competitor=competitor)

@router.get("/competitors/", response_model=List[CompetitorResponse])
async def read_competitors(
    project_id: str = None, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    competitors = await competitor_service.get_competitors(
        db, project_id=project_id, skip=skip, limit=limit
    )
    return competitors

@router.get("/competitors/{competitor_id}", response_model=CompetitorResponse)
async def read_competitor(competitor_id: int, db: Session = Depends(get_db)):
    db_competitor = await competitor_service.get_competitor(db, competitor_id=competitor_id)
    if db_competitor is None:
        raise HTTPException(status_code=404, detail="Competitor not found")
    return db_competitor 