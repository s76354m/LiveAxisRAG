from typing import List, Dict, Any
from sqlalchemy import text

class StoredProcedure:
    """Utility for executing stored procedures"""
    
    def __init__(self, db_session):
        self.session = db_session
    
    def execute(self, proc_name: str, params: Dict[str, Any] = None) -> List[Dict]:
        """Execute stored procedure with parameters"""
        try:
            result = self.session.execute(
                text(f"EXEC {proc_name} {self._format_params(params)}"),
                params or {}
            )
            return [dict(row) for row in result]
        except Exception as e:
            print(f"Error executing {proc_name}: {str(e)}")
            raise
    
    def _format_params(self, params: Dict[str, Any]) -> str:
        """Format stored procedure parameters"""
        if not params:
            return ""
        return " ".join([f"@{k}=:{k}," for k in params.keys()])[:-1] 