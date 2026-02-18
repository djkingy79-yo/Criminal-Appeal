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
    DB_SSL_MODE = os.getenv('DB_SSL_MODE', 'prefer')
    
    # Connection pool settings
    DB_POOL_SIZE = int(os.getenv('DB_POOL_SIZE', '5'))
    DB_MAX_OVERFLOW = int(os.getenv('DB_MAX_OVERFLOW', '10'))
    DB_POOL_TIMEOUT = int(os.getenv('DB_POOL_TIMEOUT', '30'))
    
    # Connection timeout settings
    DB_CONNECT_TIMEOUT = int(os.getenv('DB_CONNECT_TIMEOUT', '10'))
    
    @classmethod
    def get_database_url(cls):
        """
        Construct and return the database URL for SQLAlchemy with SSL support.
        
        Returns:
            str: Database URL in the format: postgresql://user:password@host:port/dbname?sslmode=...
        """
        if cls.DB_PASSWORD:
            base_url = f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
        else:
            base_url = f"postgresql://{cls.DB_USER}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
        
        # Add SSL mode if configured
        if cls.DB_SSL_MODE and cls.DB_SSL_MODE != 'disable':
            base_url += f"?sslmode={cls.DB_SSL_MODE}"
        
        return base_url
    
    @classmethod
    def get_connection_params(cls):
        """
        Get database connection parameters as a dictionary.
        
        Returns:
            dict: Dictionary containing all database connection parameters
        """
        params = {
            'host': cls.DB_HOST,
            'port': cls.DB_PORT,
            'database': cls.DB_NAME,
            'user': cls.DB_USER,
            'password': cls.DB_PASSWORD,
            'connect_timeout': cls.DB_CONNECT_TIMEOUT
        }
        
        # Add SSL mode if configured
        if cls.DB_SSL_MODE and cls.DB_SSL_MODE != 'disable':
            params['sslmode'] = cls.DB_SSL_MODE
        
        return params
    
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
    
    # Flask settings - enforce SECRET_KEY from environment
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY or SECRET_KEY == 'dev-secret-key-change-in-production':
        if os.getenv('FLASK_ENV') == 'production':
            raise ValueError(
                "SECRET_KEY must be set in environment variables for production. "
                "Generate a random key using: python -c 'import secrets; print(secrets.token_hex(32))'"
            )
        else:
            # Use a development key but warn
            SECRET_KEY = os.urandom(24).hex()
            print("WARNING: Using auto-generated SECRET_KEY for development. Set SECRET_KEY in .env for production.")
    
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    
    # Enforce DEBUG is False in production
    if FLASK_ENV == 'production' and DEBUG:
        raise ValueError("DEBUG must be False in production environment")
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = DatabaseConfig.get_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = DatabaseConfig.DB_POOL_SIZE
    SQLALCHEMY_MAX_OVERFLOW = DatabaseConfig.DB_MAX_OVERFLOW
    SQLALCHEMY_POOL_TIMEOUT = DatabaseConfig.DB_POOL_TIMEOUT
    
    # API settings
    API_PORT = int(os.getenv('API_PORT', '5000'))
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    
    # Security settings - restrict ALLOWED_HOSTS
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
    
    # Validate ALLOWED_HOSTS in production
    if FLASK_ENV == 'production' and '*' in ALLOWED_HOSTS:
        raise ValueError(
            "ALLOWED_HOSTS cannot be '*' in production. "
            "Specify allowed domains in the ALLOWED_HOSTS environment variable."
        )
    
    # JWT settings
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', '3600'))
    
    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5000').split(',')
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    
    @classmethod
    def init_app(cls, app):
        """
        Initialize the application with this configuration.
        
        Args:
            app: Flask application instance
        """
        # Validate database configuration
        is_valid, missing_vars = DatabaseConfig.validate_config()
        if not is_valid:
            raise ValueError(f"Missing required database configuration: {', '.join(missing_vars)}")
    
    @classmethod
    def validate_required_env_vars(cls):
        """
        Validate that all required environment variables are set.
        
        Raises:
            ValueError: If required environment variables are missing
        """
        required_vars = {
            'SECRET_KEY': cls.SECRET_KEY,
            'DB_HOST': DatabaseConfig.DB_HOST,
            'DB_NAME': DatabaseConfig.DB_NAME,
            'DB_USER': DatabaseConfig.DB_USER,
        }
        
        missing = [key for key, value in required_vars.items() if not value]
        
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}. "
                f"Please set them in your .env file or environment."
            )

