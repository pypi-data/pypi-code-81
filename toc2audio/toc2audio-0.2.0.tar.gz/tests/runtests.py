#!/usr/bin/env python3

import sys
import unittest
import pathlib


def runtests():
    sys.path.insert(0, '..')
    cwd = pathlib.Path()
    alltests = unittest.TestSuite()
    tests = cwd.glob('test_*.py')
    for test in tests:
        test = str(test.name)[:-len(test.suffix)]
        module = __import__(test, globals(), locals(), test)
        alltests.addTest(module.test_suite())

    return alltests


if __name__ == '__main__':
    unittest.main(defaultTest='runtests')
