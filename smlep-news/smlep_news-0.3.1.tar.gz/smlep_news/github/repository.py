class Repository:
    def __init__(self, repo_json):
        self.name = repo_json["name"]
        self.author = repo_json["owner"]["login"]
        self.description = repo_json["description"]
        self.stars = repo_json["stargazers_count"]
        self.url = repo_json["html_url"]

    def __repr__(self):
        return "Repository: {}".format(self.name)

    def short_string(self):
        return "{} ({}): {} author: {}".format(
            self.name, self.stars, self.description, self.author
        )
