from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app import crud
from app.schemas.location import LocationCreate, LocationUpdate
from app.tests.utils.location import create_random_location
from app.tests.utils.utils import random_lower_string, randome_int_number, random_float_number


def test_create_location(db: Session) -> None:
    key = randome_int_number()
    kind = randome_int_number()
    country = random_lower_string()
    label = random_lower_string()
    location_in = LocationCreate(key=key, kind=kind, country=country, label=label)
    location = crud.location.create(db=db, obj_in=location_in)

    assert location.key == key
    assert location.kind == kind
    assert location.country == country
    assert location.label == label


def test_get_location(db: Session) -> None:
    key = randome_int_number()
    kind = randome_int_number()
    country = random_lower_string()
    label = random_lower_string()
    location_in = LocationCreate(key=key, kind=kind, country=country, label=label)
    location = crud.location.create(db=db, obj_in=location_in)

    stored_location = crud.location.get(db=db, id=location.id)

    assert stored_location
    assert location.id == stored_location.id
    assert location.key == stored_location.key
    assert location.kind == stored_location.kind
    assert location.country == stored_location.country
    assert location.label == stored_location.label


def test_delete_location(db: Session) -> None:
    key = randome_int_number()
    kind = randome_int_number()
    country = random_lower_string()
    label = random_lower_string()
    location_in = LocationCreate(key=key, kind=kind, country=country, label=label)
    location = crud.location.create(db=db, obj_in=location_in)

    location2 = crud.location.remove(db=db, id=location.id)
    location3 = crud.location.get(db=db, id=location.id)

    assert location3 is None
    assert location2.id == location.id
    assert location2.key == location.key
    assert location2.kind == location.kind
    assert location2.country == location.country
    assert location2.label == location.label
