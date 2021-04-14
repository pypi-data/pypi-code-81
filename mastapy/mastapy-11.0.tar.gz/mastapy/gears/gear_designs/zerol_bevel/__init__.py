'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._882 import ZerolBevelGearDesign
    from ._883 import ZerolBevelGearMeshDesign
    from ._884 import ZerolBevelGearSetDesign
    from ._885 import ZerolBevelMeshedGearDesign
