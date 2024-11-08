from sqlalchemy import create_engine, text
import logging
from src.config.database import DatabaseConfig
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StoredProcedureVerifier:
    """Verify stored procedure functionality"""
    
    def __init__(self):
        self.engine = create_engine(DatabaseConfig.get_connection_string())
    
    def verify_all_procedures(self) -> Dict[str, bool]:
        """Run verification tests for all procedures"""
        results = {}
        
        # Test usp_CS_EXP_Check_ProjectID
        results['usp_CS_EXP_Check_ProjectID'] = self.test_check_project_id()
        
        # Test usp_CS_EXP_SelCSP_Products
        results['usp_CS_EXP_SelCSP_Products'] = self.test_selcsp_products()
        
        # Test usp_CS_EXP_Project_ServiceArea_Edit
        results['usp_CS_EXP_Project_ServiceArea_Edit'] = self.test_project_service_area_edit()
        
        # Test usp_CS_EXP_Project_ServiceArea
        results['usp_CS_EXP_Project_ServiceArea'] = self.test_project_service_area()
        
        # Test usp_CS_EXP_zTrxServiceArea
        results['usp_CS_EXP_zTrxServiceArea'] = self.test_ztrx_service_area()
        
        return results
    
    def test_check_project_id(self) -> bool:
        """Test usp_CS_EXP_Check_ProjectID procedure"""
        try:
            with self.engine.connect() as conn:
                # Test with a non-existent project ID
                result = conn.execute(
                    text("EXEC usp_CS_EXP_Check_ProjectID @ProjectID = :project_id"),
                    {"project_id": "TEST123456789"}
                ).scalar()
                logger.info(f"Check ProjectID test result: {result}")
                return True
        except Exception as e:
            logger.error(f"Error testing Check ProjectID: {str(e)}")
            return False
    
    def test_selcsp_products(self) -> bool:
        """Test usp_CS_EXP_SelCSP_Products procedure"""
        try:
            with self.engine.connect() as conn:
                # Test with flag '1'
                conn.execute(
                    text("EXEC usp_CS_EXP_SelCSP_Products @Flag = :flag"),
                    {"flag": "1"}
                )
                logger.info("SelCSP Products test completed")
                return True
        except Exception as e:
            logger.error(f"Error testing SelCSP Products: {str(e)}")
            return False
    
    def test_project_service_area_edit(self) -> bool:
        """Test usp_CS_EXP_Project_ServiceArea_Edit procedure"""
        try:
            with self.engine.connect() as conn:
                # Test with sample parameters
                conn.execute(
                    text("""
                        EXEC usp_CS_EXP_Project_ServiceArea_Edit 
                        @ProjID = :proj_id, 
                        @Mileage = :mileage, 
                        @Flag = :flag
                    """),
                    {
                        "proj_id": "TEST123456789",
                        "mileage": 10,
                        "flag": 1
                    }
                )
                logger.info("Project Service Area Edit test completed")
                return True
        except Exception as e:
            logger.error(f"Error testing Project Service Area Edit: {str(e)}")
            return False
    
    def test_project_service_area(self) -> bool:
        """Test usp_CS_EXP_Project_ServiceArea procedure"""
        try:
            with self.engine.connect() as conn:
                conn.execute(
                    text("""
                        EXEC usp_CS_EXP_Project_ServiceArea 
                        @ProjID = :proj_id, 
                        @Mileage = :mileage
                    """),
                    {
                        "proj_id": "TEST123456789",
                        "mileage": 10
                    }
                )
                logger.info("Project Service Area test completed")
                return True
        except Exception as e:
            logger.error(f"Error testing Project Service Area: {str(e)}")
            return False
    
    def test_ztrx_service_area(self) -> bool:
        """Test usp_CS_EXP_zTrxServiceArea procedure"""
        try:
            with self.engine.connect() as conn:
                conn.execute(
                    text("EXEC usp_CS_EXP_zTrxServiceArea @ProjectID = :project_id"),
                    {"project_id": "TEST123456789"}
                )
                logger.info("zTrx Service Area test completed")
                return True
        except Exception as e:
            logger.error(f"Error testing zTrx Service Area: {str(e)}")
            return False

def run_verification():
    """Run all stored procedure verifications"""
    verifier = StoredProcedureVerifier()
    results = verifier.verify_all_procedures()
    
    logger.info("\nVerification Results:")
    for proc, success in results.items():
        status = "✓ Passed" if success else "✗ Failed"
        logger.info(f"{status}: {proc}")
    
    return all(results.values())

if __name__ == "__main__":
    logger.info("Starting stored procedure verification...")
    success = run_verification()
    if success:
        logger.info("\nAll procedures verified successfully")
    else:
        logger.error("\nSome procedures failed verification")