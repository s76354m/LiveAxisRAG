from typing import TypeVar, Generic, List, Optional
from sqlalchemy.exc import SQLAlchemyError
from src.exceptions import RepositoryError

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, model: T):
        self.model = model
    
    def get_by_id(self, id: int) -> Optional[T]:
        try:
            return self.model.query.get(id)
        except SQLAlchemyError as e:
            raise RepositoryError(f"Error retrieving {self.model.__name__}: {str(e)}")
    
    def create(self, **kwargs) -> T:
        try:
            instance = self.model(**kwargs)
            db.session.add(instance)
            db.session.commit()
            return instance
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RepositoryError(f"Error creating {self.model.__name__}: {str(e)}")
    
    def update(self, id: int, **kwargs) -> Optional[T]:
        try:
            instance = self.get_by_id(id)
            if instance:
                for key, value in kwargs.items():
                    setattr(instance, key, value)
                db.session.commit()
            return instance
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RepositoryError(f"Error updating {self.model.__name__}: {str(e)}") 