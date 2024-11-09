from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship, declared_attr
from typing import Any, Dict, List, Optional

class ProjectRelationshipMixin:
    """Mixin for tables with project relationships"""
    
    @declared_attr
    def project_id(cls) -> Column:
        return Column(String(12), ForeignKey('projects.project_id'))
    
    @declared_attr
    def project(cls):
        return relationship(
            "Project",
            back_populates=cls.get_back_populates_name(),
            lazy="joined"
        )
    
    @classmethod
    def get_back_populates_name(cls) -> str:
        return cls.__name__.lower() + 's'

class TranslationRelationshipMixin:
    """Mixin for translation tables"""
    
    @declared_attr
    def record_id(cls) -> Column:
        return Column(Integer, primary_key=True, autoincrement=True)
    
    @declared_attr
    def project_id(cls) -> Column:
        return Column(String(12), ForeignKey('projects.project_id', 
                                           ondelete='CASCADE'))
    
    @declared_attr
    def __table_args__(cls) -> Dict[str, Any]:
        return {
            'postgresql_with': {'fillfactor': '80'},
            'info': {'translation_table': True}
        }

class ServiceAreaRelationshipMixin:
    """Mixin for service area related tables"""
    
    @declared_attr
    def region(cls) -> Column:
        return Column(String(30))
    
    @declared_attr
    def state(cls) -> Column:
        return Column(String(2))
    
    @declared_attr
    def county(cls) -> Column:
        return Column(String(75))

class DocumentRelationshipMixin:
    """Mixin for document relationships"""
    
    @declared_attr
    def user_id(cls) -> Column:
        return Column(Integer, ForeignKey('users.id'))
    
    @declared_attr
    def user(cls):
        return relationship("User", back_populates="documents") 