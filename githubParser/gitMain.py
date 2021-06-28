from terminal_printer import TerminalPrinter
from utils import get_parser_of_link
from collections import OrderedDict
from result import Result
from sof.sof_parser import SOFParser
from githubParser.github_parser import GITHUBParser
parsers = [SOFParser, GITHUBParser]


if __name__ == '__main__':
    links_dict = OrderedDict()
    # cur_link = 'https://github.com/The-Kor/www/issues/41'
    # cur_link = 'https://github.com/OlafenwaMoses/ImageAI/issues/661'
    cur_link = 'https://github.com/OlafenwaMoses/ImageAI/issues/660'
    parser = get_parser_of_link(cur_link, parsers)
    if parser:
        links_dict[cur_link] = Result(cur_link, parser)
    titles_idx_range = range(0, 1)  # TODO 5 SHOULD BE CONST

    TerminalPrinter.print_titles(links_dict, titles_idx_range)  # Print instructions for thread selection
    curr_thread = list(links_dict.values())[0].get_thread()
    TerminalPrinter.print_question(curr_thread)
