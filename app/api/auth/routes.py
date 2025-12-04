"""
Authentication API Routes - RESTful endpoints
Following REST standards: POST /auth/login, GET /auth/status, POST /auth/logout
"""
import logging
from flask import Blueprint, jsonify
from flask_pydantic import validate
from datastore.deps import session_scope
from schemas.pydantic_models import LoginRequest, StandardResponse, UserStatusResponse, UserData
from app import bcrypt
import crud
from repositories.user_repository import UserRepository
from services.auth_service import AuthService
from util.utils import authenticate

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
logger = logging.getLogger(__name__)


def _get_auth_service():
    """Create and return AuthService instance"""
    user_repository = UserRepository(crud.user_crud_handler)
    return AuthService(user_repository=user_repository, bcrypt=bcrypt)


@auth_bp.route('/login', methods=['POST'])
@validate()
def login(body: LoginRequest):
    """
    POST /auth/login
    Authenticate user and return JWT token
    
    Returns:
        200: Login successful with auth token
        401: Invalid credentials
        404: User not found
    """
    auth_service = _get_auth_service()
    
    with session_scope() as session:
        response = auth_service.authenticate_user(db=session, login_request=body)
        return jsonify(response.model_dump(exclude_none=True)), 200


@auth_bp.route('/logout', methods=['POST'])
@authenticate
def logout():
    """
    POST /auth/logout
    Logout current user
    
    Returns:
        200: Logout successful
        401: Unauthorized
    """
    response = StandardResponse(
        status='success',
        message='Successfully logged out.'
    )
    return jsonify(response.model_dump(exclude_none=True)), 200


@auth_bp.route('/status', methods=['GET'])
@authenticate
def get_status(resp):
    """
    GET /auth/status
    Get current authenticated user status
    
    Returns:
        200: User status
        401: Unauthorized
        404: User not found
    """
    auth_service = _get_auth_service()
    
    with session_scope() as session:
        user = auth_service.get_user_status(db=session, user_id=resp)
        
        user_data = UserData(
            id=user.id,
            username=user.user_name,
            email=user.email,
            active=getattr(user, 'active', True),
            created_at=user.registered_on
        )
        response = UserStatusResponse(
            status='success',
            data=user_data
        )
        return jsonify(response.model_dump(exclude_none=True)), 200

