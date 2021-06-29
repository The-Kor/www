from site_parser import Parser
import requests
from bs4 import BeautifulSoup
from question import *
from answer import *
from result_thread import ResultThread
from utils import strip_string


class SOFParser(Parser):
    site_url = "stackoverflow.com"
    required_path_elements = ['questions']

    @staticmethod
    def parse_thread(soup_obj, url):
        """
        Parses a given soup instance to Thread instance
        """
        question = SOFParser.parse_question(soup_obj)
        if not question:
            return None
        answers = SOFParser.parse_answers(soup_obj)
        return ResultThread(SOFParser.site_url, url, question, answers)

    @staticmethod
    def parse_title(soup_obj):
        title_div = soup_obj.find('div', {"id": "question-header"})
        return strip_string(title_div.getText())

    @staticmethod
    def parse_question_attributes(soup_obj):
        """
        Parses the question attributes according to a dict
        """
        attributes = dict()
        question_attr_div = soup_obj.find("div", {"class": "grid fw-wrap pb8 mb16 bb bc-black-075"})
        if not question_attr_div:
            return None
        question_attr_parts = question_attr_div.find_all("div")
        for part in question_attr_parts:
            key = strip_string(part.find("span").getText())
            attributes[key] = strip_string(part.getText().replace(key, ""))
        return attributes

    @staticmethod
    def parse_answers(soup_obj):
        """
        Parses all of the answers from the given soup object and returns them in a list
        """
        answers_div = soup_obj.find_all("div", {"class": "answer"})
        answers = []
        for id, answer in enumerate(answers_div):
            attr = dict()
            attr["score"] = answer.get("data-score")
            answer_parts = answer.find_all("div", {"class": "s-prose js-post-body"})
            answer_data = ""
            for part in answer_parts:
                answer_data += part.getText()
            answer_data = strip_string(answer_data)
            answers.append(Answer(id, answer_data, attr))
        return answers

    @staticmethod
    def parse_question(soup_obj):
        """
        Parses a question object from the given soup object
        """
        attributes = SOFParser.parse_question_attributes(soup_obj)
        if not attributes:
            return None
        question_title = soup_obj.find(id="question-header").find("h1").getText()
        question_div = soup_obj.find("div", {"class": "question"})
        attributes['score'] = question_div.get("data-score")
        question_parts = question_div.find_all("div", {"class": "s-prose js-post-body"})
        question_data = strip_string("".join([q.getText() for q in question_parts]))

        question = Question(question_title, question_data, attributes)
        return question
