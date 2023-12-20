from enum import Enum
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


# class StateEnum(str, Enum):
#     UNKNOWN = "UNKNOWN"
#     ACTIVE = "ACTIVE"
#     INACTIVE = "INACTIVE"
#     DELETED = "DELETED"

class CloudProject(BaseModel):
    id: Optional[int] = Field(None, description="ID of the Cloud project.")
    name: Optional[str] = Field(None, description="Who sends the error message.")
    state: Optional[str] = "UNKNOWN"
    labels: Optional[dict] = Field(None, description="Labels attached to the Cloud project.")
    email: Optional[EmailStr] = Field(None, description="ID of the Cloud project.")

    parent: Optional[str] = Field(None, description="Parent resource of the Cloud project.")

    tags: Optional[dict] = Field(None, description="Tags attached to the Cloud project.")

    created_at: Optional[datetime] = Field(None, description="Createion date of the Cloud project.")
