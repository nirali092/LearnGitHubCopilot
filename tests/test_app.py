from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activity = client.get("/activities").json()[activity_name]
    assert email not in activity["participants"]


def test_unregister_unknown_participant_returns_error():
    # Arrange
    activity_name = "Chess Club"
    email = "missing@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
