import random
import string
from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def randome_int_number() -> int:
    return random.randint(1, 1000)


def random_float_number(precision: int = 2) -> float:
    return round(random.uniform(1, 1000), precision)


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.USER_ADMIN_EMAIL,
        "password": settings.USER_ADMIN_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers

def get_apikey_token_headers() -> Dict[str, str]:
    headers = {
        f"{settings.API_KEY_NAME}": f"{settings.API_KEY_SECRET}"
    }
    return headers
