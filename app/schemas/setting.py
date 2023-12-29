from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class SettingBase(BaseModel):
    pass

class SettingCreate(SettingBase):
    key: str
    value: str
    type: str
    category: Optional[str] = ""
    description: Optional[str]


class SettingUpdate(SettingBase):
    key: Optional[str]
    value: Optional[str]
    type: Optional[str]
    category: Optional[str]
    description: Optional[str]


class SettingInDBBase(SettingBase):
    id: Optional[int] = None

    key: str
    value: str
    type: str
    category: str
    description: Optional[str] = ""

    class Config:
        orm_mode = True


class Setting(SettingInDBBase):
    pass


class SettingInDB(SettingInDBBase):
    pass
