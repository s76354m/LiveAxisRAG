from typing import Dict, Any
from sqlalchemy.engine import Engine
from sqlalchemy import text
import time

class ConnectionTester:
    def __init__(self, engine: Engine):
        self.engine = engine

    async def test_connection(self) -> Dict[str, Any]:
        """Test database connection and measure latency"""
        try:
            start_time = time.perf_counter()
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            latency = time.perf_counter() - start_time
            
            return {
                "status": "success",
                "latency": latency,
                "timestamp": time.time()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": time.time()
            }

    def run_connection_tests(self) -> Dict[str, Any]:
        """Run a series of connection tests"""
        try:
            results = []
            for _ in range(3):
                with self.engine.connect() as conn:
                    start = time.perf_counter()
                    conn.execute(text("SELECT 1"))
                    end = time.perf_counter()
                    results.append(end - start)
            
            return {
                "status": "success",
                "avg_latency": sum(results) / len(results),
                "min_latency": min(results),
                "max_latency": max(results),
                "tests_run": len(results)
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }