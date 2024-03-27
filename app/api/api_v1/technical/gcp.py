from typing import Any, List
import logging
import json

from app.core.settings_api import settings_api
from fastapi import Depends

from app.api import deps
from app import schemas
from app.core.config import settings
from app.core.variables import variables

if settings_api.GCP_ENABLED:
    from app.api.api_v1.helpers.gcp import gcp_list_projects, gcp_get_project_billing, gcp_get_projects_billing, gcp_get_project_carbon_footprint, gcp_get_account_details


def list_gcp_projects(
    redis_c = Depends(deps.get_redis),
) -> list[schemas.CloudProject]:
    gcp_projects = []
    redis_key_projects = variables.redis_key_for_projects_by_provider(provider="gcp")
    redis_key_projects_tags = variables.redis_key_for_projects_tags_by_provider(provider="gcp")

    if redis_c.exists(redis_key_projects) == 0:
        gcp_projects = gcp_list_projects()
        redis_c.set(
            redis_key_projects,
            json.dumps([project.json() for project in gcp_projects]),
            ex=variables.redis_ttl_for_projects,
        )

        project_tags = []
        for project in gcp_projects:
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
            gcp_projects.append(data)

    return gcp_projects


def list_gcp_project_tags(
    redis_c = Depends(deps.get_redis),
) -> list[Any]:
    gcp_project_tags = []
    redis_key_projects_tags = variables.redis_key_for_projects_tags_by_provider(provider="gcp")

    if redis_c.exists(redis_key_projects_tags) == 0:
        pass
    else:
        gcp_project_tags = json.loads(redis_c.get(redis_key_projects_tags))
    
    return gcp_project_tags


def get_gcp_project_billing (
    project_id: int,
    year: int,
    month: int,
    redis_c = Depends(deps.get_redis),
) -> schemas.CloudBillingResponse:
    redis_key = variables.redis_key_for_billing_by_provider_project(provider="gcp", project_id=project_id, year=year, month=month)
    if redis_c.exists(redis_key) == 0:
        gcp_project_billing = gcp_get_project_billing(project_id=project_id, year=year, month=month)
        redis_c.set(
            redis_key,
            json.dumps(gcp_project_billing.json()),
            ex=variables.redis_ttl_for_billing,
        )
    project_billing = json.loads(redis_c.get(redis_key))
    
    return schemas.CloudBillingResponse(**json.loads(project_billing))


def get_gcp_projects_billing (
    year_start: int,
    month_start: int,
    year_end: int,
    month_end: int,
    redis_c = Depends(deps.get_redis),
) -> List[schemas.CloudBillingResponse]:
    redis_key = variables.redis_key_for_billing_projects_by_provider(provider="gcp", year_start=year_start, month_start=month_start, year_end=year_end, month_end=month_end)
    if redis_c.exists(redis_key) == 0:
        gcp_project_billing = gcp_get_projects_billing(year_start=year_start, month_start=month_start, year_end=year_end, month_end=month_end)
        data = [x.json() for x in gcp_project_billing]
        redis_c.set(
            redis_key,
            json.dumps(data),
            ex=variables.redis_ttl_for_billing,
        )
    project_billing = json.loads(redis_c.get(redis_key))

    return [schemas.CloudBillingResponse(**json.loads(x)) for x in project_billing]


def get_gcp_project_carbon_footprint(
    project_id: int,
    year: int,
    month: int,
    redis_c = Depends(deps.get_redis),
) -> schemas.CloudCarbonFootprintResponse:
    redis_key = variables.redis_key_for_carbon_footprint(provider="gcp", project_id=project_id, year=year, month=month)
    if redis_c.exists(redis_key) == 0:
        gcp_project_carbon_footprint = gcp_get_project_carbon_footprint(project_id=project_id, year=year, month=month)
        if gcp_project_carbon_footprint is None:
            return None
        redis_c.set(
            redis_key,
            json.dumps(gcp_project_carbon_footprint.json()),
            ex=variables.redis_ttl_for_carbon_footprint,
        )
    project_carbon_footprint = json.loads(redis_c.get(redis_key))
    
    return schemas.CloudCarbonFootprintResponse(**json.loads(project_carbon_footprint))

def show_gcp_project_details(
    project_id: int,
    provider: str = 'gcp',
    redis_c = Depends(deps.get_redis),
) -> schemas.CloudProject:
    project = None
    project = gcp_get_account_details(project_id=project_id)
    return project
