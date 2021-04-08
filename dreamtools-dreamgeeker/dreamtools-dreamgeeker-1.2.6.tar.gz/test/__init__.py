import unittest

from dreamtools import tools
from dreamtools.config import CConfig
from dreamtools.logmng import CTracker

CConfig('dreamtools')


class MyTestCase(unittest.TestCase):
    @staticmethod
    def testinit():
        print('Configuration')
        print(tools.string_me(55))

    @staticmethod
    def testlog():
        CTracker.info_tracking('test message info', 'je test')


if __name__ == '__main__':
    unittest.main()
