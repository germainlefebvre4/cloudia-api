from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import logging
import alembic.config
import alembic.command

from app.core.config import settings
from app.db.session import engine
# from app.tests.db.session import engine
from app.db.session import SessionLocal
from app.main import app
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers, get_apikey_token_headers

from app.db.init_db import init_db


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session", autouse=True)
def database_initialization(db):
    # Before running tests
    # Alembic config
    alembic_cfg = alembic.config.Config('alembic.ini')
    # alembic_cfg.set_section_option("logger_alembic", "level", "ERROR")
    # logging.getLogger('alembic').setLevel(logging.CRITICAL)
    # Database upgrade
    # try:
    #     alembic.command.downgrade(alembic_cfg, '6e523d653806')
    # except:
    #     pass
    alembic.command.upgrade(alembic_cfg, 'head')
    init_db(db)
    yield
    # After running tests
    db.commit()
    db.close()
    engine.dispose()
    alembic.command.downgrade(alembic_cfg, '6e523d653806')


@pytest.fixture(scope="module")
def apikey_token_headers(client: TestClient) -> Dict[str, str]:
    return get_apikey_token_headers()


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.USER_TEST_EMAIL, db=db
    )
