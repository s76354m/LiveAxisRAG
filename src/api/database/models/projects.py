from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
from .mixins import AuditMixin, ValidationMixin
from .events import register_project_events
import enum

class ProjectStatus(str, enum.Enum):
    ACTIVE = "Active"
    PENDING = "Pending"
    COMPLETED = "Completed"

class Project(Base, TimestampMixin, AuditMixin, ValidationMixin):
    __tablename__ = 'projects'

    __mapper_args__ = {
        'listeners': [register_project_events]
    }

    id = Column(Integer, primary_key=True)
    project_id = Column(String(12), unique=True, nullable=False)
    region = Column(String(100))
    status = Column(Enum(ProjectStatus))
    workflow_entity_id = Column(String(36))
    created_by = Column(String(100))

    competitors = relationship("Competitor", back_populates="project")
    notes = relationship("ProjectNote", back_populates="project")
    service_areas = relationship("ServiceArea", back_populates="project")

    @validates('region')
    def validate_region(self, key, value):
        if value and len(value) > 100:
            raise ValueError("Region name cannot exceed 100 characters")
        return value

class ProjectNote(Base):
    __tablename__ = 'CS_EXP_ProjectNotes'

    RecordID = Column(Integer, primary_key=True, autoincrement=True)
    ProjectID = Column(String(12), ForeignKey('projects.project_id'))
    Notes = Column(String)
    ActionItem = Column(String(3))
    ProjectStatus = Column(String(8))
    DataLoadDate = Column(DateTime)
    LastEditDate = Column(DateTime)
    OrigNoteMSID = Column(String(15))
    LastEditMSID = Column(String(15))
    ProjectCategory = Column(String(50))

    project = relationship("Project", back_populates="notes") 