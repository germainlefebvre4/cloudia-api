from typing import Any, Optional
from datetime import datetime

from pydantic import BaseModel


class SettingBase(BaseModel):
    pass

class SettingCreate(SettingBase):
    path: Optional[str] = ""
    key: str
    value: Any
    type: str
    description: Optional[str]


class SettingUpdate(SettingBase):
    value: Any


class SettingInDBBase(SettingBase):
    id: Optional[int] = None

    path: str
    key: str
    value: Any
    type: str
    description: Optional[str] = ""

    class Config:
        orm_mode = True


class Setting(SettingInDBBase):
    pass


class SettingInDB(SettingInDBBase):
    pass
