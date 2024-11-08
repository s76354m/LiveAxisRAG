import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from sqlalchemy import create_engine
from src.config.database import DatabaseConfig
from src.utils.verify_procedures import ProcedureVerifier
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_deployment():
    """Verify stored procedures deployment"""
    try:
        # Create engine
        engine = create_engine(DatabaseConfig.get_connection_string())
        
        # Initialize verifier
        verifier = ProcedureVerifier(engine)
        
        # Run verification
        logger.info("Verifying stored procedures...")
        results = verifier.verify_all()
        
        # Log results
        all_valid = True
        for proc_name, details in results.items():
            if details['exists']:
                logger.info(f"✓ {proc_name} exists")
                if details['definition']:
                    logger.debug(f"Definition length: {len(details['definition'])} characters")
            else:
                logger.error(f"✗ {proc_name} missing")
                all_valid = False
        
        return all_valid
        
    except Exception as e:
        logger.error(f"Verification failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = verify_deployment()
    if success:
        print("\nAll stored procedures verified successfully")
    else:
        print("\nVerification failed - check logs for details") 