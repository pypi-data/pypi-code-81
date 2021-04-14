'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._915 import HypoidGearDesign
    from ._916 import HypoidGearMeshDesign
    from ._917 import HypoidGearSetDesign
    from ._918 import HypoidMeshedGearDesign
