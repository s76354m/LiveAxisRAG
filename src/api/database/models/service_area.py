from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class ServiceArea(Base):
    __tablename__ = 'CS_EXP_zTrxServiceArea'

    RecordID = Column(Integer, primary_key=True, autoincrement=True)
    ProjectID = Column(String(12), ForeignKey('projects.project_id'))
    Region = Column(String(30))
    State = Column(String(2))
    County = Column(String(75))
    ReportInclude = Column(String(1))
    MaxMileage = Column(Integer)
    DataLoadDate = Column(DateTime)
    ProjectStatus = Column(String(10))

    project = relationship("Project", back_populates="service_areas") 