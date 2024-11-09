from pydantic import BaseModel
from datetime import datetime

class DocumentBase(BaseModel):
    title: str
    content: str
    user_id: int

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 