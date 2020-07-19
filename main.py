import logging

from blinkist_scraper import BlinkistScraper
from book_converter import Format
from book_to_epub_converter import BookToEpubConverter
from book_to_markdown_converter import BookToMarkDownConverter
from book_to_html_converter import BookToHtmlConverter
from email_service import EmailService, SenderFactory, Receiver, ReceiverFactory


def cronjob():
    logging.basicConfig(level=logging.INFO)
    scraper = BlinkistScraper('config.json')
    #scraper = BlinkistScraperMock()
    books = scraper.scrape()
    md_converter = BookToMarkDownConverter('blinkist/md')
    epub_converter = BookToEpubConverter('blinkist/epub')
    html_converter = BookToHtmlConverter('blinkist/html')
    email = EmailService(sender=SenderFactory.sender('config.json'))
    receivers = ReceiverFactory.receivers('config.json')
    for book in books:
        filenames= dict()
        filenames[Format.MarkDown] = md_converter.convert(book)
        filenames[Format.EPUB] = epub_converter.convert(book)
        filenames[Format.HTML] = html_converter.convert(book)
        for receiver in receivers:
            email.send_email([receiver],
                             'Your Daily Blink',
                             '',
                             filenames[receiver.format])


if __name__ == "__main__":
    cronjob()