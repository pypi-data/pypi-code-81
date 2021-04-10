class APIError(Exception):
    pass


class AuthError(APIError):
    pass


class LoginFormError(AuthError):
    def __init__(self, name, value, possible):
        self._name = name
        self._value = value
        self._possible = possible

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @property
    def possible(self):
        return self._possible

    def __str__(self):
        return 'Отсутствует "%s" со значением "%s"' % (self._value, self._name)
