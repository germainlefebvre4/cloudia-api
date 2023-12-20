from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.api.api_v1.endpoints.utils import aws_list_accounts, gcp_list_projects

router = APIRouter()


# Cloud Providers
@router.get("/providers")
async def get_providers(
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    return {"message": "Hello World"}


# AWS
@router.get("/providers/dummy/projects", response_model=List[schemas.CloudProject])
async def get_aws_projects(
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    accounts = [
        schemas.CloudProject(id=100, name="dummy1", provider="aws"),
        schemas.CloudProject(id=101, name="dummy2", provider="aws"),
        schemas.CloudProject(id=102, name="dummy3", provider="aws"),
        schemas.CloudProject(id=103, name="dummy4", provider="aws"),
        schemas.CloudProject(id=104, name="dummy5", provider="aws"),
    ]
    return accounts

# AWS
@router.get("/providers/aws/projects", response_model=List[schemas.CloudProject])
async def get_aws_projects(
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    acccounts = aws_list_accounts()
    return acccounts

@router.post("/providers/aws/projects")
async def create_aws_project():
    return {"message": "Hello World"}


# Google Cloud
@router.get("/providers/gcp/projects", response_model=List[schemas.CloudProject])
async def get_google_projects(
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    projects = gcp_list_projects()
    return projects

@router.post("/providers/gcp/projects")
async def create_google_project(
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    return {"message": "Hello World"}
