from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
from .relationship_mixins import ProjectRelationshipMixin, TranslationRelationshipMixin
import enum

class CompetitorStatus(str, enum.Enum):
    DRAFT = "Draft"
    SUBMITTED = "Submitted"
    APPROVED = "Approved"

class Competitor(Base, ProjectRelationshipMixin, TimestampMixin):
    __tablename__ = 'competitors'

    id = Column(Integer, primary_key=True)
    product = Column(String(200))
    status = Column(Enum(CompetitorStatus))
    created_by = Column(String(100))

    project = relationship("Project", back_populates="competitors")

class CompetitorTranslation(Base, TranslationRelationshipMixin):
    __tablename__ = 'CS_EXP_Competitor_Translation'

    strenuus_product_code = Column(String(50))
    payor = Column(String(50))
    product = Column(String(60))
    ei = Column(Boolean)
    cs = Column(Boolean)
    mr = Column(Boolean)
    data_load_date = Column(DateTime)
    last_edit_msid = Column(String(15)) 