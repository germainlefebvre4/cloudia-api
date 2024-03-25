import os
from pathlib import Path
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401

from app.tests.utils.utils import random_lower_string

from dotenv import load_dotenv
load_dotenv()


def init_db(db: Session) -> None:
    # Create users
    # user_admin = crud.user.get_by_email(db, email=settings.USER_ADMIN_EMAIL)
    # if not user_admin:
    #     user_in = schemas.UserCreate(
    #         email=settings.USER_ADMIN_EMAIL,
    #         full_name=settings.USER_ADMIN_FULLNAME,
    #         password=settings.USER_ADMIN_PASSWORD,
    #         is_superuser=True,
    #     )
    #     user_admin = crud.user.create(db, obj_in=user_in)

    # user_test = crud.user.get_by_email(db, email=settings.USER_TEST_EMAIL)
    # if not user_test:
    #     user_in = schemas.UserCreate(
    #         email=settings.USER_TEST_EMAIL,
    #         full_name=settings.USER_TEST_FULLNAME,
    #         password=settings.USER_TEST_PASSWORD,
    #         is_superuser=False,
    #     )
    #     user_test = crud.user.create(db, obj_in=user_in)

    # Create settings
    setting_1_in = schemas.SettingCreate(
        path="/Cloud Provider/Dummy",
        key="enabled",
        value="true",
        type="bool",
        description='Enables Dummy Cloud Provider',
    )
    setting_1 = crud.setting.create(db, obj_in=setting_1_in)

    setting_2_in = schemas.SettingCreate(
        path="/Cloud Provider/AWS",
        key="enabled",
        value="true",
        type="bool",
        description='Enables AWS Cloud Provider',
    )
    setting_2 = crud.setting.create(db, obj_in=setting_2_in)

    setting_3_in = schemas.SettingCreate(
        path="/Cloud Provider/GCP",
        key="enabled",
        value="true",
        type="bool",
        description='Enables GCP Cloud Provider',
    )
    setting_3 = crud.setting.create(db, obj_in=setting_3_in)

    # Amazon Web Services
    setting_4_in = schemas.SettingCreate(
        path="/Cloud Provider/AWS/credentials/root_account",
        key="aws_root_account_access_key_id",
        value=os.getenv("AWS_ACCESS_KEY_ID", "xxxxxxxxxxxxxxxxxxxx"),
        type="str",
        description="AWS root Account Programmatic Credentials: Access Key ID",
    )
    setting_4 = crud.setting.create(db, obj_in=setting_4_in)

    setting_5_in = schemas.SettingCreate(
        path="/Cloud Provider/AWS/credentials/root_account",
        key="aws_root_account_secret_access_key",
        value=os.getenv("AWS_SECRET_ACCESS_KEY", "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),
        type="str",
        description="AWS root Account Programmatic credentials: Secret Access Key",
    )
    setting_5 = crud.setting.create(db, obj_in=setting_5_in)

    setting_6_in = schemas.SettingCreate(
        path="/Cloud Provider/AWS/credentials/root_account",
        key="aws_root_account_region",
        value=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        type="str",
        description="AWS root Account Region",
    )
    setting_6 = crud.setting.create(db, obj_in=setting_6_in)

    # Google Cloud
    setting_7_in = schemas.SettingCreate(
        path="/Cloud Provider/GCP/root_project",
        key="gcp_organization_id",
        value=os.getenv("GCP_ORGANIZATION_ID", "xxxxxxxxxx"),
        type="str",
        description="GCP Organization ID",
    )
    setting_7 = crud.setting.create(db, obj_in=setting_7_in)

    setting_8_in = schemas.SettingCreate(
        path="/Cloud Provider/GCP/root_project",
        key="gcp_billing_account_id",
        value=os.getenv("GCP_BILLING_ACCOUNT_ID", "xxxxxxxxxx"),
        type="str",
        description="GCP Billing Account ID",
    )
    setting_8 = crud.setting.create(db, obj_in=setting_8_in)

    setting_9_in = schemas.SettingCreate(
        path="/Cloud Provider/GCP/billing_project",
        key="gcp_project_id",
        value=os.getenv("GCP_BILLING_EXPORT_PROJECT_ID", "xxxxxxxxxx"),
        type="str",
        description="GCP Project ID for Billing",
    )
    setting_9 = crud.setting.create(db, obj_in=setting_9_in)

    setting_6_in = schemas.SettingCreate(
        path="/Cloud Provider/GCP/credentials/billing_project",
        key="gcp_service_account_json_key_file",
        value=Path(os.getenv("GCP_SERVICE_ACCOUNT_JSON_KEY_FILE")).read_text(),
        type="str",
        description="GCP Service Account JSON Key File",
    )
    setting_6 = crud.setting.create(db, obj_in=setting_6_in)

    setting_10_in = schemas.SettingCreate(
        path="/Cloud Provider/GCP/billing_project",
        key="gcp_bigquery_dataset_name",
        value=os.getenv("GCP_BILLING_EXPORT_DATASET_NAME", "xxxxxxxxxx"),
        type="str",
        description="Bigquery Dataset Name for Billing Data",
    )
    setting_10 = crud.setting.create(db, obj_in=setting_10_in)

    setting_11_in = schemas.SettingCreate(
        path="/Cloud Provider/GCP/carbon_footprint_project",
        key="gcp_project_id",
        value=os.getenv("GCP_CARBON_EXPORT_PROJECT_ID", "xxxxxxxxxx"),
        type="str",
        description="Project ID for Carbon Footprint",
    )
    setting_11 = crud.setting.create(db, obj_in=setting_11_in)

    setting_13_in = schemas.SettingCreate(
        path="/Cloud Provider/GCP/credentials/carbon_footprint_project",
        key="gcp_service_account_json_key_file",
        value=Path(os.getenv("GCP_SERVICE_ACCOUNT_JSON_KEY_FILE")).read_text(),
        type="str",
        description="GCP Service Account JSON Key File",
    )
    setting_13 = crud.setting.create(db, obj_in=setting_13_in)

    setting_12_in = schemas.SettingCreate(
        path="/Cloud Provider/GCP/carbon_footprint_project",
        key="gcp_bigquery_dataset_name",
        value=os.getenv("GCP_CARBON_EXPORT_DATASET_NAME", "xxxxxxxxxx"),
        type="str",
        description="Bigquery Dataset Name for Carbon Footprint Data",
    )
    setting_12 = crud.setting.create(db, obj_in=setting_12_in)
    
    # Cloud Carbon Footprint
    setting_14_in = schemas.SettingCreate(
        path="/Cloud Carbon Footprint",
        key="enabled",
        value="true",
        type="bool",
        description='Enables Cloud Carbon Footprint',
    )
    setting_14 = crud.setting.create(db, obj_in=setting_14_in)

    # Cloud Carbon Footprint API URL
    setting_15_in = schemas.SettingCreate(
        path="/Cloud Carbon Footprint",
        key="api_url",
        value=os.getenv("CLOUD_CARBON_FOOTPRINT_API_URL", "http://localhost:4000/api"),
        type="str",
        description='Cloud Carbon Footprint API URL',
    )
    setting_15 = crud.setting.create(db, obj_in=setting_15_in)
