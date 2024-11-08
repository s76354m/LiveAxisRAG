from typing import Dict, Any, List
from sqlalchemy.engine import Engine
from sqlalchemy import inspect
import asyncio

class DatabaseVerifier:
    def __init__(self, engine: Engine):
        self.engine = engine
        self.inspector = inspect(engine)

    async def verify_tables(self) -> Dict[str, Any]:
        """Verify all required tables exist"""
        try:
            tables = self.inspector.get_table_names()
            return {
                "status": "success",
                "tables": tables
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    async def verify_constraints(self) -> Dict[str, Any]:
        """Verify table constraints"""
        try:
            constraints = {}
            for table in self.inspector.get_table_names():
                constraints[table] = self.inspector.get_foreign_keys(table)
            return {
                "status": "success",
                "constraints": constraints
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    async def verify_indexes(self) -> Dict[str, Any]:
        """Verify table indexes"""
        try:
            indexes = {}
            for table in self.inspector.get_table_names():
                indexes[table] = self.inspector.get_indexes(table)
            return {
                "status": "success",
                "indexes": indexes
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }