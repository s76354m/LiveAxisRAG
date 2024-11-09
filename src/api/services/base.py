from sqlalchemy.orm import Session
from datetime import datetime
from typing import Generic, TypeVar, Type, Optional, List
from pydantic import BaseModel
from sqlalchemy.ext.declarative import DeclarativeMeta

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    async def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    async def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        obj_data = obj_in.dict()
        obj_data["created_at"] = datetime.utcnow()
        obj_data["updated_at"] = datetime.utcnow()
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def update(self, db: Session, id: int, obj_in: UpdateSchemaType) -> Optional[ModelType]:
        obj_data = obj_in.dict(exclude_unset=True)
        obj_data["updated_at"] = datetime.utcnow()
        db.query(self.model).filter(self.model.id == id).update(obj_data)
        db.commit()
        return await self.get(db, id) 