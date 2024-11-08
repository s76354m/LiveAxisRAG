from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class Project:
    """Project data model"""
    project_id: str
    state: str
    county: Optional[str] = None
    mileage: Optional[float] = None
    status: str = 'Active'
    last_updated: datetime = datetime.now()

@dataclass
class ServiceArea:
    """Service area data model"""
    project_id: str
    region: Optional[str]
    state: str
    county: Optional[str]
    mileage: float
    report_include: bool = True 