import requests

base_url = "https://hacker-news.firebaseio.com/v0/"


class Story:
    def __init__(self, d):
        self.id = d["id"]
        self.title = d["title"]
        self.time = d["time"]
        if "url" in d:
            # External link
            self.url = d["url"]
        else:
            # Hackernews direct post
            self.url = "https://news.ycombinator.com/item?id={}".format(self.id)

    def __repr__(self):
        return "HN story: {}".format(self.title)


def get_top_stories_id():
    url = "{}topstories.json".format(base_url)

    r = requests.get(url)
    r.raise_for_status()

    return r.json()


def get_story(id):
    url = "{}item/{}.json".format(base_url, id)
    r = requests.get(url)
    r.raise_for_status()

    return Story(r.json())
