class Product:
    def __init__(self, post):
        self.id = post["id"]
        self.name = post["name"]
        self.description = post["description"]
        self.tagline = post["tagline"]
        self.votes = post["votesCount"]
        self.url = post["url"]

    def __repr__(self):
        return self.name

    def short_string(self):
        return "{} ({}): {} url: {}".format(
            self.name, self.votes, self.tagline, self.url
        )
