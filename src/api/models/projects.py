from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class ProjectStatus(str, Enum):
    ACTIVE = "Active"
    PENDING = "Pending"
    COMPLETED = "Completed"

class ProjectBase(BaseModel):
    project_id: str
    region: Optional[str] = None
    status: ProjectStatus
    workflow_entity_id: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: str

    class Config:
        from_attributes = True 