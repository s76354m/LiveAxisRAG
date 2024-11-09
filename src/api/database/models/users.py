from sqlalchemy import Column, Integer, String, Boolean
from .base import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True) 