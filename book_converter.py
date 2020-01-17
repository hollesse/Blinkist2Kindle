from enum import Enum

from model import Book


class Format(Enum):
    EPUB = 'epub'
    MarkDown = 'md'


class BookConverter:

    def __init__(self, foldername):
        self.foldername = foldername

    def convert(self, book: Book) -> str:
        raise NotImplementedError

    def get_filename(self, book: Book) -> str:
        return self.foldername + '/' + book.author.replace(" ", "_") + '-' + book.title.replace(" ", "_")

    def get_about_the_author_title(self, language: str) -> str:
        return 'Über den Author'

    def get_about_the_book_title(self, language: str) -> str:
        return 'Über das Buch'

    def get_who_should_read_title(self, language: str) -> str:
        return 'Für wen ist dieses Buch interessant'





