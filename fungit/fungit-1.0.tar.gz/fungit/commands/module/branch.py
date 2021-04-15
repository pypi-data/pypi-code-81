class Branch:
    def __init__(
        self,
        name: str,
        pushables: str,
        pullables: str,
        is_head: bool,
        upstream_name: str = "",
    ):
        self.name = name
        self.upstream_name = upstream_name
        self.pushables = pushables
        self.pullables = pullables
        self.is_head = is_head
