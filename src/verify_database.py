from utils.db_verification import DatabaseVerifier
from utils.connection_test import ConnectionTester
from config.database import DatabaseConfig
from sqlalchemy import create_engine

def main():
    """Verify database setup and connections"""
    
    # Create engine
    engine = create_engine(DatabaseConfig.get_connection_string())
    
    # Initialize verifiers
    db_verifier = DatabaseVerifier(engine)
    conn_tester = ConnectionTester(engine, DatabaseConfig)
    
    print("Starting database verification...")
    
    # Run verifications
    db_status = db_verifier.verify_database()
    conn_status = conn_tester.run_connection_tests()
    
    # Print results
    print("\nDatabase Verification Results:")
    for key, value in db_status.items():
        print(f"{key}: {'✓' if value else '✗'}")
    
    print("\nConnection Test Results:")
    for key, value in conn_status.items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for k, v in value.items():
                print(f"  {k}: {v}")
        else:
            print(f"{key}: {value}")

if __name__ == "__main__":
    main() 