"""
Organizations API Routes - RESTful endpoints
Following REST standards: GET /organizations, POST /organizations, GET /organizations/{id}, PUT /organizations/{id}, DELETE /organizations/{id}
"""
from flask import Blueprint, jsonify
from flask_pydantic import validate
from datastore.deps import session_scope
from schemas.pydantic_models import (
    AddOrganizationRequest,
    UpdateOrganizationRequest,
    StandardResponse
)
import crud
from repositories.user_repository import UserRepository
from repositories.organization_repository import OrganizationRepository
from services.organization_service import OrganizationService

organizations_bp = Blueprint('organizations', __name__, url_prefix='/organizations')


def _get_organization_service():
    """Create and return OrganizationService instance"""
    user_repository = UserRepository(crud.user_crud_handler)
    organization_repository = OrganizationRepository(crud.organizations_crud_handler)
    return OrganizationService(
        user_repository=user_repository,
        organization_repository=organization_repository
    )


@organizations_bp.route('', methods=['GET'])
def list_organizations():
    """
    GET /organizations
    Get all organizations
    
    Query Parameters:
        user_id (optional): Filter by user ID
    
    Returns:
        200: List of organizations
    """
    from exceptions.app_exceptions import InternalServerException
    raise InternalServerException(message='List organizations functionality not yet implemented')


@organizations_bp.route('', methods=['POST'])
@validate()
def create_organization(body: AddOrganizationRequest):
    """
    POST /organizations
    Create a new organization
    
    Returns:
        201: Organization created successfully
        400: Validation error or user not found
        500: Server error
    """
    org_service = _get_organization_service()
    
    with session_scope() as session:
        response = org_service.create_organization(db=session, org_request=body)
        return jsonify(response.model_dump(exclude_none=True)), 201


@organizations_bp.route('/<int:org_id>', methods=['GET'])
def get_organization(org_id: int):
    """
    GET /organizations/{id}
    Get organization by ID
    
    Returns:
        200: Organization details
        404: Organization not found
    """
    from exceptions.app_exceptions import InternalServerException
    raise InternalServerException(message='Get organization by ID functionality not yet implemented')


@organizations_bp.route('/<int:org_id>', methods=['PUT'])
@validate()
def update_organization(org_id: int, body: UpdateOrganizationRequest):
    """
    PUT /organizations/{id}
    Update organization by ID
    
    Returns:
        200: Organization updated successfully
        404: Organization not found
        400: Validation error
    """
    org_service = _get_organization_service()
    
    # Ensure the ID in body matches the URL parameter
    if body.id != org_id:
        from exceptions.app_exceptions import ValidationException
        raise ValidationException(message='Organization ID in URL does not match request body')
    
    with session_scope() as session:
        response = org_service.update_organization(db=session, org_request=body)
        return jsonify(response.model_dump(exclude_none=True)), 200


@organizations_bp.route('/<int:org_id>', methods=['DELETE'])
def delete_organization(org_id: int):
    """
    DELETE /organizations/{id}
    Delete organization by ID
    
    Returns:
        204: Organization deleted successfully
        404: Organization not found
    """
    from exceptions.app_exceptions import InternalServerException
    raise InternalServerException(message='Delete organization functionality not yet implemented')

