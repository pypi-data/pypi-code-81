class Commit:
    def __init__(
        self,
        sha: str,
        msg: str,
        author: str,
        unix_timestamp: int,
        status: str,
        extra_info: str,
        tag: list,
        action: str = "",
    ) -> None:
        self.sha = sha
        self.msg = msg
        self.author = author
        self.unix_timestamp = unix_timestamp
        self.status = status
        self.extra_info = extra_info
        self.tag = tag
        self.action = action

    def is_pushed(self):
        return self.status == "pushed"
