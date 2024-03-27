from enum import Enum
from typing import Optional
from datetime import datetime
import json

from pydantic import BaseModel, Field, EmailStr

from app.schemas.cloud_provider import CloudProvider


class CloudCarbonFootprint(BaseModel):
    project_id: Optional[int] = Field(None, description="ID of the Cloud project.")
    year: Optional[int] = Field(None, description="Year for the date range of the carbon footprint.")
    month: Optional[int] = Field(None, description="Month for the date range of the carbon footprint.")
    total: Optional[float] = Field(None, description="Total amount of the carbon footprint.")
    unit: Optional[str] = Field("kgCO2e", description="Unit of the carbon footprint.")

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


class CloudCarbonFootprintResponse(CloudCarbonFootprint):
    pass

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
