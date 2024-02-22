from enum import Enum
from typing import Optional
from datetime import datetime
import json

from pydantic import BaseModel, Field, EmailStr


# class StateEnum(str, Enum):
#     UNKNOWN = "UNKNOWN"
#     ACTIVE = "ACTIVE"
#     INACTIVE = "INACTIVE"
#     DELETED = "DELETED"

class CloudProvider(BaseModel):
    slug: Optional[str] = Field(None, description="Slug name of the Cloud provider.")
    title_full: Optional[str] = Field(None, description="Full name of the Cloud provider.")
    title_short: Optional[str] = Field(None, description="Sort name name of the Cloud provider.")

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

def AWS():
    return CloudProvider(
        slug = "aws",
        title_full = "Amazon Web Services",
        title_short = "AWS",
    )

def Dummy():
    return CloudProvider(
        slug = "dummy",
        title_full = "Dummy Cloud Provider",
        title_short = "Dummy",
    )

def GCP():
    return CloudProvider(
        slug = "gcp",
        title_full = "Google Cloud Platform",
        title_short = "GCP",
    )

def Azure():
    return CloudProvider(
        slug = "azure",
        title_full = "Microsoft Azure",
        title_short = "Azure",
    )
