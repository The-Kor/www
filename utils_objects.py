from enum import Enum
from collections import namedtuple

SiteInfo = namedtuple("SiteInfo", ["rank", "url"])

class Site(Enum):
    SOF = SiteInfo(0, "stackoverflow.com")
    GITHUB = SiteInfo(1, "github.com")


Thread = namedtuple("Thread", ["site", "url", "question", "answers"])
