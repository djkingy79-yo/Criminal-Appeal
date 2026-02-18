"""
Unit tests for API endpoints.
"""

import json
import pytest
from models import Case, Document as DocumentModel


class TestHealthEndpoint:
    """Tests for the health check endpoint."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data


class TestCaseEndpoints:
    """Tests for case endpoints."""
    
    def test_list_cases_empty(self, client):
        """Test listing cases when none exist."""
        response = client.get('/api/cases')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []
    
    def test_create_case(self, client):
        """Test creating a new case."""
        case_data = {
            'case_number': 'TEST-001',
            'title': 'Test Case',
            'status': 'pending'
        }
        response = client.post(
            '/api/cases',
            data=json.dumps(case_data),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['case_number'] == 'TEST-001'
        assert data['title'] == 'Test Case'
        assert data['status'] == 'pending'
    
    def test_create_case_duplicate(self, client, app):
        """Test creating a case with duplicate case number."""
        with app.app_context():
            from models import db
            case = Case(case_number='TEST-002', title='Existing Case')
            db.session.add(case)
            db.session.commit()
        
        case_data = {
            'case_number': 'TEST-002',
            'title': 'Duplicate Case'
        }
        response = client.post(
            '/api/cases',
            data=json.dumps(case_data),
            content_type='application/json'
        )
        assert response.status_code == 409
    
    def test_create_case_invalid_data(self, client):
        """Test creating a case with invalid data."""
        case_data = {
            'title': 'Missing case number'
        }
        response = client.post(
            '/api/cases',
            data=json.dumps(case_data),
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_get_case(self, client, app):
        """Test getting a specific case."""
        with app.app_context():
            from models import db
            case = Case(case_number='TEST-003', title='Test Case 3')
            db.session.add(case)
            db.session.commit()
            case_id = case.id
        
        response = client.get(f'/api/cases/{case_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['case_number'] == 'TEST-003'
    
    def test_get_case_not_found(self, client):
        """Test getting a non-existent case."""
        response = client.get('/api/cases/999')
        assert response.status_code == 404
    
    def test_update_case(self, client, app):
        """Test updating a case."""
        with app.app_context():
            from models import db
            case = Case(case_number='TEST-004', title='Original Title')
            db.session.add(case)
            db.session.commit()
            case_id = case.id
        
        update_data = {
            'case_number': 'TEST-004',
            'title': 'Updated Title',
            'status': 'active'
        }
        response = client.put(
            f'/api/cases/{case_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == 'Updated Title'
        assert data['status'] == 'active'
    
    def test_delete_case(self, client, app):
        """Test deleting a case."""
        with app.app_context():
            from models import db
            case = Case(case_number='TEST-005', title='To Delete')
            db.session.add(case)
            db.session.commit()
            case_id = case.id
        
        response = client.delete(f'/api/cases/{case_id}')
        assert response.status_code == 204


class TestDocumentEndpoints:
    """Tests for document endpoints."""
    
    def test_create_document(self, client, app):
        """Test creating a new document."""
        with app.app_context():
            from models import db
            case = Case(case_number='TEST-006', title='Test Case 6')
            db.session.add(case)
            db.session.commit()
            case_id = case.id
        
        doc_data = {
            'case_id': case_id,
            'title': 'Test Document',
            'content': 'This is test content',
            'document_type': 'brief'
        }
        response = client.post(
            '/api/documents',
            data=json.dumps(doc_data),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['title'] == 'Test Document'
        assert data['document_type'] == 'brief'
    
    def test_create_document_invalid_case(self, client):
        """Test creating a document with invalid case_id."""
        doc_data = {
            'case_id': 999,
            'title': 'Test Document',
            'content': 'Content',
            'document_type': 'brief'
        }
        response = client.post(
            '/api/documents',
            data=json.dumps(doc_data),
            content_type='application/json'
        )
        assert response.status_code == 404
    
    def test_list_documents_by_case(self, client, app):
        """Test listing documents filtered by case."""
        with app.app_context():
            from models import db
            case = Case(case_number='TEST-007', title='Test Case 7')
            db.session.add(case)
            db.session.commit()
            
            doc1 = DocumentModel(
                case_id=case.id,
                title='Doc 1',
                content='Content 1',
                document_type='brief'
            )
            doc2 = DocumentModel(
                case_id=case.id,
                title='Doc 2',
                content='Content 2',
                document_type='judgment'
            )
            db.session.add_all([doc1, doc2])
            db.session.commit()
            case_id = case.id
        
        response = client.get(f'/api/documents?case_id={case_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
    
    def test_get_document(self, client, app):
        """Test getting a specific document."""
        with app.app_context():
            from models import db
            case = Case(case_number='TEST-008', title='Test Case 8')
            db.session.add(case)
            db.session.commit()
            
            doc = DocumentModel(
                case_id=case.id,
                title='Test Doc',
                content='Test Content',
                document_type='brief'
            )
            db.session.add(doc)
            db.session.commit()
            doc_id = doc.id
        
        response = client.get(f'/api/documents/{doc_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == 'Test Doc'


class TestAnalysisEndpoint:
    """Tests for the case analysis endpoint."""
    
    def test_analyze_case(self, client, app):
        """Test analyzing a case."""
        with app.app_context():
            from models import db
            case = Case(case_number='TEST-009', title='Test Case 9')
            db.session.add(case)
            db.session.commit()
            
            doc = DocumentModel(
                case_id=case.id,
                title='Test Doc',
                content='Test Content',
                document_type='brief'
            )
            db.session.add(doc)
            db.session.commit()
            case_id = case.id
        
        response = client.post(f'/api/cases/{case_id}/analyze')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'analysis' in data
        assert data['case_number'] == 'TEST-009'
    
    def test_analyze_case_no_documents(self, client, app):
        """Test analyzing a case with no documents."""
        with app.app_context():
            from models import db
            case = Case(case_number='TEST-010', title='Test Case 10')
            db.session.add(case)
            db.session.commit()
            case_id = case.id
        
        response = client.post(f'/api/cases/{case_id}/analyze')
        assert response.status_code == 400
