import requests
from bs4 import BeautifulSoup
from utils import build_google_link, is_link_supported
from collections import OrderedDict

CHROME_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'


def is_main_google_link(soup_tag):
    """
    This function checks if the given BeautifulSoup4 tag is of a main link in Google page
    """
    return 'data-ved' in soup_tag.attrs


def get_title_of_result_element(soup_tag):
    """
    This function parses a title from a given BeautifulSoup4 tag element of Google result (main/secondary)
    The title can be found in span element with dir="ltr".
    """
    for child in soup_tag.children:
        for content_tag in child.contents:
            if content_tag.get('dir', False) == 'ltr':
                return child.getText()
    return ""


def is_secondary_google_link(soup_tag):
    """
    This function checks if the given BeautifulSoup4 tag is of a secondary link in Google page (see Issue #47)
    """
    if 'class' in soup_tag.attrs:
        if 'fl' in soup_tag.attrs['class']:
            return True
    return False


def run_search(query, parsers, max_num_of_results):
    """
    This function gets a query to search and parses results from Google.
    The function is using Google Chrome User-Agent to get a response in a specific form (for parsing).
    The function returns a list of tuples where each tuple is (link,title), the list is ordered by the order
    that appears in the Google search page.
    The function maintains an OrderdDict as this is the way to maintain OrderedSet
     (no duplicates while keeping the insertion order), the values of this dict are ignored (only keys are returned)
    """
    link = build_google_link(query, max_num_of_results)
    page = requests.get(
        link,
        headers={'User-Agent': CHROME_UA})
    soup_obj = BeautifulSoup(page.content, "html.parser")
    raw_results_tags = soup_obj.find_all('div', attrs={'class': "g"})
    href_tags = [r.find_all('a', href=True) for r in raw_results_tags]
    results_tags = {c for h in href_tags for c in h if
                    is_link_supported(c.attrs['href'], parsers) and (
                            is_secondary_google_link(c) or is_main_google_link(c))}

    # Maintaining an OrderedDict as an ordered set (no dups but keeping the insertion order)
    results = OrderedDict()
    for r in results_tags:
        results[(r.attrs['href'], get_title_of_result_element(r))] = None
    # Discarding the values of the dict (irrelevant)
    return results.keys()
