'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1475 import ScriptingSetup
    from ._1476 import UserDefinedPropertyKey
    from ._1477 import UserSpecifiedData
