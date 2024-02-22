from typing import Any, List, Union
import json
from app.api.api_v1.technical.dummy import list_dummy_projects

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.api.api_v1.technical.aws import get_aws_project_carbon_footprint
from app.api.api_v1.technical.gcp import get_gcp_project_carbon_footprint
from app.api.api_v1.technical.cache import flush_carbon_footprint_cache

router = APIRouter()


# Cloud Projects - Google Cloud
@router.get("/gcp/projects/{project_id}", response_model=Any)
async def get_google_projects_carbon_footprint(
    project_id: int,
    year: int,
    month: int,
    redis_c = Depends(deps.get_redis),
) -> schemas.CloudCarbonFootprintResponse:
    carbon_footprint = get_gcp_project_carbon_footprint(redis_c=redis_c, project_id=project_id, year=year, month=month)
    return carbon_footprint


# Cloud Projects - Amazon Web Services
@router.get("/aws/projects/{project_id}", response_model=Union[schemas.CloudCarbonFootprintResponse, schemas.Msg])
async def get_aws_projects_carbon_footprint(
    project_id: int,
    year: int,
    month: int,
    redis_c = Depends(deps.get_redis),
) -> schemas.CloudCarbonFootprintResponse:
    carbon_footprint = get_aws_project_carbon_footprint(redis_c=redis_c, project_id=project_id, year=year, month=month)
    return carbon_footprint


# Cache flush
@router.post("/providers/projects/cache/refresh", response_model=schemas.Msg)
async def refresh_providers_projects(
    redis_c = Depends(deps.get_redis),
) -> schemas.Msg:
    flush_carbon_footprint_cache(redis_c=redis_c)
    return {"msg": f"Cloud Project cache flushed for all providers"}
