from sqlalchemy import Column, String
from .base import Base
from .mixins import TranslationMixin, AuditMixin

class CompetitorTranslation(Base, TranslationMixin):
    __tablename__ = 'CS_EXP_Competitor_Translation'
    
    strenuus_product_code = Column(String(50))
    payor = Column(String(50))
    product = Column(String(60))

class Project(Base, AuditMixin):
    __tablename__ = 'projects'
    
    project_id = Column(String(12), unique=True, nullable=False)
    region = Column(String(100))
    workflow_entity_id = Column(String(36)) 