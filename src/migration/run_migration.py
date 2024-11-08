import argparse
from pathlib import Path
import logging
from .migration_plan import DataMigration

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
        description="Execute PowerApps data migration"
    )
    parser.add_argument(
        "--source-path",
        type=str,
        required=True,
        help="Path to PowerApps export files"
    )
    
    args = parser.parse_args()
    
    # Execute migration
    migration = DataMigration(args.source_path)
    results = migration.execute_migration()
    
    # Log results
    if results["status"] == "success":
        logger.info(
            f"Migration completed successfully. "
            f"Migrated {results['migrated_records']} records."
        )
    else:
        logger.error(
            f"Migration failed: {results.get('reason', 'Unknown error')}"
        )

if __name__ == "__main__":
    main() 