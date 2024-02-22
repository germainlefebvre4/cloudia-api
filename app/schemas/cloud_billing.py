from enum import Enum
from typing import Optional
from datetime import datetime
import json

from pydantic import BaseModel, Field, EmailStr

from app.schemas.cloud_provider import CloudProvider


class CloudBilling(BaseModel):
    project_id: Optional[int] = Field(None, description="ID of the Cloud project.")
    year: Optional[int] = Field(None, description="Year for the date range of the billing.")
    month: Optional[int] = Field(None, description="Month for the date range of the billing.")
    total: Optional[float] = Field(None, description="Total cost of the billing.")
    unit: Optional[str] = Field("USD", description="Unit of the billing.")

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


class CloudBillingResponse(CloudBilling):
    pass

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
