from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity_success():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Ensure not already signed up
    client.delete(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]


def test_signup_for_activity_already_signed_up():
    email = "michael@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "Student already signed up" in response.json()["detail"]


def test_unregister_from_activity_success():
    email = "testremove@mergington.edu"
    activity = "Chess Club"
    # Sign up first
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Unregistered {email} from {activity}" in response.json()["message"]


def test_unregister_from_activity_not_found():
    email = "notfound@mergington.edu"
    activity = "Chess Club"
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_signup_activity_not_found():
    email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_activity_not_found():
    email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_invalid_email_format():
    """Test that invalid email formats are rejected"""
    activity = "Chess Club"
    
    # Test various invalid email formats
    invalid_emails = [
        "notanemail",
        "missing@domain",
        "@nodomain.com",
        "no@domain@double.com",
        "spaces in@email.com",
        "",
        "just@",
        "@justdomain.com"
    ]
    
    for email in invalid_emails:
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 400
        assert "Invalid email format" in response.json()["detail"]


def test_signup_valid_email_format():
    """Test that valid email formats are accepted"""
    activity = "Chess Club"
    valid_email = "valid.student@mergington.edu"
    
    # Clean up first
    client.delete(f"/activities/{activity}/unregister?email={valid_email}")
    
    response = client.post(f"/activities/{activity}/signup?email={valid_email}")
    assert response.status_code == 200
    assert f"Signed up {valid_email} for {activity}" in response.json()["message"]
