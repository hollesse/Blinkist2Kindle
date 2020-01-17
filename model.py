import json
from dataclasses import dataclass
from typing import List


@dataclass
class Chapter:
    id: str
    order_number: int
    title: str
    text: str


@dataclass
class Book:
    id: str
    published_at: str
    title: str
    subtitle: str
    author: str
    language: str
    about_the_book: str
    teaser: str
    who_should_read: str
    about_the_author: str
    market: str
    image_url: str
    chapters: List[Chapter]

    def __repr__(self):
        return self.author + " - " + self.title






