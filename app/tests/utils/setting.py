from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.setting import SettingCreate, SettingUpdate
from app.tests.utils.utils import random_lower_string, randome_int_number, random_float_number


def create_random_setting(*, db: Session) -> models.Setting:
    key = random_lower_string()
    value = random_lower_string()
    category = random_lower_string()
    description = random_lower_string()
    setting_in = SettingCreate(key=key, value=value, category=category,description=description)
    return crud.setting.create(db=db, obj_in=setting_in)
