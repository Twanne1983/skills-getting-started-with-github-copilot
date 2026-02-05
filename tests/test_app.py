import pytest
from fastapi.testclient import TestClient

import copy
from src.app import app
from src.data import activities, get_initial_activities

client = TestClient(app)

# Save the original activities structure for test isolation

def get_original_activities():
    return get_initial_activities()
original_activities = copy.deepcopy(activities)
def test_get_activities():
    original = get_original_activities()
    activities.clear()
    for k, v in original.items():
        activities[k] = v
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    original = get_original_activities()
    activities.clear()
    for k, v in original.items():
        activities[k] = v
    test_email = "pytestuser@mergington.edu"
    activity = "Chess Club"
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 200
    assert f"Signed up {test_email}" in response.json()["message"]
    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 400
    # Unregister
    response = client.delete(f"/activities/{activity}/unregister?email={test_email}")
    assert response.status_code == 200
    assert f"Unregistered {test_email}" in response.json()["message"]
    # Unregister again should fail
    response = client.delete(f"/activities/{activity}/unregister?email={test_email}")
    assert response.status_code == 404
