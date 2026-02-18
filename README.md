# Criminal Appeal

## Project Overview
The Criminal Appeal project is designed to assist individuals in navigating the complexities involved in the criminal appeal process.

## Features
- User registration and authentication
- Submission of appeal documents
- Tracking of appeal status
- Notifications for updates and deadlines
- Integration with legal databases

## Getting Started

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/djkingy79-yo/Criminal-Appeal.git
cd Criminal-Appeal
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Configure required environment variables in `.env`:
```bash
SECRET_KEY=<generate-with: python -c 'import secrets; print(secrets.token_hex(32))'>
DB_HOST=localhost
DB_PORT=5432
DB_NAME=criminal_appeal
DB_USER=postgres
DB_PASSWORD=your-database-password
ALLOWED_HOSTS=localhost,127.0.0.1
```

6. Create the database:
```bash
createdb criminal_appeal
```

7. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Running Tests

```bash
python -m pytest tests/ -v
```

## Security

This application implements comprehensive security measures:

- **Environment Variable Validation**: All sensitive configuration enforced from environment
- **SSL/TLS Database Connections**: Configurable via `DB_SSL_MODE`
- **Input Validation**: All API inputs validated using marshmallow schemas
- **CORS Protection**: Configurable allowed origins
- **Password Hashing**: Bcrypt for secure password storage
- **Secure Configuration**: Production mode enforces secure defaults

See [SECURITY.md](SECURITY.md) for detailed security information.

## Architecture
The application is built using Flask with SQLAlchemy ORM, enabling scalability and flexibility. Core components include:
- **Models**: Database models for Cases, Documents, and Users
- **API Endpoints**: RESTful API with comprehensive error handling
- **Validation**: Input validation using marshmallow schemas
- **Logging**: Comprehensive application and security logging

## API Endpoints

### Cases
- `GET /api/cases`: List all cases
- `POST /api/cases`: Create a new case
- `GET /api/cases/:id`: Get a specific case
- `PUT /api/cases/:id`: Update a case
- `DELETE /api/cases/:id`: Delete a case
- `POST /api/cases/:id/analyze`: Analyze case merit

### Documents
- `GET /api/documents`: List all documents (filter by case_id)
- `POST /api/documents`: Create a new document
- `GET /api/documents/:id`: Get a specific document
- `PUT /api/documents/:id`: Update a document
- `DELETE /api/documents/:id`: Delete a document

### Health Check
- `GET /health`: Application health status

## Documentation Links
- [Configuration Guide](CONFIGURATION.md) - Database and firewall setup
- [API Documentation](docs/API.md) - Detailed API reference
- [Architecture](docs/ARCHITECTURE.md) - System architecture details
- [Contribution Guidelines](CONTRIBUTING.md)
- [Security Policy](SECURITY.md) - Security measures and reporting
- [Branch Protection Setup](BRANCH_PROTECTION.md) - For repository administrators
- [Quick Setup Guide](.github/SETUP.md) - Getting started for admins

## License
See [LICENSE](LICENSE) file for details.