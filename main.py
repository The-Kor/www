import sys
import webbrowser

from googlesearch import search
from termcolor import colored

import utils
from parser_factory import ParserFactory
from terminal_printer import TerminalPrinter
from utils import build_google_link
from utils_objects import Site, Thread

sites_to_search = [Site.SOF]


def print_thread_by_index(cur_thread_idx, links_dict):
    curr_thread = links_dict.items()[cur_thread_idx][1]
    TerminalPrinter.print_question(curr_thread)
    answer_idx = 0
    if menu_next_answer_in_thread(curr_thread, answer_idx):
        answer_idx += 1
    else:
        print("No more answers in this thread..\nEnter 'n' for next thread")
    return answer_idx


def menu_open_answer_in_web(thread):
    """
    Opens the thread in the user's browsers
    """
    if thread:
        webbrowser.open(thread.url)
    else:
        print("No more threads for this query, try searching edit the query using 'e'")


def menu_next_answer_in_thread(thread: Thread, answer_idx):
    """
    Prints the next answer in the thread, returns True if such answer exists, other False
    """
    if thread and answer_idx < len(thread.answers):
        TerminalPrinter.print_answer(thread.answers[answer_idx])
        return True
    return False


def menu_open_google_in_web(query):
    """
    Opens the google search page on the given query in the user's browsers
    """
    webbrowser.open(build_google_link(query))


def get_results_generator(site, query):
    """
    Return a generator of results(Threads) of the given site to the given query
    """
    query = "site: {} {}".format(site.url, query)
    TerminalPrinter.print_query(query)
    search_generator = search(query)
    return search_generator


def get_links_by_query(query):
    # Runs search on all sites_to_search and returns a OrderedDict of links
    # validate that the link is from a known source
    # (of num_of_links size) (value is Result instance)
    pass


def all_sites_results_generator(site_generators):
    """
    A general generator of threads to all given site generators
    """
    for site in site_generators:
        for result in site:
            yield result
    while (True):
        yield None


def menu_update_query(run_args):
    """
    Asks the user for input a new query, updates the run_args given dict
    """
    run_args['command'] = input("input command:")
    run_args['error'] = input("input error:")
    run_args['query'] = utils.get_query(run_args['command'], run_args['error'])


def run(run_args):
    """
    Runs the main menu loop according to the given run_args dict
    """
    site_parsers = ParserFactory.generate_parser_objects(sites_to_search)
    query = run_args['query']
    ############
    cur_thread_idx = None
    answer_idx = 0
    titles_idx_range = range(0, 5)  # TODO 5 SHOULD BE CONST
    links_dict = get_links_by_query(query)
    TerminalPrinter.print_titles(links_dict, titles_idx_range)  # Print instructions for thread selection
    ########
    while True:
        user_input = input(colored("please choose next action (input {} for help)", "green").format("'h'"))
        if user_input == "h":
            TerminalPrinter.print_help_menu()
        elif user_input == "na":
            if cur_thread_idx is None:
                TerminalPrinter.print_no_thead_selected()
                continue
            curr_thread = links_dict.items()[cur_thread_idx][1]
            if menu_next_answer_in_thread(curr_thread, answer_idx):
                answer_idx += 1
            else:
                print("No more answers in this thread..\nEnter 'n' for next thread")
        elif user_input.isnumeric() and int(user_input) in range(len(links_dict)):
            cur_thread_idx = int(user_input)
            answer_idx = print_thread_by_index(cur_thread_idx, links_dict)
        elif user_input == "nt":
            if cur_thread_idx is None:
                TerminalPrinter.print_no_thead_selected()
                continue
            if cur_thread_idx < len(links_dict) - 1:
                cur_thread_idx += 1
                answer_idx = print_thread_by_index(cur_thread_idx, links_dict)
            else:
                print("No more threads for this query..\nEnter 'e' to edit your query")
        elif user_input == "pt":
            if cur_thread_idx is None:
                TerminalPrinter.print_no_thead_selected()
                continue
            if cur_thread_idx > 0:
                cur_thread_idx -= 1
                answer_idx = print_thread_by_index(cur_thread_idx, links_dict)
            else:
                print("No more threads for this query..\nEnter 'e' to edit your query")
        elif user_input == "n":
            # Implement threads range navigation (change the current range to next one)
            pass
        elif user_input == "p":
            # Implement threads range navigation (change the current range to previous one)
            pass
        elif user_input == "o":
            if cur_thread_idx is None:
                TerminalPrinter.print_no_thead_selected()
                continue
            curr_thread = links_dict.items()[cur_thread_idx][1]
            menu_open_answer_in_web(curr_thread)
        elif user_input == "g":
            menu_open_google_in_web(query)
        elif user_input == "cmd":
            print(run_args.get('command', query))
        elif user_input == "err":
            print(run_args.get('error', query))
        elif user_input == "e":
            menu_update_query(run_args)
            return run_args
        elif user_input.startswith("x"):
            sys.exit()
        else:
            print("Invalid input")


if __name__ == '__main__':
    run_args = {}
    if sys.argv[1] == 'h':
        print("Run Examples:\nwww --q [query to search]\nwww [command to run]")
        exit()
    elif sys.argv[1] == 'e':
        menu_update_query(run_args)
    elif sys.argv[1] == "q":
        run_args['query'] = " ".join(sys.argv[2:])
    else:
        run_args = utils.get_run_info(sys.argv)
        run_args['query'] = utils.get_query(run_args['command'], run_args['error'])
    while True:
        try:
            run(run_args)
        except SystemExit:
            sys.exit()
