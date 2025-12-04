from operator import or_
from typing import List, Dict, Any
from sqlalchemy import func
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.users import User


class UserCrudHandler(CRUDBase[User, None, None]):

    def get_row_by_user_name(
            self, db: Session, *, user_name: str
    ) -> User:
        return (
            db.query(self.model)
            .filter(or_(func.lower(User.email) == func.lower(user_name),
                        func.lower(User.user_name) == func.lower(user_name))).first()
        )

    def get_row_by_user_id(
            self, db: Session, *, id: str
    ) -> User:
        return (
            super().get(db=db, id=id)
        )

    def get_multi_rows(
            self, db: Session
    ) -> List[User]:
        return (
            [r.serialize() for r in db.query(self.model).all()]
        )

    def create_user(
            self, db: Session, obj_in: Dict[str, Any]
    ) -> User:
        return super().create(db, obj_in)

    def update_user(
            self, db: Session, db_obj: User, obj_in: Dict[str, Any]
    ) -> User:
        return super().update(db, db_obj=db_obj, obj_in=obj_in)


user_crud_handler = UserCrudHandler(User)
