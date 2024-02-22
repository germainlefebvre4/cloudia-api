from typing import Any
import logging
import json

from fastapi import Depends

from app.api import deps
from app import schemas
from app.core.config import settings
from app.core.variables import variables


def flush_cloud_projects_cache(
    cloud_provider: str = "*",
    redis_c = Depends(deps.get_redis),
) -> Any:
    for key in redis_c.scan_iter(variables.redis_key_for_projects_by_provider(provider=cloud_provider)):
        redis_c.delete(key)
    for key in redis_c.scan_iter(variables.redis_key_for_projects_tags_by_provider(provider=cloud_provider)):
        redis_c.delete(key)
    return {}


def flush_billing_cache(
    cloud_provider: str = "*",
    project_id: int = "*",
    year: str = "*",
    month: str = "*",
    redis_c = Depends(deps.get_redis),
) -> Any:
    for key in redis_c.scan_iter(variables.redis_key_for_billing_by_provider_project(provider=cloud_provider, project_id=project_id, year=year, month=month)):
        redis_c.delete(key)
    return {}


def flush_carbon_footprint_cache(
    cloud_provider: str = "*",
    project_id: int = "*",
    year: str = "*",
    month: str = "*",
    redis_c = Depends(deps.get_redis),
) -> Any:
    for key in redis_c.scan_iter(variables.redis_key_for_carbon_footprint(provider=cloud_provider, project_id=project_id, year=year, month=month)):
        redis_c.delete(key)
    return {}
