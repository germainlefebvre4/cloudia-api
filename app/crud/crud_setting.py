from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.setting import Setting
from app.schemas.setting import SettingCreate, SettingUpdate


class CRUDSetting(CRUDBase[Setting, SettingCreate, SettingUpdate]):
    def get_by_key(
        self, db: Session, *,
        key: str,
    ) -> Setting:
        return (
            db.query(Setting)
            .filter(Setting.key == key)
            .order_by(Setting.category.asc())
            .first()
        )


setting = CRUDSetting(Setting)
