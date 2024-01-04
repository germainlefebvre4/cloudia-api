from typing import Any
import logging
import json

from fastapi import Depends

from app.api import deps
from app import schemas
from app.core.config import settings

from app.api.api_v1.helpers.aws import aws_list_accounts


def list_aws_projects(
    redis_c = Depends(deps.get_redis),
) -> list[schemas.CloudProject]:
    aws_projects = []
    if redis_c.exists(f"cloud:aws:projects") == 0:
        logging.debug("non-cached")
        aws_projects = aws_list_accounts()
        redis_c.set(
            f"cloud:aws:projects",
            json.dumps([project.json() for project in aws_projects]),
            ex=60*60*24,
        )

        project_tags = []
        for project in aws_projects:
            project_tags += project.tags.keys()
        project_tags = sorted(list(set(project_tags)))
        redis_c.set(
            f"cloud:aws:projects:tags",
            json.dumps(project_tags),
            ex=60*60*24,
        )
        project_tags = json.loads(redis_c.get(f"cloud:aws:projects:tags"))
    else:
        logging.debug("cached")
        projects = json.loads(redis_c.get(f"cloud:aws:projects"))
        for project in projects:
            data = schemas.CloudProject(**json.loads(project))
            aws_projects.append(data)

    return aws_projects


def list_aws_project_tags(
    redis_c = Depends(deps.get_redis),
) -> list[Any]:
    aws_project_tags = []

    if redis_c.exists(f"cloud:aws:projects:tags") == 0:
        logging.debug("non-cached")
        pass
    else:
        logging.debug("cached")
        aws_project_tags = json.loads(redis_c.get(f"cloud:aws:projects:tags"))
    
    return aws_project_tags
