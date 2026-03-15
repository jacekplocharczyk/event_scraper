import pytest
import httpx
import respx
from unittest.mock import AsyncMock, patch
from event_scraper.models import Event
from event_scraper.server import list_sources, get_events
from datetime import datetime


def test_list_sources():
    sources = list_sources()
    assert isinstance(sources, list)
    assert "zacheta" in sources


@pytest.mark.asyncio
async def test_get_events_zacheta(zacheta_html):
    async with respx.mock:
        respx.get("https://zacheta.art.pl/pl/kalendarz").mock(
            return_value=httpx.Response(200, text=zacheta_html)
        )

        events = await get_events("zacheta")

        assert len(events) == 3
        assert all(isinstance(e, Event) for e in events)
        assert events[0].source == "zacheta"


@pytest.mark.asyncio
async def test_get_events_unknown_source():
    with pytest.raises(ValueError) as exc_info:
        await get_events("unknown_source")
    assert "Unknown source: unknown_source" in str(exc_info.value)
