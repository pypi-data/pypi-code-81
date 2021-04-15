from .gileum import BaseGileum


class MockGileum(BaseGileum):
    """Mock gileum class for testing.

    Attributes:
        test_name (str): Test name to be conducting.
        developer_name (str): Developer name of the package.
        current_time (float): The current Unix time.
    """
    test_name: str
    developer_name: str
    current_time: float
