from collections.abc import Iterator

from pytest import fixture
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from sqlmodel import create_engine, Session, SQLModel

from expoplanner.dependency import get_session
from expoplanner.main import app


@fixture(scope="session", autouse=True)
def fake_db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@fixture
def client(fake_db_session) -> Iterator[TestClient]:
    def get_session_override():
        return fake_db_session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_presenter(client: TestClient) -> None:
    create_response = client.post(
        "/presenter",
        json={
            "name": "Jane Smith",
            "identity_id": "ID67890",
            "website": "https://janesmith.com",
        },
    )
    create_response.raise_for_status()
    new_presenter = create_response.json()

    get_response = client.get(f"/presenter/{new_presenter['id']}")
    get_response.raise_for_status()
    assert get_response.json() == new_presenter

    delete_response = client.delete(f"/presenter/{new_presenter['id']}")
    delete_response.raise_for_status()

    get_response = client.get(f"/presenter/{new_presenter['id']}")
    get_response.raise_for_status()
    assert get_response.json() is None
