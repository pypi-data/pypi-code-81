class FigArticle:
    def __init__(self, entry):
        self.title = entry.title
        self.summary = entry.summary
        self.url = entry.link

    def __repr__(self):
        return "Article: {}".format(self.title)
