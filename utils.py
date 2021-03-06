import os
import re

max_results_per_site = 5
# from the link ""http://www.stackoverflow.com/questions/1234567/blah-bla""
# group(1) -> 'stackoverflow.com'
# group(0) -> 'http://www.stackoverflow.com'
url_pattern = re.compile("^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)")


def is_not_warning_filter(txt):
    '''
    check if txt is a line starting with 'warning'
    '''
    return not txt.lower().lstrip().startswith("warning")


def is_not_param_filter(txt):
    '''
    check if txt is a 'param' line of the form XXX = YYY
    '''
    pattern = "\s*[^\s]+\s*=\s*[^\s]+\s*$"
    return not re.match(pattern, txt)


def get_basename_if_path(txt):
    '''
    returns the basename of a path, when txt is a path
    '''
    full_path = txt
    if "/" in txt:
        path_no_base_name = os.path.join(*txt.split("/")[:-1])
        if os.path.exists(path_no_base_name):
            return os.path.basename(txt)
    if os.path.exists(full_path):
        return os.path.basename(txt)
    return txt


def clean_command(cmd):
    '''
    cleans the command from paths
    '''
    command_parts = cmd.split(" ")
    command_parts = map(get_basename_if_path, command_parts)
    return " ".join(command_parts)


def clean_error(error_msg):
    '''
    clean the error by filters
    '''
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
    '''
    cleaning the input command and error and returning them
    '''
    input_cmd = clean_command(" ".join(args[1:-1]))
    input_err_file = args[-1]
    error_str = clean_error(" ".join(open(input_err_file).readlines()))
    input_cmd = input_cmd.replace("'", "")
    input_cmd = input_cmd.replace('"', "")
    error_str = error_str.replace("'", "")
    error_str = error_str.replace('"', "")
    return dict(command=input_cmd, error=error_str)


def get_query(cmd, error):
    '''
    compose a query out of command and error
    '''
    query = "{} {}".format(cmd, error)
    return query


def build_google_link(query, max_num_of_results):
    '''
    returns the pre-searched google link for the given query,
    with max number of results in the output page of the given number
    '''
    template = "http://www.google.com/search?q="
    return template + query.replace(" ", "+") + "&num={}".format(max_num_of_results)


def strip_string(string):
    '''
    Normalizing a "paragraph" string
    '''
    return re.sub("[\r\n\t\s]*\n[\r\n\t\s]*\n[\r\n\t\s]*", "\n\n", string.strip("[ \t\n\r]"))


def is_link_supported(link, parsers):
    '''
    :param link: a link (url)
    :param parsers: the parsers
    :return: true if the link is supported by any parser, false otherwise
    '''
    if link:
        return any([is_link_of_parser(link, p) for p in parsers])
    return False


def is_link_of_parser(link, parser):
    '''
    :param link: a full link url
    :param parser: a parser object to check
    :return: True is the link is of this site and has all the required_path_elements of the given parser, False otherwise
    '''
    link_path_elements = link.split("/")
    link_regex_match = url_pattern.match(link)
    if link_regex_match:
        return parser.site_url in url_pattern.match(link).group(0) and all(
            [element in link_path_elements for element in parser.required_path_elements])


def get_parser_of_link(link, parsers):
    '''
    :param link: a full link url
    :param parsers: list of sites to match to this link
    :return: the parser from the list matches this link, None if no parser matches
    '''
    for parser in parsers:
        if is_link_of_parser(link, parser):
            return parser
    return None
