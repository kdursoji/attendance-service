from operator import or_
from typing import List, Dict, Any
from sqlalchemy import func
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.users import User, UserActivity


class UserActivityCrudHandler(CRUDBase[UserActivity, None, None]):

    def create_user_activity(
            self, db: Session, obj_in: Dict[str, Any]
    ) -> User:
        return super().create(db, obj_in)


user_activity_crud_handler = UserActivityCrudHandler(UserActivity)
