import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.append(project_root)

from sqlalchemy import create_engine
from src.config.database import DatabaseConfig
from src.migrations.stored_procedures import StoredProcedureMigration
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    """Run all database migrations"""
    try:
        # Create engine
        engine = create_engine(DatabaseConfig.get_connection_string())
        
        # Initialize migration
        sp_migration = StoredProcedureMigration(engine)
        
        # Run stored procedure migrations
        logger.info("Starting stored procedure migrations...")
        results = sp_migration.create_all_procedures()
        
        # Log results
        for result in results:
            if result['status'] == 'success':
                logger.info(f"Created {result['procedure']}: {result['message']}")
            else:
                logger.error(f"Failed {result['procedure']}: {result['message']}")
        
        return True
        
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_migrations()
    if success:
        print("Migrations completed successfully")
    else:
        print("Migration failed - check logs for details") 