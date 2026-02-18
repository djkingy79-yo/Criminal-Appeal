from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///criminal_appeal.db')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Initialize database
db = SQLAlchemy(app)

# Simple User model for demonstration
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name
        }

# Simple Appeal model for demonstration
class Appeal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('name'):
        return jsonify({'error': 'Missing email or name'}), 400
    
    try:
        user = User(email=data['email'], name=data['name'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully', 'user': user.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Authenticate a user"""
    data = request.get_json()
    
    if not data or not data.get('email'):
        return jsonify({'error': 'Missing email'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'message': 'Login successful', 'user': user.to_dict()}), 200

@app.route('/api/appeals', methods=['POST'])
def submit_appeal():
    """Submit a new appeal"""
    data = request.get_json()
    
    if not data or not data.get('user_id'):
        return jsonify({'error': 'Missing user_id'}), 400
    
    try:
        appeal = Appeal(user_id=data['user_id'], status='pending')
        db.session.add(appeal)
        db.session.commit()
        return jsonify({'message': 'Appeal submitted successfully', 'appeal': appeal.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/appeals/<int:appeal_id>', methods=['GET'])
def get_appeal(appeal_id):
    """Retrieve status of an appeal"""
    appeal = Appeal.query.get(appeal_id)
    
    if not appeal:
        return jsonify({'error': 'Appeal not found'}), 404
    
    return jsonify({'appeal': appeal.to_dict()}), 200

@app.route('/api/docs', methods=['GET'])
def get_docs():
    """Access documentation links"""
    return jsonify({
        'documentation': {
            'api': '/docs/api.md',
            'user_guide': '/docs/user-guide.md',
            'contributing': '/CONTRIBUTING.md'
        }
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('API_PORT', 5000))
    app.run(debug=True, port=port)