import requests
from bs4 import BeautifulSoup
from utils import build_google_link

COMMON_URL_PREFIX = "/url?q="


def strip_url(url):
    if url.startswith(COMMON_URL_PREFIX):
        return url[len(COMMON_URL_PREFIX):]
    return url


def run_search(query):
    link = build_google_link(query)
    page = requests.get(link + "&num=30")
    soup_obj = BeautifulSoup(page.text, "html.parser")
    results = soup_obj.find_all('div', attrs={'class': 'ZINbbc xpd O9g5cc uUPGi'})
    for result in results:
        inner_bs = result.find('div', attrs={'class': 'kCrYT'})
        if inner_bs:
            a = inner_bs.find('a')
            h3 = inner_bs.find('h3')
            yield strip_url(a['href']), h3.get_text()