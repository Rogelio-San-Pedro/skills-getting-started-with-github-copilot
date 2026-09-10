from src.app import activities

EXISTING_ACTIVITY = "Chess Club"
EXISTING_PARTICIPANT = "michael@mergington.edu"
NEW_EMAIL = "newstudent@mergington.edu"


def test_root_redirects_to_static_index(client):
    # Arrange
    # (no setup needed)

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities(client):
    # Arrange
    # (no setup needed, using default in-memory activities)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert EXISTING_ACTIVITY in body
    assert body[EXISTING_ACTIVITY]["participants"] == activities[EXISTING_ACTIVITY]["participants"]


def test_signup_adds_participant_to_activity(client):
    # Arrange
    activity_name = EXISTING_ACTIVITY

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": NEW_EMAIL})

    # Assert
    assert response.status_code == 200
    assert NEW_EMAIL in activities[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity_name = EXISTING_ACTIVITY

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": EXISTING_PARTICIPANT}
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Activity"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": NEW_EMAIL})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_removes_participant_from_activity(client):
    # Arrange
    activity_name = EXISTING_ACTIVITY

    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister", params={"email": EXISTING_PARTICIPANT}
    )

    # Assert
    assert response.status_code == 200
    assert EXISTING_PARTICIPANT not in activities[activity_name]["participants"]


def test_unregister_not_signed_up_returns_400(client):
    # Arrange
    activity_name = EXISTING_ACTIVITY

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": NEW_EMAIL})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Activity"

    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister", params={"email": EXISTING_PARTICIPANT}
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
