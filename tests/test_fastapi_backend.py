from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def test_get_activities_returns_catalog():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_adds_new_participant():
    activity_name = "Chess Club"
    email = "newstudent@example.com"
    original_participants = activities[activity_name]["participants"].copy()

    try:
        response = client.post(
            "/activities/{}/signup?email={}".format(quote(activity_name), quote(email))
        )

        assert response.status_code == 200
        assert response.json() == {
            "message": f"Signed up {email} for {activity_name}"
        }
        assert email in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants


def test_duplicate_signup_is_rejected():
    activity_name = "Chess Club"
    email = activities[activity_name]["participants"][0]

    response = client.post(
        "/activities/{}/signup?email={}".format(quote(activity_name), quote(email))
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student is already signed up for this activity"
    }


def test_unknown_activity_returns_404():
    response = client.post(
        "/activities/Unknown%20Activity/signup?email=student@example.com"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
