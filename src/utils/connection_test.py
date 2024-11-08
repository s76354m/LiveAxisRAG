from contextlib import contextmanager
from typing import Generator, List
import time

class ConnectionTester:
    """Connection testing utility for ndar database"""
    
    def __init__(self, db_engine, config):
        self.engine = db_engine
        self.config = config
    
    def run_connection_tests(self) -> Dict[str, Any]:
        """Run comprehensive connection tests"""
        results = {
            'basic_connection': self.test_basic_connection(),
            'connection_pool': self.test_connection_pool(),
            'transaction_handling': self.test_transaction(),
            'stored_proc_access': self.test_stored_procedures(),
            'performance': self.test_connection_performance()
        }
        return results
    
    def test_basic_connection(self) -> Dict[str, Any]:
        """Test basic database connectivity"""
        start_time = time.time()
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT @@VERSION"))
                return {
                    'success': True,
                    'latency': time.time() - start_time,
                    'message': 'Connection successful'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Connection failed'
            }
    
    def test_stored_procedures(self) -> Dict[str, List[str]]:
        """Test stored procedure accessibility"""
        accessible_procs = []
        failed_procs = []
        
        for proc in DatabaseVerifier.REQUIRED_PROCEDURES:
            try:
                with self.engine.connect() as conn:
                    # Try to get procedure definition
                    conn.execute(text(
                        f"SELECT OBJECT_DEFINITION(OBJECT_ID('{proc}'))"
                    ))
                    accessible_procs.append(proc)
            except Exception:
                failed_procs.append(proc)
        
        return {
            'accessible': accessible_procs,
            'failed': failed_procs
        } 