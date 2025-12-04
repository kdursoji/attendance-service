from operator import or_
from typing import List, Dict, Any
from sqlalchemy import func
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.geography import Countries
from models.users import User


class CountriesCrudHandler(CRUDBase[Countries, None, None]):
    def get_countries(
            self, db: Session
    ) -> List[Countries]:
        return (
            [r.serialize() for r in db.query(self.model).all()]
        )


countries_crud_handler = CountriesCrudHandler(Countries)
