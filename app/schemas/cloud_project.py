from enum import Enum
from typing import Optional
from datetime import datetime
import json

from pydantic import BaseModel, Field, EmailStr

from app.schemas.cloud_provider import CloudProvider


# class StateEnum(str, Enum):
#     UNKNOWN = "UNKNOWN"
#     ACTIVE = "ACTIVE"
#     INACTIVE = "INACTIVE"
#     DELETED = "DELETED"

class CloudProject(BaseModel):
    id: Optional[int] = Field(None, description="ID of the Cloud project.")
    provider: Optional[str] = Field(None, description="Cloud provider of the Cloud project.")
    name: Optional[str] = Field(None, description="Who sends the error message.")
    state: Optional[str] = "UNKNOWN"
    labels: Optional[dict] = Field(None, description="Labels attached to the Cloud project.")
    email: Optional[EmailStr] = Field(None, description="ID of the Cloud project.")
    parent: Optional[str] = Field(None, description="Parent resource of the Cloud project.")
    tags: Optional[dict] = Field(None, description="Tags attached to the Cloud project.")
    created_at: Optional[datetime] = Field(None, description="Createion date of the Cloud project.")
    additionals: Optional[dict] = Field(None, description="Additional information of the Cloud project.")

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


class CloudProjectsResponse(BaseModel):
    provider: Optional[CloudProvider] = Field(None, description="Cloud provider of the Cloud project.")
    projects: Optional[list[CloudProject]] = Field(None, description="Cloud projects of the Cloud provider.")
    count: Optional[int] = Field(None, description="Number of Cloud projects of the Cloud provider.")

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
