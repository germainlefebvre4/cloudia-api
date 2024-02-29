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
        key="enabled",
        value="true",
        type="bool",
        category="Cloud Provider/Dummy",
        description='Enables Dummy Cloud Provider',
    )
    setting_1 = crud.setting.create(db, obj_in=setting_1_in)

    setting_2_in = schemas.SettingCreate(
        key="enabled",
        value="true",
        type="bool",
        category="Cloud Provider/AWS",
        description='Enables AWS Cloud Provider',
    )
    setting_2 = crud.setting.create(db, obj_in=setting_2_in)

    setting_3_in = schemas.SettingCreate(
        key="enabled",
        value="true",
        type="bool",
        category="Cloud Provider/GCP",
        description='Enables GCP Cloud Provider',
    )
    setting_3 = crud.setting.create(db, obj_in=setting_3_in)

    setting_4_in = schemas.SettingCreate(
        key="aws_root_account_access_key_id",
        value="xxxxxxxxxxxxxxxxxxxx",
        type="string",
        category="Cloud Provider/AWS/credentials/root_account",
        description="AWS root Account Programmatic Credentials: Access Key ID",
    )
    setting_4 = crud.setting.create(db, obj_in=setting_4_in)

    setting_5_in = schemas.SettingCreate(
        key="aws_root_account_secret_access_key",
        value="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        type="string",
        category="Cloud Provider/AWS/credentials/root_account",
        description="AWS root Account Programmatic credentials: Secret Access Key",
    )
    setting_5 = crud.setting.create(db, obj_in=setting_5_in)

    setting_6_in = schemas.SettingCreate(
        key="aws_root_account_region",
        value="us-east-1",
        type="string",
        category="Cloud Provider/AWS/region/root_account",
        description="AWS root Account Region",
    )
    setting_6 = crud.setting.create(db, obj_in=setting_6_in)
    

