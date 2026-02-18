from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Initialize app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appeals.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Database model
class Appeal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_number = db.Column(db.String(255), unique=True)
    appellant_name = db.Column(db.String(255))
    appeal_date = db.Column(db.Date)
    status = db.Column(db.String(100))

    def __init__(self, case_number, appellant_name, appeal_date, status):
        self.case_number = case_number
        self.appellant_name = appellant_name
        self.appeal_date = appeal_date
        self.status = status

# Schema
class AppealSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Appeal

# Initialize database
with app.app_context():
    db.create_all()

# API Endpoints
@app.route('/api/appeals', methods=['POST'])
def add_appeal():
    case_number = request.json['case_number']
    appellant_name = request.json['appellant_name']
    appeal_date = request.json['appeal_date']
    status = request.json['status']

    new_appeal = Appeal(case_number, appellant_name, appeal_date, status)
    db.session.add(new_appeal)
    db.session.commit()

    return AppealSchema().jsonify(new_appeal)

@app.route('/api/appeals', methods=['GET'])
def get_appeals():
    all_appeals = Appeal.query.all()
    return AppealSchema(many=True).jsonify(all_appeals)

@app.route('/api/appeals/<int:id>', methods=['GET'])
def get_appeal(id):
    appeal = Appeal.query.get(id)
    return AppealSchema().jsonify(appeal)

@app.route('/api/appeals/<int:id>', methods=['PUT'])
def update_appeal(id):
    appeal = Appeal.query.get(id)
    appeal.status = request.json['status']
    db.session.commit()
    return AppealSchema().jsonify(appeal)

@app.route('/api/appeals/<int:id>', methods=['DELETE'])
def delete_appeal(id):
    appeal = Appeal.query.get(id)
    db.session.delete(appeal)
    db.session.commit()
    return '', 204

# Run the app
if __name__ == '__main__':
    app.run(debug=True)