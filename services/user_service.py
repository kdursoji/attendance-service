"""
User Service - Business Logic Layer
Following Single Responsibility Principle
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from flask import current_app
from flask_bcrypt import Bcrypt
from schemas.pydantic_models import AddUserRequest, StandardResponse, UserData
from repositories.user_repository import IUserRepository
from repositories.organization_repository import IOrganizationRepository
from exceptions.app_exceptions import ConflictException, ValidationException, DatabaseException


class UserService:
    """User Service - Single Responsibility: Handle user business logic"""
    
    def __init__(
        self,
        user_repository: IUserRepository,
        organization_repository: IOrganizationRepository,
        bcrypt: Bcrypt
    ):
        """Dependency Injection - Dependency Inversion Principle"""
        self._user_repository = user_repository
        self._organization_repository = organization_repository
        self._bcrypt = bcrypt
    
    def create_user(
        self,
        db: Session,
        user_request: AddUserRequest,
        profile_pic_location: Optional[str] = None
    ) -> StandardResponse:
        """
        Create a new user
        
        Returns:
            StandardResponse on success
            
        Raises:
            ConflictException: If user already exists
            ValidationException: If validation fails
            DatabaseException: If database operation fails
        """
        # Check if user already exists
        existing_user = self._user_repository.get_by_username(
            db=db,
            username=user_request.user_name
        )
        
        if existing_user:
            raise ConflictException(message='Sorry. That user name already exists.')
        
        try:
            # Hash password
            hashed_password = self._bcrypt.generate_password_hash(
                user_request.password,
                current_app.config.get('BCRYPT_LOG_ROUNDS', 12)
            ).decode()
            
            # Prepare user data
            user_data = user_request.model_dump(exclude={'password'})
            user_data['password'] = hashed_password
            
            if profile_pic_location:
                user_data['profile_pic_location'] = profile_pic_location
            
            # Create user
            user = self._user_repository.create(db=db, user_data=user_data)
            
            # Update profile pic if provided
            if profile_pic_location and user:
                self._user_repository.update(
                    db=db,
                    user=user,
                    user_data={'profile_pic_location': profile_pic_location}
                )
            
            return StandardResponse(
                status='success',
                message=f'{user.user_name} was added!'
            )
        except ValueError as e:
            raise ValidationException(message=f'Invalid payload: {str(e)}')
        except Exception as e:
            raise DatabaseException(message='An error occurred while creating the user.')
    
    def get_all_users(self, db: Session) -> List[UserData]:
        """Get all users with their organizations"""
        users = self._user_repository.get_all(db=db)
        user_data_list = []
        
        for user_dict in users:
            user_id = user_dict.get('id')
            if user_id:
                organizations = self._organization_repository.get_by_user_id(
                    db=db,
                    user_id=user_id
                )
                user_dict['organizations'] = organizations
            
            user_data = UserData(**user_dict)
            user_data_list.append(user_data)
        
        return user_data_list

