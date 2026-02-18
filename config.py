"""
Database Configuration Module

This module manages database connection settings for the Criminal Appeal application.
It securely sources sensitive information from environment variables.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class DatabaseConfig:
    """
    Database configuration class that manages connection settings.
    
    All sensitive information is loaded from environment variables to ensure security.
    """
    
    # Database connection settings
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'criminal_appeal')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # Connection pool settings
    DB_POOL_SIZE = int(os.getenv('DB_POOL_SIZE', '5'))
    DB_MAX_OVERFLOW = int(os.getenv('DB_MAX_OVERFLOW', '10'))
    DB_POOL_TIMEOUT = int(os.getenv('DB_POOL_TIMEOUT', '30'))
    
    # Connection timeout settings
    DB_CONNECT_TIMEOUT = int(os.getenv('DB_CONNECT_TIMEOUT', '10'))
    
    @classmethod
    def get_database_url(cls):
        """
        Construct and return the database URL for SQLAlchemy.
        
        Returns:
            str: Database URL in the format: postgresql://user:password@host:port/dbname
        """
        if cls.DB_PASSWORD:
            return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
        else:
            return f"postgresql://{cls.DB_USER}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
    
    @classmethod
    def get_connection_params(cls):
        """
        Get database connection parameters as a dictionary.
        
        Returns:
            dict: Dictionary containing all database connection parameters
        """
        return {
            'host': cls.DB_HOST,
            'port': cls.DB_PORT,
            'database': cls.DB_NAME,
            'user': cls.DB_USER,
            'password': cls.DB_PASSWORD,
            'connect_timeout': cls.DB_CONNECT_TIMEOUT
        }
    
    @classmethod
    def validate_config(cls):
        """
        Validate that all required configuration variables are set.
        
        Returns:
            tuple: (bool, list) - Success status and list of missing variables
        """
        required_vars = ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER']
        missing_vars = []
        
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        return len(missing_vars) == 0, missing_vars


class Config:
    """
    Application configuration class that includes database settings.
    """
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = DatabaseConfig.get_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = DatabaseConfig.DB_POOL_SIZE
    SQLALCHEMY_MAX_OVERFLOW = DatabaseConfig.DB_MAX_OVERFLOW
    SQLALCHEMY_POOL_TIMEOUT = DatabaseConfig.DB_POOL_TIMEOUT
    
    # API settings
    API_PORT = int(os.getenv('API_PORT', '5000'))
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    
    # Security settings
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')
    
    @classmethod
    def init_app(cls, app):
        """
        Initialize the application with this configuration.
        
        Args:
            app: Flask application instance
        """
        pass
