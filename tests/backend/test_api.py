from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module
from src.app import app


ORIGINAL_ACTIVITIES = deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange
    app_module.activities.clear()
    app_module.activities.update(deepcopy(ORIGINAL_ACTIVITIES))
    yield
    app_module.activities.clear()
    app_module.activities.update(deepcopy(ORIGINAL_ACTIVITIES))


client = TestClient(app)


def test_root_redirects_to_static_index():
    # Arrange
    path = "/"

    # Act
    response = client.get(path, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_available_activities():
    # Arrange
    path = "/activities"

    # Act
    response = client.get(path)

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["max_participants"] == 12


def test_signup_for_activity_adds_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_duplicate_participant_returns_error():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
