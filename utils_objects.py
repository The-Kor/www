from collections import namedtuple
# from enum import Enum

# from sof.sof_parser import SOFParser

# SiteInfo = namedtuple("SiteInfo", ["rank", "parser"])
#
#
# class Site(Enum):
#     SOF = SiteInfo(0, SOFParser)
#     GITHUB = SiteInfo(1, None)  # TODO enter GitHub parser


Thread = namedtuple("Thread", ["site", "url", "question", "answers"])