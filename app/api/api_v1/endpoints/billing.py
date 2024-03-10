from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Any, List
import json
from app.api.api_v1.technical.dummy import list_dummy_projects

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.api.api_v1.technical.aws import get_aws_project_billing, list_aws_projects
from app.api.api_v1.technical.gcp import get_gcp_project_billing, get_gcp_projects_billing, list_gcp_projects
from app.api.api_v1.technical.cache import flush_billing_cache, flush_billing_cache, flush_billing_cache

router = APIRouter()


# Charts
@router.get("/all/projects/chart", response_model=Any)
def read_all_providers_prices_for_chart(
    start_year: int = 2023,
    start_month: int = 9,
    end_year: int = 2023,
    end_month: int = 12,
    redis_c = Depends(deps.get_redis),
) -> List[schemas.ProjectBillingOutputForChart]:
    aws = read_aws_prices_by_provider_for_chart(
        start_year=start_year,
        start_month=start_month,
        end_year=end_year,
        end_month=end_month,
        redis_c=redis_c,
    )
    gcp = read_gcp_prices_by_provider_for_chart(
        start_year=start_year,
        start_month=start_month,
        end_year=end_year,
        end_month=end_month,
        redis_c=redis_c,
    )

    return aws + gcp


@router.get("/aws/projects/chart", response_model=Any)
def read_aws_prices_by_provider_for_chart(
    start_year: int = 2023,
    start_month: int = 9,
    end_year: int = 2023,
    end_month: int = 12,
    redis_c = Depends(deps.get_redis),
) -> List[schemas.ProjectBillingOutputForChart]:
    start_date = datetime.strptime(f"{start_month}/{start_year}", "%m/%Y")
    end_date = datetime.strptime(f"{end_month}/{end_year}", "%m/%Y")
    date_delta = relativedelta(end_date, start_date)

    projects = list_aws_projects(redis_c)

    chart_res = []
    for project in projects:
        prices_chart = []
        for i in range(date_delta.months + 1):
            date_work = datetime.strptime(f"{start_year}-{start_month}", "%Y-%m") + relativedelta(months=i)
            billing = get_aws_project_billing(redis_c=redis_c, project_id=project.id, year=date_work.year, month=date_work.month)

            date_tmp = datetime.strptime(f"{date_work.year}-{date_work.month}", "%Y-%m")
            if billing.total is None:
                billing.total = 0
            prices_chart.append({"x": date_tmp, "y": billing.total})

        prices_res = schemas.ProjectBillingOutputForChart(
            label=f"{project.name} ({project.id})",
            data=prices_chart,
        )

        chart_res.append(prices_res)

    return chart_res


@router.get("/gcp/projects/chart", response_model=Any)
def read_gcp_prices_by_provider_for_chart(
    start_year: int = 2023,
    start_month: int = 9,
    end_year: int = 2023,
    end_month: int = 12,
    redis_c = Depends(deps.get_redis),
) -> List[schemas.ProjectBillingOutputForChart]:
    start_date = datetime.strptime(f"{start_month}/{start_year}", "%m/%Y")
    end_date = datetime.strptime(f"{end_month}/{end_year}", "%m/%Y")
    date_delta = relativedelta(end_date, start_date)

    projects = list_gcp_projects(redis_c)

    chart_res = []
    billing = get_gcp_projects_billing(redis_c=redis_c, year_start=start_year, month_start=start_month, year_end=end_year, month_end=end_month)

    prices_res = []
    for project in projects:
        prices_chart = []
        billing_filtered = [x for x in billing if x.project_id == project.id]
        if len(billing_filtered) == 0:
            for month in range(date_delta.months + 1):
                date_tmp = datetime.strptime(f"{start_year}-{start_month}", "%Y-%m") + relativedelta(months=month)
                prices_chart.append({"x": date_tmp, "y": 0})
        else:
            for month in billing_filtered:
                date_tmp = datetime.strptime(f"{month.year}-{month.month}", "%Y-%m")
                prices_chart.append({"x": date_tmp, "y": month.total})

        prices_res = schemas.ProjectBillingOutputForChart(
            label=f"{project.name} ({project.id})",
            data=prices_chart,
        )

        chart_res.append(prices_res)

    return chart_res


@router.get("/aws/projects/{project_id}/chart", response_model=List[schemas.ProjectBillingOutputForChart])
def read_aws_prices_by_provider_by_project_for_chart(
    project_id: str,
    start_year: int = 2023,
    start_month: int = 9,
    end_year: int = 2023,
    end_month: int = 12,
    redis_c = Depends(deps.get_redis),
) -> Any:
    start_date = datetime.strptime(f"{start_month}/{start_year}", "%m/%Y")
    end_date = datetime.strptime(f"{end_month}/{end_year}", "%m/%Y")
    date_delta = relativedelta(end_date, start_date)

    prices_chart = []
    for i in range(date_delta.months + 1):
        date_work = datetime.strptime(f"{start_year}-{start_month}", "%Y-%m") + relativedelta(months=i)
        billing = get_aws_project_billing(redis_c=redis_c, project_id=project_id, year=date_work.year, month=date_work.month)

        date_tmp = datetime.strptime(f"{date_work.year}-{date_work.month}", "%Y-%m")
        prices_chart.append({"x": date_tmp, "y": billing.total})

    prices_res = schemas.ProjectBillingOutputForChart(
        label=project_id,
        data=prices_chart,
    )

    return [prices_res]


@router.get("/gcp/projects/{project_id}/chart", response_model=List[schemas.ProjectBillingOutputForChart])
def read_gcp_prices_by_provider_by_project_for_chart(
    project_id: str,
    start_year: int = 2023,
    start_month: int = 9,
    end_year: int = 2023,
    end_month: int = 12,
    redis_c = Depends(deps.get_redis),
) -> Any:
    start_date = datetime.strptime(f"{start_month}/{start_year}", "%m/%Y")
    end_date = datetime.strptime(f"{end_month}/{end_year}", "%m/%Y")
    date_delta = relativedelta(end_date, start_date)

    prices_chart = []
    for i in range(date_delta.months + 1):
        date_work = datetime.strptime(f"{start_year}-{start_month}", "%Y-%m") + relativedelta(months=i)
        billing = get_gcp_project_billing(redis_c=redis_c, project_id=project_id, year=date_work.year, month=date_work.month)

        date_tmp = datetime.strptime(f"{date_work.year}-{date_work.month}", "%Y-%m")
        prices_chart.append({"x": date_tmp, "y": billing.total})

    prices_res = schemas.ProjectBillingOutputForChart(
        label=project_id,
        data=prices_chart,
    )

    return [prices_res]


# Cloud Billing - Google Cloud
@router.get("/gcp/projects/{project_id}", response_model=Any)
async def get_google_projects_billing(
    project_id: int,
    year: int,
    month: int,
    redis_c = Depends(deps.get_redis),
) -> Any:
    billing = get_gcp_project_billing(redis_c=redis_c, project_id=project_id, year=year, month=month)
    return billing


# Cloud Billing - Amazon Web Services
@router.get("/aws/projects/{project_id}", response_model=Any)
async def get_aws_projects_billing(
    project_id: int,
    year: int,
    month: int,
    redis_c = Depends(deps.get_redis),
) -> Any:
    billing = get_aws_project_billing(redis_c=redis_c, project_id=project_id, year=year, month=month)
    return billing


# Cache flush
@router.post("/providers/projects/cache/refresh", response_model=schemas.Msg)
async def refresh_providers_projects(
    redis_c = Depends(deps.get_redis),
) -> Any:
    flush_billing_cache(redis_c=redis_c)
    return {"msg": f"Cloud Project cache flushed for all providers"}

@router.post("/providers/{provider}/projects/cache/refresh", response_model=schemas.Msg)
async def refresh_provider_projects(
    provider: str,
    redis_c = Depends(deps.get_redis),
) -> Any:
    flush_billing_cache(redis_c=redis_c, cloud_provider=provider)
    return {"msg": f"Cloud Project cache flushed for provider {provider}"}


@router.post("/providers/{provider}/projects/{project_id}/cache/refresh", response_model=schemas.Msg)
async def refresh_provider_project(
    provider: str,
    project_id: str,
    redis_c = Depends(deps.get_redis),
) -> Any:
    flush_billing_cache(redis_c=redis_c, cloud_provider=provider, project_id=project_id)
    return {"msg": f"Cloud Project cache flushed for provider {provider} and project {project_id}"}
