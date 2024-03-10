import os
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


class Variables(BaseSettings):
    redis_ttl_for_projects: int = 60 * 60 * 24 * 7
    redis_ttl_for_projects_tags: int = 60 * 60 * 24 * 7
    redis_ttl_for_billing: int = 60 * 60 * 24 * 7
    redis_ttl_for_carbon_footprint: int = 60 * 60 * 24 * 7

    class Config:
        case_sensitive = True
    
    def redis_key_for_projects_by_provider(self, provider: str) -> str:
        return f"cloudia:projects:cloud:{provider}:projects"

    def redis_key_for_projects_tags_by_provider(self, provider: str) -> str:
        return f"cloudia:tags:cloud:{provider}:projects:tags"

    def redis_key_for_billing_by_provider_project(self, provider: str, project_id: str, year: int, month: int) -> str:
        return f"cloudia:billing:cloud:{provider}:project:{project_id}:billing:{year}{month}"

    def redis_key_for_billing_projects_by_provider(self, provider: str, year_start: int, month_start: int, year_end: int, month_end: int) -> str:
        return f"cloudia:billing:cloud:{provider}:projects:billing:{year_start}{month_start}:{year_end}{month_end}"

    def redis_key_for_carbon_footprint(self, provider: str, project_id: str, year: int, month: int) -> str:
        return f"cloudia:carbon:cloud:{provider}:project{project_id}:date:{year}{month}"


variables = Variables()
