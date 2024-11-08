import pyodbc
import logging
from src.config.database import DatabaseConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StoredProcedureMigration:
    """Handles stored procedure migrations for ndar database"""
    
    def __init__(self):
        self.conn_str = DatabaseConfig.get_pyodbc_string()
    
    def create_all_procedures(self):
        """Create all required stored procedures"""
        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()
            
            procedures = {
                'usp_CS_EXP_Check_ProjectID': self._get_check_project_id_proc(),
                'usp_CS_EXP_SelCSP_Products': self._get_selcsp_products_proc(),
                'usp_CS_EXP_Project_ServiceArea_Edit': self._get_project_service_area_edit_proc(),
                'usp_CS_EXP_Project_ServiceArea': self._get_project_service_area_proc(),
                'usp_CS_EXP_zTrxServiceArea': self._get_ztrx_service_area_proc()
            }
            
            for proc_name, proc_sql in procedures.items():
                logger.info(f"Creating procedure: {proc_name}")
                try:
                    # Drop if exists
                    cursor.execute(f"""
                        IF OBJECT_ID('{proc_name}', 'P') IS NOT NULL
                            DROP PROCEDURE {proc_name}
                    """)
                    cursor.commit()
                    
                    # Create new procedure
                    cursor.execute(proc_sql)
                    cursor.commit()
                    logger.info(f"Successfully created {proc_name}")
                except Exception as e:
                    logger.error(f"Error creating {proc_name}: {str(e)}")
                    
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"Migration failed: {str(e)}")
            return False
    
    def _get_check_project_id_proc(self) -> str:
        return """
        CREATE PROCEDURE [dbo].[usp_CS_EXP_Check_ProjectID]
            @ProjectID VARCHAR(12)
        AS
        BEGIN
            SET NOCOUNT ON;
            
            IF EXISTS(SELECT NULL FROM dbo.CS_EXP_Project_Translation WHERE ProjectID = @ProjectID)
            BEGIN
                SELECT 1 AS 'Exists';
            END
            ELSE
            BEGIN
                SELECT 0 AS 'Exists'
            END
        END
        """
    
    def _get_selcsp_products_proc(self) -> str:
        return """
        CREATE PROCEDURE [dbo].[usp_CS_EXP_SelCSP_Products] 
            @Flag varchar
        WITH EXECUTE AS 'dbo'    
        AS
        BEGIN
            SET NOCOUNT ON;
            -- ... (full procedure implementation)
        END
        """
    
    def _get_project_service_area_edit_proc(self) -> str:
        return """
        CREATE PROCEDURE [dbo].[usp_CS_EXP_Project_ServiceArea_Edit] 
            @ProjID NVARCHAR(12), 
            @Mileage int, 
            @Flag int
        WITH EXECUTE AS 'dbo'    
        AS
        BEGIN
            SET NOCOUNT OFF;
            -- ... (full procedure implementation)
        END
        """
    
    def _get_project_service_area_proc(self) -> str:
        return """
        CREATE PROCEDURE [dbo].[usp_CS_EXP_Project_ServiceArea] 
            @ProjID NVARCHAR(12), 
            @Mileage int
        WITH EXECUTE AS 'dbo'  
        AS
        BEGIN
            SET NOCOUNT OFF;
            -- ... (full procedure implementation)
        END
        """
    
    def _get_ztrx_service_area_proc(self) -> str:
        return """
        CREATE PROCEDURE [dbo].[usp_CS_EXP_zTrxServiceArea]
            @ProjectID NVARCHAR(12)
        AS
        BEGIN
            SET NOCOUNT ON;
            -- ... (full procedure implementation)
        END
        """ 