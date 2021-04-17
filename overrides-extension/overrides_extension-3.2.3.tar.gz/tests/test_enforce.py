import unittest

from overrides_extension import EnforceOverrides, final, override


class Enforcing(EnforceOverrides):

    classVariableIsOk = "OK?"

    @final
    def finality(self) -> str:
        return "final"

    def nonfinal1(self, param: int) -> str:
        return "super1"

    def nonfinal2(self) -> str:
        return "super2"

    @property
    def nonfinal_property(self) -> str:
        return "super_property"

    @staticmethod
    def nonfinal_staticmethod() -> str:
        return "super_staticmethod"

    @classmethod
    def nonfinal_classmethod(cls) -> str:
        return "super_classmethod"


class EnforceTests(unittest.TestCase):
    def test_enforcing_when_all_ok(self) -> None:
        class Subclazz(Enforcing):
            classVariableIsOk = "OK!"

            @override
            def nonfinal1(self, param: int) -> int:
                return 2

        sc = Subclazz()
        self.assertEqual(sc.finality(), "final")
        self.assertEqual(sc.nonfinal1(1), 2)
        self.assertEqual(sc.nonfinal2(), "super2")
        self.assertEqual(sc.classVariableIsOk, "OK!")

    def tests_enforcing_when_finality_broken(self) -> None:
        try:

            class BrokesFinality(Enforcing):
                def finality(self) -> str:
                    return "NEVER HERE"

            raise RuntimeError("Should not go here")
        except AssertionError:
            pass

    def test_enforcing_when_none_explicit_override(self) -> None:
        try:

            class Overrider(Enforcing):
                def nonfinal2(self) -> str:
                    return "NEVER HERE EITHER"

            raise RuntimeError("Should not go here")
        except AssertionError:
            pass

    def test_enforcing_when_property_overriden(self) -> None:
        class PropertyOverrider(Enforcing):
            @property
            @override
            def nonfinal_property(self) -> str:
                return "subclass_property"

        self.assertNotEqual(
            PropertyOverrider.nonfinal_property, Enforcing.nonfinal_property
        )

    def test_enforcing_when_staticmethod_overriden(self) -> None:
        class StaticMethodOverrider(Enforcing):
            @staticmethod
            @override
            def nonfinal_staticmethod() -> str:
                return "subclass_staticmethod"

        self.assertNotEqual(
            StaticMethodOverrider.nonfinal_staticmethod(),
            Enforcing.nonfinal_staticmethod(),
        )

    def test_enforcing_when_classmethod_overriden(self) -> None:
        class ClassMethodOverrider(Enforcing):
            @classmethod
            @override
            def nonfinal_classmethod(cls) -> str:
                return "subclass_classmethod"

        self.assertNotEqual(
            ClassMethodOverrider.nonfinal_classmethod(),
            Enforcing.nonfinal_classmethod(),
        )
