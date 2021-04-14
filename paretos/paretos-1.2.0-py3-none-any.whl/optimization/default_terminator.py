from ..interface.run_terminator import RunTerminator

# this is supposed to be enough to produce a meaningful result in most cases
StopAt = 100


class DefaultTerminator(RunTerminator):
    def __init__(self):
        super().__init__(StopAt)
