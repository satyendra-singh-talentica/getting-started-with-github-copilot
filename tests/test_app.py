import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test activity listing
def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# Test signup for activity
@pytest.mark.parametrize("activity,email", [
    ("Chess Club", "newstudent@mergington.edu"),
    ("Programming Class", "coder@mergington.edu"),
])
def test_signup_for_activity(activity, email):
    # Ensure not already signed up
    client.post(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Duplicate signup should fail
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]

# Test unregister from activity
@pytest.mark.parametrize("activity,email", [
    ("Chess Club", "newstudent@mergington.edu"),
    ("Programming Class", "coder@mergington.edu"),
])
def test_unregister_from_activity(activity, email):
    # Ensure signed up
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Unregistered {email} from {activity}" in response.json()["message"]
    # Unregister again should fail
    response2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response2.status_code == 400
    assert "not registered" in response2.json()["detail"]

# Test invalid activity
def test_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    response2 = client.post("/activities/Nonexistent/unregister?email=test@mergington.edu")
    assert response2.status_code == 404
