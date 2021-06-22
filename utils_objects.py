from collections import namedtuple
from enum import Enum

from sof.sof_parser import SOFParser

SiteInfo = namedtuple("SiteInfo", ["rank", "url", "parser"])


class Site(Enum):
    SOF = SiteInfo(0, "stackoverflow.com", SOFParser)
    GITHUB = SiteInfo(1, "github.com", None)  # TODO enter GitHub parser


Thread = namedtuple("Thread", ["site", "url", "question", "answers"])