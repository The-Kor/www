import requests
from bs4 import BeautifulSoup


def init_soup_obj_decor(func):
    def wrapper(*args):
        self = args[0]
        if self.soup_obj is None:
            page = requests.get(self.link)
            self.soup_obj = BeautifulSoup(page.content, 'html.parser')
        return func(*args)

    return wrapper


class Result:
    def __init__(self, link, parser_class, link_title):
        self.link = link
        self.parser = parser_class
        self.soup_obj = None
        self.link_title = link_title
        self.thread_title = ""
        self.thread = None

    def get_title(self):
        return self.link_title

    @init_soup_obj_decor
    def get_thread_title(self):
        if not self.thread_title:
            self.thread_title = self.parser.parse_title(self.soup_obj).split("\n\n")[0]
        return self.thread_title

    @init_soup_obj_decor
    def get_thread(self):
        if not self.thread:
            self.thread = self.parser.parse_thread(self.soup_obj, self.link)
        return self.thread
