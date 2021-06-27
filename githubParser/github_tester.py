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
link1 = 'https://github.com/OlafenwaMoses/ImageAI/issues/660'
parser = get_parser_of_link(link1, parsers)
links_dict[link1] = Result(link1, parser)
thread1 = links_dict[link1].get_thread()

link2 = 'https://github.com/OlafenwaMoses/ImageAI/issues/661'
parser = get_parser_of_link(link2, parsers)
links_dict[link2] = Result(link2, parser)
thread2 = links_dict[link2].get_thread()

link3 = 'https://github.com/The-Kor/www/issues/41'
parser = get_parser_of_link(link3, parsers)
links_dict[link3] = Result(link3, parser)
thread3 = links_dict[link3].get_thread()
link4 = ""

# ---------------------------------------------------------------------------------------


class MyTestCase(unittest.TestCase):

    def test_is_valid_link(self):
        github = g.GITHUBParser()
        self.assertEqual(True, github.is_valid_link("https://github.com/Z3Prover/z3/issues/1846"))  # an issue
        self.assertEqual(False, github.is_valid_link("https://github.com/eviatar-ben/Bumper"))  # not an issue
        self.assertEqual(True, github.is_valid_link("https://github.com/Z3Prover/z3/issues/1846"))  # an issue

    def test_parse_thread(self):
        self.assertEqual(["issues"], parser.required_path_elements)  # an issue
        self.assertNotEqual(["questions"], parser.required_path_elements)
        self.assertIsNotNone(links_dict[link1])
        self.assertEqual(thread1.url, link1)
        # Dynamic: can and should be changed at the repository, manuel changes will be required:
        self.assertEqual(thread1.question.attributes["status"], "Open")
        self.assertEqual(thread1.question.title, '"No training configuration found in the save file"')
        self.assertEqual(thread1.question.attributes["date"], "May 13, 2021")

    def test_parse_question(self):
        self.assertEqual(thread2.url, link2)
        # Dynamic: can and should be changed at the repository, manuel changes will be required:
        self.assertEqual(thread2.question.attributes["status"], "Open")
        self.assertEqual(thread2.question.title, 'Problem with idenprof!')
        self.assertEqual(thread2.question.attributes["date"], "May 14, 2021")

    def test_parse_answers(self):
        self.assertEqual(len(thread1.answers), 1)
        self.assertEqual(len(thread2.answers), 12)
        self.assertEqual(len(thread3.answers), 1)
        self.assertEqual(True, thread1.answers[0].data.startswith("This was fixed"))
        self.assertEqual(True, thread2.answers[0].data.startswith('Plz comment your Program you used'))
        self.assertEqual(None, thread3.answers[0].data)

    def test_parse_title(self):
        self.assertEqual(thread1.question.title, '"No training configuration found in the save file"')
        self.assertEqual(thread2.question.title, 'Problem with idenprof!')
        self.assertEqual(thread3.question.title, 'Permanently delete parser_factory')


if __name__ == '__main__':
    unittest.main()
