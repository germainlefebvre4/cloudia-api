from typing import Any
import logging
import json

from fastapi import Depends

from app.api import deps
from app import schemas
from app.core.config import settings
from app.core.variables import variables

from app.api.api_v1.helpers.aws import aws_get_account_details, aws_list_accounts, aws_get_project_billing, aws_get_project_carbon_footprint


def list_aws_projects(
    redis_c = Depends(deps.get_redis),
) -> list[schemas.CloudProject]:
    aws_projects = []
    redis_key_projects = variables.redis_key_for_projects_by_provider(provider="aws")
    redis_key_projects_tags = variables.redis_key_for_projects_tags_by_provider(provider="aws")

    if redis_c.exists(redis_key_projects) == 0:
        aws_projects = aws_list_accounts()
        redis_c.set(
            redis_key_projects,
            json.dumps([project.json() for project in aws_projects]),
            ex=variables.redis_ttl_for_projects,
        )

        project_tags = []
        for project in aws_projects:
            project_tags += project.tags.keys()
        project_tags = sorted(list(set(project_tags)))
        redis_c.set(
            redis_key_projects_tags,
            json.dumps(project_tags),
            ex=variables.redis_ttl_for_projects_tags,
        )
        project_tags = json.loads(redis_c.get(redis_key_projects_tags))
    else:
        projects = json.loads(redis_c.get(redis_key_projects))
        for project in projects:
            data = schemas.CloudProject(**json.loads(project))
            aws_projects.append(data)

    return aws_projects


def list_aws_project_tags(
    redis_c = Depends(deps.get_redis),
) -> list[Any]:
    aws_project_tags = []
    redis_key_projects_tags = variables.redis_key_for_projects_tags_by_provider(provider="aws")

    if redis_c.exists(redis_key_projects_tags) == 0:
        pass
    else:
        aws_project_tags = json.loads(redis_c.get(redis_key_projects_tags))
    
    return aws_project_tags


def get_aws_project_billing (
    project_id: int,
    year: int,
    month: int,
    redis_c = Depends(deps.get_redis),
) -> schemas.CloudBillingResponse:
    redis_key = variables.redis_key_for_billing_by_provider_project(provider="aws", project_id=project_id, year=year, month=month)
    if redis_c.exists(redis_key) == 0:
        aws_project_billing = aws_get_project_billing(project_id=project_id, year=year, month=month)
        redis_c.set(
            redis_key,
            json.dumps(aws_project_billing.json()),
            ex=variables.redis_ttl_for_billing,
        )
    project_billing = json.loads(redis_c.get(redis_key))
    
    return schemas.CloudBillingResponse(**json.loads(project_billing))


def get_aws_project_carbon_footprint(
    project_id: int,
    year: int,
    month: int,
    redis_c = Depends(deps.get_redis),
) -> schemas.CloudCarbonFootprintResponse:
    redis_key = variables.redis_key_for_carbon_footprint(provider="aws", project_id=project_id, year=year, month=month)
    if redis_c.exists(redis_key) == 0:
        aws_project_carbon_footprint = aws_get_project_carbon_footprint(project_id=project_id, year=year, month=month)
        redis_c.set(
            redis_key,
            json.dumps(aws_project_carbon_footprint.json()),
            ex=variables.redis_ttl_for_carbon_footprint,
        )
    project_carbon_footprint = json.loads(redis_c.get(redis_key))
    
    return schemas.CloudCarbonFootprintResponse(**json.loads(project_carbon_footprint))

def show_aws_project_details(
    project_id: int,
    provider: str = 'aws',
    redis_c = Depends(deps.get_redis),
) -> schemas.CloudProject:
    project = None
    project = aws_get_account_details(project_id=project_id)
    return project
