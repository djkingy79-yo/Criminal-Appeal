"""
Test configuration and fixtures for Criminal Appeal Application.
"""

import os
import pytest
from app import create_app
from models import db
from config import Config


class TestConfig(Config):
    """Configuration for testing."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'test-secret-key-for-testing-only'
    DEBUG = False
    FLASK_ENV = 'testing'
    ALLOWED_HOSTS = ['localhost', 'testserver']
    WTF_CSRF_ENABLED = False


@pytest.fixture
def app():
    """Create and configure a test Flask application."""
    # Override environment variables for testing
    os.environ['SECRET_KEY'] = 'test-secret-key'
    os.environ['DB_HOST'] = 'localhost'
    os.environ['DB_NAME'] = 'test_db'
    os.environ['DB_USER'] = 'test_user'
    
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner for the app."""
    return app.test_cli_runner()
