from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_existing_participant():
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "student@example.edu"},
    )
    assert response.status_code == 200

    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "student@example.edu"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered student@example.edu from Chess Club"


def test_signup_updates_activity_participant_list():
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@example.edu"},
    )
    assert response.status_code == 200

    response = client.get("/activities")
    assert response.status_code == 200
    assert "newstudent@example.edu" in response.json()["Chess Club"]["participants"]


def test_unregister_participant_returns_error_for_missing_participant():
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "missing@example.edu"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
