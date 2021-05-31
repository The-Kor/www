from utils_objects import Site
from sof.sof_parser import SOFParser


class ParserFactory:

    @staticmethod
    def generate_parser_objects(sites=(Site.SOF,)) -> list:
        """
        Generates a list of parses according to the given sites list
        """
        site_parsers = []
        for site in sites:
            if site == Site.SOF:
                site_parsers.append(SOFParser())
        return site_parsers
#         returns instances by request
