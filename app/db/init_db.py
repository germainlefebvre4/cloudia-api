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

    setting_4_in = schemas.SettingCreate(
        path="/Cloud Provider/AWS/credentials/root_account",
        key="aws_root_account_access_key_id",
        value="xxxxxxxxxxxxxxxxxxxx",
        type="str",
        description="AWS root Account Programmatic Credentials: Access Key ID",
    )
    setting_4 = crud.setting.create(db, obj_in=setting_4_in)

    setting_5_in = schemas.SettingCreate(
        path="/Cloud Provider/AWS/credentials/root_account",
        key="aws_root_account_secret_access_key",
        value="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        type="str",
        description="AWS root Account Programmatic credentials: Secret Access Key",
    )
    setting_5 = crud.setting.create(db, obj_in=setting_5_in)

    setting_6_in = schemas.SettingCreate(
        path="/Cloud Provider/AWS/credentials/root_account",
        key="aws_root_account_region",
        value="us-east-1",
        type="str",
        description="AWS root Account Region",
    )
    setting_6 = crud.setting.create(db, obj_in=setting_6_in)
    setting_5 = crud.setting.create(db, obj_in=setting_5_in)

    setting_6_in = schemas.SettingCreate(
        path="/Cloud Provider/GCP/credentials/root_project",
        key="gcp_service_account_json_key_file",
        value='''
{
    "type": "service_account",
    "project_id": "xxxxxxxxxx",
    "private_key_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "private_key": "-----BEGIN PRIVATE KEY-----\nxxxxxxxxxxx\n-----END PRIVATE KEY-----\n",
    "client_email": "xxxxxxxxxxx@xxxxxxxxxx.iam.gserviceaccount.com",
    "client_id": "xxxxxxxxxxxxxxxxxxxxx",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/xxxxxxxxxxx%40xxxxxxxxxx.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}
        ''',
        type="str",
        description="GCP Service Account JSON Key File",
    )
    setting_6 = crud.setting.create(db, obj_in=setting_6_in)
    

