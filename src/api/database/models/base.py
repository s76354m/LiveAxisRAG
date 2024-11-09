from sqlalchemy.ext.declarative import declarative_base, declared_attr
from .events import register_model_events

class Model:
    @declared_attr
    def __mapper_args__(cls):
        """Register events for all models"""
        return {
            'listeners': [register_model_events]
        }

Base = declarative_base(cls=Model) 