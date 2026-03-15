from fastmcp import FastMCP
from .scrapers.zacheta import ZachetaScraper
from .models import Event
import httpx

mcp = FastMCP("event-scraper")

SCRAPERS = {"zacheta": ZachetaScraper}


@mcp.tool
async def get_events(source: str) -> list[Event]:
    """Scrape events from a named source."""
    if source not in SCRAPERS:
        raise ValueError(f"Unknown source: {source}. Available: {list(SCRAPERS)}")

    async with httpx.AsyncClient() as client:
        scraper = SCRAPERS[source](client)
        return await scraper.scrape()


@mcp.tool
def list_sources() -> list[str]:
    """List all available event sources."""
    return list(SCRAPERS)
