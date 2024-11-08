from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
import logging

logger = logging.getLogger(__name__)
Base = declarative_base()

class DatabaseSetup:
    """Database setup and management"""
    
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        self.metadata = MetaData()
        
    def create_required_tables(self):
        """Create any additional required tables"""
        try:
            # Example table creation
            project_metrics = Table(
                'CS_EXP_ProjectMetrics', self.metadata,
                Column('ProjectID', String(12), primary_key=True),
                Column('LastUpdated', DateTime),
                Column('ProcessingTime', Integer),
                Column('Status', String(50))
            )
            
            self.metadata.create_all(self.engine)
            logger.info("Required tables created successfully")
            return True
        except Exception as e:
            logger.error(f"Error creating tables: {str(e)}")
            return False 