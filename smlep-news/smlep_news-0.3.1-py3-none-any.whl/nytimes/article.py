class Article:
    def __init__(self, article_json):
        self.title = article_json["title"]
        self.pub_date = article_json["published_date"]
        self.url = article_json["url"]
        self.abstract = article_json["abstract"]

    def __repr__(self):
        return "NYT Article: {}".format(self.title)
