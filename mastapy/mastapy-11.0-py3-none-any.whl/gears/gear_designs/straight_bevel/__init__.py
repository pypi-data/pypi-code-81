'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._895 import StraightBevelGearDesign
    from ._896 import StraightBevelGearMeshDesign
    from ._897 import StraightBevelGearSetDesign
    from ._898 import StraightBevelMeshedGearDesign
