# Global Exception Handling

This document explains the global exception handling system implemented in the Flask application.

## Overview

The application uses a centralized exception handling system that:
- Provides consistent error responses across all endpoints
- Handles different types of exceptions appropriately
- Logs errors for debugging
- Returns user-friendly error messages

## Exception Classes

All custom exceptions inherit from `AppException` base class:

### `AppException` (Base)
- Base class for all application exceptions
- Contains `message`, `status_code`, and `payload` attributes
- Provides `to_dict()` method for JSON serialization

### Custom Exception Types

1. **`ValidationException`** (400)
   - Invalid input data
   - Pydantic validation errors
   - Missing required fields

2. **`UnauthorizedException`** (401)
   - Invalid credentials
   - Missing authentication

3. **`ForbiddenException`** (403)
   - Insufficient permissions
   - Access denied

4. **`NotFoundException`** (404)
   - Resource not found
   - User/Organization not found

5. **`ConflictException`** (409)
   - Resource conflicts
   - Duplicate entries

6. **`DatabaseException`** (500)
   - Database errors
   - SQLAlchemy errors
   - Integrity constraint violations

7. **`InternalServerException`** (500)
   - Unexpected server errors
   - Unhandled exceptions

## Exception Handlers

Global exception handlers are registered in `exceptions/exception_handlers.py`:

### Handled Exception Types

1. **Custom App Exceptions**
   - All `AppException` subclasses
   - Returns consistent JSON response format

2. **Pydantic Validation Errors**
   - Automatically converts to `ValidationException`
   - Includes detailed field-level error messages

3. **SQLAlchemy Errors**
   - `IntegrityError` → `DatabaseException`
   - `SQLAlchemyError` → `DatabaseException`

4. **Python Built-in Exceptions**
   - `ValueError` → `ValidationException`
   - `KeyError` → `ValidationException`

5. **HTTP Status Codes**
   - 404 (Not Found)
   - 405 (Method Not Allowed)
   - 500 (Internal Server Error)

6. **Generic Exception Handler**
   - Catches all unhandled exceptions
   - Returns generic error message (doesn't expose internal details)

## Response Format

All error responses follow this format:

```json
{
    "status": "error",
    "message": "Error message here",
    "data": {
        // Optional additional error details
    }
}
```

## Usage in Services

Services raise exceptions instead of returning error tuples:

```python
# Before (returning error tuples)
def create_user(...):
    if error:
        return None, error_response, 400
    return success_response, None, 201

# After (raising exceptions)
def create_user(...):
    if error:
        raise NotFoundException(message="User not found")
    return success_response
```

## Usage in Routes

Routes simply call services - exceptions are automatically handled:

```python
@route('/users', methods=['POST'])
@validate()
def create_user(body: CreateUserRequest):
    service = _get_user_service()
    with session_scope() as session:
        # Exception is automatically caught by global handler
        response = service.create_user(db=session, request=body)
        return jsonify(response.model_dump()), 201
```

## Benefits

1. **Consistency**: All errors follow the same format
2. **Clean Code**: Services don't need to return error tuples
3. **Centralized**: All error handling in one place
4. **Logging**: All errors are automatically logged
5. **Security**: Internal error details not exposed to clients
6. **Maintainability**: Easy to add new exception types

## Example Error Responses

### Validation Error (400)
```json
{
    "status": "error",
    "message": "Validation error: email: field required; password: ensure this value has at least 8 characters",
    "data": {
        "errors": [...]
    }
}
```

### Not Found (404)
```json
{
    "status": "error",
    "message": "User not found.",
    "data": null
}
```

### Database Error (500)
```json
{
    "status": "error",
    "message": "Database integrity constraint violation",
    "data": {
        "detail": "..."
    }
}
```

## Adding New Exception Types

1. Create new exception class in `exceptions/app_exceptions.py`:
```python
class CustomException(AppException):
    def __init__(self, message: str = "Custom error", payload: Optional[Dict] = None):
        super().__init__(message=message, status_code=400, payload=payload)
```

2. Add handler in `exceptions/exception_handlers.py`:
```python
@app.errorhandler(CustomException)
def handle_custom_exception(e: CustomException):
    logger.warning(f"CustomException: {e.message}")
    return jsonify(e.to_dict()), e.status_code
```

3. Register in `exceptions/__init__.py`:
```python
from exceptions.app_exceptions import CustomException
__all__ = [..., 'CustomException']
```

4. Use in services:
```python
raise CustomException(message="Something went wrong")
```

