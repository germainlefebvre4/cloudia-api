from datetime import datetime

from google.cloud import resourcemanager_v3
from google.oauth2 import service_account

from app import schemas
from app.core.config import settings


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


def gcp_list_projects() -> list[schemas.CloudProject]:
    active_project = []

    for projects in search_projects(f"organizations/{settings.GCP_ORGANIZATION_ID}"):
        data = schemas.CloudProject(
            id=projects.name.split("/")[-1],
            name=projects.display_name,
            parent=projects.parent,
            tags=projects.labels,
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
                tags=projects.labels,
                state=str(projects.state).split(".")[1],
                created_at=datetime.fromtimestamp(projects.create_time.timestamp()),
            )
            active_project.append(data)

    return active_project
