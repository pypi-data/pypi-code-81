import unittest

from overrides_extension import final, override

import tests.test_somefinalpackage as test_somefinalpackage


class SuperClass(object):
    def some_method(self) -> str:
        """Super Class Docs"""
        return "super"

    @final
    def some_finalized_method(self) -> str:
        return "super_final"


class SubClass(SuperClass):
    @override
    def some_method(self) -> str:
        return "sub"

    @final
    def another_finalized(self) -> str:
        return "sub_final"


class Sub2(test_somefinalpackage.SomeClass, SuperClass):
    @override
    def somewhat_fun_method(self) -> str:
        return "foo"

    @override
    def some_method(self) -> None:
        pass


class FinalTests(unittest.TestCase):
    def test_final_passes_simple(self) -> None:
        sub = SubClass()
        self.assertEqual(sub.some_method(), "sub")
        self.assertEqual(sub.some_method.__doc__, "Super Class Docs")
        self.assertEqual(sub.some_finalized_method(), "super_final")

    def test_final_passes_for_superclass_in_another_package(self) -> None:
        sub2 = Sub2()
        self.assertEqual(sub2.somewhat_fun_method(), "foo")
        self.assertEqual(sub2.somewhat_fun_method.__doc__, "LULZ")
        self.assertEqual(sub2.some_finalized_method(), "super_final")
        self.assertEqual(sub2.somewhat_finalized_method(), "some_final")

    def test_final_fails_simple(self) -> None:
        try:

            class SubClassFail(SuperClass):
                @override
                def some_method(self) -> str:
                    return "subfail"

                @override
                def some_finalized_method(self) -> None:
                    pass

            raise RuntimeError("Should not go here")
        except AssertionError:
            pass

    def test_final_fails_another_package(self):
        try:

            class Sub2Fail(test_somefinalpackage.SomeClass, SuperClass):
                @override
                def somewhat_fun_method(self) -> str:
                    return "foo"

                @override
                def some_method(self) -> None:
                    pass

                @override
                def some_finalized_method(self) -> None:
                    pass

            raise RuntimeError("Should not go here")
        except AssertionError:
            pass

    def test_final_fails_deep(self) -> None:
        try:

            class Sub3Fail(test_somefinalpackage.SomeClass, SubClass):
                @override
                def somewhat_fun_method(self) -> str:
                    return "foo"

                @override
                def some_method(self) -> None:
                    pass

                @override
                def some_finalized_method(self) -> None:
                    pass

            raise RuntimeError("Should not go here")
        except AssertionError:
            pass

    def test_final_fails_in_middle(self):
        try:

            class Sub4Fail(test_somefinalpackage.SomeClass, SubClass):
                @override
                def somewhat_fun_method(self) -> str:
                    return "foo"

                @override
                def some_method(self) -> None:
                    pass

                @override
                def another_finalized(self) -> None:
                    pass

            raise RuntimeError("Should not go here")
        except AssertionError:
            pass

    def test_final_fails_from_another_package(self):
        try:

            class Sub5Fail(test_somefinalpackage.SomeClass, SubClass):
                @override
                def somewhat_fun_method(self) -> str:
                    return "foo"

                @override
                def some_method(self) -> None:
                    pass

                @override
                def some_finalized_method(self) -> None:
                    pass

            raise RuntimeError("Should not go here")
        except AssertionError:
            pass


if __name__ == "__main__":
    unittest.main()
