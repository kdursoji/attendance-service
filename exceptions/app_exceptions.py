"""
Application Exception Classes
Following Single Responsibility Principle: Each exception handles a specific error type
"""
from typing import Optional, Dict, Any


class AppException(Exception):
    """Base exception class for all application exceptions"""
    
    def __init__(
        self,
        message: str = "An error occurred",
        status_code: int = 500,
        payload: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for JSON response"""
        return {
            'status': 'error',
            'message': self.message,
            'data': self.payload if self.payload else None
        }


class ValidationException(AppException):
    """Exception for validation errors (400)"""
    
    def __init__(self, message: str = "Validation error", payload: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=400, payload=payload)


class UnauthorizedException(AppException):
    """Exception for unauthorized access (401)"""
    
    def __init__(self, message: str = "Unauthorized access", payload: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=401, payload=payload)


class ForbiddenException(AppException):
    """Exception for forbidden access (403)"""
    
    def __init__(self, message: str = "Forbidden", payload: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=403, payload=payload)


class NotFoundException(AppException):
    """Exception for resource not found (404)"""
    
    def __init__(self, message: str = "Resource not found", payload: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=404, payload=payload)


class ConflictException(AppException):
    """Exception for resource conflicts (409)"""
    
    def __init__(self, message: str = "Resource conflict", payload: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=409, payload=payload)


class DatabaseException(AppException):
    """Exception for database errors (500)"""
    
    def __init__(self, message: str = "Database error occurred", payload: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=500, payload=payload)


class InternalServerException(AppException):
    """Exception for internal server errors (500)"""
    
    def __init__(self, message: str = "Internal server error", payload: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=500, payload=payload)

