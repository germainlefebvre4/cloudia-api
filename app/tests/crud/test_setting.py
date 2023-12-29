from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app import crud
from app.schemas.setting import SettingCreate, SettingUpdate
from app.tests.utils.setting import create_random_setting
from app.tests.utils.utils import random_lower_string, randome_int_number, random_float_number


def test_create_setting(db: Session) -> None:
    key = randome_int_number()
    kind = randome_int_number()
    country = random_lower_string()
    label = random_lower_string()
    setting_in = SettingCreate(key=key, kind=kind, country=country, label=label)
    setting = crud.setting.create(db=db, obj_in=setting_in)

    assert setting.key == key
    assert setting.kind == kind
    assert setting.country == country
    assert setting.label == label


def test_get_setting(db: Session) -> None:
    key = randome_int_number()
    kind = randome_int_number()
    country = random_lower_string()
    label = random_lower_string()
    setting_in = SettingCreate(key=key, kind=kind, country=country, label=label)
    setting = crud.setting.create(db=db, obj_in=setting_in)

    stored_setting = crud.setting.get(db=db, id=setting.id)

    assert stored_setting
    assert setting.id == stored_setting.id
    assert setting.key == stored_setting.key
    assert setting.kind == stored_setting.kind
    assert setting.country == stored_setting.country
    assert setting.label == stored_setting.label


def test_delete_setting(db: Session) -> None:
    key = randome_int_number()
    kind = randome_int_number()
    country = random_lower_string()
    label = random_lower_string()
    setting_in = SettingCreate(key=key, kind=kind, country=country, label=label)
    setting = crud.setting.create(db=db, obj_in=setting_in)

    setting2 = crud.setting.remove(db=db, id=setting.id)
    setting3 = crud.setting.get(db=db, id=setting.id)

    assert setting3 is None
    assert setting2.id == setting.id
    assert setting2.key == setting.key
    assert setting2.kind == setting.kind
    assert setting2.country == setting.country
    assert setting2.label == setting.label
