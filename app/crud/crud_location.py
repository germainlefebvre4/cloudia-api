from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.location import Location
from app.schemas.location import LocationCreate, LocationUpdate


class CRUDLocation(CRUDBase[Location, LocationCreate, LocationUpdate]):
    def get_by_key(
        self, db: Session, *,
        key: str,
    ) -> Location:
        return (
            db.query(Location)
            .filter(Location.key == key)
            .order_by(Location.id.asc())
            .first()
        )


location = CRUDLocation(Location)
