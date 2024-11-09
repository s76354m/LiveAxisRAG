from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class CompetitorStatus(str, Enum):
    DRAFT = "Draft"
    SUBMITTED = "Submitted"
    APPROVED = "Approved"

class CompetitorBase(BaseModel):
    project_id: str
    product: str
    status: CompetitorStatus

class CompetitorCreate(CompetitorBase):
    pass

class CompetitorResponse(CompetitorBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: str

    class Config:
        from_attributes = True 