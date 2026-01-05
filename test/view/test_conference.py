from fastapi.testclient import TestClient


def test_conference(client: TestClient) -> None:
    create_response = client.post(
        "/rest/conference",
        json={
            "name": "Test Conference",
            "location": "Test Location",
            "start_date": "1986-09-24T00:00:00",
            "end_date": "2025-12-31T00:00:00",
        },
    )
    create_response.raise_for_status()
    new_conference = create_response.json()

    get_response = client.get(f"/rest/conference/{new_conference['id']}")
    get_response.raise_for_status()
    assert get_response.json() == new_conference

    delete_response = client.delete(f"/rest/conference/{new_conference['id']}")
    delete_response.raise_for_status()

    get_response = client.get(f"/rest/conference/{new_conference['id']}")
    get_response.raise_for_status()
