'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2286 import ActiveFESubstructureSelection
    from ._2287 import ActiveFESubstructureSelectionGroup
    from ._2288 import ActiveShaftDesignSelection
    from ._2289 import ActiveShaftDesignSelectionGroup
    from ._2290 import BearingDetailConfiguration
    from ._2291 import BearingDetailSelection
    from ._2292 import PartDetailConfiguration
    from ._2293 import PartDetailSelection
