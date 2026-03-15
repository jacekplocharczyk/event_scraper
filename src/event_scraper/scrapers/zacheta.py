import httpx
import re
from datetime import datetime
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from ..base import BaseScraper
from ..models import Event


class ZachetaScraper(BaseScraper):
    BASE_URL = "https://zacheta.art.pl"
    CALENDAR_URL = f"{BASE_URL}/pl/kalendarz"

    async def scrape(self) -> list[Event]:
        response = await self.client.get(self.CALENDAR_URL)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        events = []

        date_pattern = re.compile(r"(\d{2})\.(\d{2})\s*\([A-Z]{2}\)\s*(\d{2}):(\d{2})")
        current_year = datetime.now().year

        for item in soup.select("li"):
            link = item.find("a", href=True)
            if not link or "/kalendarz/" not in link.get("href", ""):
                continue

            href = link["href"]
            url = urljoin(self.CALENDAR_URL, href)
            text = item.get_text(" ", strip=True)

            match = date_pattern.search(text)
            if not match:
                continue

            day, month, hour, minute = match.groups()
            date = datetime(
                year=current_year,
                month=int(month),
                day=int(day),
                hour=int(hour),
                minute=int(minute),
            )

            rest = text[match.end():].strip()
            parts = rest.split("  ")
            title = parts[0] if parts else ""
            location = parts[-1] if len(parts) > 1 else None

            events.append(Event(
                title=title,
                date=date,
                location=location,
                url=url,
                source="zacheta",
            ))

        return events
