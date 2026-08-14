from urllib.parse import quote

from src.app import activities, app

from fastapi.testclient import TestClient

client = TestClient(app)


def test_delete_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "newstudent@example.com"
    original_participants = activities[activity_name]["participants"].copy()

    try:
        signup_response = client.post(
            "/activities/{}/signup?email={}".format(activity_name, quote(email))
        )
        assert signup_response.status_code == 200
        assert email in activities[activity_name]["participants"]

        delete_response = client.delete(
            "/activities/{}/participants/{}".format(activity_name, quote(email))
        )

        assert delete_response.status_code == 200
        assert email not in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants
