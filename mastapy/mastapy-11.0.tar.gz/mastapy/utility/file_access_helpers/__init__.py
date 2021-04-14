'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1546 import ColumnTitle
    from ._1547 import TextFileDelimiterOptions
