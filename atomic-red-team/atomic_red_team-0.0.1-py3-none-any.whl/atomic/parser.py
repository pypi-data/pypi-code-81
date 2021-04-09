from .testparser import TestParser


class Parser:

    def parse(self, atomic_dict):
        if isinstance(atomic_dict, dict):
            self.__parse_atomic_tests(atomic_dict.pop('atomic_tests'))
            self.__set_properties(atomic_dict)
            return self

    def __set_properties(self, item):
        for key,val in item.items():
            if hasattr(self, key):
                if not isinstance(getattr(self, key), list):
                    v = getattr(self, key)
                    setattr(self, key, [v])
                v = getattr(self, key)
                v.append(val)
                setattr(self, key, v)
            if not hasattr(self, key):
                setattr(self, key, val)

    def __parse_atomic_tests(self, atomic_tests):
        if not isinstance(atomic_tests, list):
            atomic_tests = [atomic_tests]
        self.tests = []
        for test in atomic_tests:
            self.tests.append(TestParser().parse(test))
           
