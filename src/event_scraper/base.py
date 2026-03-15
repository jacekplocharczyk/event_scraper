from abc import ABC, abstractmethod
import httpx
from .models import Event


class BaseScraper(ABC):
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    @abstractmethod
    async def scrape(self) -> list[Event]:
        ...
