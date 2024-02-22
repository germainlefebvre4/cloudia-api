from typing import Any, List
import json
from app.api.api_v1.technical.dummy import list_dummy_projects

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.api.api_v1.technical.aws import get_aws_project_billing
from app.api.api_v1.technical.gcp import get_gcp_project_billing
from app.api.api_v1.technical.cache import flush_billing_cache, flush_billing_cache, flush_billing_cache

router = APIRouter()


# Cloud Billing - Google Cloud
@router.get("/gcp/projects/{project_id}", response_model=Any)
async def get_google_projects_billing(
    project_id: int,
    year: int,
    month: int,
    redis_c = Depends(deps.get_redis),
) -> Any:
    billing = get_gcp_project_billing(redis_c=redis_c, project_id=project_id, year=year, month=month)
    return billing


# Cloud Billing - Amazon Web Services
@router.get("/aws/projects/{project_id}", response_model=Any)
async def get_aws_projects_billing(
    project_id: int,
    year: int,
    month: int,
    redis_c = Depends(deps.get_redis),
) -> Any:
    billing = get_aws_project_billing(redis_c=redis_c, project_id=project_id, year=year, month=month)
    return billing


# Cache flush
@router.post("/providers/projects/cache/refresh", response_model=schemas.Msg)
async def refresh_providers_projects(
    redis_c = Depends(deps.get_redis),
) -> Any:
    flush_billing_cache(redis_c=redis_c)
    return {"msg": f"Cloud Project cache flushed for all providers"}

@router.post("/providers/{provider}/projects/cache/refresh", response_model=schemas.Msg)
async def refresh_provider_projects(
    provider: str,
    redis_c = Depends(deps.get_redis),
) -> Any:
    flush_billing_cache(redis_c=redis_c, cloud_provider=provider)
    return {"msg": f"Cloud Project cache flushed for provider {provider}"}


@router.post("/providers/{provider}/projects/{project_id}/cache/refresh", response_model=schemas.Msg)
async def refresh_provider_project(
    provider: str,
    project_id: str,
    redis_c = Depends(deps.get_redis),
) -> Any:
    flush_billing_cache(redis_c=redis_c, cloud_provider=provider, project_id=project_id)
    return {"msg": f"Cloud Project cache flushed for provider {provider} and project {project_id}"}
