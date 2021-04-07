class Article:
    def __init__(self, article_json):
        self.title = article_json["webTitle"]
        self.pub_date = article_json["webPublicationDate"]
        self.section = Section(article_json["sectionId"], article_json["sectionName"])
        self.url = article_json["webUrl"]

    def __repr__(self):
        res = self.title + "\n"
        res += str(self.section)
        return res


class Section:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return self.name
