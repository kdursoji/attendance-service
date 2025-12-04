"""
Users API Routes - RESTful endpoints
Following REST standards: GET /users, POST /users, GET /users/{id}, PUT /users/{id}, DELETE /users/{id}
"""
from flask import Blueprint, request, jsonify
from flask_pydantic import validate
from datastore.deps import session_scope
from schemas.pydantic_models import AddUserRequest, StandardResponse, UsersListResponse
from app import bcrypt
import crud
from repositories.user_repository import UserRepository
from repositories.organization_repository import OrganizationRepository
from services.user_service import UserService
from services.file_service import FileService

users_bp = Blueprint('users', __name__, url_prefix='/users')


def _get_user_service():
    """Create and return UserService instance"""
    user_repository = UserRepository(crud.user_crud_handler)
    organization_repository = OrganizationRepository(crud.organizations_crud_handler)
    return UserService(
        user_repository=user_repository,
        organization_repository=organization_repository,
        bcrypt=bcrypt
    )


def _get_file_service():
    """Create and return FileService instance"""
    return FileService()


@users_bp.route('', methods=['GET'])
def list_users():
    """
    GET /users
    Get all users with their organizations
    
    Returns:
        200: List of users
    """
    user_service = _get_user_service()
    
    with session_scope() as session:
        all_users = user_service.get_all_users(db=session)
        
        response = UsersListResponse(
            status='success',
            data={'users': all_users}
        )
        return jsonify(response.model_dump(exclude_none=True)), 200


@users_bp.route('', methods=['POST'])
@validate()
def create_user(form: AddUserRequest):
    """
    POST /users
    Create a new user
    
    Request Body:
        form-data with user fields and optional user_file for profile picture
    
    Returns:
        201: User created successfully
        400: Validation error or user already exists
        500: Server error
    """
    user_service = _get_user_service()
    file_service = _get_file_service()
    
    # Handle file upload if present
    profile_pic_location = None
    if "user_file" in request.files:
        file = request.files["user_file"]
        profile_pic_location = file_service.upload_profile_picture(file)
    
    with session_scope() as session:
        response = user_service.create_user(
            db=session,
            user_request=form,
            profile_pic_location=profile_pic_location
        )
        return jsonify(response.model_dump(exclude_none=True)), 201


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    """
    GET /users/{id}
    Get user by ID
    
    Returns:
        200: User details
        404: User not found
    """
    user_service = _get_user_service()
    
    with session_scope() as session:
        from exceptions.app_exceptions import NotFoundException
        from schemas.pydantic_models import UserData, UserStatusResponse
        
        user_repository = UserRepository(crud.user_crud_handler)
        user = user_repository.get_by_id(db=session, user_id=user_id)
        
        if not user:
            raise NotFoundException(message='User not found.')
        
        organizations = OrganizationRepository(crud.organizations_crud_handler).get_by_user_id(
            db=session, user_id=user_id
        )
        
        user_data = UserData(
            id=user.id,
            username=user.user_name,
            email=user.email,
            active=getattr(user, 'active', True),
            created_at=user.registered_on,
            organizations=organizations
        )
        
        response = UserStatusResponse(
            status='success',
            data=user_data
        )
        return jsonify(response.model_dump(exclude_none=True)), 200


@users_bp.route('/<int:user_id>', methods=['PUT'])
@validate()
def update_user(user_id: int, form: AddUserRequest):
    """
    PUT /users/{id}
    Update user by ID
    
    Returns:
        200: User updated successfully
        404: User not found
        400: Validation error
    """
    from exceptions.app_exceptions import InternalServerException
    raise InternalServerException(message='Update user functionality not yet implemented')


@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int):
    """
    DELETE /users/{id}
    Delete user by ID
    
    Returns:
        204: User deleted successfully
        404: User not found
    """
    from exceptions.app_exceptions import InternalServerException
    raise InternalServerException(message='Delete user functionality not yet implemented')

