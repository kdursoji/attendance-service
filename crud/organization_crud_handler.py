from operator import or_
from typing import List, Dict, Any
from sqlalchemy import func
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.organizations import organizations
from models.users import User


class organizationsCrudHandler(CRUDBase[organizations, None, None]):

    def get_organization(
            self, db: Session, id: int
    ) -> organizations:
        return super().get(db=db, id=id)

    def get_organizations_by_user_id(
            self, db: Session, user_id: int
    ) -> List[organizations]:
        return (
            [r.serialize() for r in db.query(self.model).filter(organizations.user_id == user_id).all()]
        )

    def create_organization(
            self, db: Session, obj_in: Dict[str, Any]
    ) -> organizations:
        return super().create(db, obj_in)

    def update_organization(
            self, db: Session, db_obj: User, obj_in: Dict[str, Any]
    ) -> organizations:
        return super().update(db, db_obj=db_obj, obj_in=obj_in)


organizations_crud_handler = organizationsCrudHandler(organizations)
