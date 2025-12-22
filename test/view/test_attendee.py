from fastapi.testclient import TestClient


def test_attendee(client: TestClient) -> None:
    create_response = client.post(
        "/attendee",
        json={
            "name": "John Doe",
            "identity_id": "ID12345",
        },
    )
    create_response.raise_for_status()
    new_attendee = create_response.json()

    get_response = client.get(f"/attendee/{new_attendee['id']}")
    get_response.raise_for_status()
    assert get_response.json() == new_attendee

    delete_response = client.delete(f"/attendee/{new_attendee['id']}")
    delete_response.raise_for_status()

    get_response = client.get(f"/attendee/{new_attendee['id']}")
    get_response.raise_for_status()
    assert get_response.json() is None
