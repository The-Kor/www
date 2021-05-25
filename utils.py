from parser_factory import ParserFactory
import sys
from googlesearch import search
import os
from utils_objects import Site
import webbrowser
import re

max_results_per_site = 5

sites_to_search = [Site.SOF]


def is_not_warning_filter(txt):
    return not txt.lower().lstrip().startswith("warning")


def is_not_param_filter(txt):
    pattern = "\s*[^\s]+\s*=\s*[^\s]+\s*$"
    return not re.match(pattern, txt)


def get_basename_if_path(txt):
    full_path = txt
    if "/" in txt:
        path_no_base_name = os.path.join(*txt.split("/")[:-1])
        if os.path.exists(path_no_base_name):
            return os.path.basename(txt)
    if os.path.exists(full_path):
        return os.path.basename(txt)
    return txt


def clean_command(cmd):
    command_parts = cmd.split(" ")
    command_parts = map(get_basename_if_path, command_parts)
    return " ".join(command_parts)


def clean_error(error_msg):
    error_rows = error_msg.split("\n")
    error_rows = list(filter(is_not_warning_filter, error_rows))
    error_rows = list(filter(is_not_param_filter, error_rows))
    clean_error_rows = []
    for row in error_rows:
        row_parts = row.split(" ")
        clean_row = []
        for part in row_parts:
            if not re.match("^(.+)\/([^\/]+)$", part):
                clean_row.append(part)
        clean_error_rows.append(" ".join(clean_row))
    return "\n".join(clean_error_rows)


def get_run_info(args) -> dict:
    input_cmd = clean_command(" ".join(args[1:-1]))
    input_err_file = args[-1]
    error_str = clean_error(" ".join(open(input_err_file).readlines()))
    input_cmd = input_cmd.replace("'", "")
    input_cmd = input_cmd.replace('"', "")
    error_str = error_str.replace("'", "")
    error_str = error_str.replace('"', "")
    return dict(command=input_cmd, error=error_str, sites=sites_to_search)


def get_query(cmd, error):
    query = "{} {}".format(cmd, error)
    return query


def run_search(site, cmd, error):
    query = get_query(cmd, error)
    query = "site: {} {}".format(site.url, query)
    print(query)
    search_generator = search(query)
    return search_generator


def build_google_link(query):
    template = "http://www.google.com/search?q="
    return template + query.replace(" ", "+")


def all_sites_results(site_results):
    for site in site_results:
        for result in site:
            yield result
    while (True):
        yield None


def print_thread_data(thread):
    if not thread:
        print("Oops! no solutions found")
        return
    print("Thread from {}".format(thread.url))
    print(thread.question)


def menu_help():
    print("HELP")


def menu_open_answer_in_web(thread):
    if thread:
        webbrowser.open(thread.url)
    else:
        print("No more threads for this query, try searching edit the query using 'e'")


def menu_next_answer_in_thread(thread, answer_idx):
    if answer_idx < len(thread.answers) and thread:
        print(thread.answers[answer_idx])
        return True
    return False


def menu_open_google_in_web(query):
    webbrowser.open(build_google_link(query))


def run(run_args):
    site_parsers = ParserFactory.generate_parser_objects(run_args['sites'])
    query = get_query(run_args['command'], run_args['error'])
    site_results = [
        parser.parse_links(run_search(parser.site.value, run_args['command'], run_args['error']), parser.site.value.url)
        for parser in site_parsers]
    results = all_sites_results(site_results)

    curr_result = next(results)
    print_thread_data(curr_result)
    answer_idx = 0
    if menu_next_answer_in_thread(curr_result, answer_idx):
        answer_idx += 1
    else:
        print("No more answers in this thread..")

    while (True):
        # what do you want to do?
        user_input = input("please choose next action (input 'h' for help)")
        if user_input == "h":
            menu_help()
        elif user_input == "na":
            if menu_next_answer_in_thread(curr_result, answer_idx):
                answer_idx += 1
            else:
                print("No more answers in this thread..")
        elif user_input == "n":
            curr_result = next(results)
            print_thread_data(curr_result)
            answer_idx = 0
            if menu_next_answer_in_thread(curr_result, answer_idx):
                answer_idx += 1
            else:
                print("No more answers in this thread..")
        elif user_input == "o":
            menu_open_answer_in_web(curr_result)
        elif user_input == "g":
            menu_open_google_in_web(query)
        elif user_input == "cmd":
            print(run(['command']))
        elif user_input == "err":
            print(run(['error']))
        elif user_input == "e":
            run_args['command'] = input("input command:")
            run_args['error'] = input("input error:")
            return run_args
        elif user_input == "x":
            exit(0)
    # show help menu

    # open answer in web
    # next answer (next answer in thread)
    # next result (break inner loop)
    # google it for me
    # show command
    # show error
    # edit query and run again:
    #     -set command (enter for same)
    #     -set error (enter for same)
    # search google free text & abort
    # abort (exit(0))
