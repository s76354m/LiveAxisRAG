from sqlalchemy import event
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session, Mapper
from datetime import datetime
import logging
from typing import Any

logger = logging.getLogger(__name__)

def register_model_events(mapper: Mapper, class_: Any) -> None:
    """Register all model events for a given class"""
    
    @event.listens_for(class_, 'before_insert')
    def before_insert(mapper: Mapper, connection: Connection, target: Any) -> None:
        """Handle before insert events"""
        now = datetime.utcnow()
        if hasattr(target, 'created_at'):
            target.created_at = now
        if hasattr(target, 'updated_at'):
            target.updated_at = now
        if hasattr(target, 'DataLoadDate'):
            target.DataLoadDate = now
        
        logger.debug(f"Before insert: {class_.__name__} {getattr(target, 'id', '')}")

    @event.listens_for(class_, 'before_update')
    def before_update(mapper: Mapper, connection: Connection, target: Any) -> None:
        """Handle before update events"""
        now = datetime.utcnow()
        if hasattr(target, 'updated_at'):
            target.updated_at = now
        if hasattr(target, 'LastEditDate'):
            target.LastEditDate = now
            
        logger.debug(f"Before update: {class_.__name__} {getattr(target, 'id', '')}")

    @event.listens_for(class_, 'after_delete')
    def after_delete(mapper: Mapper, connection: Connection, target: Any) -> None:
        """Handle after delete events"""
        logger.info(f"Deleted: {class_.__name__} {getattr(target, 'id', '')}")

def register_project_events(mapper: Mapper, class_: Any) -> None:
    """Register project-specific events"""
    
    @event.listens_for(class_, 'before_update')
    def before_project_update(mapper: Mapper, connection: Connection, target: Any) -> None:
        """Handle project status changes"""
        if hasattr(target, 'status'):
            history = getattr(target, 'status').history
            if history.has_changes():
                old_status = history.deleted[0] if history.deleted else None
                new_status = history.added[0] if history.added else None
                logger.info(f"Project status change: {old_status} -> {new_status}")

def register_competitor_events(mapper: Mapper, class_: Any) -> None:
    """Register competitor-specific events"""
    
    @event.listens_for(class_, 'before_insert')
    def before_competitor_insert(mapper: Mapper, connection: Connection, target: Any) -> None:
        """Handle new competitor creation"""
        if hasattr(target, 'status'):
            target.status = 'Draft'  # Default status for new competitors

def register_translation_events(mapper: Mapper, class_: Any) -> None:
    """Register translation table events"""
    
    @event.listens_for(class_, 'before_insert')
    def before_translation_insert(mapper: Mapper, connection: Connection, target: Any) -> None:
        """Handle translation record creation"""
        if hasattr(target, 'DataLoadDate'):
            target.DataLoadDate = datetime.utcnow() 