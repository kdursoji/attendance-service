"""
User Repository Interface and Implementation
Following Interface Segregation and Dependency Inversion Principles
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from models.users import User


class IUserRepository(ABC):
    """Interface for User Repository - Interface Segregation Principle"""
    
    @abstractmethod
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """Get user by username or email"""
        pass
    
    @abstractmethod
    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        pass
    
    @abstractmethod
    def get_all(self, db: Session) -> List[Dict[str, Any]]:
        """Get all users as serialized dictionaries"""
        pass
    
    @abstractmethod
    def create(self, db: Session, user_data: Dict[str, Any]) -> User:
        """Create a new user"""
        pass
    
    @abstractmethod
    def update(self, db: Session, user: User, user_data: Dict[str, Any]) -> User:
        """Update an existing user"""
        pass


class UserRepository(IUserRepository):
    """User Repository Implementation - Single Responsibility Principle"""
    
    def __init__(self, crud_handler):
        """Dependency Injection - Dependency Inversion Principle"""
        self._crud_handler = crud_handler
    
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """Get user by username or email"""
        return self._crud_handler.get_row_by_user_name(db=db, user_name=username)
    
    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self._crud_handler.get_row_by_user_id(db=db, id=user_id)
    
    def get_all(self, db: Session) -> List[Dict[str, Any]]:
        """Get all users as serialized dictionaries"""
        return self._crud_handler.get_multi_rows(db=db)
    
    def create(self, db: Session, user_data: Dict[str, Any]) -> User:
        """Create a new user"""
        return self._crud_handler.create_user(db=db, obj_in=user_data)
    
    def update(self, db: Session, user: User, user_data: Dict[str, Any]) -> User:
        """Update an existing user"""
        return self._crud_handler.update_user(db=db, db_obj=user, obj_in=user_data)

