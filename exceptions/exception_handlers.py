"""
Global Exception Handlers
Following Single Responsibility Principle: Handles all exception types consistently
"""
import logging
from traceback import print_exc
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from pydantic import ValidationError as PydanticValidationError
from exceptions.app_exceptions import (
    AppException,
    ValidationException,
    NotFoundException,
    UnauthorizedException,
    ForbiddenException,
    ConflictException,
    DatabaseException,
    InternalServerException
)

logger = logging.getLogger(__name__)


def register_exception_handlers(app):
    """Register all global exception handlers with Flask app"""
    
    @app.errorhandler(AppException)
    def handle_app_exception(e: AppException):
        """Handle custom application exceptions"""
        logger.error(f"AppException: {e.message}", exc_info=True)
        return jsonify(e.to_dict()), e.status_code
    
    @app.errorhandler(ValidationException)
    def handle_validation_exception(e: ValidationException):
        """Handle validation exceptions"""
        logger.warning(f"ValidationException: {e.message}")
        return jsonify(e.to_dict()), e.status_code
    
    @app.errorhandler(NotFoundException)
    def handle_not_found_exception(e: NotFoundException):
        """Handle not found exceptions"""
        logger.warning(f"NotFoundException: {e.message}")
        return jsonify(e.to_dict()), e.status_code
    
    @app.errorhandler(UnauthorizedException)
    def handle_unauthorized_exception(e: UnauthorizedException):
        """Handle unauthorized exceptions"""
        logger.warning(f"UnauthorizedException: {e.message}")
        return jsonify(e.to_dict()), e.status_code
    
    @app.errorhandler(ForbiddenException)
    def handle_forbidden_exception(e: ForbiddenException):
        """Handle forbidden exceptions"""
        logger.warning(f"ForbiddenException: {e.message}")
        return jsonify(e.to_dict()), e.status_code
    
    @app.errorhandler(ConflictException)
    def handle_conflict_exception(e: ConflictException):
        """Handle conflict exceptions"""
        logger.warning(f"ConflictException: {e.message}")
        return jsonify(e.to_dict()), e.status_code
    
    @app.errorhandler(PydanticValidationError)
    def handle_pydantic_validation_error(e: PydanticValidationError):
        """Handle Pydantic validation errors"""
        error_messages = []
        for error in e.errors():
            field = '.'.join(str(loc) for loc in error['loc'])
            message = error['msg']
            error_messages.append(f"{field}: {message}")
        
        validation_exception = ValidationException(
            message='Validation error: ' + '; '.join(error_messages),
            payload={'errors': e.errors()}
        )
        logger.warning(f"PydanticValidationError: {validation_exception.message}")
        return jsonify(validation_exception.to_dict()), validation_exception.status_code
    
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(e: IntegrityError):
        """Handle database integrity errors"""
        logger.error(f"IntegrityError: {str(e)}", exc_info=True)
        db_exception = DatabaseException(
            message="Database integrity constraint violation",
            payload={'detail': str(e.orig) if hasattr(e, 'orig') else str(e)}
        )
        return jsonify(db_exception.to_dict()), db_exception.status_code
    
    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(e: SQLAlchemyError):
        """Handle SQLAlchemy errors"""
        logger.error(f"SQLAlchemyError: {str(e)}", exc_info=True)
        db_exception = DatabaseException(
            message="Database error occurred",
            payload={'detail': str(e)}
        )
        return jsonify(db_exception.to_dict()), db_exception.status_code
    
    @app.errorhandler(ValueError)
    def handle_value_error(e: ValueError):
        """Handle value errors"""
        logger.warning(f"ValueError: {str(e)}")
        validation_exception = ValidationException(
            message=f"Invalid value: {str(e)}"
        )
        return jsonify(validation_exception.to_dict()), validation_exception.status_code
    
    @app.errorhandler(KeyError)
    def handle_key_error(e: KeyError):
        """Handle key errors"""
        logger.warning(f"KeyError: {str(e)}")
        validation_exception = ValidationException(
            message=f"Missing required field: {str(e)}"
        )
        return jsonify(validation_exception.to_dict()), validation_exception.status_code
    
    @app.errorhandler(Exception)
    def handle_generic_exception(e: Exception):
        """Handle all other unhandled exceptions"""
        print_exc()
        logger.error(f"Unhandled Exception: {type(e).__name__}: {str(e)}", exc_info=True)
        
        # In production, don't expose internal error details
        internal_exception = InternalServerException(
            message="An unexpected error occurred. Please try again later."
        )
        return jsonify(internal_exception.to_dict()), internal_exception.status_code
    
    @app.errorhandler(404)
    def handle_404_error(e):
        """Handle 404 errors for routes not found"""
        not_found = NotFoundException(
            message=f"Route not found: {request.path}"
        )
        return jsonify(not_found.to_dict()), not_found.status_code
    
    @app.errorhandler(405)
    def handle_405_error(e):
        """Handle 405 method not allowed errors"""
        method_exception = ValidationException(
            message=f"Method {request.method} not allowed for {request.path}"
        )
        return jsonify(method_exception.to_dict()), method_exception.status_code
    
    @app.errorhandler(500)
    def handle_500_error(e):
        """Handle 500 internal server errors"""
        internal_exception = InternalServerException(
            message="Internal server error occurred"
        )
        return jsonify(internal_exception.to_dict()), internal_exception.status_code

