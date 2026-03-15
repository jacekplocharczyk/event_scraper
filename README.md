# Event Scraper

A modular, generic event scraper with MCP integration. Scrapes predefined websites (starting with Zacheta) and returns events in a unified format.

## Features

- **Unified Event Format** — All events standardized with title, date, location, URL, and source
- **Modular Design** — Easy to add new scrapers by subclassing `BaseScraper`
- **MCP Integration** — Expose scraping functionality to agentic systems via FastMCP
- **Async-First** — Built on `httpx` async client for scalability
- **TDD-Driven** — Full test coverage with mocked HTTP responses
- **No Data Persistence** — Stateless scraper, all computation on-demand

## Quick Start

### Install

```bash
uv sync
```

### Run Tests

```bash
uv run pytest .
```

### Try the Example

```bash
uv run python examples/zacheta_example.py
```

### Start MCP Server

```bash
uv run python -m event_scraper
```

## Project Structure

```
event_scraper/
├── src/event_scraper/
│   ├── __init__.py
│   ├── __main__.py              # MCP server entry point
│   ├── models.py                # Event Pydantic model
│   ├── base.py                  # Abstract BaseScraper
│   ├── scrapers/
│   │   ├── __init__.py
│   │   └── zacheta.py           # Zacheta gallery scraper
│   └── server.py                # FastMCP server with tools
├── tests/
│   ├── conftest.py              # Shared fixtures (HTML samples)
│   ├── test_models.py
│   ├── test_zacheta.py          # Scraper tests (mocked HTTP)
│   └── test_server.py           # MCP integration tests
├── examples/
│   └── zacheta_example.py       # Static usage example
└── pyproject.toml
```

## Usage

### As a Library

```python
import asyncio
import httpx
from event_scraper.scrapers.zacheta import ZachetaScraper

async def main():
    async with httpx.AsyncClient() as client:
        scraper = ZachetaScraper(client)
        events = await scraper.scrape()
        for event in events:
            print(f"{event.title} on {event.date}")

asyncio.run(main())
```

### Via MCP Server

```bash
uv run python -m event_scraper
```

Then use the MCP client to call:
- `list_sources()` — List available event sources
- `get_events(source)` — Scrape events from a specific source

## Dependencies

- **fastmcp** ≥3.1 — MCP framework
- **httpx** ≥0.28 — Async HTTP client
- **beautifulsoup4** ≥4.14 — HTML parsing
- **pydantic** ≥2.0 — Data validation

## Extending with New Scrapers

1. Create a new file in `src/event_scraper/scrapers/`
2. Subclass `BaseScraper` and implement `async def scrape()`
3. Register in `server.py`'s `SCRAPERS` dict
4. Add tests to `tests/`

Example:

```python
from ..base import BaseScraper
from ..models import Event

class MyVenueScraper(BaseScraper):
    async def scrape(self) -> list[Event]:
        response = await self.client.get("https://example.com/events")
        # Parse and return Event objects
        return []
```

## License

Internal project