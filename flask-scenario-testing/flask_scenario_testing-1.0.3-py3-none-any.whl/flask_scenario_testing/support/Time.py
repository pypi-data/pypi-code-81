class Time(object):

    def __init__(self, seconds):
        self._seconds = seconds

    def seconds(self) -> int:
        return self._seconds

    @staticmethod
    def from_string(s: str):
        num = int(s[0:-1])

        if s.endswith('s'):
            return Time(num)
        elif s.endswith('m'):
            return Time(num * 60)

    def __str__(self):
        return "{}s".format(self._seconds)
