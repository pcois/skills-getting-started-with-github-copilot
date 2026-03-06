import uuid

from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def unique_email() -> str:
    return f"test-{uuid.uuid4()}@mergington.edu"


def test_get_activities_returns_data():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_success():
    email = unique_email()
    activity = "Chess Club"

    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    cleanup = client.delete(
        f"/activities/{activity}/participants",
        params={"email": email},
    )
    assert cleanup.status_code == 200


def test_signup_duplicate_returns_error():
    email = unique_email()
    activity = "Programming Class"

    first = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )
    assert first.status_code == 200

    duplicate = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )
    assert duplicate.status_code == 400

    cleanup = client.delete(
        f"/activities/{activity}/participants",
        params={"email": email},
    )
    assert cleanup.status_code == 200


def test_signup_missing_activity_returns_404():
    response = client.post(
        "/activities/Nonexistent%20Club/signup",
        params={"email": unique_email()},
    )

    assert response.status_code == 404


def test_unregister_success():
    email = unique_email()
    activity = "Gym Class"

    signup = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )
    assert signup.status_code == 200

    response = client.delete(
        f"/activities/{activity}/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert "Removed" in response.json()["message"]


def test_unregister_missing_participant_returns_404():
    activity = "Gym Class"
    response = client.delete(
        f"/activities/{activity}/participants",
        params={"email": unique_email()},
    )

    assert response.status_code == 404
