from sqlalchemy import create_engine, text
import logging
from src.config.database import DatabaseConfig
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseCleaner:
    """Clean up test data from database"""
    
    def __init__(self):
        self.engine = create_engine(DatabaseConfig.get_connection_string())
    
    def cleanup_test_data(self, project_ids: List[str]) -> Dict[str, Any]:
        """Remove test data from all relevant tables"""
        cleanup_results = {}
        
        try:
            with self.engine.connect() as conn:
                # Create project IDs string for IN clause
                project_ids_str = "'" + "','".join(project_ids) + "'"
                
                # Clean up Project_Translation
                result = conn.execute(
                    text(f"""
                        DELETE FROM dbo.CS_EXP_Project_Translation 
                        WHERE ProjectID IN ({project_ids_str})
                    """)
                )
                cleanup_results['project_translation'] = result.rowcount
                
                # Clean up zTrxServiceArea
                result = conn.execute(
                    text(f"""
                        DELETE FROM dbo.CS_EXP_zTrxServiceArea 
                        WHERE ProjectID IN ({project_ids_str})
                    """)
                )
                cleanup_results['service_area'] = result.rowcount
                
                # Clean up Sel_PLProducts
                result = conn.execute(
                    text(f"""
                        DELETE FROM dbo.CS_EXP_Sel_PLProducts 
                        WHERE ProjectID IN ({project_ids_str})
                    """)
                )
                cleanup_results['products'] = result.rowcount
                
                conn.commit()
                
                return {
                    'status': 'success',
                    'records_removed': cleanup_results
                }
                
        except Exception as e:
            logger.error(f"Cleanup failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            } 