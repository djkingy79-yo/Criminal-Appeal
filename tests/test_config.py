"""
Unit tests for configuration validation.
"""

import os
import pytest
from config import Config, DatabaseConfig


class TestDatabaseConfig:
    """Tests for DatabaseConfig class."""
    
    def test_validate_config_success(self):
        """Test validation with all required variables."""
        # Set environment variables
        os.environ['DB_HOST'] = 'localhost'
        os.environ['DB_PORT'] = '5432'
        os.environ['DB_NAME'] = 'test_db'
        os.environ['DB_USER'] = 'test_user'
        
        is_valid, missing = DatabaseConfig.validate_config()
        assert is_valid is True
        assert len(missing) == 0
    
    def test_get_database_url_with_password(self):
        """Test database URL generation with password."""
        os.environ['DB_HOST'] = 'localhost'
        os.environ['DB_PORT'] = '5432'
        os.environ['DB_NAME'] = 'testdb'
        os.environ['DB_USER'] = 'testuser'
        os.environ['DB_PASSWORD'] = 'testpass'
        os.environ['DB_SSL_MODE'] = 'require'
        
        # Reload config
        from importlib import reload
        import config
        reload(config)
        
        url = config.DatabaseConfig.get_database_url()
        assert 'postgresql://testuser:testpass@localhost:5432/testdb' in url
        assert 'sslmode=require' in url
    
    def test_get_database_url_without_password(self):
        """Test database URL generation without password."""
        os.environ['DB_HOST'] = 'localhost'
        os.environ['DB_PORT'] = '5432'
        os.environ['DB_NAME'] = 'testdb'
        os.environ['DB_USER'] = 'testuser'
        os.environ['DB_PASSWORD'] = ''
        
        # Reload config
        from importlib import reload
        import config
        reload(config)
        
        url = config.DatabaseConfig.get_database_url()
        assert url.startswith('postgresql://testuser@localhost:5432/testdb')


class TestConfig:
    """Tests for Config class."""
    
    def test_validate_required_env_vars_success(self):
        """Test validation with all required variables set."""
        os.environ['SECRET_KEY'] = 'test-secret-key'
        os.environ['DB_HOST'] = 'localhost'
        os.environ['DB_NAME'] = 'test_db'
        os.environ['DB_USER'] = 'test_user'
        
        # Reload config
        from importlib import reload
        import config
        reload(config)
        
        # Should not raise
        config.Config.validate_required_env_vars()
    
    def test_secret_key_validation_production(self):
        """Test that production requires proper SECRET_KEY."""
        os.environ['FLASK_ENV'] = 'production'
        os.environ['SECRET_KEY'] = 'dev-secret-key-change-in-production'
        
        with pytest.raises(ValueError, match='SECRET_KEY must be set'):
            from importlib import reload
            import config
            reload(config)
    
    def test_debug_false_in_production(self):
        """Test that DEBUG must be False in production."""
        os.environ['FLASK_ENV'] = 'production'
        os.environ['DEBUG'] = 'True'
        os.environ['SECRET_KEY'] = 'proper-secret-key-for-production'
        
        with pytest.raises(ValueError, match='DEBUG must be False'):
            from importlib import reload
            import config
            reload(config)
    
    def test_allowed_hosts_validation_production(self):
        """Test that ALLOWED_HOSTS cannot be wildcard in production."""
        os.environ['FLASK_ENV'] = 'production'
        os.environ['ALLOWED_HOSTS'] = '*'
        os.environ['SECRET_KEY'] = 'proper-secret-key'
        os.environ['DEBUG'] = 'False'
        
        with pytest.raises(ValueError, match='ALLOWED_HOSTS cannot be'):
            from importlib import reload
            import config
            reload(config)
