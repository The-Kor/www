import utils
from site_parser import Parser
from utils_objects import Thread, Site
import requests
from bs4 import BeautifulSoup


class SOFParser(Parser):
    site = Site.SOF

    def parse_links(self, links, site_url) -> Thread:
        # parse sof links
        links_counter = 0
        for link in links:
            links_counter += 1
            yield self.parse_link(link, site_url)
            if links_counter >= utils.max_results_per_site:
                break

    def parse_link(self, link, site_url):
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        mydivs = soup.find_all("div", {"class": "answer"})
        question_div = soup.find("div", {"class": "question"})
        question_parts = question_div.find_all("div", {"class": "s-prose js-post-body"})
        answers = []
        question = " ".join([q.getText() for q in question_parts])
        for answer in mydivs:
            # answers.append(answer.getText())
            answer_parts = answer.find_all("div", {"class": "s-prose js-post-body"})
            answer_str = ""
            for part in answer_parts:
                answer_str += part.getText()
            # answer_soup = BeautifulSoup(answer.html)
            answers.append(answer_str)
        return Thread(site_url, link, question, answers)
