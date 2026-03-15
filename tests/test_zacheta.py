import pytest
import httpx
import respx
from datetime import datetime
from event_scraper.scrapers.zacheta import ZachetaScraper
from event_scraper.models import Event


@pytest.mark.asyncio
async def test_zacheta_scraper_parses_events(zacheta_html):
    async with respx.mock:
        respx.get("https://zacheta.art.pl/pl/kalendarz").mock(
            return_value=httpx.Response(200, text=zacheta_html)
        )

        async with httpx.AsyncClient() as client:
            scraper = ZachetaScraper(client)
            events = await scraper.scrape()

        assert len(events) == 3
        assert all(isinstance(e, Event) for e in events)


@pytest.mark.asyncio
async def test_zacheta_scraper_event_attributes(zacheta_html):
    async with respx.mock:
        respx.get("https://zacheta.art.pl/pl/kalendarz").mock(
            return_value=httpx.Response(200, text=zacheta_html)
        )

        async with httpx.AsyncClient() as client:
            scraper = ZachetaScraper(client)
            events = await scraper.scrape()

        first = events[0]
        assert first.title == "Modern Perspectives"
        assert first.date == datetime(2026, 3, 15, 19, 0)
        assert first.location == "Sala Główna"
        assert "/pl/kalendarz/wystawka-sztuki-wspolczesnej-123" in first.url
        assert first.source == "zacheta"


@pytest.mark.asyncio
async def test_zacheta_scraper_optional_location(zacheta_html):
    async with respx.mock:
        respx.get("https://zacheta.art.pl/pl/kalendarz").mock(
            return_value=httpx.Response(200, text=zacheta_html)
        )

        async with httpx.AsyncClient() as client:
            scraper = ZachetaScraper(client)
            events = await scraper.scrape()

        third = events[2]
        assert third.title == "Lecture on Art History"
        assert third.location is None


@pytest.mark.asyncio
async def test_zacheta_scraper_multiple_events(zacheta_html):
    async with respx.mock:
        respx.get("https://zacheta.art.pl/pl/kalendarz").mock(
            return_value=httpx.Response(200, text=zacheta_html)
        )

        async with httpx.AsyncClient() as client:
            scraper = ZachetaScraper(client)
            events = await scraper.scrape()

        assert events[0].title == "Modern Perspectives"
        assert events[1].title == "Painting Workshop"
        assert events[1].date == datetime(2026, 3, 20, 15, 30)
        assert events[1].location == "Studio B"
