'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2241 import GearMaterialExpertSystemMaterialDetails
    from ._2242 import GearMaterialExpertSystemMaterialOptions
