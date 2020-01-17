import logging
import os

from book_converter import BookConverter
from model import Book
import mkepub


class BookToEpubConverter(BookConverter):
    file_suffix = 'epub'

    def __init__(self, foldername):
        super().__init__(foldername)

    def convert(self, book: Book) -> str:
        epub = mkepub.Book(title=book.title, author=book.author)
        epub.add_page('Cover', self.h1(book.title) + '\n' + self.h2(book.subtitle) + '\n' + book.author + '\n')
        epub.add_page(self.get_about_the_book_title(book.language),
                      self.get_chapter_text(self.get_about_the_book_title(book.language), book.about_the_book))
        epub.add_page(self.get_who_should_read_title(book.language),
                      self.get_chapter_text(self.get_who_should_read_title(book.language), book.who_should_read))
        epub.add_page(self.get_about_the_author_title(book.language),
                      self.get_chapter_text(self.get_about_the_author_title(book.language), book.about_the_author))

        for chapter in book.chapters:
            title = str(chapter.order_number) + '. ' + chapter.title
            epub.add_page(title, self.get_chapter_text(title, chapter.text))
        logging.info('Converted book "' + book.author + ' - ' + book.title + '" to EPUB')

        if not os.path.exists(self.foldername):
            os.makedirs(self.foldername)
        complete_filename = self.get_filename(book) + '.' + self.file_suffix
        try:
            epub.save(complete_filename)
            logging.info('Saved book "' + book.author + ' - ' + book.title + '" to "' + complete_filename + '"')
        except FileExistsError:
            logging.warning('Could not save book "' + book.author + ' - ' + book.title + '". File "' + complete_filename
                            + '" exists already.')
        return complete_filename

    @staticmethod
    def get_chapter_text(heading, text):
        return BookToEpubConverter.h3(heading) + '\n' + text + '\n'

    @staticmethod
    def h1(heading):
        return BookToEpubConverter.simple_html_tag('h1', heading)

    @staticmethod
    def h2(heading):
        return BookToEpubConverter.simple_html_tag('h2', heading)

    @staticmethod
    def h3(heading):
        return BookToEpubConverter.simple_html_tag('h3', heading)

    @staticmethod
    def simple_html_tag(tag, string):
        return '<' + tag + '>' + string + '</' + tag + '>'
