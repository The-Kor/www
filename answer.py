class Answer:
    def __init__(self, data, html=None, attributes=None):
        self.data = data
        self.html = html
        self.attributes = attributes
    
    def __str__(self):
        res = ""
        if self.attributes:
            formatted_attributes = " || ".join(["{}:{}".format(k, v) for k, v in self.attributes.items()])
            res += formatted_attributes + "\n"
        formatted_data = self.data
        res += formatted_data + "\n"
        return res