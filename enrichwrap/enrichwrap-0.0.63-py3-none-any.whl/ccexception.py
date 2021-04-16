class CustomCallException(Exception):
    """Exception raised for errors in connection to third party enrichment

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Salary is not in (5000, 15000) range"):
        self.message = message
        super().__init__(self.message)
