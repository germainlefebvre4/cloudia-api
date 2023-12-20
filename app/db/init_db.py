from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401

from app.tests.utils.utils import random_lower_string

from dotenv import load_dotenv
load_dotenv()


def init_db(db: Session) -> None:
    # Create users
    user_admin = crud.user.get_by_email(db, email=settings.USER_ADMIN_EMAIL)
    if not user_admin:
        user_in = schemas.UserCreate(
            email=settings.USER_ADMIN_EMAIL,
            full_name=settings.USER_ADMIN_FULLNAME,
            password=settings.USER_ADMIN_PASSWORD,
            is_superuser=True,
        )
        user_admin = crud.user.create(db, obj_in=user_in)

    user_test = crud.user.get_by_email(db, email=settings.USER_TEST_EMAIL)
    if not user_test:
        user_in = schemas.UserCreate(
            email=settings.USER_TEST_EMAIL,
            full_name=settings.USER_TEST_FULLNAME,
            password=settings.USER_TEST_PASSWORD,
            is_superuser=False,
        )
        user_test = crud.user.create(db, obj_in=user_in)

    # Create locations
    location_1_in = schemas.LocationCreate(
        key=203,
        kind=1,
        country='Baleares',
        label='Palma de Majorque Aeroport PMI',
    )
    location_1 = crud.location.create(db, obj_in=location_1_in)

    location_2_in = schemas.LocationCreate(
        key=2372,
        kind=2,
        country='France',
        label='Lille Aeroport Lesquin LIL',
    )
    location_2 = crud.location.create(db, obj_in=location_2_in)
