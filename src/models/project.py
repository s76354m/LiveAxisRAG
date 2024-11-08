from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(String(50), unique=True, nullable=False)
    region = Column(String(50))
    status = Column(String(20))
    created_by = Column(String(100))
    
    service_area = relationship("ServiceArea", back_populates="project", uselist=False)
    
    def __repr__(self):
        return f"<Project(project_id='{self.project_id}', region='{self.region}')>"

class ServiceArea(Base):
    __tablename__ = 'service_areas'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    state = Column(String(2))
    county = Column(String(100))
    mileage = Column(Float)
    
    project = relationship("Project", back_populates="service_area")
    
    def __repr__(self):
        return f"<ServiceArea(state='{self.state}', county='{self.county}')>"