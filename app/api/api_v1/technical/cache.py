from typing import Any
import logging
import json

from fastapi import Depends

from app.api import deps
from app import schemas
from app.core.config import settings


def flush_cloud_projects_cache(
    redis_c = Depends(deps.get_redis),
) -> Any:
    redis_c.delete("cloud:*:projects")
    redis_c.delete("cloud:*:projects:tags")
    return {}


def flush_cloud_project_cache(
    cloud_provider: str,
    redis_c = Depends(deps.get_redis),
) -> Any:
    redis_c.delete(f"cloud:{cloud_provider}:projects")
    redis_c.delete(f"cloud:{cloud_provider}:projects:tags")
    return {}
