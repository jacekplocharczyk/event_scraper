import pytest
from datetime import datetime
from event_scraper.models import Event


def test_event_creation():
    event = Event(
        title="Test Event",
        date=datetime(2026, 3, 20, 19, 0),
        location="Test Location",
        url="https://example.com/event",
        source="zacheta",
    )
    assert event.title == "Test Event"
    assert event.date == datetime(2026, 3, 20, 19, 0)
    assert event.location == "Test Location"
    assert event.url == "https://example.com/event"
    assert event.source == "zacheta"


def test_event_optional_location():
    event = Event(
        title="No Location Event",
        date=datetime(2026, 3, 20, 19, 0),
        location=None,
        url="https://example.com/event",
        source="zacheta",
    )
    assert event.location is None


def test_event_serialization():
    event = Event(
        title="Test Event",
        date=datetime(2026, 3, 20, 19, 0),
        location="Test Location",
        url="https://example.com/event",
        source="zacheta",
    )
    data = event.model_dump()
    assert data["title"] == "Test Event"
    assert data["date"] == datetime(2026, 3, 20, 19, 0)
    assert data["location"] == "Test Location"
    assert data["source"] == "zacheta"


def test_event_json_serialization():
    event = Event(
        title="Test Event",
        date=datetime(2026, 3, 20, 19, 0),
        location="Test Location",
        url="https://example.com/event",
        source="zacheta",
    )
    json_str = event.model_dump_json()
    assert "Test Event" in json_str
    assert "zacheta" in json_str
