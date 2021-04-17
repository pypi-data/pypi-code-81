
from generallibrary import Date


class _PackagerPypi:
    def get_latest_release(self):
        """ Use current datetime if bumped, otherwise fetch.

            :param generalpackager.Packager self: """
        if self.is_bumped():
            return Date.now()
        else:
            return self.pypi.get_date()





























