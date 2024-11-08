from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.core import db
from src.config.settings import get_settings
import logging

logger = logging.getLogger(__name__)

def init_db():
    """Initialize database connection"""
    settings = get_settings()
    
    try:
        engine = create_engine(settings.DATABASE_URL)
        db.metadata.create_all(engine)
        
        Session = sessionmaker(bind=engine)
        return Session()
        
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise 