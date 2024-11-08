from datetime import datetime
from sqlalchemy import Column, DateTime, String, Integer, Enum, Index
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declarative_base
from src.exceptions import ValidationError

db = declarative_base()

class BaseModel(db.Model):
    """Base model with common fields"""
    __abstract__ = True
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    created_by = db.Column(db.String(100))  # Maps to PowerApps User().Email
    
    @validates('created_by')
    def validate_created_by(self, key, value):
        if not value or '@' not in value:
            raise ValidationError("Invalid email format")
        return value

class Project(BaseModel):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.String(12), unique=True, nullable=False)
    region = db.Column(db.String(100))
    status = db.Column(
        Enum('Active', 'Pending', 'Completed', name='project_status'),
        default='Pending'
    )
    workflow_entity_id = db.Column(db.String(36))
    competitors = relationship("Competitor", back_populates="project")
    
    __table_args__ = (
        Index('idx_project_search', 'project_id', 'status'),
    )
    
    @validates('project_id')
    def validate_project_id(self, key, value):
        if not value or len(value) != 12:
            raise ValidationError("Project ID must be 12 characters")
        return value

class Competitor(BaseModel):
    __tablename__ = 'competitors'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.String(12), ForeignKey('projects.project_id'))
    product = db.Column(db.String(200))
    status = db.Column(
        Enum('Draft', 'Submitted', 'Approved', name='competitor_status'),
        default='Draft'
    )
    project = relationship("Project", back_populates="competitors")