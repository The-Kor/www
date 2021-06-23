import requests
from bs4 import BeautifulSoup


def init_soup_obj_decor(func):
    def wrapper(*args):
        self = args[0]
        if self.page is None or self.soup_obj is None:
            self.page = requests.get(self.link)
            self.soup_obj = BeautifulSoup(self.page.content, 'html.parser')
        return func(*args)

    return wrapper


class Result:
    def __init__(self, link, parser_class):
        self.link = link
        self.parser = parser_class
        self.page = None
        self.soup_obj = None
        self.title = ""
        self.thread = None

    @init_soup_obj_decor
    def get_title(self):
        # Fill page_content if None
        # Calls self.parser parse title, is self.title is "" , returns self.title
        if not self.title:
            self.title = self.parser.parse_title(self.soup_obj).split("\n\n")[0]
        return self.title

    @init_soup_obj_decor
    def get_thread(self):
        # Fill page_content if None
        # Calls self.parser parse link if self.thread is None, retuns self.thread
        if not self.thread:
            self.thread = self.parser.parse_thread(self.soup_obj, self.link)
        return self.thread
