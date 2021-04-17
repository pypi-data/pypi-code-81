import unittest
from typing import Generic, TypeVar

from overrides_extension import override

from tests.test_somepackage import SomeClass

TObject = TypeVar("TObject", bound=SomeClass)


class SubClassOfGeneric(Generic[TObject]):
    def some_method(self) -> None:
        """Generic sub class."""


class SubSubClassOfGeneric(SubClassOfGeneric["SubSubClassOfGeneric"]):
    @override
    def some_method(self) -> int:
        return 17


class SuperClass(object):
    def some_method(self) -> str:
        """Super Class Docs"""
        return "super"


class SubClass(SuperClass):
    @override
    def some_method(self) -> str:
        return "sub"


class Subber(SuperClass):
    @override
    def some_method(self) -> int:
        """Subber"""
        return 1


class Sub2(SomeClass, SuperClass):
    @override
    def somewhat_fun_method(self) -> str:
        return "foo"

    @override
    def some_method(self) -> None:
        pass


class SubclassOfInt(int):
    @override
    def __str__(self) -> str:
        return "subclass of int"


class OverridesTests(unittest.TestCase):
    def test_overrides_passes_for_same_package_superclass(self) -> None:
        sub = SubClass()
        self.assertEqual(sub.some_method(), "sub")
        self.assertEqual(sub.some_method.__doc__, "Super Class Docs")

    def test_overrides_does_not_override_method_doc(self) -> None:
        sub = Subber()
        self.assertEqual(sub.some_method(), 1)
        self.assertEqual(sub.some_method.__doc__, "Subber")

    def test_overrides_passes_for_superclass_in_another_package(self) -> None:
        sub2 = Sub2()
        self.assertEqual(sub2.somewhat_fun_method(), "foo")
        self.assertEqual(sub2.somewhat_fun_method.__doc__, "LULZ")

    def test_assertion_error_is_thrown_when_method_not_in_superclass(self) -> None:
        try:

            class ShouldFail(SuperClass):
                @override
                def somo_method(self) -> None:
                    pass

            raise RuntimeError("Should not go here")
        except AssertionError:
            pass

    def test_can_override_builtin(self) -> None:
        x = SubclassOfInt(10)
        self.assertEqual(str(x), "subclass of int")

    def test_overrides_method_from_generic_subclass(self) -> None:
        genericsub = SubSubClassOfGeneric()
        self.assertEqual(genericsub.some_method(), 17)
        self.assertEqual(genericsub.some_method.__doc__, "Generic sub class.")


if __name__ == "__main__":
    unittest.main()
