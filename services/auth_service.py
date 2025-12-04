"""
Authentication Service - Business Logic Layer
Following Single Responsibility Principle
"""
from typing import Optional
from sqlalchemy.orm import Session
from flask_bcrypt import Bcrypt
from models.users import User
from schemas.pydantic_models import LoginRequest, LoginResponse
from repositories.user_repository import IUserRepository
from exceptions.app_exceptions import NotFoundException, UnauthorizedException, InternalServerException


class AuthService:
    """Authentication Service - Single Responsibility: Handle authentication logic"""
    
    def __init__(self, user_repository: IUserRepository, bcrypt: Bcrypt):
        """Dependency Injection - Dependency Inversion Principle"""
        self._user_repository = user_repository
        self._bcrypt = bcrypt
    
    def authenticate_user(self, db: Session, login_request: LoginRequest) -> LoginResponse:
        """
        Authenticate a user
        
        Returns:
            LoginResponse on success
            
        Raises:
            NotFoundException: If user does not exist
            UnauthorizedException: If credentials are invalid
            InternalServerException: If token generation fails
        """
        user = self._user_repository.get_by_username(db=db, username=login_request.username)
        
        if not user:
            raise NotFoundException(message='User does not exist.')
        
        if not self._bcrypt.check_password_hash(user.password, login_request.password):
            raise UnauthorizedException(message='Invalid credentials.')
        
        # Generate auth token
        auth_token = user.encode_auth_token(user.id)
        if not auth_token:
            raise InternalServerException(message='Failed to generate authentication token.')
        
        return LoginResponse(
            status='success',
            message='Successfully logged in.',
            auth_token=auth_token.decode() if isinstance(auth_token, bytes) else str(auth_token),
            user_id=user.id
        )
    
    def get_user_status(self, db: Session, user_id: int) -> User:
        """
        Get user status by ID
        
        Returns:
            User object
            
        Raises:
            NotFoundException: If user does not exist
        """
        user = self._user_repository.get_by_id(db=db, user_id=user_id)
        if not user:
            raise NotFoundException(message='User not found.')
        return user

