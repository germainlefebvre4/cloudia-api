from datetime import datetime
# from dateutils import relativedelta
from typing import Any, List, Union
import json
import requests
from app.api.api_v1.technical.dummy import list_dummy_projects

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core.config import settings
from app.api import deps
from app.api.api_v1.technical.ccf import get_ccf_estimation

router = APIRouter()


# Cloud Carbon Footprint
@router.get("/footprint", response_model=Any)
async def get_ccf_estimation_from_date_range(
    cloud_provider: str = None,
    start_year: int = 2024,
    start_month: int = 3,
    start_day: int = 1,
    end_year: int = 2024,
    end_month: int = 2,
    end_day: int = 1,
    redis_c = Depends(deps.get_redis),
) -> schemas.CloudCarbonFootprintResponse:
    carbon_footprint = get_ccf_estimation(redis_c=redis_c, start_year=start_year, start_month=start_month, start_day=start_day, end_year=end_year, end_month=end_month, end_day=end_day)

    providers = set([])
    for data in carbon_footprint:
        for i in data["serviceEstimates"]:
            providers.add(i["cloudProvider"])

    if cloud_provider and cloud_provider not in providers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cloud Provider {cloud_provider} not found",
        )

    results = []
    result_provider = []
    for provider in providers:
        for data in carbon_footprint:
            if cloud_provider is None:
                data_filtered = [x for x in data["serviceEstimates"]]
            else:
                data_filtered = [x for x in data["serviceEstimates"] if x["cloudProvider"] == provider]
            data_tmp = {
                "timestamp": data["timestamp"],
                "co2e": sum([float(x["co2e"]) for x in data_filtered if x["co2e"] is not None]),
                "cost": sum([x["cost"] for x in data_filtered]),
            }
            result_provider.append(data_tmp)
    
        results.append({
            "provider": provider,
            "results": result_provider,
        })

    return results

@router.get("/footprint/{cloud_provider}/projects/chart", response_model=Any)
async def get_ccf_estimation_from_date_range_for_chart(
    cloud_provider: str = None,
    start_year: int = 2024,
    start_month: int = 3,
    start_day: int = 1,
    end_year: int = 2024,
    end_month: int = 2,
    end_day: int = 1,
    redis_c = Depends(deps.get_redis),
) -> schemas.CloudCarbonFootprintResponse:
    carbon_footprint = get_ccf_estimation(redis_c=redis_c, start_year=start_year, start_month=start_month, start_day=start_day, end_year=end_year, end_month=end_month, end_day=end_day)

    providers = set([])
    for data in carbon_footprint:
        for i in data["serviceEstimates"]:
            providers.add(i["cloudProvider"])

    if cloud_provider and cloud_provider not in list(map(lambda x: x.lower(), providers)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cloud Provider {cloud_provider} not found",
        )

    results = []
    result_provider = []
    for provider in providers:
        for data in carbon_footprint:
            if cloud_provider is None:
                data_filtered = [x for x in data["serviceEstimates"]]
            else:
                data_filtered = [x for x in data["serviceEstimates"] if x["cloudProvider"] == provider]
            data_tmp = {
                "timestamp": data["timestamp"],
                "co2e": sum([float(x["co2e"]) for x in data_filtered if x["co2e"] is not None]),
                "cost": sum([x["cost"] for x in data_filtered]),
            }
            result_provider.append(data_tmp)
    
        results.append({
            "provider": provider,
            "results": result_provider,
        })

    return results
