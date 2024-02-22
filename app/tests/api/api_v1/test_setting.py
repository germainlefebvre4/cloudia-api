from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.utils import random_lower_string, randome_int_number, random_float_number
from app.tests.utils.setting import create_random_setting


def test_create_setting_as_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"key": randome_int_number(), "kind": randome_int_number(), "country": random_lower_string(), "label": random_lower_string(), "additional": random_lower_string()}
    response = client.post(
        url=f"{settings.API_V1_STR}/settings/",
        headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 201
    content = response.json()
    assert content["key"] == data["key"]
    assert content["kind"] == data["kind"]
    assert content["country"] == data["country"]
    assert content["label"] == data["label"]
    assert content["additional"] == data["additional"]
    assert "id" in content


def test_create_setting_as_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    data = {"key": randome_int_number(), "kind": randome_int_number(), "country": random_lower_string(), "label": random_lower_string(), "additional": random_lower_string()}
    response = client.post(
        url=f"{settings.API_V1_STR}/settings/",
        headers=normal_user_token_headers, json=data,
    )
    assert response.status_code == 400


def test_read_setting(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    setting = create_random_setting(db=db)
    response = client.get(
        url=f"{settings.API_V1_STR}/settings/{setting.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["key"] == setting.key
    assert content["kind"] == setting.kind
    assert content["country"] == setting.country
    assert content["label"] == setting.label
    assert content["additional"] == setting.additional
    assert "id" in content


def test_read_setting(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    setting = create_random_setting(db=db)
    response = client.get(
        url=f"{settings.API_V1_STR}/settings/{setting.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["key"] == setting.key
    assert content["kind"] == setting.kind
    assert content["country"] == setting.country
    assert content["label"] == setting.label
    assert content["additional"] == setting.additional
    assert "id" in content


def test_read_settings_as_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    response = client.get(
        url=f"{settings.API_V1_STR}/settings/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    count1 = len(content)

    setting = create_random_setting(db=db)
    response = client.get(
        url=f"{settings.API_V1_STR}/settings/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    count2 = len(content)

    assert count2 == count1 + 1


def test_read_settings_as_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    response = client.get(
        url=f"{settings.API_V1_STR}/settings/",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    count1 = len(content)

    setting = create_random_setting(db=db)
    response = client.get(
        url=f"{settings.API_V1_STR}/settings/",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    count2 = len(content)

    assert count2 == count1 + 1


# def test_update_setting(
#     client: TestClient, superuser_token_headers: dict, db: Session
# ) -> None:
#     setting = create_random_setting(db=db)
#     data = {"key": randome_int_number(), "kind": randome_int_number(), "country": random_lower_string(), "label": random_lower_string(), "additional": random_lower_string()}
#     response = client.put(
#         url=f"{settings.API_V1_STR}/settings/{setting.id}",
#         headers=superuser_token_headers, json=data,
#     )
#     assert response.status_code == 200
#     content = response.json()

#     assert content["key"] == data["key"]
#     assert content["kind"] == data["kind"]
#     assert content["country"] == data["country"]
#     assert content["label"] == data["label"]
#     assert content["additional"] == data["additional"]


def test_remove_setting_as_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    setting = create_random_setting(db=db)

    response = client.delete(
        url=f"{settings.API_V1_STR}/settings/{setting.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["key"] == setting.key
    assert content["kind"] == setting.kind
    assert content["country"] == setting.country
    assert content["label"] == setting.label
    assert content["additional"] == setting.additional
    assert "id" in content

    response = client.get(
        url=f"{settings.API_V1_STR}/settings/{setting.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404


def test_remove_setting_as_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    setting = create_random_setting(db=db)

    response = client.delete(
        url=f"{settings.API_V1_STR}/settings/{setting.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
