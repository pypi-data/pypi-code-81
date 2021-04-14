'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._891 import StraightBevelDiffGearDesign
    from ._892 import StraightBevelDiffGearMeshDesign
    from ._893 import StraightBevelDiffGearSetDesign
    from ._894 import StraightBevelDiffMeshedGearDesign
