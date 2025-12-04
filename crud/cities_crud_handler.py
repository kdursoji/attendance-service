from operator import or_
from typing import List, Dict, Any
from sqlalchemy import func
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.geography import Countries, States, Cities
from models.users import User


class CitiesCrudHandler(CRUDBase[Cities, None, None]):
    def get_cities(
            self, db: Session, state_id: int
    ) -> List[Cities]:
        return (
            [r.serialize() for r in db.query(self.model).filter(Cities.state_id == state_id).all()]
        )


cities_crud_handler = CitiesCrudHandler(Cities)
