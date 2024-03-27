from typing import Any
import logging
import json
import requests

from fastapi import Depends

from app.api import deps
from app import schemas
from app.core.config import settings
from app.core.variables import variables

from app.api.api_v1.helpers.gcp import gcp_list_projects, gcp_get_project_billing, gcp_get_project_carbon_footprint, gcp_get_account_details


def get_ccf_estimation(
    start_year: int,
    start_month: int,
    start_day: int,
    end_year: int,
    end_month: int,
    end_day: int,
    redis_c = Depends(deps.get_redis),
) -> Any:
    results = requests.get(
        f"{settings.CCF_API_URL}/footprint?start={start_year:0>4}-{start_month:0>2}-{start_day:0>2}&end={end_year:0>4}-{end_month:0>2}-{end_day:0>2}&ignoreCache=false&groupBy=month&limit=50000&skip=0",
    ).json()

    return results
