import logging
import os

from book_converter import BookConverter
from model import Book


class BookToMarkDownConverter(BookConverter):
    file_suffix = 'md'

    def h1(self, string: str) -> str:
        return '# ' + string + '\n'

    def h2(self, string: str) -> str:
        return '## ' + string + '\n'

    def h3(self, string: str) -> str:
        return '### ' + string + '\n'

    def h4(self, string: str) -> str:
        return '#### ' + string + '\n'

    def italic(self, string: str) -> str:
        return '*' + string + '*'

    def bold(self, string: str) -> str:
        return '**' + string + '**'

    def convert_html_text(self, text: str) -> str:
        text = text.replace('\xa0', ' ')
        text = text.replace('<p>', '')
        text = text.replace('</p>', '\n')
        text = text.replace('<ul>', '')
        text = text.replace('</ul>', '')
        text = text.replace('<li>', '* ')
        text = text.replace('</li>', '')
        text = text.replace('<em>', '*')
        text = text.replace('</em>', '*')
        text = text.replace('</strong><strong>', '</strong> <strong>')
        text = text.replace(' </strong>', '</strong>')
        text = text.replace('<strong> ', '<strong>')
        text = text.replace('<strong>', '**')
        text = text.replace('</strong>', '**')

        return text

    def convert(self, book: Book) -> str:
        title = self.h1(book.title)
        subtitle = self.h2(book.subtitle)
        author = self.italic(book.author) + ' \n'
        payload = title + \
                  subtitle + \
                  author + \
                  self.get_about_the_author(book) + \
                  self.get_about_the_book(book) + \
                  self.get_who_should_read(book) + \
                  self.get_table_of_contents(book) + \
                  self.get_chapters(book)
        logging.info('Converted book "' + book.author + ' - ' + book.title + '" to MarkDown')
        complete_filename = self.get_filename(book) + '.' + self.file_suffix
        if not os.path.exists(self.foldername):
            os.makedirs(self.foldername)
        with open(complete_filename, 'w') as f:
            f.writelines(payload)
        logging.info('Saved book "' + book.author + ' - ' + book.title + '" to "' + complete_filename + '"')
        return complete_filename

    def h3_with_text(self, heading, text):
        return self.h3(heading) + '\n' + self.convert_html_text(text) + '\n'

    def get_about_the_book(self, book: Book) -> str:
        return self.h3_with_text(self.get_about_the_author_title(book.language), book.about_the_book)

    def get_who_should_read(self, book: Book) -> str:
        return self.h3_with_text(self.get_who_should_read_title(book.language), book.who_should_read)

    def get_about_the_author(self, book: Book) -> str:
        return self.h3_with_text(self.get_about_the_author_title(book.language), book.about_the_author)

    def get_table_of_contents(self, book: Book) -> str:
        payload = self.h2('TOC')
        for chapter in book.chapters:
            payload += str(chapter.order_number) + '. ' + chapter.title + '\n'
        return payload

    def get_chapters(self, book: Book) -> str:
        payload = ""
        for chapter in book.chapters:
            payload += self.h2(str(chapter.order_number) + '. ' + chapter.title)
            payload += self.convert_html_text(chapter.text) + '\n'
        return payload