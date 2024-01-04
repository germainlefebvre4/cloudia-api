from typing import Any, List
import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.api.api_v1.technical.aws import list_aws_projects, list_aws_project_tags
from app.api.api_v1.technical.gcp import list_gcp_projects, list_gcp_project_tags
from app.api.api_v1.technical.cache import flush_cloud_projects_cache, flush_cloud_project_cache

router = APIRouter()


# Cloud Providers
@router.get("/providers")
async def get_providers() -> Any:
    return {}


# Dummy
@router.get("/providers/dummy/projects", response_model=List[schemas.CloudProject])
async def get_aws_projects() -> Any:
    accounts = [
        schemas.CloudProject(id=100, name="dummy1", provider="aws", tags=[{"env": "prod", "customer": "My Company"}]),
        schemas.CloudProject(id=101, name="dummy2", provider="aws"),
        schemas.CloudProject(id=102, name="dummy3", provider="aws"),
        schemas.CloudProject(id=103, name="dummy4", provider="aws"),
        schemas.CloudProject(id=104, name="dummy5", provider="aws"),
    ]
    return accounts


# AWS
@router.get("/providers/aws/projects", response_model=List[schemas.CloudProject])
async def get_aws_projects(
    redis_c = Depends(deps.get_redis),
) -> Any:
    projects = list_aws_projects(redis_c)
    return projects

@router.get("/providers/aws/projects/tags", response_model=List[Any])
async def get_aws_projects(
    redis_c = Depends(deps.get_redis),
) -> Any:
    projects = list_aws_project_tags(redis_c)
    return projects

@router.post("/providers/aws/projects")
async def create_aws_project() -> Any:
    return {}


# Google Cloud
@router.get("/providers/gcp/projects", response_model=List[schemas.CloudProject])
async def get_google_projects(
    redis_c = Depends(deps.get_redis),
) -> Any:
    projects = list_gcp_projects(redis_c)
    return projects

@router.get("/providers/gcp/projects/tags", response_model=List[Any])
async def get_google_projects(
    redis_c = Depends(deps.get_redis),
) -> Any:
    projects = list_gcp_project_tags(redis_c)
    return projects

@router.post("/providers/gcp/projects")
async def create_google_project() -> Any:
    return {}


# Cache flush
@router.post("/providers/{provider}/projects/refresh", response_model=schemas.Msg)
async def refresh_provider_projects(
    provider: str,
    redis_c = Depends(deps.get_redis),
) -> Any:
    flush_cloud_project_cache(redis_c=redis_c, cloud_provider=provider)
    return {"msg": f"Cloud Project cache flushed for provider {provider}"}


@router.post("/providers/refresh", response_model=schemas.Msg)
async def refresh_provider_projects(
    redis_c = Depends(deps.get_redis),
) -> Any:
    flush_cloud_projects_cache(redis_c)
    return {"msg": f"Cloud Project cache flushed for all providers"}
