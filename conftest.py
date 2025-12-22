import sys
from collections.abc import Iterator

from loguru import logger
import pytest

from sqlalchemy import StaticPool
from sqlmodel import create_engine, Session, SQLModel
from fastapi.testclient import TestClient

from expoplanner.dependency import get_session
from expoplanner.main import app


@pytest.fixture(scope="session", autouse=True)
def configure_loguru():
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:HH:mm:ss}</green> <level>{level: <8}</level> - <level>{message}</level>",
        level="DEBUG",
        colorize=True,
    )
    yield


@pytest.fixture
def caplog_loguru(capfd):
    yield
    captured = capfd.readouterr()
    return captured


@pytest.fixture(scope="session", autouse=True)
def fake_db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(fake_db_session) -> Iterator[TestClient]:
    def get_session_override():
        return fake_db_session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
