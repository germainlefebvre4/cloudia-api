from typing import Any, List
import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.api.api_v1.helpers.aws import aws_list_accounts
from app.api.api_v1.helpers.gcp import gcp_list_projects

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
    # redis_c.get("cloud:aws:projects")
    acccounts = aws_list_accounts(redis_c)
    # redis_c.set("cloud:aws:projects", json.dumps(acccounts.toJSON()))
    return acccounts

@router.post("/providers/aws/projects")
async def create_aws_project() -> Any:
    return {}


# Google Cloud
@router.get("/providers/gcp/projects", response_model=List[schemas.CloudProject])
async def get_google_projects(
    redis_c = Depends(deps.get_redis),
) -> Any:
    projects = gcp_list_projects(redis_c)
    return projects

@router.post("/providers/gcp/projects")
async def create_google_project() -> Any:
    return {}
