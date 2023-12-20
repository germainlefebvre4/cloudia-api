from typing import Any
from datetime import datetime

import boto3
from google.cloud import resourcemanager_v3
from google.oauth2 import service_account

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app import models, schemas
from app.api import deps
from app.core.celery_app import celery_app
from app.utils import send_test_email

from app.core.config import settings


router = APIRouter()


# @router.post("/test-celery/", response_model=schemas.Msg, status_code=201)
# def test_celery(
#     msg: schemas.Msg,
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Test Celery worker.
#     """
#     celery_app.send_task("app.worker.test_celery", args=[msg.msg])
#     return {"msg": "Word received"}


@router.post("/test-email/", response_model=schemas.Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}


def aws_list_accounts():
    client = boto3.client(
        'organizations',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    res = client.list_accounts()

    accounts = []
    # for page in page_iterator:
    for account in res['Accounts']:
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


        accounts.append(data)

    return accounts



credentials = service_account.Credentials.from_service_account_file(settings.GCP_SERVICE_ACCOUNT_JSON_KEY_FILE)

def get_folders(
    parent_id = f"organizations/{settings.GCP_ORGANIZATION_ID}",
    folders = None,
):
    if folders is None:
        folders = []

    client = resourcemanager_v3.FoldersClient(credentials=credentials)
    request = resourcemanager_v3.ListFoldersRequest(
        parent=parent_id,
    )

    page_result = client.list_folders(request=request)
    for pages in page_result:
        folders.append(pages.name)
        get_folders(parent_id=pages.name, folders=folders)
    return folders


def search_projects(folder_id):
    client = resourcemanager_v3.ProjectsClient(credentials=credentials)

    query = f"parent:{folder_id}"
    request = resourcemanager_v3.SearchProjectsRequest(query=query)
    page_result = client.search_projects(request=request)
    search_result = []
    for pages in page_result:
        search_result.append(pages)
    return search_result


def gcp_list_projects():
    active_project = []
    for projects in search_projects(f"organizations/{settings.GCP_ORGANIZATION_ID}"):
        data = schemas.CloudProject(
            id=projects.name.split("/")[1],
            name=projects.display_name,
            parent=projects.parent,
            labels=projects.labels,
            state=str(projects.state).split(".")[1],
            created_at=datetime.fromtimestamp(projects.create_time.timestamp()),
        )
        active_project.append(data)

    for folders in get_folders(parent_id=f"organizations/{settings.GCP_ORGANIZATION_ID}", folders=None):
        for projects in search_projects(folders):
            data = schemas.CloudProject(
                id=projects.name.split("/")[1],
                name=projects.display_name,
                parent=projects.parent,
                labels=projects.labels,
                state=str(projects.state).split(".")[1],
                created_at=datetime.fromtimestamp(projects.create_time.timestamp()),
            )
            active_project.append(data)

    return active_project
