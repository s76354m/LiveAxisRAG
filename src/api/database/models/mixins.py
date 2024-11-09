from sqlalchemy import Column, DateTime, String, Integer, event
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import validates
from datetime import datetime
import re

class ValidationMixin:
    @validates('project_id')
    def validate_project_id(self, key, value):
        if not value:
            raise ValueError("Project ID cannot be empty")
        if not re.match(r'^[A-Z0-9]{12}$', value):
            raise ValueError("Project ID must be 12 characters alphanumeric")
        return value

    @validates('email')
    def validate_email(self, key, value):
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
            raise ValueError("Invalid email format")
        return value

    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['Active', 'Pending', 'Completed', 'Draft', 'Submitted', 'Approved']
        if value not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value

class EventMixin:
    @classmethod
    def __declare_last__(cls):
        event.listen(cls, 'before_update', cls._before_update)
        event.listen(cls, 'before_insert', cls._before_insert)
        
    @staticmethod
    def _before_update(mapper, connection, target):
        target.updated_at = datetime.utcnow()
        
    @staticmethod
    def _before_insert(mapper, connection, target):
        now = datetime.utcnow()
        target.created_at = now
        target.updated_at = now

class AuditMixin(EventMixin):
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    created_by = Column(String(100))
    last_edit_msid = Column(String(15))

    def track_change(self, user_id: str):
        self.last_edit_msid = user_id
        self.updated_at = datetime.utcnow()

    @validates('created_by')
    def validate_created_by(self, key, value):
        if not value:
            raise ValueError("created_by cannot be empty")
        return value

class TranslationMixin(ValidationMixin):
    @declared_attr
    def __tablename__(cls):
        return f"CS_EXP_{cls.__name__}"

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String(12), nullable=False)
    project_status = Column(String(10))
    data_load_date = Column(DateTime)
    last_edit_date = Column(DateTime)
    last_edit_msid = Column(String(15))

    @declared_attr
    def __table_args__(cls):
        return {
            'postgresql_with': {'fillfactor': '80'},
            'info': {'translation_table': True}
        }

    @validates('project_status')
    def validate_project_status(self, key, value):
        if value and len(value) > 10:
            raise ValueError("Project status cannot exceed 10 characters")
        return value