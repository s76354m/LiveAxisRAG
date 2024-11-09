import os
import sys
import subprocess
import pyodbc

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.database import DatabaseConfig

def check_sql_server_running():
    try:
        # Check SQL Server service status
        result = subprocess.run(['sc', 'query', 'MSSQL$SQLEXPRESS'], capture_output=True, text=True)
        return "RUNNING" in result.stdout
    except Exception as e:
        print(f"Error checking SQL Server service: {e}")
        return False

def list_sql_drivers():
    try:
        drivers = [driver for driver in pyodbc.drivers()]
        return drivers
    except Exception as e:
        print(f"Error listing SQL drivers: {e}")
        return []

def test_connection():
    print("\n=== SQL Server Connection Test ===")
    
    # Check SQL Server service
    print("\n1. Checking SQL Server service...")
    if check_sql_server_running():
        print("✅ SQL Server service is running")
    else:
        print("❌ SQL Server service is not running")
    
    # List available drivers
    print("\n2. Available SQL Server drivers:")
    drivers = list_sql_drivers()
    for driver in drivers:
        print(f"   - {driver}")
    
    # Test database connection
    print("\n3. Testing database connection...")
    print(f"Server: {DatabaseConfig.SERVER}")
    print(f"Instance: {DatabaseConfig.INSTANCE}")
    print(f"Database: {DatabaseConfig.DATABASE}")
    print(f"Driver: {DatabaseConfig.DRIVER}")
    
    if DatabaseConfig.test_connection():
        print("✅ Database connection successful!")
    else:
        print("❌ Database connection failed!")
        print("\nTroubleshooting steps:")
        print("1. Verify SQL Server service is running:")
        print("   - Open Services (services.msc)")
        print("   - Look for 'SQL Server (SQLEXPRESS)'")
        print("   - Ensure it's running")
        print("\n2. Check SQL Server Browser service:")
        print("   - Look for 'SQL Server Browser' in Services")
        print("   - Start it if not running")
        print("\n3. Enable TCP/IP:")
        print("   - Open SQL Server Configuration Manager")
        print("   - SQL Server Network Configuration > Protocols for SQLEXPRESS")
        print("   - Enable TCP/IP")
        print("   - Restart SQL Server service")

if __name__ == "__main__":
    test_connection() 