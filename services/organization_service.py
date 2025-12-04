"""
Organization Service - Business Logic Layer
Following Single Responsibility Principle
"""
from sqlalchemy.orm import Session
from models.organizations import organizations
from schemas.pydantic_models import (
    AddOrganizationRequest,
    UpdateOrganizationRequest,
    OrganizationResponse
)
from repositories.user_repository import IUserRepository
from repositories.organization_repository import IOrganizationRepository
from exceptions.app_exceptions import NotFoundException, DatabaseException


class OrganizationService:
    """Organization Service - Single Responsibility: Handle organization business logic"""
    
    def __init__(
        self,
        user_repository: IUserRepository,
        organization_repository: IOrganizationRepository
    ):
        """Dependency Injection - Dependency Inversion Principle"""
        self._user_repository = user_repository
        self._organization_repository = organization_repository
    
    def create_organization(
        self,
        db: Session,
        org_request: AddOrganizationRequest
    ) -> OrganizationResponse:
        """
        Create a new organization
        
        Returns:
            OrganizationResponse on success
            
        Raises:
            NotFoundException: If user does not exist
            DatabaseException: If database operation fails
        """
        # Verify user exists
        user = self._user_repository.get_by_id(db=db, user_id=org_request.user_id)
        if not user:
            raise NotFoundException(message='User does not exist.')
        
        try:
            # Create organization
            org_data = org_request.model_dump()
            organization = self._organization_repository.create(db=db, org_data=org_data)
            
            return OrganizationResponse(
                status='success',
                message=f'{organization.name} was added!'
            )
        except Exception as e:
            raise DatabaseException(message='An error occurred while creating the organization.')
    
    def update_organization(
        self,
        db: Session,
        org_request: UpdateOrganizationRequest
    ) -> OrganizationResponse:
        """
        Update an existing organization
        
        Returns:
            OrganizationResponse on success
            
        Raises:
            NotFoundException: If user or organization does not exist
            DatabaseException: If database operation fails
        """
        # Verify user exists
        user = self._user_repository.get_by_id(db=db, user_id=org_request.user_id)
        if not user:
            raise NotFoundException(message='User does not exist.')
        
        # Verify organization exists
        organization = self._organization_repository.get_by_id(db=db, org_id=org_request.id)
        if not organization:
            raise NotFoundException(message='Organization does not exist.')
        
        try:
            # Update organization
            org_data = org_request.model_dump()
            updated_org = self._organization_repository.update(
                db=db,
                org=organization,
                org_data=org_data
            )
            
            return OrganizationResponse(
                status='success',
                message=f'{updated_org.name} was updated!'
            )
        except Exception as e:
            raise DatabaseException(message='An error occurred while updating the organization.')

