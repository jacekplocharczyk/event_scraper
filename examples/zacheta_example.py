"""
Zacheta Gallery Event Scraper Example

Fetches and displays upcoming events from Zacheta Gallery in a nicely formatted table.

Run with: uv run python examples/zacheta_example.py
"""

import asyncio
import httpx
from datetime import datetime
from event_scraper.scrapers.zacheta import ZachetaScraper


def format_event_table(events):
    """Pretty print events in a table format."""
    if not events:
        print("No events found.")
        return

    print("\n" + "=" * 165)
    print(f"{'Title':<100} | {'Date':<20} | {'Location':<25} | {'URL':<20}")
    print("=" * 165)

    for event in events:
        date_str = event.date.strftime("%Y-%m-%d %H:%M")
        location = event.location or "—"
        # Truncate long URLs for display
        url = event.url[-20:] if len(event.url) > 20 else event.url

        print(f"{event.title[:100]:<100} | {date_str:<20} | {location:<25} | {event.url}")

    print("=" * 165)
    print(f"Total: {len(events)} events\n")


async def main():
    """Fetch and display Zacheta events."""
    print("Fetching events from Zacheta Gallery...")

    async with httpx.AsyncClient(timeout=10.0) as client:
        scraper = ZachetaScraper(client)
        try:
            events = await scraper.scrape()
            format_event_table(events)

            # Print detailed info for first event
            if events:
                first = events[0]
                print("First Event Details:")
                print(f"  Title:    {first.title}")
                print(f"  Date:     {first.date.strftime('%A, %B %d, %Y at %H:%M')}")
                print(f"  Location: {first.location or 'Not specified'}")
                print(f"  URL:      {first.url}")
                print(f"  Source:   {first.source}")
        except Exception as e:
            print(f"Error fetching events: {e}")


if __name__ == "__main__":
    asyncio.run(main())
