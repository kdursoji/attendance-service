from operator import or_
from typing import List, Dict, Any
from sqlalchemy import func
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.geography import Countries, States
from models.users import User


class StatesCrudHandler(CRUDBase[States, None, None]):
    def get_states(
            self, db: Session, *, country_id
    ) -> List[States]:
        return (
            [r.serialize() for r in db.query(self.model)
            .filter(States.country_id == country_id).all()]
        )


states_crud_handler = StatesCrudHandler(States)
