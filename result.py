class Result:
    def __init__(self, link, parser_class):
        self.link = link
        self.parser = parser_class
        self.page_content = None
        self.title = ""
        self.thread = None

    def get_title(self):
        # Fill page_content if None
        # Calls self.parser parse title, is self.title is "" , returns self.title
        pass

    def get_thread(self):
        # Fill page_content if None
        # Calls self.parser parse link if self.thread is None, retuns self.thread
        pass
