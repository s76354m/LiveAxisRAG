from sqlalchemy import create_engine, text
import logging
from src.config.database import DatabaseConfig
from src.utils.test_data import TestData, TestDataGenerator
from src.utils.cleanup import DatabaseCleaner
from src.utils.performance import measure_time
from typing import Dict, Any, List, Tuple
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StoredProcedureTester:
    """Comprehensive stored procedure testing with metrics"""
    
    def __init__(self):
        self.engine = create_engine(DatabaseConfig.get_connection_string())
        self.test_data = TestDataGenerator()
        self.cleaner = DatabaseCleaner()
        self.tested_project_ids = []
    
    @measure_time
    def run_comprehensive_tests(self) -> Dict[str, Dict[str, Any]]:
        """Run comprehensive tests for all procedures"""
        start_time = time.time()
        results = {}
        
        try:
            # Generate test data
            test_records = self.test_data.generate_test_data(count=3)
            self.tested_project_ids = [record.project_id for record in test_records]
            
            for test_record in test_records:
                logger.info(f"\nTesting with Project ID: {test_record.project_id}")
                
                # Test sequence
                results[test_record.project_id] = {
                    'check_project': self.test_check_project_id(test_record),
                    'service_area': self.test_service_area_workflow(test_record),
                    'products': self.test_products_workflow(test_record)
                }
            
            return results
            
        finally:
            # Clean up test data
            logger.info("\nCleaning up test data...")
            cleanup_result = self.cleaner.cleanup_test_data(self.tested_project_ids)
            logger.info(f"Cleanup result: {cleanup_result}")
    
    @measure_time
    def test_check_project_id(self, test_data: TestData) -> Dict[str, Any]:
        """Test project ID check with validation"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("EXEC usp_CS_EXP_Check_ProjectID @ProjectID = :project_id"),
                    {"project_id": test_data.project_id}
                ).scalar()
                
                return {
                    'status': 'success',
                    'exists': bool(result),
                    'project_id': test_data.project_id
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'project_id': test_data.project_id
            }
    
    @measure_time
    def test_service_area_workflow(self, test_data: TestData) -> Dict[str, Any]:
        """Test complete service area workflow"""
        results = {}
        workflow_times = {}
        
        try:
            with self.engine.connect() as conn:
                # 1. Create service area
                start = time.time()
                conn.execute(
                    text("""
                        EXEC usp_CS_EXP_Project_ServiceArea 
                        @ProjID = :proj_id, 
                        @Mileage = :mileage
                    """),
                    {
                        "proj_id": test_data.project_id,
                        "mileage": test_data.mileage
                    }
                )
                workflow_times['create'] = f"{time.time() - start:.3f}s"
                results['create'] = 'success'
                
                # 2. Edit service area
                start = time.time()
                conn.execute(
                    text("""
                        EXEC usp_CS_EXP_Project_ServiceArea_Edit 
                        @ProjID = :proj_id, 
                        @Mileage = :mileage, 
                        @Flag = :flag
                    """),
                    {
                        "proj_id": test_data.project_id,
                        "mileage": test_data.mileage + 10,
                        "flag": 1
                    }
                )
                workflow_times['edit'] = f"{time.time() - start:.3f}s"
                results['edit'] = 'success'
                
                # 3. Verify in zTrxServiceArea
                start = time.time()
                conn.execute(
                    text("EXEC usp_CS_EXP_zTrxServiceArea @ProjectID = :project_id"),
                    {"project_id": test_data.project_id}
                )
                workflow_times['verify'] = f"{time.time() - start:.3f}s"
                results['verify'] = 'success'
                
                return {
                    'status': 'success',
                    'workflow_results': results,
                    'execution_times': workflow_times
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'workflow_results': results,
                'execution_times': workflow_times
            }
    
    @measure_time
    def test_products_workflow(self, test_data: TestData) -> Dict[str, Any]:
        """Test products workflow"""
        flag_times = {}
        
        try:
            with self.engine.connect() as conn:
                # Test all flags
                for flag in ['1', '2', '3']:
                    start = time.time()
                    conn.execute(
                        text("EXEC usp_CS_EXP_SelCSP_Products @Flag = :flag"),
                        {"flag": flag}
                    )
                    flag_times[f'flag_{flag}'] = f"{time.time() - start:.3f}s"
                
                return {
                    'status': 'success',
                    'flags_tested': ['1', '2', '3'],
                    'execution_times': flag_times
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'execution_times': flag_times
            }

def run_comprehensive_testing():
    """Run comprehensive testing suite with metrics"""
    start_time = time.time()
    tester = StoredProcedureTester()
    results = tester.run_comprehensive_tests()
    
    logger.info("\nComprehensive Test Results:")
    for project_id, test_results in results.items():
        if project_id != 'execution_time':  # Skip execution time entry
            logger.info(f"\nProject ID: {project_id}")
            for test_name, result in test_results.items():
                status = "✓" if result.get('status') == 'success' else "✗"
                logger.info(f"{status} {test_name}:")
                # Remove execution_time from result display
                display_result = {k: v for k, v in result.items() if k != 'execution_time'}
                logger.info(f"  Results: {display_result}")
                if 'execution_times' in result:
                    logger.info(f"  Timing: {result['execution_times']}")
    
    total_time = time.time() - start_time
    logger.info(f"\nTotal test execution time: {total_time:.3f}s")
    
    return all(
        all(r.get('status') == 'success' for r in test_results.values())
        for project_id, test_results in results.items()
        if project_id != 'execution_time'
    )

if __name__ == "__main__":
    logger.info("Starting comprehensive stored procedure testing...")
    success = run_comprehensive_testing()
    if success:
        logger.info("\nAll comprehensive tests passed successfully")
    else:
        logger.error("\nSome comprehensive tests failed") 