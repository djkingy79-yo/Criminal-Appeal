# Criminal Appeal Case Management System - API Usage Guide

## Overview
A comprehensive RESTful API for managing NSW murder appeal cases with document management, timeline tracking, AI-powered legal analysis, and automated barrister report generation.

## Quick Start

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable for development
export FLASK_ENV=development

# Run the application
python app.py
```

The API will be available at `http://localhost:5000`

### Production Deployment
```bash
# Set required environment variables
export SECRET_KEY="your-secure-random-secret-key"
export DATABASE_URL="sqlite:///criminal_appeal.db"  # or PostgreSQL/MySQL URL
export FLASK_ENV="production"

# Run with a production WSGI server (e.g., gunicorn)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## API Endpoints

### Health Check
```bash
GET /api/health
```
Returns the health status of the API and database connection.

### Cases

#### Create a Case
```bash
POST /api/cases
Content-Type: application/json

{
  "case_number": "NSW-2024-MURDER-001",
  "defendant_name": "John Doe",
  "offense_type": "Murder",           # Optional, defaults to "Murder"
  "court": "NSW Supreme Court",       # Optional, defaults to "NSW Supreme Court"
  "status": "In Progress"             # Optional, defaults to "Open"
}
```

#### Get All Cases
```bash
GET /api/cases
```

#### Get Specific Case
```bash
GET /api/cases/{case_id}
```

#### Update Case
```bash
PUT /api/cases/{case_id}
Content-Type: application/json

{
  "defendant_name": "Updated Name",
  "status": "Under Review"
}
```

#### Delete Case
```bash
DELETE /api/cases/{case_id}
```

### Documents

#### Upload Document
```bash
POST /api/cases/{case_id}/documents
Content-Type: multipart/form-data

file: <file>                          # PDF, DOCX, or TXT file
title: "Appeal Brief"                 # Document title
document_type: "brief"                # Type: brief, case_note, evidence, judgment, etc.
```

The system automatically extracts text from uploaded documents.

#### Get Case Documents
```bash
GET /api/cases/{case_id}/documents
```

#### Get Specific Document
```bash
GET /api/documents/{document_id}
```

#### Download Document
```bash
GET /api/documents/{document_id}/download
```

#### Delete Document
```bash
DELETE /api/documents/{document_id}
```

### Timeline Events

#### Create Timeline Event
```bash
POST /api/cases/{case_id}/timeline
Content-Type: application/json

{
  "event_date": "2024-03-15T10:00:00",
  "event_type": "Trial Commenced",
  "description": "Trial began at NSW Supreme Court",
  "significance": "High",             # High, Medium, Low
  "relevance_to_appeal": "Original trial proceedings",
  "document_id": 1                    # Optional, link to document
}
```

**Note:** Timeline events are automatically created when documents are uploaded.

#### Get Case Timeline
```bash
GET /api/cases/{case_id}/timeline
```
Returns events in chronological order.

#### Get Specific Timeline Event
```bash
GET /api/timeline/{event_id}
```

#### Update Timeline Event
```bash
PUT /api/timeline/{event_id}
Content-Type: application/json

{
  "event_type": "Updated Event Type",
  "description": "Updated description"
}
```

#### Delete Timeline Event
```bash
DELETE /api/timeline/{event_id}
```

### Legal Analysis

#### Perform AI Analysis
```bash
POST /api/cases/{case_id}/analyze
Content-Type: application/json
```

Analyzes all case documents and generates grounds of merit with:
- Ground description
- Legal basis
- Strength assessment (Strong, Medium, Weak)
- NSW law references (Criminal Appeal Act 1912, Criminal Procedure Act 1986)
- Federal law references (Evidence Act 1995)
- Supporting evidence links

**Note:** Current implementation uses sample analyses. In production, integrate with OpenAI API for actual AI-powered analysis.

#### Get Case Analyses
```bash
GET /api/cases/{case_id}/analyses
```

#### Get Specific Analysis
```bash
GET /api/analyses/{analysis_id}
```

#### Update Analysis
```bash
PUT /api/analyses/{analysis_id}
Content-Type: application/json

{
  "ground_of_merit": "Updated ground",
  "strength_assessment": "Strong"
}
```

#### Delete Analysis
```bash
DELETE /api/analyses/{analysis_id}
```

### Barrister Reports

#### Generate Report
```bash
POST /api/cases/{case_id}/reports
Content-Type: application/json
```

Automatically generates a professional barrister report including:
- Executive summary
- Identified grounds with strength assessments
- Detailed legal analysis
- NSW and Federal law references
- Professional recommendations

#### Get Case Reports
```bash
GET /api/cases/{case_id}/reports
```

#### Get Specific Report
```bash
GET /api/reports/{report_id}
```

#### Delete Report
```bash
DELETE /api/reports/{report_id}
```

## Complete Workflow Example

```bash
# 1. Create a case
curl -X POST http://localhost:5000/api/cases \
  -H "Content-Type: application/json" \
  -d '{
    "case_number": "NSW-2024-MURDER-001",
    "defendant_name": "John Smith"
  }'

# Response: {"id": 1, "case_number": "NSW-2024-MURDER-001", ...}

# 2. Upload case documents
curl -X POST http://localhost:5000/api/cases/1/documents \
  -F "file=@trial_transcript.pdf" \
  -F "title=Trial Transcript" \
  -F "document_type=judgment"

curl -X POST http://localhost:5000/api/cases/1/documents \
  -F "file=@psychiatric_report.docx" \
  -F "title=Psychiatric Evaluation" \
  -F "document_type=evidence"

# 3. View auto-generated timeline
curl http://localhost:5000/api/cases/1/timeline

# 4. Perform legal analysis
curl -X POST http://localhost:5000/api/cases/1/analyze \
  -H "Content-Type: application/json"

# 5. Generate barrister report
curl -X POST http://localhost:5000/api/cases/1/reports \
  -H "Content-Type: application/json"

# 6. Retrieve the report
curl http://localhost:5000/api/cases/1/reports
```

## Supported File Types

- **PDF** (.pdf) - Extracted using PyPDF2
- **DOCX** (.docx) - Extracted using python-docx
- **TXT** (.txt) - Direct text reading with encoding fallback (UTF-8, Latin-1, CP1252)

Maximum file size: 50MB

## Legal References

The system references the following NSW and Federal legislation:

**NSW Legislation:**
- Criminal Appeal Act 1912 (NSW)
- Crimes (Appeal and Review) Act 2001 (NSW)
- Criminal Procedure Act 1986 (NSW)
- Crimes (Sentencing Procedure) Act 1999 (NSW)

**Federal Legislation:**
- Evidence Act 1995 (Cth)

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource already exists
- `413 Payload Too Large` - File too large
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Database unavailable

Error responses include a JSON body with an `error` field:
```json
{
  "error": "Error description",
  "details": "Additional details if available"
}
```

## Security Considerations

1. **SECRET_KEY**: Must be set in production environment. The application will fail to start if not set.
2. **File Uploads**: Only PDF, DOCX, and TXT files are accepted. Files are validated and stored securely.
3. **Input Validation**: All inputs are validated using Marshmallow schemas.
4. **SQL Injection**: Protected by SQLAlchemy ORM parameterized queries.
5. **File Size Limits**: Enforced at 50MB to prevent DoS attacks.

## Database Schema

The application uses SQLAlchemy with the following models:

- **Case** - Criminal appeal cases
- **Document** - Case documents with extracted text
- **TimelineEvent** - Chronological case events
- **LegalAnalysis** - AI-generated grounds of merit
- **BarristerReport** - Professional legal reports

Database migrations can be handled using Flask-Migrate or Alembic.

## Logging

The application logs to:
- Console (stdout)
- File: `app.log`

Log levels:
- INFO - Normal operations
- WARNING - Non-critical issues (e.g., file deletion failures)
- ERROR - Critical errors requiring attention

## Development

### Running Tests
```bash
pytest
```

### Code Quality
```bash
# Format code
black app.py

# Lint code
pylint app.py
flake8 app.py
```

## Support

For issues, questions, or contributions, please refer to the repository documentation.

## License

See LICENSE file for details.
