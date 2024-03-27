from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Any
import json

from google.cloud import resourcemanager_v3, bigquery
from google.oauth2 import service_account

from app import schemas
from app.core.config import settings
from app.core.settings_api import settings_api


credentials = service_account.Credentials.from_service_account_info(json.loads(settings_api.GCP_SERVICE_ACCOUNT_JSON_KEY_FILE))

def get_folders(
    parent_id = f"organizations/{settings_api.GCP_ORGANIZATION_ID}",
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

    for projects in search_projects(f"organizations/{settings_api.GCP_ORGANIZATION_ID}"):
        data = schemas.CloudProject(
            id=projects.name.split("/")[-1],
            provider = schemas.cloud_provider.GCP().slug,
            name=projects.display_name,
            parent=projects.parent,
            tags=projects.labels,
            state=str(projects.state).split(".")[1],
            created_at=datetime.fromtimestamp(projects.create_time.timestamp()),
        )
        active_project.append(data)

    for folders in get_folders(parent_id=f"organizations/{settings_api.GCP_ORGANIZATION_ID}", folders=None):
        for projects in search_projects(folders):
            data = schemas.CloudProject(
                id=projects.name.split("/")[1],
                provider = schemas.cloud_provider.GCP().slug,
                name=projects.display_name,
                parent=projects.parent,
                tags=projects.labels,
                state=str(projects.state).split(".")[1],
                created_at=datetime.fromtimestamp(projects.create_time.timestamp()),
            )
            active_project.append(data)

    return active_project


def gcp_get_project_billing(
    project_id: int,
    year: int,
    month: int,
) -> schemas.CloudBillingResponse:
    date_tmp = datetime.strptime(f"{year}-{month}", "%Y-%m")
    date_partition_current_month = date_tmp.strftime("%Y-%m-%d")
    date_partition_next_month = (date_tmp + relativedelta(months=1)).strftime("%Y-%m-%d")
    bigquery_billing_query = f"""
        SELECT
            project.number as project_id,
            sum(cost) as total_cost,
            SUM(IFNULL((SELECT SUM(c.amount) FROM UNNEST(credits) c), 0)) as total_credits
        FROM `{settings_api.GCP_BILLING_EXPORT_PROJECT_ID}.{settings_api.GCP_BILLING_EXPORT_DATASET_NAME}.gcp_billing_export_v1_{settings_api.GCP_BILLING_ACCOUNT_ID}`
        WHERE
            invoice.month = "{year:04d}{month:02d}" AND
            project.number = "{project_id}"
        GROUP BY 1;
    """
    client = bigquery.Client(credentials=credentials)
    query_job = client.query(bigquery_billing_query)
    results = query_job.result()
    res_total = None
    res_unit = None
    for row in results:
        res_total = float("{:.2f}".format(row[1]))
        res_unit = "USD"

    return schemas.CloudBillingResponse(
        project_id=project_id,
        year=year,
        month=month,
        total=res_total,
        unit=res_unit,
    )


def gcp_get_projects_billing(
    year_start: int,
    month_start: int,
    year_end: int,
    month_end: int,
) -> Any:
    bigquery_billing_query = f"""
        SELECT
            project.number as project_id,
            invoice.month as invoice_month,
            sum(cost) as total_cost,
            SUM(IFNULL((SELECT SUM(c.amount) FROM UNNEST(credits) c), 0)) as total_credits
        FROM `{settings_api.GCP_BILLING_EXPORT_PROJECT_ID}.{settings_api.GCP_BILLING_EXPORT_DATASET_NAME}.gcp_billing_export_v1_{settings_api.GCP_BILLING_ACCOUNT_ID}`
        WHERE
            invoice.month >= "{year_start:04d}{month_start:02d}" AND
            invoice.month <= "{year_end:04d}{month_end:02d}"
        GROUP BY
            1, 2
        ORDER BY
            invoice_month ASC, project_id DESC;
    """
    client = bigquery.Client(credentials=credentials)
    query_job = client.query(bigquery_billing_query)
    query_results = query_job.result()
    results = []
    for row in query_results:
        results.append(schemas.CloudBillingResponse(
            project_id=row[0],
            year=int(row[1][:4]),
            month=int(row[1][4:]),
            total=float("{:.2f}".format(row[2])),
            unit="USD",
        ))

    return results


def gcp_get_project_carbon_footprint(
    project_id: int,
    year: int,
    month: int,
) -> schemas.CloudCarbonFootprintResponse:
    date_tmp = datetime.strptime(f"{year}-{month}", "%Y-%m")
    date_current_month = date_tmp.strftime("%Y-%m-%d")
    date_next_month = (date_tmp + relativedelta(months=1) - relativedelta(days=1)).strftime("%Y-%m-%d")
    bigquery_carbon_query = f"""
        SELECT
            usage_month,
            project.number,
            SUM(carbon_footprint_total_kgCO2e.location_based)
        FROM `{settings_api.GCP_CARBON_EXPORT_PROJECT_ID}.{settings_api.GCP_CARBON_EXPORT_DATASET_NAME}.carbon_footprint`
        WHERE
            usage_month = "{year:04d}-{month:02d}-01" AND
            project.number = "{project_id}"
        GROUP BY 1, 2;
    """
    client = bigquery.Client(credentials=credentials)
    query_job = client.query(bigquery_carbon_query)
    results = query_job.result()
    emissions_carbonEmissionEntries = None
    for row in results:
        emissions_carbonEmissionEntries = float("{:.2f}".format(row[2]))

    return schemas.CloudCarbonFootprintResponse(
        project_id = project_id,
        year = year,
        month = month,
        total = emissions_carbonEmissionEntries,
    )

def gcp_get_account_details(
    project_id: int,
) -> schemas.CloudProject:
    client = resourcemanager_v3.ProjectsClient(credentials=credentials)
    request = resourcemanager_v3.GetProjectRequest(
        name=f"projects/{project_id}",
    )
    gcp_project = client.get_project(request=request)

    return schemas.CloudProject(
        id=gcp_project.name.split("/")[-1],
        provider = schemas.cloud_provider.GCP().slug,
        name=gcp_project.display_name,
        parent=gcp_project.parent,
        tags=gcp_project.labels,
        state=str(gcp_project.state).split(".")[1],
        created_at=datetime.fromtimestamp(gcp_project.create_time.timestamp()),
    )
