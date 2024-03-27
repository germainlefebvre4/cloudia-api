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

# print(crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/GCP", key="enabled").__dict__)
# print(crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/GCP", key="enabled").value)

class SettingsAPI(BaseSettings):
    # Amazon Web Services
    AWS_ENABLED = crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/AWS", key="enabled").value
    AWS_ACCESS_KEY_ID: Optional[str] = crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/AWS/credentials/root_account", key="aws_root_account_access_key_id") or ""
    AWS_SECRET_ACCESS_KEY: Optional[str] = crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/AWS/credentials/root_account", key="aws_root_account_secret_access_key") or ""
    AWS_DEFAULT_REGION: Optional[str] = crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/AWS/credentials/root_account", key="aws_root_account_region") or ""

    # Google Cloud
    GCP_ENABLED = crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/GCP", key="enabled").value
    GCP_ORGANIZATION_ID: Optional[str] = crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/GCP/root_project", key="gcp_organization_id") or ""
    GCP_BILLING_ACCOUNT_ID: Optional[str] = crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/GCP/root_project", key="gcp_billing_account_id") or ""
    GCP_SERVICE_ACCOUNT_JSON_KEY_FILE_CONTENT: Optional[str] = crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/GCP/credentials/billing_project", key="gcp_service_account_json_key_file_content") or '{}'
    GCP_BILLING_EXPORT_PROJECT_ID: Optional[str] = crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/GCP/billing_project", key="gcp_project_id") or ""
    GCP_BILLING_EXPORT_DATASET_NAME: Optional[str] = crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/GCP/billing_project", key="gcp_bigquery_dataset_name") or ""
    # GCP_BILLLING_SERVICE_ACCOUNT_JSON_KEY_FILE: str = crud.setting.get_by_path_by_key("/Cloud Provider/GCP/credentials/billing_project", "gcp_service_account_json_key_file")
    GCP_CARBON_EXPORT_PROJECT_ID: Optional[str] = crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/GCP/carbon_footprint_project", key="gcp_project_id") or ""
    GCP_CARBON_EXPORT_DATASET_NAME: Optional[str] = crud.setting.get_by_path_by_key(db=db, path="/Cloud Provider/GCP/carbon_footprint_project", key="gcp_bigquery_dataset_name") or ""
    # GCP_CARBON_SERVICE_ACCOUNT_JSON_KEY_FILE: str = crud.setting.get_by_path_by_key("/Cloud Provider/GCP/credentials/billing_project", "gcp_service_account_json_key_file")

    # Cloud Carbon Footprint
    CCF_API_ENABLED: bool = crud.setting.get_by_path_by_key(db=db, path="/Cloud Carbon Footprint", key="cloud_carbon_footprint_enabled") or False
    CCF_API_URL: Optional[str] = crud.setting.get_by_path_by_key(db=db, path="/Cloud Carbon Footprint", key="cloud_carbon_footprint_api_url") or ""

settings_api = SettingsAPI()
