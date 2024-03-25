import os
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator
from app import crud

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps

from dotenv import load_dotenv
load_dotenv()

db: Session = next(deps.get_db())
print(db)

class SettingsAPI(BaseSettings):
    # Amazon Web Services
    AWS_ACCESS_KEY_ID: str = crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/AWS/credentials/root_account", key="aws_root_account_access_key_id")
    AWS_SECRET_ACCESS_KEY: str = crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/AWS/credentials/root_account", key="aws_root_account_secret_access_key")
    AWS_DEFAULT_REGION: str = crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/AWS/credentials/root_account", key="aws_root_account_region")

    # Google Cloud
    GCP_ORGANIZATION_ID: str = crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/GCP/root_project", key="gcp_organization_id")
    GCP_BILLING_ACCOUNT_ID: str = crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/GCP/root_project", key="gcp_billing_account_id")
    GCP_SERVICE_ACCOUNT_JSON_KEY_FILE: str = crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/GCP/credentials/billing_project", key="gcp_service_account_json_key_file")
    GCP_BILLING_EXPORT_PROJECT_ID: str = crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/GCP/billing_project", key="gcp_project_id")
    GCP_BILLING_EXPORT_DATASET_NAME: str = crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/GCP/billing_project", key="gcp_bigquery_dataset_name")
    # GCP_BILLLING_SERVICE_ACCOUNT_JSON_KEY_FILE: str = crud.setting.get_by_path_by_key("/Cloud Provider/GCP/credentials/billing_project", "gcp_service_account_json_key_file")
    GCP_CARBON_EXPORT_PROJECT_ID: str = crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/GCP/carbon_foorptin_project", key="gcp_project_id")
    GCP_CARBON_EXPORT_DATASET_NAME: str = crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/GCP/carbon_foorptin_project", key="gcp_bigquery_dataset_name")
    # GCP_CARBON_SERVICE_ACCOUNT_JSON_KEY_FILE: str = crud.setting.get_by_path_by_key("/Cloud Provider/GCP/credentials/billing_project", "gcp_service_account_json_key_file")

settings_api = SettingsAPI()
