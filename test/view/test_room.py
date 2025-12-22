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


def test_room(client: TestClient) -> None:
    # First create a conference because room has a foreign key to conference
    conf_response = client.post(
        "/conference",
        json={
            "name": "Test Conference",
            "location": "Test Location",
            "start_date": "2025-12-21",
            "end_date": "2025-12-22",
        },
    )
    conf_response.raise_for_status()
    conference = conf_response.json()

    create_response = client.post(
        "/room",
        json={
            "label": "Room A",
            "location": "First Floor",
            "capacity": 100,
            "conference": conference["id"],
        },
    )
    create_response.raise_for_status()
    new_room = create_response.json()

    get_response = client.get(f"/room/{new_room['id']}")
    get_response.raise_for_status()
    assert get_response.json() == new_room

    delete_response = client.delete(f"/room/{new_room['id']}")
    delete_response.raise_for_status()

    get_response = client.get(f"/room/{new_room['id']}")
    get_response.raise_for_status()
    assert get_response.json() is None
