#!/usr/bin/env python3
"""
Database Connection Test Script

This script validates database connectivity using the configuration settings
defined in config.py. It can be used to verify that the database is accessible
and properly configured before running the main application.

Usage:
    python test_db_connection.py
"""

import sys
import os
from datetime import datetime

try:
    import psycopg2
    from psycopg2 import OperationalError, ProgrammingError
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.exc import SQLAlchemyError
    HAS_SQLALCHEMY = True
except ImportError:
    HAS_SQLALCHEMY = False

from config import DatabaseConfig


def test_with_psycopg2():
    """
    Test database connection using psycopg2 directly.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    if not HAS_PSYCOPG2:
        print("❌ psycopg2 is not installed. Skipping psycopg2 test.")
        print("   Install it with: pip install psycopg2-binary")
        return False
    
    print("\n" + "="*60)
    print("Testing Database Connection with psycopg2")
    print("="*60)
    
    try:
        conn_params = DatabaseConfig.get_connection_params()
        print(f"\nConnecting to database:")
        print(f"  Host: {conn_params['host']}")
        print(f"  Port: {conn_params['port']}")
        print(f"  Database: {conn_params['database']}")
        print(f"  User: {conn_params['user']}")
        print(f"  Timeout: {conn_params['connect_timeout']}s")
        
        # Attempt to connect
        conn = psycopg2.connect(**conn_params)
        
        # Create a cursor and execute a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        
        print(f"\n✅ Connection successful!")
        print(f"   PostgreSQL version: {db_version[0]}")
        
        # Test a simple query
        cursor.execute("SELECT NOW();")
        current_time = cursor.fetchone()
        print(f"   Server time: {current_time[0]}")
        
        # Close cursor and connection
        cursor.close()
        conn.close()
        
        print("\n✅ Connection closed successfully")
        return True
        
    except OperationalError as e:
        print(f"\n❌ Connection failed (Operational Error):")
        print(f"   {str(e)}")
        print("\nPossible causes:")
        print("  - Database server is not running")
        print("  - Incorrect host or port")
        print("  - Firewall blocking the connection")
        print("  - Network connectivity issues")
        return False
        
    except ProgrammingError as e:
        print(f"\n❌ Connection failed (Programming Error):")
        print(f"   {str(e)}")
        print("\nPossible causes:")
        print("  - Incorrect database name")
        print("  - Permission issues")
        return False
        
    except Exception as e:
        print(f"\n❌ Connection failed (Unexpected Error):")
        print(f"   {type(e).__name__}: {str(e)}")
        return False


def test_with_sqlalchemy():
    """
    Test database connection using SQLAlchemy.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    if not HAS_SQLALCHEMY:
        print("❌ SQLAlchemy is not installed. Skipping SQLAlchemy test.")
        print("   Install it with: pip install sqlalchemy")
        return False
    
    print("\n" + "="*60)
    print("Testing Database Connection with SQLAlchemy")
    print("="*60)
    
    try:
        database_url = DatabaseConfig.get_database_url()
        # Hide password in output
        safe_url = database_url.replace(DatabaseConfig.DB_PASSWORD, "****") if DatabaseConfig.DB_PASSWORD else database_url
        print(f"\nDatabase URL: {safe_url}")
        
        # Create engine
        engine = create_engine(
            database_url,
            pool_size=DatabaseConfig.DB_POOL_SIZE,
            max_overflow=DatabaseConfig.DB_MAX_OVERFLOW,
            pool_timeout=DatabaseConfig.DB_POOL_TIMEOUT
        )
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"\n✅ Connection successful!")
            print(f"   PostgreSQL version: {version}")
            
            result = connection.execute(text("SELECT NOW();"))
            current_time = result.fetchone()[0]
            print(f"   Server time: {current_time}")
            
            # Test connection pool
            print(f"\n   Pool size: {DatabaseConfig.DB_POOL_SIZE}")
            print(f"   Max overflow: {DatabaseConfig.DB_MAX_OVERFLOW}")
        
        print("\n✅ Connection closed successfully")
        engine.dispose()
        return True
        
    except SQLAlchemyError as e:
        print(f"\n❌ Connection failed:")
        print(f"   {str(e)}")
        return False
        
    except Exception as e:
        print(f"\n❌ Connection failed (Unexpected Error):")
        print(f"   {type(e).__name__}: {str(e)}")
        return False


def validate_configuration():
    """
    Validate database configuration before testing connection.
    
    Returns:
        bool: True if configuration is valid, False otherwise
    """
    print("\n" + "="*60)
    print("Validating Database Configuration")
    print("="*60)
    
    is_valid, missing_vars = DatabaseConfig.validate_config()
    
    if is_valid:
        print("\n✅ All required configuration variables are set")
        return True
    else:
        print("\n❌ Missing required configuration variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables in your .env file")
        return False


def main():
    """
    Main function to run all database connection tests.
    """
    print("="*60)
    print("Database Connection Test Utility")
    print("="*60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Validate configuration first
    if not validate_configuration():
        sys.exit(1)
    
    # Run tests
    results = []
    
    # Test with psycopg2
    if HAS_PSYCOPG2:
        results.append(("psycopg2", test_with_psycopg2()))
    
    # Test with SQLAlchemy
    if HAS_SQLALCHEMY:
        results.append(("SQLAlchemy", test_with_sqlalchemy()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    if not results:
        print("\n❌ No database drivers available for testing")
        print("   Please install psycopg2-binary or sqlalchemy")
        sys.exit(1)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    
    if all_passed:
        print("\n✅ All tests passed! Database is properly configured.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the configuration.")
        print("\nTroubleshooting steps:")
        print("1. Verify database server is running")
        print("2. Check .env file has correct settings")
        print("3. Ensure firewall allows connection to database port")
        print("4. Verify database user has proper permissions")
        print("5. Check CONFIGURATION.md for network setup guide")
        sys.exit(1)


if __name__ == "__main__":
    main()
