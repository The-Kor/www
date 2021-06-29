from site_parser import Parser
from question import *
from answer import *
from utils_objects import Thread
from utils import strip_string


class GITHUBParser(Parser):
    site_url = "github.com"
    required_path_elements = ['issues']

    @staticmethod
    def parse_thread(soup_obj, url):
        """
        Parses a given soup instance to Thread instance
        """
        question = GITHUBParser.parse_question(soup_obj)
        if not question:
            return None
        answers = GITHUBParser.parse_answers(soup_obj)
        return Thread(GITHUBParser.site_url, url, question, answers)

    @staticmethod
    def parse_title(soup_obj):
        title_div = soup_obj.find('span', {"class": "js-issue-title markdown-title"})
        return strip_string(title_div.getText())

    @staticmethod
    def parse_question_attributes(soup_obj):
        """
        Parses the question attributes according to a dict
        """
        attributes = dict()
        question_attr_div = soup_obj.find("div", {"class": "d-flex flex-items-center flex-wrap mt-0 gh-header-meta"})
        if not question_attr_div:
            return None
        question_attr_parts = question_attr_div.find_all("div")
        for part in question_attr_parts:
            raw = part.find("span")
            if not raw:
                continue
            key = strip_string(raw.getText())
            attributes[key] = strip_string(part.getText().replace(key, ""))

        return attributes

    @staticmethod
    def parse_answers(soup_obj):
        """
        Parses all of the answers from the given soup object and returns them in a list
        """
        answers_div = soup_obj.find("div", {"id": "discussion_bucket"})
        answers = []
        answer_parts = answers_div.find_all("div",
                                            {"class": "js-timeline-item js-timeline-progressive-focus-container"})
        if not answer_parts:
            return None
        answer_idx = 0
        for answer in answer_parts:
            answer_data = answer.find("p")
            if answer_data:
                answer_str = answer_data.getText()
                if answer_str:
                    answers.append(Answer(answer_idx, answer_str, None))
                    answer_idx += 1
        # if answer_data no comment has published yet
        return answers

    @staticmethod
    def parse_question(soup_obj):
        """
        Parses a question object from the given soup object
        """

        def set_attributes():
            result = {}
            if "Open" in attributes.keys():
                result["status"] = "Open"
            else:
                result["status"] = "Close"
            if "" in attributes.keys():
                result["date"] = attributes[""].split("\n")[-2]
            return result

        attributes = GITHUBParser.parse_question_attributes(soup_obj)
        if not attributes:
            return None
        attributes = set_attributes()
        question_title = soup_obj.find('span', {"class": "js-issue-title markdown-title"}).getText().strip()
        question_div = soup_obj.find("div", {"id": "discussion_bucket"})
        question_parts = question_div.find_all("p")
        question_data = "".join([q.getText().strip() for q in question_parts])
        question = Question(question_title, question_data, attributes)
        return question

    @staticmethod
    def is_valid_link(link: str) -> bool:
        """
        Checks that the given link is a link that suits the parser
        """

        def is_issue() -> bool:
            return link.split("/")[-2] == "issues"

        return 'github.com' in link and is_issue()
