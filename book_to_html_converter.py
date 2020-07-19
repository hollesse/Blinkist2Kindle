import logging
import os
import html

from book_converter import BookConverter
from model import Book
import mkepub


class BookToHtmlConverter(BookConverter):
    file_suffix = 'html'

    def __init__(self, foldername):
        super().__init__(foldername)

    def convert(self, book: Book) -> str:
        html = "<!DOCTYPE html><html><head><title>" + book.title + "</title></head><body>"

        html += self.h1(book.title) + self.h2(book.title) + self.h3(book.author) + \
               self.get_chapter_text(self.get_about_the_book_title(book.language), book.about_the_book) + \
               self.get_chapter_text(self.get_who_should_read_title(book.language), book.who_should_read) + \
               self.get_chapter_text(self.get_about_the_author_title(book.language), book.about_the_author)

        for chapter in book.chapters:
            title = str(chapter.order_number) + '. ' + chapter.title
            html += self.get_chapter_text(title, chapter.text)
        html += "</body></html>"
        logging.info('Converted book "' + book.author + ' - ' + book.title + '" to HTML')

        if not os.path.exists(self.foldername):
            os.makedirs(self.foldername)
        complete_filename = self.get_filename(book) + '.' + self.file_suffix
        try:
            with open(complete_filename, 'w') as file:
                file.write(html)
            logging.info('Saved book "' + book.author + ' - ' + book.title + '" to "' + complete_filename + '"')
        except FileExistsError:
            logging.warning('Could not save book "' + book.author + ' - ' + book.title + '". File "' + complete_filename
                            + '" exists already.')
        return complete_filename

    @staticmethod
    def get_chapter_text(heading, text):
        return BookToHtmlConverter.h3(heading) + '\n' + BookToHtmlConverter.replace_special_chars(text) + '\n'

    @staticmethod
    def h1(heading):
        return BookToHtmlConverter.simple_html_tag('h1', heading)

    @staticmethod
    def h2(heading):
        return BookToHtmlConverter.simple_html_tag('h2', heading)

    @staticmethod
    def h3(heading):
        return BookToHtmlConverter.simple_html_tag('h3', heading)

    @staticmethod
    def simple_html_tag(tag, string):
        return '<' + tag + '>' + BookToHtmlConverter.replace_special_chars(string) + '</' + tag + '>'

    @staticmethod
    def replace_special_chars(string):
        for r in (("’", "&rsquo;"), ("–", "&ndash;"), ("“", "&ldquo;"), ("”", "&rdquo;")):
            string = string.replace(*r)
        return string
