"""
Organization Repository Interface and Implementation
Following Interface Segregation and Dependency Inversion Principles
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from models.organizations import organizations


class IOrganizationRepository(ABC):
    """Interface for Organization Repository - Interface Segregation Principle"""
    
    @abstractmethod
    def get_by_id(self, db: Session, org_id: int) -> Optional[organizations]:
        """Get organization by ID"""
        pass
    
    @abstractmethod
    def get_by_user_id(self, db: Session, user_id: int) -> List[Dict[str, Any]]:
        """Get all organizations for a user"""
        pass
    
    @abstractmethod
    def create(self, db: Session, org_data: Dict[str, Any]) -> organizations:
        """Create a new organization"""
        pass
    
    @abstractmethod
    def update(self, db: Session, org: organizations, org_data: Dict[str, Any]) -> organizations:
        """Update an existing organization"""
        pass


class OrganizationRepository(IOrganizationRepository):
    """Organization Repository Implementation - Single Responsibility Principle"""
    
    def __init__(self, crud_handler):
        """Dependency Injection - Dependency Inversion Principle"""
        self._crud_handler = crud_handler
    
    def get_by_id(self, db: Session, org_id: int) -> Optional[organizations]:
        """Get organization by ID"""
        return self._crud_handler.get_organization(db=db, id=org_id)
    
    def get_by_user_id(self, db: Session, user_id: int) -> List[Dict[str, Any]]:
        """Get all organizations for a user"""
        return self._crud_handler.get_organizations_by_user_id(db=db, user_id=user_id)
    
    def create(self, db: Session, org_data: Dict[str, Any]) -> organizations:
        """Create a new organization"""
        return self._crud_handler.create_organization(db=db, obj_in=org_data)
    
    def update(self, db: Session, org: organizations, org_data: Dict[str, Any]) -> organizations:
        """Update an existing organization"""
        return self._crud_handler.update_organization(db=db, db_obj=org, obj_in=org_data)

