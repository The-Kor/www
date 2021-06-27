import sys
import webbrowser

from google_searcher import run_search
from termcolor import colored

from terminal_printer import TerminalPrinter
from utils import build_google_link, \
    get_run_info, get_query, get_parser_of_link
from utils_objects import Thread
from result import Result
from sof.sof_parser import SOFParser

NO_THREAD_SELECTED_MSG = "No thread selected. please choose a thread before executing this operation"
RANGE_LEN = 5
max_num_of_results = 20
parsers = [SOFParser]


def print_thread_by_index(cur_thread_idx, results):
    """
    This function gets the results and a specific idx and prints the question
    of the Thread and the first answer.
    :return: The next answer index of the given Thread's index.
    """

    curr_thread = results[cur_thread_idx].get_thread()
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
    webbrowser.open(build_google_link(query, max_num_of_results))


def get_links_generator(sites_str, query):
    """
    Return a list of results(Tuples of link,title) of the given site string to the given query
    """
    query = "site: {} {}".format(sites_str, query)
    TerminalPrinter.print_query(query)
    search_results = run_search(query, parsers, max_num_of_results)
    return search_results


def get_results(query):
    """
    This function builds a query to search from the given query and the site_to_search urls.
    The function runs google search on the query and takes up to max_num_of_results links from the outputted list.
    Each tuple is converted into a Result instance.
    """
    sites_str = "|".join([parser.site_url for parser in parsers])
    results_tuples = get_links_generator(sites_str, query)
    results = []
    for cur_link, cur_link_title in results_tuples:
        parser = get_parser_of_link(cur_link, parsers)
        if parser:
            results.append(Result(cur_link, parser, cur_link_title))
    return results


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
    run_args['query'] = get_query(run_args['command'], run_args['error'])


def move_range_up(curr_range, results_len):
    '''
    :param curr_range: the current range of the printed results
    :param results_len: the length of the results' list
    :return: the next results' chunk range
    '''
    old_low = list(curr_range)[0]
    new_low = old_low + RANGE_LEN if old_low + RANGE_LEN < results_len else old_low
    new_high = min(results_len, new_low + RANGE_LEN)
    return range(new_low, new_high)


def move_range_down(curr_range, results_len):
    '''
    :param curr_range: the current range of the printed results
    :param results_len: the length of the results' list
    :return: the previous results' chunk range
    '''
    old_low = list(curr_range)[0]
    new_low = max(0, old_low - RANGE_LEN)
    new_high = min(results_len, new_low + RANGE_LEN)
    return range(new_low, new_high)


def run(run_args):
    """
    Runs the main menu loop according to the given run_args dict
    """
    query = run_args['query']
    cur_thread_idx = None
    answer_idx = 0
    results = get_results(query)
    titles_idx_range = range(0, min(RANGE_LEN, len(results)))
    TerminalPrinter.print_titles(results, titles_idx_range)  # Print instructions for thread selection
    while True:
        user_input = input(colored("please choose next action (input {} for help)", "green").format("'h'"))
        if user_input == "h":
            TerminalPrinter.print_help_menu()
        elif user_input == "na":
            if cur_thread_idx is None:
                TerminalPrinter.print_error(NO_THREAD_SELECTED_MSG)
                continue
            curr_thread = results[cur_thread_idx].get_thread()
            if menu_next_answer_in_thread(curr_thread, answer_idx):
                answer_idx += 1
            else:
                print("No more answers in this thread..\nEnter 'n' for next thread")
        elif user_input.isnumeric() and int(user_input) in range(len(results)):
            cur_thread_idx = int(user_input)
            answer_idx = print_thread_by_index(cur_thread_idx, results)
        elif user_input == "nt":
            if cur_thread_idx is None:
                TerminalPrinter.print_error(NO_THREAD_SELECTED_MSG)
                continue
            if cur_thread_idx < len(results) - 1:
                cur_thread_idx += 1
                answer_idx = print_thread_by_index(cur_thread_idx, results)
            else:
                print("No more threads for this query..\nEnter 'e' to edit your query")
        elif user_input == "pt":
            if cur_thread_idx is None:
                TerminalPrinter.print_error(NO_THREAD_SELECTED_MSG)
                continue
            if cur_thread_idx > 0:
                cur_thread_idx -= 1
                answer_idx = print_thread_by_index(cur_thread_idx, results)
            elif cur_thread_idx == 0:
                print("No previous thread to show")
            else:
                print("No more threads for this query..\nEnter 'e' to edit your query")
        elif user_input == "n":
            titles_idx_range = move_range_up(titles_idx_range, len(results))
            TerminalPrinter.print_titles(results, titles_idx_range)
            pass
        elif user_input == "p":
            titles_idx_range = move_range_down(titles_idx_range, len(results))
            TerminalPrinter.print_titles(results, titles_idx_range)
            pass
        elif user_input == "r":
            TerminalPrinter.print_titles(results, titles_idx_range)
        elif user_input == "o":
            if cur_thread_idx is None:
                TerminalPrinter.print_error(NO_THREAD_SELECTED_MSG)
                continue
            curr_result = results[cur_thread_idx]
            menu_open_answer_in_web(curr_result.get_thread())
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
            TerminalPrinter.print_error("Invalid input")


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
        run_args = get_run_info(sys.argv)
        run_args['query'] = get_query(run_args['command'], run_args['error'])
    while True:
        try:
            run(run_args)
        except SystemExit:
            sys.exit()
