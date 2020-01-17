import datetime
import logging
import uuid
from typing import Tuple, List

import requests
import json

from abstract_scraper import Scraper
from api import Api
from blinkst_scraper_mock import BlinkistScraperMock
from book_to_epub_converter import BookToEpubConverter
from book_to_markdown_converter import BookToMarkDownConverter
from model import Book, Chapter
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


class BlinkistScraper(Scraper):

    def __init__(self, configfile_name='config.json'):
        with open(configfile_name) as config_file:
            self.__config = json.load(config_file)['blinkist']
            logging.info('Loaded configuration from ' + configfile_name)
        self.__api = Api('api.json', 'blinkist')
        self.token = self.__get_token(email=self.__config['email'], password=self.__config['password'])

    def __get_client_information(self) -> Tuple[str, str]:
        data = {'client_name': str(uuid.uuid4()),
                'email': self.__config['email'],
                'password': self.__config['password']}
        r = requests.post(self.__api.get_url('client_info'), data=json.dumps(data))
        response = r.json()
        return response['client']['client_id'], response['client']['client_secret']

    def __get_token(self, email, password) -> str:
        (client_id, client_secret) = self.__get_client_information()
        client = BackendApplicationClient(client_id=client_id, scope='api')
        oauth = OAuth2Session(client=client, )
        token = oauth.fetch_token(token_url=self.__api.get_url('token'),
                                  include_client_id=True,
                                  client_secret=client_secret)
        return token

    def get_free_books(self, language_code: str):
        params = {'languages[]': language_code}

        r = requests.get(self.__api.get_url('free_books'), params=params)
        return r.json()['free_books']

    def get_free_book_id(self, date: datetime.datetime, language_code: str) -> str:
        for free_book in self.get_free_books(language_code):
            if date.strftime("%Y-%m-%d") == free_book['free_at']:
                return free_book['book_id']

    def get_book(self, book_id: str) -> Book:
        r = requests.get(self.__api.get_url('books') + '/' + book_id)
        json_book = r.json()['book']
        chapters = list()
        for json_chapter in json_book['chapters']:
            chapters.append(Chapter(id=json_chapter['id'],
                                    order_number=json_chapter['order_nr'],
                                    title=json_chapter['title'],
                                    text=json_chapter['text']))

        book = Book(id=json_book['id'],
                    published_at=json_book['published_at'],
                    title=json_book['title'],
                    subtitle=json_book['subtitle'],
                    author=json_book['author'],
                    language=json_book['language'],
                    about_the_book=json_book['about_the_book'],
                    teaser=json_book['teaser'],
                    who_should_read=json_book['who_should_read'],
                    about_the_author=json_book['about_the_author'],
                    market=json_book['market'],
                    image_url=json_book['image_url'],
                    chapters=chapters)
        return book

    def scrape(self) -> List[Book]:
        books = list()
        for language in self.__config['languages']:
            books.append(self.get_book(self.get_free_book_id(datetime.datetime.now(), language)))
        logging.info('Found the following books: ' + str(books))
        return books