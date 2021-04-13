from .qradarmodel import QRadarModel


class LoginAttempt(QRadarModel):

    def __init__(self, *, attempt_time: int = None, user_id: int = None, remote_ip: str = None, attempt_result: str = None, attempt_method: str = None):
        """

        Args:
            attempt_time (int, optional): The time the login attempt happens. This time is in milliseconds since epoch. Defaults to None.
            user_id (int, optional): ID of user who tried login attempt. Users are accessible through the /api/config/access/users APIs. Defaults to None.
            remote_ip (str, optional): The remote IP address that made the login attempt. Defaults to None.
            attempt_result (str, optional): The result of login attempt. Defaults to None.
            attempt_method (str, optional): The method of the login attempt. HTTP_BASIC is for API based HTTP basic, and LOGIN_PAGE is for UI login attempt. Defaults to None.
        """
        self.attempt_time = attempt_time
        self.user_id = user_id
        self.remote_ip = remote_ip
        self.attempt_result = attempt_result
        self.attempt_method = attempt_method
