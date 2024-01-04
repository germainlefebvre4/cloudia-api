
from datetime import datetime
import json
import boto3
import logging

from fastapi import Depends

from app.api import deps
from app import schemas
from app.core.config import settings


def aws_list_accounts(
    redis_c = Depends(deps.get_redis),
):
    active_project = []
    if redis_c.exists(f"cloud:aws:projects") == 0:
        logging.debug("non-cached")
        client = boto3.client(
            'organizations',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        aws_accounts = client.list_accounts()

        # for page in page_iterator:
        for account in aws_accounts['Accounts']:
            res = client.list_tags_for_resource(
                ResourceId = account['Id'],
            )
            tags = {res['Tags'][i]['Key']: res['Tags'][i]['Value'] for i in range(len(res['Tags']))}
            data = schemas.CloudProject(
                id = account['Id'],
                name = account['Name'],
                email = account['Email'],
                state = account['Status'],
                tags = tags,
                created_at = account['JoinedTimestamp'],
            )
            active_project.append(data)

        redis_c.set(
            f"cloud:aws:projects",
            json.dumps([project.json() for project in active_project]),
            ex=60*60*24,
        )
    else:
        logging.debug("cached")
        projects = json.loads(redis_c.get(f"cloud:aws:projects"))
        for project in projects:
            data = schemas.CloudProject(**json.loads(project))
            active_project.append(data)

    return active_project
