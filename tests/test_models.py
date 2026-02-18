"""
Unit tests for database models.
"""

import pytest
from datetime import datetime
from models import Case, Document, User


class TestCaseModel:
    """Tests for the Case model."""
    
    def test_case_creation(self, app):
        """Test creating a case."""
        with app.app_context():
            from models import db
            
            case = Case(
                case_number='TEST-001',
                title='Test Case',
                status='pending'
            )
            db.session.add(case)
            db.session.commit()
            
            assert case.id is not None
            assert case.case_number == 'TEST-001'
            assert case.title == 'Test Case'
            assert case.status == 'pending'
            assert case.created_at is not None
    
    def test_case_to_dict(self, app):
        """Test case to_dict method."""
        with app.app_context():
            from models import db
            
            case = Case(
                case_number='TEST-002',
                title='Test Case 2',
                status='active'
            )
            db.session.add(case)
            db.session.commit()
            
            case_dict = case.to_dict()
            assert case_dict['case_number'] == 'TEST-002'
            assert case_dict['title'] == 'Test Case 2'
            assert case_dict['status'] == 'active'
            assert 'id' in case_dict
            assert 'created_at' in case_dict


class TestDocumentModel:
    """Tests for the Document model."""
    
    def test_document_creation(self, app):
        """Test creating a document."""
        with app.app_context():
            from models import db
            
            # Create a case first
            case = Case(case_number='TEST-003', title='Test Case 3')
            db.session.add(case)
            db.session.commit()
            
            # Create a document
            doc = Document(
                case_id=case.id,
                title='Test Document',
                content='This is test content',
                document_type='brief'
            )
            db.session.add(doc)
            db.session.commit()
            
            assert doc.id is not None
            assert doc.case_id == case.id
            assert doc.title == 'Test Document'
            assert doc.content == 'This is test content'
            assert doc.document_type == 'brief'
    
    def test_document_relationship(self, app):
        """Test case-document relationship."""
        with app.app_context():
            from models import db
            
            case = Case(case_number='TEST-004', title='Test Case 4')
            db.session.add(case)
            db.session.commit()
            
            doc1 = Document(
                case_id=case.id,
                title='Doc 1',
                content='Content 1',
                document_type='brief'
            )
            doc2 = Document(
                case_id=case.id,
                title='Doc 2',
                content='Content 2',
                document_type='judgment'
            )
            db.session.add_all([doc1, doc2])
            db.session.commit()
            
            # Test relationship
            assert case.documents.count() == 2
            assert doc1.case == case
            assert doc2.case == case


class TestUserModel:
    """Tests for the User model."""
    
    def test_user_creation(self, app):
        """Test creating a user."""
        with app.app_context():
            from models import db
            
            user = User(
                username='testuser',
                email='test@example.com',
                password_hash='hashed_password',
                role='user'
            )
            db.session.add(user)
            db.session.commit()
            
            assert user.id is not None
            assert user.username == 'testuser'
            assert user.email == 'test@example.com'
            assert user.is_active is True
    
    def test_user_to_dict(self, app):
        """Test user to_dict method."""
        with app.app_context():
            from models import db
            
            user = User(
                username='testuser2',
                email='test2@example.com',
                password_hash='hashed_password',
                role='admin'
            )
            db.session.add(user)
            db.session.commit()
            
            # Test without sensitive data
            user_dict = user.to_dict()
            assert user_dict['username'] == 'testuser2'
            assert user_dict['email'] == 'test2@example.com'
            assert user_dict['role'] == 'admin'
            assert 'password_hash' not in user_dict
            
            # Test with sensitive data
            user_dict_sensitive = user.to_dict(include_sensitive=True)
            assert 'password_hash' in user_dict_sensitive
