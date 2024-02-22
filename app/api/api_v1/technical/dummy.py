from typing import Any
import logging
import json

from fastapi import Depends

from app.api import deps
from app import schemas
from app.core.config import settings


def list_dummy_projects(
    redis_c = Depends(deps.get_redis),
) -> list[schemas.CloudProject]:
    projects = [
        {
            "id": 100200300401,
            "name": "Cloud Root Account",
            "state": "ACTIVE",
            "labels": None,
            "email": "aws-cloudia-root@cloudia.fr",
            "parent": None,
            "tags": {
                "company": "cloudia",
                "team": "core",
                "project": "billing",
                "env": "billing"
            },
            "created_at": "2021-04-06T10:28:49.723000+02:00"
        },
        {
            "id": 100200300402,
            "name": "Cloudia Website Dev",
            "state": "ACTIVE",
            "labels": None,
            "email": "aws-cloudia-website-dev@cloudia.fr",
            "parent": None,
            "tags": {
                "company": "cloudia",
                "team": "core",
                "project": "website",
                "env": "dev"
            },
            "created_at": "2022-02-16T15:02:30.069000+01:00"
        },
        {
            "id": 100200300403,
            "name": "Cloudia Website QA",
            "state": "ACTIVE",
            "labels": None,
            "email": "aws-cloudia-website-qa@cloudia.fr",
            "parent": None,
            "tags": {
                "company": "cloudia",
                "team": "core",
                "project": "website",
                "env": "qa"
            },
            "created_at": "2022-03-16T13:14:09.044000+01:00"
        },
        {
            "id": 100200300404,
            "name": "Cloudia Website Preprod",
            "state": "ACTIVE",
            "labels": None,
            "email": "aws-cloudia-website-preprod@cloudia.fr",
            "parent": None,
            "tags": {
                "company": "cloudia",
                "team": "core",
                "project": "website",
                "env": "preprod"
            },
            "created_at": "2019-01-09T18:49:13.834000+01:00"
        },
        {
            "id": 100200300201,
            "name": "Cloudia Website Prod",
            "state": "ACTIVE",
            "labels": None,
            "email": "aws-cloudia-website-prod@cloudia.fr",
            "parent": None,
            "tags": {
                "company": "cloudia",
                "team": "core",
                "project": "website",
                "env": "prod"
            },
            "created_at": "2020-04-17T10:51:55.324000+02:00"
        },
        {
            "id": 100200300202,
            "name": "Cloudia Demo Dev",
            "state": "ACTIVE",
            "labels": None,
            "email": "aws-cloudia-demo-dev@cloudia.fr",
            "parent": None,
            "tags": {
                "company": "cloudia",
                "team": "sales",
                "project": "demo",
                "env": "dev"
            },
            "created_at": "2019-05-09T16:35:11.574000+02:00"
        },
        {
            "id": 100200300203,
            "name": "Cloudia Demo Prod",
            "state": "ACTIVE",
            "labels": None,
            "email": "aws-cloudia-demo-prod@cloudia.fr",
            "parent": None,
            "tags": {
                "company": "cloudia",
                "team": "sales",
                "project": "demo",
                "env": "prod"
            },
            "created_at": "2022-03-17T09:07:54.732000+01:00"
        },
        {
            "id": 100200300204,
            "name": "Cloudia Carbon Footprint Dev",
            "state": "ACTIVE",
            "labels": None,
            "email": "aws-cloudia-carbonfootprint-dev@cloudia.fr",
            "parent": None,
            "tags": {
                "company": "cloudia",
                "team": "carbon",
                "project": "carbonfootprint",
            },
            "created_at": "2019-12-19T11:26:04.892000+01:00"
        },
        {
            "id": 100200300205,
            "name": "Cloudia Carbon Footprint Prod",
            "state": "ACTIVE",
            "labels": None,
            "email": "aws-cloudia-carbonfootprint-prod@cloudia.fr",
            "parent": None,
            "tags": {
                "company": "cloudia",
                "team": "carbon",
                "project": "carbonfootprint",
            },
            "created_at": "2022-03-16T13:13:25.018000+01:00"
        },
        {
            "id": 100200300105,
            "name": "Cloudia Advisor AI Dev",
            "state": "ACTIVE",
            "labels": None,
            "email": "aws-cloudia-advisorai-dev@cloudia.fr",
            "parent": None,
            "tags": {
                "company": "cloudia",
                "team": "ai",
                "project": "advisorai",
                "env": "dev"
            },
            "created_at": "2020-04-16T22:31:48.971000+02:00"
        },
        {
            "id": 100200300104,
            "name": "Cloudia Advisor AI Prod",
            "state": "ACTIVE",
            "labels": None,
            "email": "aws-cloudia-advisorai-prod@cloudia.fr",
            "parent": None,
            "tags": {
                "company": "cloudia",
                "team": "ai",
                "project": "advisorai",
                "env": "prod"
            },
            "created_at": "2020-09-07T09:34:58.141000+02:00"
        },
    ]
    for project in projects:
        project["provider"] = schemas.cloud_provider.Dummy().slug
    return [schemas.CloudProject(**account) for account in projects]
