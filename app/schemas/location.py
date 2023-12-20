from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class LocationBase(BaseModel):
    pass

class LocationCreate(LocationBase):
    key: int
    kind: int
    country: str
    label: Optional[str] = ""
    additional: Optional[str] = ""


class LocationUpdate(LocationBase):
    key: Optional[int]
    kind: Optional[int]
    country: Optional[str]
    label: Optional[str] = ""
    additional: Optional[str] = ""


class LocationInDBBase(LocationBase):
    id: int

    key: int
    kind: int
    country: str
    label: Optional[str] = ""
    additional: Optional[str] = ""

    class Config:
        orm_mode = True


class Location(LocationInDBBase):
    pass


class LocationInDB(LocationInDBBase):
    pass
