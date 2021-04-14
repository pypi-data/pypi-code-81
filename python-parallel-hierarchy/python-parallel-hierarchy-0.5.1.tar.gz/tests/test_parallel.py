#
#     Copyright 2021 Joël Larose
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
#

from __future__ import annotations

import pytest

from parallel_hierarchy import ParallelFactory
from sampleclasses import *

class TestParallelFactory:
    def test_factory_classdef(self):
        class Factory_1(ParallelFactory[A, View], suffix="_1"):
            pass

        assert Factory_1

    def test_factory_root(self):
        class Factory_2(ParallelFactory[A, View], suffix="_2"):
            pass

        new_cls = Factory_2.get(A)
        assert new_cls.__name__ == "A_2"
        assert new_cls.source_class == A

    def test_factory_with_ancestor(self):
        class Factory_3(ParallelFactory[A, View], suffix="_3"):
            pass

        new_cls = Factory_3(B)
        assert new_cls.__name__ == "B_3"
        assert new_cls.source_class == B
        assert len(new_cls.__bases__) == 1
        assert new_cls.__bases__[0].__name__ == "A_3"

    def test_factory_multiple_inheritance(self):
        class Factory_4(ParallelFactory[A, View], suffix="_4"):
            pass

        new_cls = Factory_4(E)
        assert new_cls.__name__ == "E_4"
        assert new_cls.source_class == E

        base_names = {b.__name__ for b in new_cls.__bases__}
        assert len(base_names) == 2
        assert {"B_4",  "D_4"} == base_names

        # At the moment, I don't care about the actual order, just the content
        mro_names = {b.__name__ for b in new_cls.mro()}
        assert len(mro_names) == 7
        assert {"A_4", "B_4", "C_4", "D_4", "E_4", "object", "View"} == mro_names

    def test_no_generic_params(self):
        with pytest.raises(TypeError) as err:
            class BadFactory(ParallelFactory, suffix="_Bad"):
                pass

        assert err
        assert locals().get("BadFactory") is None
        err_msgs = err.value.args[0]
        assert isinstance(err_msgs, list)
        assert err_msgs == ["SourceBase must be provided", "ParaBase must be provided",
                            "SourceBase must be a type", "ParaBase must be a type"]

    def test_no_affix(self):
        with pytest.raises(AttributeError) as err:
            class NoAffixFactory(ParallelFactory[A, View]):
                pass

        assert err
        assert locals().get("NoAffixFactory") is None
        err_msg = err.value.args[0]
        assert err_msg == "At least one of 'prefix' or 'suffix' must be specified with a " \
                          "non-empty string."

    def test_cover_affix_none(self):
        class Factory_5(ParallelFactory[A, View], prefix="F5_", suffix=None):
            pass

        class Factory_6(ParallelFactory[A, View], prefix=None, suffix="_6"):
            pass

        assert Factory_5.parallel_suffix == ""
        assert Factory_6.parallel_prefix == ""

    def test_register_error(self):
        class Factory_7(ParallelFactory[A, View], suffix="_7"):
            pass

        class B_7:
            """Intentionally "forgot" to provide base class."""

        with pytest.raises(TypeError) as err:
            Factory_7.register(B_7)

        assert err.type is TypeError

    def test_get_none(self):
        class Factory_8(ParallelFactory[A, View], suffix="_8"):
            pass

        with pytest.raises(ValueError) as err:
            Factory_8(None)

        assert err.type is ValueError

    def test_get_wrong_type(self):
        class Factory_9(ParallelFactory[A, View], suffix="_9"):
            pass

        with pytest.raises(TypeError) as err:
            Factory_9(str)

        assert err.type is TypeError

    def test_bad_custom_build_call(self):
        class Factory_10(ParallelFactory[A, View], suffix="_10"):
            pass

        class F:
            """Intentionally "forgot" to provide base class."""

        with pytest.raises(TypeError) as err:
            Factory_10.build_parallel_class(F, "F_10")

        assert err.type is TypeError

    def test_has(self):
        class Factory_11(ParallelFactory[A, View], suffix="_11"):
            pass

        assert not Factory_11.has("A_11")
        assert not Factory_11.has("A")
        assert not Factory_11.has(A)

        ViewA = Factory_11(A)  # Local alias for class A_11
        assert Factory_11.has("A_11")
        assert Factory_11.has("A")
        assert Factory_11.has(A)
        assert Factory_11.has(ViewA)

        assert not Factory_11.has("B_11")
        ViewE = Factory_11(E)  # Local alias for class E_11
        assert Factory_11.has("B_11")
        assert Factory_11.has("B")
        assert Factory_11.has("C")
        assert Factory_11.has("D")
        assert Factory_11.has(ViewE)

        assert not Factory_11.has(str)
        assert not Factory_11.has(99)

    def test_register_good(self):
        class Factory_12(ParallelFactory[A, View], suffix="_12"):
            pass

        class B_12(Factory_12(A)):
            """Intentionally "forgot" to provide base class."""

        assert not Factory_12.has(B)
        Factory_12.register(B_12)
        assert Factory_12.has(B)
        assert Factory_12(B) is B_12

    def test_build_with_mixin(self):
        class Factory_13(ParallelFactory[A, View], suffix="_13"):
            pass

        class Mixin_13:
            pass

        class D_13(Mixin_13, Factory_13(C)):
            pass

        assert not Factory_13.has(D)
        assert Factory_13.has(C)
        assert not Factory_13.has(B)
        gen_D_13 = Factory_13(D)
        assert gen_D_13 is not D_13
        Factory_13.register(D_13)
        my_D_13 = Factory_13(D)
        assert my_D_13 is D_13
        assert Mixin_13 in my_D_13.__bases__
        assert Mixin not in my_D_13.__bases__

        gen_E_13 = Factory_13(E)
        assert issubclass(gen_E_13, Mixin_13)

