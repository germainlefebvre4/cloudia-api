
import boto3

from app import schemas
from app.core.config import settings


def aws_list_accounts() -> list[schemas.CloudProject]:
    active_project = []

    client = boto3.client(
        'organizations',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    aws_accounts = client.list_accounts()

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

    return active_project
