from typing import Any, Dict, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.setting import Setting
from app.schemas.setting import SettingCreate, SettingUpdate


class CRUDSetting(CRUDBase[Setting, SettingCreate, SettingUpdate]):
    def get_keys(
        self, db: Session, *,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Setting]:
        settings = db.query(Setting).offset(skip).limit(limit).all()
        for setting in settings:
            if setting.type ==  "bool":
                if setting.value == "true":
                    setting.value = True
                elif setting.value == "false":
                    setting.value = False
                else:
                    setting.value = eval(setting.type)(setting.value)
            else:
                setting.value = eval(setting.type)(setting.value)
        return settings

    def get_key(
        self, db: Session, *,
        id: Any,
    ) -> Setting:
        setting = db.query(Setting).filter(Setting.id == id).first()
        if setting.type ==  "bool":
            if setting.value == "true":
                setting.value = True
            elif setting.value == "false":
                setting.value = False
            else:
                setting.value = eval(setting.type)(setting.value)
        else:
            setting.value = eval(setting.type)(setting.value)
        return setting

    def get_by_key(
        self, db: Session, *,
        key: str,
    ) -> Setting:
        setting = (
            db.query(Setting)
            .filter(Setting.key == key)
            .order_by(Setting.category.asc())
            .first()
        )
        if setting.type ==  "bool":
            if setting.value == "true":
                setting.value = True
            elif setting.value == "false":
                setting.value = False
            else:
                setting.value = eval(setting.type)(setting.value)
        else:
            setting.value = eval(setting.type)(setting.value)
        return setting

    def get_by_path(
        self, db: Session, *,
        path: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Setting]:
        settings = (
            db.query(Setting)
            .filter(Setting.path == path)
            .order_by(Setting.key.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        for setting in settings:
            if setting.type ==  "bool":
                if setting.value == "true":
                    setting.value = True
                elif setting.value == "false":
                    setting.value = False
                else:
                    setting.value = eval(setting.type)(setting.value)
            else:
                setting.value = eval(setting.type)(setting.value)
        return settings

    def get_by_path_by_key(
        self, db: Session, *,
        path: str,
        key: str,
    ) -> Setting:
        setting = (
            db.query(Setting)
            .filter(Setting.path == path)
            .filter(Setting.key == key)
            .first()
        )
        if not setting:
            return None
        if setting.type ==  "bool":
            if setting.value == "true":
                setting.value = True
            elif setting.value == "false":
                setting.value = False
            else:
                setting.value = eval(setting.type)(setting.value)
        else:
            setting.value = eval(setting.type)(setting.value)
        # print(setting.path, setting.key, setting.value, setting.type)
        return setting


    def update_value(
        self, db: Session, *,
        db_obj: Setting,
        obj_in: SettingUpdate,
    ) -> Setting:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        setattr(db_obj, "value", update_data["value"])
        db.add(db_obj)
        db.commit()
        db_obj.value = eval(db_obj.type)(update_data["value"])
        return db_obj


setting = CRUDSetting(Setting)
