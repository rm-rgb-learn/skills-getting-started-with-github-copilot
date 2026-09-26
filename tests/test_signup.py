import pytest
from fastapi import HTTPException, Response

from src.app import activities, get_activities, signup_for_activity, unregister_from_activity


def test_signup_rejects_duplicate_email(monkeypatch):
    activity_name = "Duplicate Signup Test"
    participants = []
    monkeypatch.setitem(activities, activity_name, {"participants": participants})

    signup_for_activity(activity_name, "student@example.test")

    with pytest.raises(HTTPException) as error:
        signup_for_activity(activity_name, "student@example.test")

    assert error.value.status_code == 409
    assert participants == ["student@example.test"]


def test_unregister_removes_all_matching_entries(monkeypatch):
    activity_name = "Unregister Test"
    participants = ["student@example.test", "other@example.test", "student@example.test"]
    monkeypatch.setitem(activities, activity_name, {"participants": participants})

    result = unregister_from_activity(activity_name, "student@example.test")

    assert result["message"] == "Unregistered student@example.test from Unregister Test"
    assert participants == ["other@example.test"]


def test_activities_are_not_cacheable():
    response = Response()

    get_activities(response)

    assert response.headers["cache-control"] == "no-store"