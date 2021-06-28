import unittest
import githubParser.github_parser as g
from sof.sof_parser import SOFParser
from githubParser.github_parser import GITHUBParser
from utils import get_parser_of_link
from collections import OrderedDict
from result import Result

parsers = [SOFParser, GITHUBParser]

# ----------------------------------- Global Segment------------------------------------
links_dict = OrderedDict()
link1 = 'https://stackoverflow.com/questions/379906/how-do-i-parse-a-string-to-a-float-or-int'
parser = get_parser_of_link(link1, parsers)
links_dict[link1] = Result(link1, parser, 'How do I parse a string to a float or int?')
thread1 = links_dict[link1].get_thread()

link2 = 'https://stackoverflow.com/questions/11902458/i-want-to-exception-handle-list-index-out-of-range/11902480'
parser = get_parser_of_link(link2, parsers)
links_dict[link2] = Result(link2, parser, 'I want to exception handle \'list index out of range.\'')
thread2 = links_dict[link2].get_thread()

link3 = 'https://stackoverflow.com/questions/40744216/exit-python-program-if-data-directory-is-empty?noredirect=1&lq=1'
parser = get_parser_of_link(link3, parsers)
links_dict[link3] = Result(link3, parser, 'Exit Python program if data directory is empty')
thread3 = links_dict[link3].get_thread()
link4 = ""

# ---------------------------------------------------------------------------------------


class MyTestCase(unittest.TestCase):

    def test_parse_thread(self):
        self.assertEqual(["questions"], parser.required_path_elements)
        self.assertNotEqual(["issues"], parser.required_path_elements)
        self.assertIsNotNone(links_dict[link1])
        self.assertEqual(thread1.url, link1)
        # Dynamic: can and should be changed at the repository, manuel changes will be required:
        self.assertEqual(thread1.question.attributes["score"], '2472')
        self.assertEqual(thread1.question.attributes["Asked"], '12 years, 6 months ago')
        self.assertEqual(thread1.question.attributes["Viewed"], '4.3m times')
        self.assertEqual(thread1.question.attributes["Active"], '8 months ago')

        self.assertEqual(thread1.question.title, 'How do I parse a string to a float or int?')

    def test_parse_question(self):
        self.assertEqual(thread2.url, link2)
        # Dynamic: can and should be changed at the repository, manuel changes will be required:
        self.assertEqual(thread2.question.attributes["score"], '121')
        self.assertEqual(thread2.question.attributes["Asked"], '8 years, 10 months ago')
        self.assertEqual(thread2.question.attributes["Viewed"], '310k times')
        self.assertEqual(thread2.question.attributes["Active"], '10 months ago')
        self.assertEqual(thread2.question.title, 'I want to exception handle \'list index out of range.\'')

    def test_parse_answers(self):
        # Dynamic: can and should be changed at the repository, manuel changes will be required:
        self.assertEqual(len(thread1.answers), 28)
        self.assertEqual(len(thread2.answers), 6)
        self.assertEqual(len(thread3.answers), 5)
        self.assertEqual(True, thread1.answers[0].data.startswith('>>> a'))
        self.assertEqual(True, thread2.answers[0].data.startswith('Handling the exception is the way to go:'))
        self.assertEqual(True, thread3.answers[0].data.startswith('To exit your program immediately you should'))

    def test_parse_title(self):
        # Dynamic: can and should be changed at the repository, manuel changes will be required:
        self.assertEqual(thread1.question.title, 'How do I parse a string to a float or int?')
        self.assertEqual(thread2.question.title, 'I want to exception handle \'list index out of range.\'')
        self.assertEqual(thread3.question.title, 'Exit Python program if data directory is empty')


if __name__ == '__main__':
    unittest.main()
