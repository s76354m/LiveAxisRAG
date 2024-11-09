from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from ..models.projects import ProjectCreate, ProjectResponse
from ..database import get_db
from ..services import project_service

router = APIRouter()

@router.post("/projects/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    db_project = await project_service.get_project_by_id(db, project_id=project.project_id)
    if db_project:
        raise HTTPException(status_code=400, detail="Project ID already exists")
    return await project_service.create_project(db=db, project=project)

@router.get("/projects/", response_model=List[ProjectResponse])
async def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = await project_service.get_projects(db, skip=skip, limit=limit)
    return projects

@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def read_project(project_id: str, db: Session = Depends(get_db)):
    db_project = await project_service.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: str, project: ProjectCreate, db: Session = Depends(get_db)):
    db_project = await project_service.update_project(db, project_id=project_id, project=project)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project 