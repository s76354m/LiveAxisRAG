from urllib.parse import quote_plus

class DatabaseConfig:
    """SQL Server configuration"""
    
    # SQL Server connection details
    SERVER = 'DESKTOP-PJTAP42'  # Remove SQLEXPRESS from server name
    INSTANCE = 'SQLEXPRESS'     # Specify instance separately
    DATABASE = 'ndar'
    DRIVER = '{SQL Server}'     # Use exact driver name in braces
    
    @classmethod
    def get_connection_string(cls) -> str:
        """Generate SQL Server connection string"""
        server = f"{cls.SERVER}\\{cls.INSTANCE}"
        params = {
            'DRIVER': cls.DRIVER,
            'SERVER': server,
            'DATABASE': cls.DATABASE,
            'Trusted_Connection': 'yes',
            'TrustServerCertificate': 'yes'
        }
        
        connection_str = ';'.join([f'{k}={v}' for k, v in params.items()])
        return f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_str)}"

    @classmethod
    def get_pyodbc_string(cls) -> str:
        """Get raw connection string for testing"""
        server = f"{cls.SERVER}\\{cls.INSTANCE}"
        return (
            f"DRIVER={cls.DRIVER};"
            f"SERVER={server};"
            f"DATABASE={cls.DATABASE};"
            f"Trusted_Connection=yes;"
            f"TrustServerCertificate=yes"
        )

class Config:
    """Application configuration"""
    SQLALCHEMY_DATABASE_URI = DatabaseConfig.get_connection_string()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_timeout': 30,
        'pool_recycle': 1800
    } 