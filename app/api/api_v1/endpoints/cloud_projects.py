from typing import Any, List
import json
from app.api.api_v1.technical.dummy import list_dummy_projects

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.api.api_v1.technical.aws import list_aws_projects, list_aws_project_tags, show_aws_project_details
from app.api.api_v1.technical.gcp import list_gcp_projects, list_gcp_project_tags, show_gcp_project_details
from app.api.api_v1.technical.cache import flush_cloud_projects_cache

router = APIRouter()


# Cloud Providers
@router.get("/providers")
async def get_providers() -> Any:
    return {}


# Cloud Projects - All
@router.get("/providers/projects", response_model=schemas.CloudProjectsResponse)
async def get_all_projects(
    redis_c = Depends(deps.get_redis),
) -> Any:
    dummy_projects = list_dummy_projects()
    aws_projects = list_aws_projects(redis_c)
    gcp_projects = list_gcp_projects(redis_c)
    projects = aws_projects + gcp_projects
    return schemas.CloudProjectsResponse(
        projects = projects,
        count = len(projects),
    )

# Cloud Projects - Dummy
@router.get("/providers/dummy/projects", response_model=schemas.CloudProjectsResponse)
async def get_aws_projects() -> Any:
    projects = list_dummy_projects()
    return schemas.CloudProjectsResponse(
        provider = schemas.cloud_provider.Dummy(),
        projects = projects,
        count = len(projects),
    )


# Cloud Projects - AWS
@router.get("/providers/aws/projects", response_model=schemas.CloudProjectsResponse)
async def get_aws_projects(
    redis_c = Depends(deps.get_redis),
) -> Any:
    projects = list_aws_projects(redis_c)
    return schemas.CloudProjectsResponse(
        provider = schemas.cloud_provider.AWS(),
        projects = projects,
        count = len(projects),
    )

@router.get("/providers/aws/projects/tags", response_model=List[Any])
async def get_aws_projects(
    redis_c = Depends(deps.get_redis),
) -> Any:
    tags = list_aws_project_tags(redis_c)
    return tags

@router.post("/providers/aws/projects")
async def create_aws_project() -> Any:
    return {}

@router.get("/providers/aws/projects/{project_id}", response_model=schemas.CloudProject)
async def get_aws_project_details(
    project_id: int,
    redis_c = Depends(deps.get_redis),
) -> Any:
    project = show_aws_project_details(redis_c=redis_c, project_id=project_id)
    return project


# Cloud Projects - Google Cloud
@router.get("/providers/gcp/projects", response_model=schemas.CloudProjectsResponse)
async def get_google_projects(
    redis_c = Depends(deps.get_redis),
) -> Any:
    projects = list_gcp_projects(redis_c)
    return schemas.CloudProjectsResponse(
        provider = schemas.cloud_provider.GCP(),
        projects = projects,
        count = len(projects),
    )

@router.get("/providers/gcp/projects/tags", response_model=List[Any])
async def get_google_projects(
    redis_c = Depends(deps.get_redis),
) -> Any:
    tags = list_gcp_project_tags(redis_c)
    return tags

@router.post("/providers/gcp/projects")
async def create_google_project() -> Any:
    return {}

@router.get("/providers/gcp/projects/{project_id}", response_model=schemas.CloudProject)
async def get_gcp_project_details(
    project_id: int,
    redis_c = Depends(deps.get_redis),
) -> Any:
    project = show_gcp_project_details(redis_c=redis_c, project_id=project_id)
    return project


# Cache flush
@router.post("/providers/{provider}/projects/cache/refresh", response_model=schemas.Msg)
async def refresh_provider_projects(
    provider: str,
    redis_c = Depends(deps.get_redis),
) -> Any:
    flush_cloud_projects_cache(redis_c=redis_c, cloud_provider=provider)
    return {"msg": f"Cloud Project cache flushed for provider {provider}"}


@router.post("/providers/cache/refresh", response_model=schemas.Msg)
async def refresh_provider_projects(
    redis_c = Depends(deps.get_redis),
) -> Any:
    flush_cloud_projects_cache(redis_c=redis_c)
    return {"msg": f"Cloud Project cache flushed for all providers"}
