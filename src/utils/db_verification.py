from sqlalchemy import text, inspect
from typing import List, Dict

class DatabaseVerifier:
    """Verification utility for ndar database"""
    
    REQUIRED_TABLES = [
        'CS_EXP_Project_Translation',
        'CS_EXP_Competitor_Translation',
        'CS_EXP_PlatformLoadProducts',
        'CS_EXP_ProjectNotes',
        'CS_EXP_ProjectNotes_Categories',
        'CS_EXP_Sel_PLProducts',
        'CS_EXP_YLine_Translation',
        'CS_EXP_zTrxServiceArea'
    ]
    
    REQUIRED_PROCEDURES = [
        'uspCsExpCheckProjectId',
        'uspCsExpProjectServiceAreaV2',
        'uspCsExpProjectServiceAreaEditV2',
        'uspCsExpSelCspProducts',
        'uspCsExpZtrxServiceAreaV4'
    ]
    
    def __init__(self, db_engine):
        self.engine = db_engine
        self.inspector = inspect(self.engine)
    
    def verify_database(self) -> Dict[str, bool]:
        """Verify all database components"""
        return {
            'database_connection': self.check_connection(),
            'tables_exist': self.verify_tables(),
            'procedures_exist': self.verify_procedures(),
            'table_permissions': self.check_table_permissions(),
            'procedure_permissions': self.check_procedure_permissions()
        }
    
    def check_connection(self) -> bool:
        """Verify database connection"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT DB_NAME()"))
                return True
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return False
    
    def verify_tables(self) -> bool:
        """Verify required tables exist"""
        existing_tables = self.inspector.get_table_names()
        missing_tables = set(self.REQUIRED_TABLES) - set(existing_tables)
        
        if missing_tables:
            print(f"Missing tables: {missing_tables}")
            return False
        return True
    
    def verify_procedures(self) -> bool:
        """Verify required stored procedures"""
        try:
            with self.engine.connect() as conn:
                for proc in self.REQUIRED_PROCEDURES:
                    result = conn.execute(text(
                        "SELECT OBJECT_ID(?) AS proc_id",
                        [proc]
                    )).scalar()
                    if not result:
                        print(f"Missing procedure: {proc}")
                        return False
            return True
        except Exception as e:
            print(f"Procedure verification error: {str(e)}")
            return False 