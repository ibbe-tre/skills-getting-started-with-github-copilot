from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_existing_participant():
    # Arrange
    email = "student@example.edu"

    # Act
    signup_response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )
    unregister_response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email},
    )

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == "Unregistered student@example.edu from Chess Club"


def test_signup_updates_activity_participant_list():
    # Arrange
    email = "newstudent@example.edu"

    # Act
    signup_response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert activities_response.status_code == 200
    assert email in activities_response.json()["Chess Club"]["participants"]


def test_unregister_participant_returns_error_for_missing_participant():
    # Arrange
    email = "missing@example.edu"

    # Act
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
