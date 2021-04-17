from typing import TypeVar

from formerbox.common.overrides import EnforceOverrides, final, override
from formerbox.common.deprecated import deprecated
from typing import Any

Foo = TypeVar("Foo")


class SuperClass(EnforceOverrides):
    @final
    def method(self) -> int:
        """This is the doc for a method and will be shown in subclass method too!"""
        return 2

    @deprecated()
    def method2(self) -> int:
        """This is the doc for a method and will be shown in subclass method too!"""
        return 2

    @staticmethod
    def method3() -> int:
        """This is the doc for a method and will be shown in subclass method too!"""
        return 2


class SubClass3(SuperClass):
    @override
    def method2(self) -> int:
        super().method2()
        return 1


if __name__ == "__main__":
    obj = SubClass3()
    obj.method2()
