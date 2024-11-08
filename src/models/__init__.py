from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()

# Import models after Base is defined
from .project import Project, ServiceArea
