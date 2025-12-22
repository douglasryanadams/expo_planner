from fastapi.testclient import TestClient


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
