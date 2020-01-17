from typing import List

from model import Book


class Scraper:

    def scrape(self) -> List[Book]:
        raise NotImplementedError
