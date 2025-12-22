from fastapi.testclient import TestClient


def test_panel(client: TestClient) -> None:
    create_response = client.post(
        "/panel",
        json={
            "room": "Room A",
            "start_time": "2025-12-21T10:00:00",
            "end_time": "2025-12-21T11:00:00",
        },
    )
    create_response.raise_for_status()
    new_panel = create_response.json()

    get_response = client.get(f"/panel/{new_panel['id']}")
    get_response.raise_for_status()
    assert get_response.json() == new_panel

    delete_response = client.delete(f"/panel/{new_panel['id']}")
    delete_response.raise_for_status()

    get_response = client.get(f"/panel/{new_panel['id']}")
    get_response.raise_for_status()
    assert get_response.json() is None
