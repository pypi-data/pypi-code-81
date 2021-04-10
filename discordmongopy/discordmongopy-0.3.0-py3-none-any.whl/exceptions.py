class NoIDPassed(Exception):
    def __init__(self):
        super().__init__("There was no id passed")
