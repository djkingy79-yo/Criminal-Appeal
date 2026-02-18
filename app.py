"""
Criminal Appeal Document Management System - Flask Application

This module initializes the Flask application with proper security,
database models, API endpoints, and error handling.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError

from config import Config
from models import db, Case, Document as DocumentModel, User
from schemas import CaseSchema, DocumentSchema, UserSchema, UserLoginSchema


# Initialize Flask extensions
bcrypt = Bcrypt()


def create_app(config_class=Config):
    """
    Application factory pattern for creating Flask app.
    
    Args:
        config_class: Configuration class to use
        
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Validate configuration at startup
    try:
        config_class.validate_required_env_vars()
        config_class.init_app(app)
    except ValueError as e:
        print(f"Configuration Error: {e}")
        raise
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    CORS(app, origins=config_class.CORS_ORIGINS)
    
    # Setup logging
    setup_logging(app)
    
    # Register blueprints/routes
    register_routes(app)
    register_error_handlers(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
        app.logger.info("Database tables created successfully")
    
    return app


def setup_logging(app):
    """
    Configure application logging.
    
    Args:
        app: Flask application instance
    """
    if not app.debug:
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(app.config['LOG_FILE'])
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Setup file handler with rotation
        file_handler = RotatingFileHandler(
            app.config['LOG_FILE'],
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))
        app.logger.info('Criminal Appeal Application startup')


def register_routes(app):
    """
    Register API routes.
    
    Args:
        app: Flask application instance
    """
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat()
        }), 200
    
    # Case routes
    @app.route('/api/cases', methods=['GET', 'POST'])
    def cases():
        """List all cases or create a new case."""
        if request.method == 'GET':
            cases = Case.query.all()
            return jsonify([case.to_dict() for case in cases]), 200
        
        elif request.method == 'POST':
            try:
                # Validate input
                schema = CaseSchema()
                data = schema.load(request.get_json())
                
                # Check if case number already exists
                existing = Case.query.filter_by(case_number=data['case_number']).first()
                if existing:
                    return jsonify({'error': 'Case number already exists'}), 409
                
                # Create new case
                case = Case(**data)
                db.session.add(case)
                db.session.commit()
                
                app.logger.info(f"Created new case: {case.case_number}")
                return jsonify(case.to_dict()), 201
                
            except ValidationError as err:
                return jsonify({'errors': err.messages}), 400
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Error creating case: {str(e)}")
                return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/cases/<int:case_id>', methods=['GET', 'PUT', 'DELETE'])
    def case_detail(case_id):
        """Get, update, or delete a specific case."""
        case = Case.query.get_or_404(case_id)
        
        if request.method == 'GET':
            return jsonify(case.to_dict()), 200
        
        elif request.method == 'PUT':
            try:
                schema = CaseSchema()
                data = schema.load(request.get_json())
                
                # Update case fields
                for key, value in data.items():
                    setattr(case, key, value)
                
                db.session.commit()
                app.logger.info(f"Updated case: {case.case_number}")
                return jsonify(case.to_dict()), 200
                
            except ValidationError as err:
                return jsonify({'errors': err.messages}), 400
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Error updating case: {str(e)}")
                return jsonify({'error': 'Internal server error'}), 500
        
        elif request.method == 'DELETE':
            try:
                db.session.delete(case)
                db.session.commit()
                app.logger.info(f"Deleted case: {case.case_number}")
                return '', 204
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Error deleting case: {str(e)}")
                return jsonify({'error': 'Internal server error'}), 500
    
    # Document routes
    @app.route('/api/documents', methods=['GET', 'POST'])
    def documents():
        """List all documents or create a new document."""
        if request.method == 'GET':
            case_id = request.args.get('case_id', type=int)
            if case_id:
                docs = DocumentModel.query.filter_by(case_id=case_id).all()
            else:
                docs = DocumentModel.query.all()
            return jsonify([doc.to_dict() for doc in docs]), 200
        
        elif request.method == 'POST':
            try:
                # Validate input
                schema = DocumentSchema()
                data = schema.load(request.get_json())
                
                # Verify case exists
                case = Case.query.get(data['case_id'])
                if not case:
                    return jsonify({'error': 'Case not found'}), 404
                
                # Create new document
                document = DocumentModel(**data)
                db.session.add(document)
                db.session.commit()
                
                app.logger.info(f"Created new document: {document.title} for case {case.case_number}")
                return jsonify(document.to_dict()), 201
                
            except ValidationError as err:
                return jsonify({'errors': err.messages}), 400
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Error creating document: {str(e)}")
                return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/documents/<int:doc_id>', methods=['GET', 'PUT', 'DELETE'])
    def document_detail(doc_id):
        """Get, update, or delete a specific document."""
        document = DocumentModel.query.get_or_404(doc_id)
        
        if request.method == 'GET':
            return jsonify(document.to_dict()), 200
        
        elif request.method == 'PUT':
            try:
                schema = DocumentSchema()
                data = schema.load(request.get_json())
                
                # Update document fields
                for key, value in data.items():
                    if key != 'case_id':  # Don't allow changing case_id
                        setattr(document, key, value)
                
                db.session.commit()
                app.logger.info(f"Updated document: {document.title}")
                return jsonify(document.to_dict()), 200
                
            except ValidationError as err:
                return jsonify({'errors': err.messages}), 400
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Error updating document: {str(e)}")
                return jsonify({'error': 'Internal server error'}), 500
        
        elif request.method == 'DELETE':
            try:
                db.session.delete(document)
                db.session.commit()
                app.logger.info(f"Deleted document: {document.title}")
                return '', 204
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Error deleting document: {str(e)}")
                return jsonify({'error': 'Internal server error'}), 500
    
    # Analysis endpoint
    @app.route('/api/cases/<int:case_id>/analyze', methods=['POST'])
    def analyze_case(case_id):
        """Analyze the merit of a case based on its documents."""
        case = Case.query.get_or_404(case_id)
        documents = DocumentModel.query.filter_by(case_id=case_id).all()
        
        if not documents:
            return jsonify({'error': 'No documents found for this case'}), 400
        
        # Placeholder analysis logic
        analysis_result = {
            'case_id': case_id,
            'case_number': case.case_number,
            'document_count': len(documents),
            'analysis': 'Analysis of grounds of merit completed.',
            'recommendation': 'Further review required',
            'timestamp': datetime.now().isoformat()
        }
        
        app.logger.info(f"Analyzed case: {case.case_number}")
        return jsonify(analysis_result), 200


def register_error_handlers(app):
    """
    Register error handlers for the application.
    
    Args:
        app: Flask application instance
    """
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        db.session.rollback()
        app.logger.error(f"Internal error: {str(error)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(ValidationError)
    def validation_error(error):
        """Handle validation errors."""
        return jsonify({'errors': error.messages}), 400


# Legacy CaseManagementSystem class for backward compatibility
class Document:
    """Legacy Document class for backward compatibility."""
    def __init__(self, title, content):
        self.title = title
        self.content = content


class CaseManagementSystem:
    """Legacy CaseManagementSystem class for backward compatibility."""
    def __init__(self):
        self.documents = {
            "case_info": None,
            "briefs": [],
            "case_notes": [],
            "judgments": [],
            "sentencing_reports": [],
            "psychological_reports": []
        }

    def upload_case_info(self, title, content):
        self.documents["case_info"] = Document(title, content)

    def upload_brief(self, title, content):
        self.documents["briefs"].append(Document(title, content))

    def upload_case_notes(self, title, content):
        self.documents["case_notes"].append(Document(title, content))

    def upload_judgment(self, title, content):
        self.documents["judgments"].append(Document(title, content))

    def upload_sentencing_report(self, title, content):
        self.documents["sentencing_reports"].append(Document(title, content))

    def upload_psychological_report(self, title, content):
        self.documents["psychological_reports"].append(Document(title, content))

    def analyze_merit(self):
        return "Analysis of grounds of merit completed."


if __name__ == "__main__":
    app = create_app()
    app.run(
        host=app.config['API_HOST'],
        port=app.config['API_PORT'],
        debug=app.config['DEBUG']
    )
