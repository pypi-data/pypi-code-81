'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._886 import WormDesign
    from ._887 import WormGearDesign
    from ._888 import WormGearMeshDesign
    from ._889 import WormGearSetDesign
    from ._890 import WormWheelDesign
