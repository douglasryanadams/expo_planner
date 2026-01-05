from fastapi.testclient import TestClient


def test_room(client: TestClient) -> None:
    conf_response = client.post(
        "/rest/conference",
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
        "/rest/room",
        json={
            "label": "Room A",
            "location": "First Floor",
            "capacity": 100,
            "conference": conference["id"],
        },
    )
    create_response.raise_for_status()
    new_room = create_response.json()

    get_response = client.get(f"/rest/room/{new_room['id']}")
    get_response.raise_for_status()
    assert get_response.json() == new_room

    delete_response = client.delete(f"/rest/room/{new_room['id']}")
    delete_response.raise_for_status()

    get_response = client.get(f"/rest/room/{new_room['id']}")
    get_response.raise_for_status()
    assert get_response.json() is None
