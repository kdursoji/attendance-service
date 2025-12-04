from operator import or_
from typing import List, Dict, Any
from sqlalchemy import func
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.profile_imge import ProfileImages
from models.users import User


class ProfileImagesCrudHandler(CRUDBase[ProfileImages, None, None]):

    def get_row(
            self, db: Session, *, id: str
    ) -> ProfileImages:
        return (
            super().get(db=db, id=id)
        )

    def create_profile_pic(
            self, db: Session, obj_in: Dict[str, Any]
    ) -> ProfileImages:
        return super().create(db, obj_in)

    def update_profile_pic(
            self, db: Session, db_obj: User, obj_in: Dict[str, Any]
    ) -> ProfileImages:
        return super().update(db, db_obj=db_obj, obj_in=obj_in)


profile_pic_crud_handler = ProfileImagesCrudHandler(ProfileImages)
