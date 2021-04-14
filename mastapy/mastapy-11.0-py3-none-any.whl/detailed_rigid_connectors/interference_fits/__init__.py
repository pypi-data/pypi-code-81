'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1207 import AssemblyMethods
    from ._1208 import CalculationMethods
    from ._1209 import InterferenceFitDesign
    from ._1210 import InterferenceFitHalfDesign
    from ._1211 import StressRegions
    from ._1212 import Table4JointInterfaceTypes
