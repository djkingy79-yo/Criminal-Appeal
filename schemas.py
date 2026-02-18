"""
Input Validation Schemas for Criminal Appeal Application

This module defines marshmallow schemas for input validation.
"""

from marshmallow import Schema, fields, validate, validates, ValidationError


class CaseSchema(Schema):
    """Schema for validating case data."""
    case_number = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50),
        error_messages={'required': 'Case number is required'}
    )
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=200),
        error_messages={'required': 'Case title is required'}
    )
    status = fields.Str(
        validate=validate.OneOf(['pending', 'active', 'closed', 'appealed']),
        missing='pending'
    )


class DocumentSchema(Schema):
    """Schema for validating document data."""
    case_id = fields.Int(
        required=True,
        error_messages={'required': 'Case ID is required'}
    )
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=200),
        error_messages={'required': 'Document title is required'}
    )
    content = fields.Str(
        required=True,
        validate=validate.Length(min=1),
        error_messages={'required': 'Document content is required'}
    )
    document_type = fields.Str(
        required=True,
        validate=validate.OneOf([
            'case_info',
            'brief',
            'case_notes',
            'judgment',
            'sentencing_report',
            'psychological_report'
        ]),
        error_messages={'required': 'Document type is required'}
    )
    
    @validates('content')
    def validate_content(self, value):
        """Validate content length and ensure it's not just whitespace."""
        if not value or not value.strip():
            raise ValidationError('Content cannot be empty or whitespace only')
        if len(value) > 1000000:  # 1MB max
            raise ValidationError('Content is too large (max 1MB)')


class UserSchema(Schema):
    """Schema for validating user data."""
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=80),
        error_messages={'required': 'Username is required'}
    )
    email = fields.Email(
        required=True,
        error_messages={'required': 'Email is required'}
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8),
        load_only=True,
        error_messages={'required': 'Password is required'}
    )
    role = fields.Str(
        validate=validate.OneOf(['user', 'admin', 'lawyer']),
        missing='user'
    )
    
    @validates('username')
    def validate_username(self, value):
        """Validate username format."""
        if not value.replace('_', '').replace('-', '').isalnum():
            raise ValidationError('Username can only contain letters, numbers, hyphens, and underscores')
    
    @validates('password')
    def validate_password(self, value):
        """Validate password strength."""
        if not any(c.isupper() for c in value):
            raise ValidationError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in value):
            raise ValidationError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in value):
            raise ValidationError('Password must contain at least one number')


class UserLoginSchema(Schema):
    """Schema for validating user login data."""
    username = fields.Str(
        required=True,
        error_messages={'required': 'Username is required'}
    )
    password = fields.Str(
        required=True,
        load_only=True,
        error_messages={'required': 'Password is required'}
    )
