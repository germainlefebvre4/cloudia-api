from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_dummy(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    assert True
