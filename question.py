class Question:
    def __init__(self, title, data, html=None, attributes=None):
        self.title = title
        self.data = data
        self.attributes = attributes
        self.html = html

    def __str__(self):
        res = ""
        formatted_title = self.title
        res += formatted_title + "'\n"
        if self.attributes:
            formatted_attributes = " || ".join(["{}:{}".format(k, v) for k, v in self.attributes.items()])
            res += formatted_attributes + "\n"
        formatted_data = self.data
        res += formatted_data + "\n"
        return res
