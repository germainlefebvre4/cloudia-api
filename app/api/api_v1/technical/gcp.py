from typing import Any
import logging
import json

from fastapi import Depends

from app.api import deps
from app import schemas
from app.core.config import settings

from app.api.api_v1.helpers.gcp import gcp_list_projects


def list_gcp_projects(
    redis_c = Depends(deps.get_redis),
) -> list[schemas.CloudProject]:
    gcp_projects = []
    if redis_c.exists(f"cloud:gcp:projects") == 0:
        logging.debug("non-cached")
        gcp_projects = gcp_list_projects()
        redis_c.set(
            f"cloud:gcp:projects",
            json.dumps([project.json() for project in gcp_projects]),
            ex=60*60*24,
        )

        project_tags = []
        for project in gcp_projects:
            project_tags += project.tags.keys()
        project_tags = sorted(list(set(project_tags)))
        redis_c.set(
            f"cloud:gcp:projects:tags",
            json.dumps(project_tags),
            ex=60*60*24,
        )
        project_tags = json.loads(redis_c.get(f"cloud:gcp:projects:tags"))
    else:
        logging.debug("cached")
        projects = json.loads(redis_c.get(f"cloud:gcp:projects"))
        for project in projects:
            data = schemas.CloudProject(**json.loads(project))
            gcp_projects.append(data)

    return gcp_projects


def list_gcp_project_tags(
    redis_c = Depends(deps.get_redis),
) -> list[Any]:
    gcp_project_tags = []

    if redis_c.exists(f"cloud:gcp:projects:tags") == 0:
        logging.debug("non-cached")
        pass
    else:
        logging.debug("cached")
        gcp_project_tags = json.loads(redis_c.get(f"cloud:gcp:projects:tags"))
    
    return gcp_project_tags
