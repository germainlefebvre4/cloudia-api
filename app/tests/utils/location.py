from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.location import LocationCreate, LocationUpdate
from app.tests.utils.utils import random_lower_string, randome_int_number, random_float_number


def create_random_location(*, db: Session) -> models.Location:
    key = randome_int_number()
    kind = randome_int_number()
    country = random_lower_string()
    label = random_lower_string()
    additional = random_lower_string()
    location_in = LocationCreate(key=key, kind=kind, country=country, label=label, additional=additional)
    return crud.location.create(db=db, obj_in=location_in)
