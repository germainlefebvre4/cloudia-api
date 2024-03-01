import os
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator

from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str = os.getenv("SERVER_NAME", "localhost")
    SERVER_HOST: AnyHttpUrl = os.getenv("SERVER_HOST", "http://localhost:8080")
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = os.getenv("BACKEND_CORS_ORIGINS", [])

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Default project")
    # SENTRY_DSN: Optional[HttpUrl] = os.getenv("SENTRY_DSN", None)

    # @validator("SENTRY_DSN", pre=True)
    # def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
    #     if len(v) == 0:
    #         return None
    #     return v

    API_KEY_NAME: str = "access_token"
    API_KEY_SECRET: Optional[str] = os.getenv("API_KEY_SECRET", "abc123")

    POSTGRES_SERVER: str = os.getenv("POSTGRES_USER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "cloudia")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_USER", "cloudia")
    POSTGRES_DB: str = os.getenv("POSTGRES_USER", "cloudia")
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )
    
    REDIS_SERVER: str = os.getenv("REDIS_SERVER", "localhost")
    REDIS_PORT: str = os.getenv("REDIS_PORT", "6379")
    # REDIS_DB: str = os.getenv("REDIS_DB", "0")
    # REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "cloudia")

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    USER_TEST_FULLNAME: str = os.getenv("USER_TEST_FULLNAME", "Test")
    USER_TEST_EMAIL: EmailStr = os.getenv("USER_TEST_EMAIL", "test@domain.fr")
    USER_TEST_PASSWORD: str = os.getenv("USER_TEST_PASSWORD", "test")

    USER_ADMIN_FULLNAME: str = os.getenv("USER_ADMIN_FULLNAME", "Admin")
    USER_ADMIN_EMAIL: EmailStr = os.getenv("USER_ADMIN_EMAIL", "admin@domain.fr")
    USER_ADMIN_PASSWORD: str = os.getenv("USER_ADMIN_PASSWORD", "admin")

    USERS_OPEN_REGISTRATION: bool = os.getenv("USERS_OPEN_REGISTRATION", False)


    GCP_SERVICE_ACCOUNT_JSON_KEY_FILE = os.getenv("GCP_SERVICE_ACCOUNT_JSON_KEY_FILE")
    GCP_ORGANIZATION_ID: str = os.getenv("GCP_ORGANIZATION_ID")
    GCP_BILLING_ACCOUNT_ID: str = os.getenv("GCP_BILLING_ACCOUNT_ID")
    GCP_BILLING_EXPORT_PROJECT_ID: str = os.getenv("GCP_BILLING_EXPORT_PROJECT_ID")
    GCP_BILLING_EXPORT_DATASET_NAME: str = os.getenv("GCP_BILLING_EXPORT_DATASET_NAME")
    GCP_CARBON_EXPORT_PROJECT_ID: str = os.getenv("GCP_CARBON_EXPORT_PROJECT_ID")
    GCP_CARBON_EXPORT_DATASET_NAME: str = os.getenv("GCP_CARBON_EXPORT_DATASET_NAME")

    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_DEFAULT_REGION: str = os.getenv("AWS_DEFAULT_REGION")


    CCF_ENABLED: bool = os.getenv("CCF_ENABLED", False)
    CCF_API_URL: str = os.getenv("CCF_API_URL", "http://localhost:4000/api")

    class Config:
        case_sensitive = True


settings = Settings()
