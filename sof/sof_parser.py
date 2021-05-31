import utils
from site_parser import Parser
from utils_objects import Thread, Site
import requests
from bs4 import BeautifulSoup
from question import *
from answer import *


class SOFParser(Parser):
    site = Site.SOF
    site_url = site.value.url

    def parse_links(self, links) -> Thread:
        """
        A generator that yields a Thread instance for every link in the given list
        """
        # parse sof links
        links_counter = 0
        for link in links:
            links_counter += 1
            parsed_thread = self.parse_link(link)
            if parsed_thread:
                yield parsed_thread
            if links_counter >= utils.max_results_per_site:
                break

    def parse_link(self, link):
        """
        Parses a link to Thread instance
        """
        if not SOFParser.is_valid_link(link):
            return None
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        question = self.parse_question(soup)
        if not question:
            return None
        answers = self.parse_answers(soup)
        return Thread(self.site_url, link, question, answers)

    @staticmethod
    def is_valid_link(link):
        """
        Checks that
        """
        return 'stackoverflow.com' in link

    def parse_question_attributes(self, soup):
        attributes = dict()
        question_attr_div = soup.find("div", {"class": "grid fw-wrap pb8 mb16 bb bc-black-075"})
        if not question_attr_div:
            return None
        question_attr_parts = question_attr_div.find_all("div")
        for part in question_attr_parts:
            key = utils.strip_string(part.find("span").getText())
            attributes[key] = utils.strip_string(part.getText().replace(key, ""))
        return attributes

    def parse_answers(self, soup):
        answers_div = soup.find_all("div", {"class": "answer"})
        answers = []
        for id, answer in enumerate(answers_div):
            attr = dict()
            attr["score"] = answer.get("data-score")
            answer_parts = answer.find_all("div", {"class": "s-prose js-post-body"})
            answer_data = ""
            for part in answer_parts:
                answer_data += part.getText()
            answer_data = utils.strip_string(answer_data)
            answers.append(Answer(id, answer_data, attr))
        return answers

    def parse_question(self, soup):
        attributes = self.parse_question_attributes(soup)
        if not attributes:
            return None
        question_title = soup.find(id="question-header").find("h1").getText()
        question_div = soup.find("div", {"class": "question"})
        attributes['score'] = question_div.get("data-score")
        question_parts = question_div.find_all("div", {"class": "s-prose js-post-body"})
        question_data = utils.strip_string("".join([q.getText() for q in question_parts]))

        question = Question(question_title, question_data, attributes)
        return question
