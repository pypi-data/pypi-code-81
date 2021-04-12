import json


class Annotation:
    def __init__(self, id: str, media_bucket: str, username: str, metadata: dict):
        self.id = id
        self.media_bucket = media_bucket
        self.username = username
        self.metadata = metadata

    def __repr__(self):
        kdict = {"id": self.id, "username": self.username, "metadata": self.metadata}
        return json.dumps(kdict, indent=4)
